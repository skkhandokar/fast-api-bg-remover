FROM python:3.10-slim

WORKDIR /app

# প্রয়োজনীয় সি-লাইব্রেরি
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render-এর জন্য ১০০০০ পোর্ট এক্সপোজ ও সেট করা
EXPOSE 10000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000", "--workers", "1"]