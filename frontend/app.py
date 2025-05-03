import streamlit as st
import frontend.interface as interface


def main():
	"""
	load all necessary components of the web page
	to start app run this command in terminal "python -m streamlit run frontend/app.py"
	"""
	# load page configuration
	interface.configure_page()
	# creates two active tabs
	tab1, tab2 = st.tabs(["Загрузка", "Текст запроса"])
	# contains file uploader and process function
	with tab1:
		response, name = interface.upload_tab()
		if response is not None:
			with st.expander("Отчёт"):
				st.write(response)
			st.download_button("Скачать", response, f"{name.split('.')[0]}_результат.txt")
	# contains default prompt and allows to change it
	with tab2:
		text = interface.show_prompt()
		interface.save_prompt(text)


if __name__ == "__main__":
	main()
