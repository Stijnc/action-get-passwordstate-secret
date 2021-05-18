FROM python:3-slim
COPY ./src /app
WORKDIR /app
RUN pip install --target=/app -r requirements.txt
ENV PYTHONPATH /app

ENTRYPOINT [ "python3", "/app/entrypoint.py"]