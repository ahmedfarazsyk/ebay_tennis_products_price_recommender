from python:3.11-slim
workdir /app
RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*
copy requirements.txt .
run pip install --no-cache-dir -r requirements.txt
copy . .
cmd ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]