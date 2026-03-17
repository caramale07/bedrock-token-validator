# Bedrock Token Validator

A lightweight Streamlit app to test if your AWS Bedrock API key and model ID are working correctly. No conversation — just a single request/response.

## Run with Docker Compose

```bash
docker compose up --build
```

Open [http://localhost:8501](http://localhost:8501), paste your Bedrock API key, adjust the model ID if needed, and hit **Send Request**.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
