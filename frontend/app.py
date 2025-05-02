import streamlit as st
from streamlit_theme import st_theme
from backend.llm_call import send_request

# to start app run this command in terminal "streamlit run ./frontend/app.py"

# set browser tab name and icon
st.set_page_config(page_title="Presentation evaluation", page_icon="frontend/images/urfu_logo.png", layout="wide")

# add rtf logo based on theme
try:
	if st_theme()["base"] == "light":
		st.image("frontend/images/Long_logo_light.png", use_container_width=True)
	else:
		st.image("frontend/images/Long_logo_dark.png", use_container_width=True)
except TypeError:
	pass


# show title
st.title('Оценивание презентаций по проектному практикуму')

# creates two active tabs
tab1, tab2 = st.tabs(["Загрузка", "Текст запроса"])

with tab1:
	# Contains main parameters to send a request to LLM

	st.header("Загрузка презентации")

	# select models from these options (change names later)
	models = {
		"Meta: Llama 4 Maverick": "meta-llama/llama-4-maverick:free",
		"Meta: Llama 4 Scout": "meta-llama/llama-4-scout:free",
		"Google: Gemini 2.0 Flash Experimental": "google/gemini-2.0-flash-exp:free",
		"Google: Gemma 3 27B": "google/gemma-3-27b-it:free",
		"Qwen: Qwen2.5 VL 72B Instruct": "qwen/qwen2.5-vl-72b-instruct:free"
	}

	# allow user upload pdf and pptx formats only
	uploaded_file = st.file_uploader("Загрузите презентацию или pdf", type=["pptx", "pdf"])

	# stores user's model choice
	selected_model = st.selectbox('Выберите модель:', models.keys())

	# ensures that user wants to send presentation for evaluation
	user_consent = st.toggle("Подтверждаю обработку моей презентации")

	# checks if all requirements are met
	button_state = True
	if uploaded_file is not None and user_consent:
		button_state = False

	# add activation button that starts evaluation process
	activation_button = st.button("Отправить презентацию", disabled=button_state)
	if activation_button:
		# loading icon during evaluation time
		with st.spinner('Пожалуйста, подожите окончания оцненивания'):
			# insert here your processing function
			response = send_request(
				prompt="Опиши о чем говорится в презенации на каждом слайде не менне чем на 10000 символов, если хочешь напиши что-нибудь",
				presentation=uploaded_file.getvalue(),
				file_format=f"{uploaded_file.name.split(".")[-1]}",
				model=models[selected_model],

			)

		# show download button
		st.write('Оценка завершена, скачать отчет:')
		st.write('Скачать', response)


with tab2:
	# Takes default or user instructions on how to evaluate presentation

	st.header("Этот запрос отправится с вашей презентацией на оценку")

	# shows default prompt(change later) and allows to change it
	with open("frontend/default_prompt.txt", "r") as f:
		file = f.read()
	text = st.text_area("Запрос:", value=file, height=400)

	# saves changed prompt
	if st.button("Изменить текст запроса"):
		#  checks if prompt is empty
		if not text.strip():
			st.error("Добавьте текст запроса, поле не может быть пустым")
		else:
			with open("frontend/test.txt", "w") as f:
				f.write(text)
				st.toast("Текст запроса обновлен", icon="✅")
