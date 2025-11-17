#!/bin/sh
# Run backend in background
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# Run Streamlit frontend
streamlit run /app/app.py --server.port=8501 --server.address=0.0.0.0
