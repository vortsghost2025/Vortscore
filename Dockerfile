FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 7860
CMD ["uvicorn", "src.api.engine_api:app", "--host", "0.0.0.0", "--port", "7860"]
