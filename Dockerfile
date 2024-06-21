FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y curl && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app /app/app
COPY ./streamlit_app.py /app/streamlit_app.py

# Run both FastAPI and Streamlit
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run /app/streamlit_app.py --server.port=8501 --server.address=0.0.0.0"]
