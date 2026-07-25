FROM python:3.10-slim

WORKDIR /app

# AI ও সি-লাইব্রেরির জন্য প্রয়োজনীয় ডিপেন্ডেন্সি ইন্সটল
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render-এর দেওয়া $PORT ব্যবহার করার জন্য sh -c ব্যবহার করা হয়েছে (ডিফল্ট পোর্ট ১০০০০)
ENV PORT=10000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1"]