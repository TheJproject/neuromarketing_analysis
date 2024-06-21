# Neuromarketing Analysis

## Overview
This project provides a FastAPI-based service to analyze marketing assets and generate insights based on visual salience and cognitive load. It includes a Streamlit application for interactive demonstrations.

## Directory Structure
- `app/`: Contains the FastAPI application code.
- `streamlit_app.py`: Streamlit app for the demo.
- `Dockerfile`: Docker configuration for containerizing the application.
- `requirements.txt`: Python dependencies.
- `docker-compose.yaml`: Docker Compose configuration for orchestrating the application and its services.

## Getting Started
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/neuromarketing_analysis.git
   cd neuromarketing_analysis
   ```
2. **Build and run the application using Docker Compose:**
   ```sh
   docker-compose up --build
   ```
3. **Access the FastAPI application:**
   - Navigate to `http://localhost:8000/docs` in your web browser.
4. **Access the Streamlit application:**
   - Navigate to `http://localhost:8501` in your web browser.
