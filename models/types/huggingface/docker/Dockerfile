FROM alvarobartt/torch-gpu:py310-cu12.3-torch-2.2.0 AS build

WORKDIR /app

COPY requirements.txt .
COPY predictor.py .

RUN pip install --no-cache-dir -r requirements.txt

ARG HF_TASK
ENV HF_TASK=${HF_TASK}
ENV VERTEX_CPR_WEB_CONCURRENCY=1

ENTRYPOINT ["python", "-m", "google.cloud.aiplatform.prediction.server.app", "--predictor_class", "predictor.HuggingFacePredictor"] 