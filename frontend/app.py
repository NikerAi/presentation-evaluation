import streamlit as st
import frontend.interface as interface


def main():
    """
    load all necessary components of the web page
    to start app run this command in terminal "python -m streamlit run frontend/app.py"
    """
    # load page configuration
    interface.configure_page()
    # Initialize session state variables if they don't exist
    if "response" not in st.session_state:
        st.session_state["response"] = None
    if "docx_bytes" not in st.session_state:
        st.session_state["docx_bytes"] = None
    if "pdf_bytes" not in st.session_state:
        st.session_state["pdf_bytes"] = None
    if "name" not in st.session_state:
        st.session_state["name"] = None

    # creates two active tabs
    tab1, tab2 = st.tabs(["Загрузка", "Текст запроса"])
    # contains file uploader and process function
    with tab1:
        response, docx_bytes, pdf_bytes, name = interface.upload_tab()
        if response is not None:
            # Save results to session state
            st.session_state["response"] = response
            st.session_state["docx_bytes"] = docx_bytes
            st.session_state["pdf_bytes"] = pdf_bytes
            st.session_state["name"] = name

        # Display download buttons and report if available in session state
        if st.session_state["response"] is not None:
            interface.response_download(
                st.session_state["response"],
                st.session_state["docx_bytes"],
                st.session_state["pdf_bytes"],
                st.session_state["name"]
            )

    # contains default prompt and allows to change it
    with tab2:
        text = interface.show_prompt()
        interface.save_prompt(text)


if __name__ == "__main__":
    main()