import os
from openai import OpenAI
from .converter import convert_to_img


def send_request(prompt, presentation, file_format, model="meta-llama/llama-4-maverick:free"):
	"""
	Send a request to OpenAI based on received params

	Parameters
		----------
		prompt: str
			text instructions on how to perform presentation evaluation
		presentation: bytes
			presentation uploaded by user in bytes format
		file_format: srt
			format of the uploaded presentation pdf or pptx
		model: str
			chosen by user llm default llama-4-maverick
	Returns
		----------
		json
			report in json format, contains structure, content evaluation and correction advices
	"""
	# get OPENAI_API_KEY from env variables
	api_key = os.environ["OPENAI_API_KEY"]
	client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
	# process and decode presentation
	converted_presentation = convert_to_img(presentation, file_format)
	image = converted_presentation.base64().decode()
	# get information about fonts on each slide (for pptx format only)
	fonts = f", информация о шрифтах {str(converted_presentation.fonts)}"
	# Prepare message content
	content = [{"type": "text", "text": prompt + fonts}, {
		"type": "image_url",
		"image_url": {
			"url": f"data:image/jpeg;base64,{image}"
		}
	}]
	response = client.chat.completions.create(
		model=model,
		messages=[{
			"role": "user",
			"content": content
		}]
	)

	return response
