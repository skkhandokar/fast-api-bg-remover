FROM python:3.10-slim

WORKDIR /app

# অনিক্স ও ইমেজ প্রসেসিংয়ের জন্য প্রয়োজনীয় লাইব্রেরি
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render-এর দেওয়া PORT পরিবেশক ভেরিয়েবলে uvicorn বাইন্ড করা
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000} --workers 1"]