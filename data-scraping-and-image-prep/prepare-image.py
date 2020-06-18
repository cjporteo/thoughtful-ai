import process_output
from PIL import Image, ImageEnhance, ImageFilter
import requests
from io import BytesIO
import imgkit
import tweepy
import json
from random import randint

IMAGE_WIDTH = 1800
IMAGE_HEIGHT = 900

TWEET = True

with open('credentials.json') as f:
      credentials = json.load(f)

def get_unsplash_data(client_id, query, orientation):
    
    root = 'https://api.unsplash.com/'
    path = 'photos/random/?client_id={}&query={}&orientation={}'
    search_url = root + path.format(client_id, query, orientation)
    
    api_response = requests.get(search_url)
    data = api_response.json()
    api_response.close()
    #print(json.dumps(data, indent=4, sort_keys=True))
    
    return data['urls']['raw'], data['user']['name']

client_id = credentials['unsplash-client-id']
query = 'nature dark'
orientation = 'landscape'

image_url, photo_credit_name = get_unsplash_data(client_id, query, orientation)

if not photo_credit_name:
    photo_credit_name = 'Anonymous'

quote_text = process_output.get_quote()

image_response = requests.get(image_url)
img = Image.open(BytesIO(image_response.content))
image_response.close()

# resize down until either a desired width or height is acheived, then crop the other dimension
# to acheive a non-distorted version of the image with desired dimensions
def resize_crop(im, desired_width=1440, desired_height=1080):
    
    width, height = im.size
    if width/height > desired_width/desired_height:
        im.thumbnail((width, desired_height))
    else:
        im.thumbnail((desired_width, height))
        
    width, height = im.size
    box = [0, 0, width, height] # left, upper, right, lower
    if width > desired_width:
        box[0] = width/2 - desired_width/2
        box[2] = width/2 + desired_width/2
    if height > desired_height:
        box[1] = height/2 - desired_height/2
        box[3] = height/2 + desired_height/2
    
    im = im.crop(box=box)
    return im

def reduce_color(im, desired_color=0.5):
    converter = ImageEnhance.Color(im)
    im = converter.enhance(desired_color)
    return im

def gaussian_blur(im, radius=2):
    im = im.filter(ImageFilter.GaussianBlur(radius=radius))
    return im

img = resize_crop(img, IMAGE_WIDTH, IMAGE_HEIGHT)
img = reduce_color(img)
#img = gaussian_blur(img)

img.save('templates-and-assets/backdrop.jpg')

html_doc = None

with open('templates-and-assets/image_template.html', 'r') as f:
    html_doc = f.read()

html_doc = html_doc.replace('dynamictext', quote_text)

#print(len(quote_text))

def get_font_size(text):
    size = len(text)
    if size < 40:
        return '88'
    if size < 75:
        return '76'
    return '64'

html_doc = html_doc.replace('dynamicfontsize', get_font_size(quote_text))

with open('templates-and-assets/image_out.html', 'w') as f:
    f.write(html_doc)


imgkit.from_file('templates-and-assets/image_out.html',
                 'templates-and-assets/image_out.jpg',
                options={'width' : IMAGE_WIDTH, 'height' : IMAGE_HEIGHT,
                          'quality' : 100, 'encoding' : 'utf-8'})


def tw_OAuth():

    consumer_key = credentials["twitter-api-key"]
    consumer_key_secret = credentials["twitter-api-secret-key"]
    access_token = credentials["twitter-access-token"]
    access_token_secret = credentials["twitter-access-token-secret"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

tw_oauth = tw_OAuth()
tw_api = tweepy.API(tw_oauth)

if TWEET:

    hts = ['ai', 'nlp']
    hashtags = ' '.join('#' + ht for ht in hts)

    emoji = u'\U0001F4AD'

    credits = f'Photo: {photo_credit_name} (Unsplash)'

    composition = [quote_text, hashtags]

    if randint(0, 20) != 0:
        composition.pop(1)

    status = '\n\n'.join(composition)
    tw_api.update_with_media('templates-and-assets/image_out.jpg', status=status)