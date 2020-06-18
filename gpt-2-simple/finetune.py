import gpt_2_simple as gpt2
import os
import requests
import json

with open('config.json') as f:
  config = json.load(f)

model_name = config['model']
if not os.path.isdir(os.path.join('models', model_name)):
    print(f'Downloading {model_name} model...')
    gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/

'''
if not os.path.isfile(file_name):
    url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
    data = requests.get(url)
    
    with open(file_name, 'w') as f:
        f.write(data.text)
'''

sess = gpt2.start_tf_sess()
gpt2.finetune(sess,
              config['text_to_train'],
              model_name=model_name,
              run_name=config['run_name'],
              restore_from=config['restore_from'],
              steps=config['training_steps'],
              sample_every=config['sample_every'],
              save_every=config['save_every'])   # steps is max number of training steps

#gpt2.generate(sess)