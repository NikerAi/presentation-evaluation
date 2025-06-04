import streamlit as st
from streamlit_theme import st_theme
from backend.llm_call import send_request
from backend.converter import response_handler
import os

# config settings
PAGE_CONFIG = {
    "page_title": "Presentation evaluation",
    "page_icon": "frontend/images/urfu_logo.png",
    "layout": "wide"
}

MODELS = {
    "Meta: Llama 4 Maverick": "meta-llama/llama-4-maverick:free",
    "Meta: Llama 4 Scout": "meta-llama/llama-4-scout:free",
    "Mistral: Mistral Small 3.1 24B": "mistralai/mistral-small-3.1-24b-instruct:free",
    "Google: Gemma 3 27B": "google/gemma-3-27b-it:free",
    "Qwen: Qwen2.5 VL 72B Instruct": "qwen/qwen2.5-vl-72b-instruct:free",
    "Google: Gemini 2.5 Pro Experimental": "google/gemini-2.5-pro-exp-03-25"
}


def configure_page():
    """
    set main view of the page
    """
    # set browser tab name and icon
    st.set_page_config(**PAGE_CONFIG)
    # add rtf logo based on theme
    try:
        if st_theme()["base"] == "light":
            st.image("frontend/images/Long_logo_light.png", use_container_width=True)
        else:
            st.image("frontend/images/Long_logo_dark.png", use_container_width=True)
    except TypeError:
        pass
    # set title
    st.title("Оценивание презентаций по проектному практикуму")


def upload_tab():
    """
    Take uploaded file, prompt and pass them to the process function.
    Returns
    -------
        tuple[str, bytes, bytes, str]
            Response text, DOCX bytes, PDF bytes, and file name
    """
    st.header("Загрузка презентации")
    # allow user upload pdf and pptx formats only
    uploaded_file = st.file_uploader("Загрузите презентацию или pdf", type=["pptx", "pdf"])
    # warns user about supported file type for font analysis
    if uploaded_file is not None and uploaded_file.name.split(".")[-1] == "pdf":
        st.warning("⚠️ Анализ шрифтов поддерживается только в формате pptx ⚠️")
    # stores user's model choice
    selected_model = st.selectbox('Выберите модель:', MODELS.keys())
    # checks if presentation was uploaded
    if st.button("Отправить презентацию", disabled=not uploaded_file):
        try:
            with st.spinner('Пожалуйста, дождитесь окончания оценивания', show_time=True):
                response = process_presentation(uploaded_file, selected_model)
                response_text = response.choices[0].message.content
                docx_bytes, pdf_bytes = response_handler(response_text)
                return response_text, docx_bytes, pdf_bytes, uploaded_file.name
        except Exception as e:
            st.error(
                f"""Во время выполнения запроса возникла ошибка.
                Проверьте правильность загруженного документа или попробуйте воспользоваться другой моделью.
                \n\nИнформация об ошибке: {e}"""
            )
    return None, None, None, None


def process_presentation(uploaded_file, selected_model):
    """
    Send a request to OpenAI

    Parameters
    ----------
        uploaded_file: bytes
            An array of bytes from presentation uploaded by user
        selected_model: str
            Name of a model selected by user or default
    Returns
    ----------
        json
            text information received from LLM
    """
    response = send_request(
        prompt=st.session_state["prompt"],
        presentation=uploaded_file.getvalue(),
        file_format=f"{uploaded_file.name.split('.')[-1]}",
        model=MODELS[selected_model])
    return response


def show_prompt():
    """
    Show default instructions on how to evaluate presentation

    Returns
        ----------
        str
            text instructions on how to evaluate presentation
    """
    st.header("Этот запрос отправится с вашей презентацией на оценку")
    # shows default prompt(change later) and allows to change it
    with open("frontend/default_prompt.txt", "r") as f:
        file = f.read()
    text = st.text_area("Запрос:", value=file, height=400)
    st.session_state["prompt"] = text
    return text


def save_prompt(text):
    """
    Save user's prompt in session_state variable
    """
    # saves changed prompt
    if st.button("Изменить текст запроса"):
        #  checks if prompt is empty
        if not text.strip():
            st.error("❗Добавьте текст запроса, поле не может быть пустым❗")
        else:
            st.write(st.session_state["prompt"])
            st.toast("Текст запроса обновлен", icon="✅")
            st.session_state["prompt"] = text


def response_download(response, docx_bytes, pdf_bytes, name):
    """
    Uses response_handler to convert Markdown to DOCX and PDF, and allows downloading both
    """
    file_name = name.split('.')[0]
    with st.expander("Отчет"):
        st.markdown(response)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.download_button(
            label="Скачать отчет в DOCX",
            data=docx_bytes,
            file_name=f"{file_name}_результат.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    with col2:
        st.download_button(
            label="Скачать отчет в PDF",
            data=pdf_bytes,
            file_name=f"{file_name}_результат.pdf",
            mime="application/pdf",
        )
