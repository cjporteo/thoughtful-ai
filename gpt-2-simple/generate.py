import gpt_2_simple as gpt2
import json
from datetime import datetime

def attempt_generate(sess=None):
	
	with open('config.json') as f:
	  	config = json.load(f)

	if not sess:
		sess = gpt2.start_tf_sess()
	else:
		sess = gpt2.reset_session(sess)

	gpt2.load_gpt2(sess,
		run_name=config['run_name'])

	file_core = 'motivational_quotes'
	time_string = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
	model_type = config['model']
	output_file = f'{file_core}_{model_type}.txt'

	gpt2.generate(sess,
		top_k=40,
		run_name=config['run_name'],
		nsamples=config['samples_to_generate'],
		destination_path= config['model_output_path'] + output_file)

	return sess

if __name__ == '__main__':
	attempt_generate()