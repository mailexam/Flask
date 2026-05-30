FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY mail.py app.py ./

ENV HTTP_HOST=0.0.0.0
ENV HTTP_PORT=5000

EXPOSE 5000

CMD ["sh", "-c", "python app.py"]
