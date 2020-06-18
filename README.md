# @thoughtfulAi

This project uses a deep learning language model to generate thought-provoking quotes. Quotes are given a high res nature-themed backdrop and posted to Twitter at [@thoughtfulAi](https://twitter.com/thoughtfulAi). The project is deployed on Google Cloud Compute Engine and posts every 8 hours.

## Sample Tweets
![enter link description here](https://i.imgur.com/6omsEIM.png)
![enter link description here](https://i.imgur.com/tf8oCUi.png)![enter link description here](https://i.imgur.com/o6K7DO4.png)
## About
Text is generated using [GPT-2](https://github.com/openai/gpt-2), a transformer based language model from OpenAI. I finetuned the model on over 3000 inspirational quotes from various authors at [goodreads.com](goodreads.com). In an attempt to boost model integrity, only quotes exceeding a threshold quantity of user likes are used in the training set. Quotes in the dataset come from the likes of Maya Angelou, Roy T. Bennett, Mahatma Gandhi, Oscar Wilde, Eleanor Roosevelt, Albert Einstein, Dr. Seuss, and many other authors. Scraped quotes are added to an SQLite database.

I used an adapted version Max Woolf's [gpt-2-simple utility](https://github.com/minimaxir/gpt-2-simple) to finetune the GPT-2 base model to this quote database.

Images are sourced using the Unsplash API, fetching a random landscape image from the query "nature dark". The logic behind the "dark" is that this would hopefully make the white text on top easier to read. This works decently, but backdrops involving gray clouds are still pretty problematic.

I used HTML/CSS to overlay the text, signature, and SVG logo. The .html then gets converted to .jpg using `imgkit` and `wkhtmltopdf`. I played around with the idea of just using PIL (Python Image Library) to do the overlays, but some of my requirements like drop shadow and format-obeying text wrapping proved difficult to implement - so I went the CSS route.

Once we have the .jpg, we post it to Twitter using the Tweepy API.

## Output Integrity and Limitations
I was pretty satisfied overall with the quality of the generated text, but it's far from perfect. Quotes range wildly in coherence - sometimes it creates something far-reaching and whimsical, but other times it just spits out contradictory nonsense.

A possible defense for this is the (relatively) small model size. GPT-2 has been released in four different sizes 124M, 355M, 762M, and 1.5B. These numbers represent the varying number of parameters present in the model - more parameters means less portability but higher complexity and richer output. Since I planned to deploy this project to the cloud from the start, I opted for the 124M model. I suspect that a lot of the contradictory patterns currently occurring with the 124M model would be ironed out in the bigger versions. 

Here's an example of a generated quote exhibiting this contradictory behavior:

![enter link description here](https://i.imgur.com/iYoqbrL.png)<br>
Grammar mistakes in generated text are more prevalent than I would like, and this almost surely can be traced back to grammatical errors in the training set. A good next step for this project would be to run all of the quotes in the database through a spelling and grammar check, to ensure that the model doesn't pick up any bad habits.
