FROM python:3.12-slim
RUN apt update -y
RUN apt install -y libreoffice poppler-utils libpoppler-cpp-dev pandoc
COPY . /opt/pe_project
WORKDIR /opt/pe_project/
RUN if [ -f backend/requirements.txt ]; then pip install -r backend/requirements.txt; fi
RUN if [ -f frontend/requirements.txt ]; then pip install -r frontend/requirements.txt; fi
CMD ["python3", "-m", "streamlit", "run", "frontend/app.py"]
