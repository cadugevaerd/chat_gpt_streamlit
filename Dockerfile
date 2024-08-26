FROM python:slim

EXPOSE 8501
WORKDIR /app

COPY *.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "openai_chat.py", "--server.port=8501", "--server.address=0.0.0.0"]