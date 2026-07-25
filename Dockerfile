FROM python:3.10-slim

WORKDIR /app

# AI ও সি-লাইব্রেরির জন্য প্রয়োজনীয় ডিপেন্ডেন্সি ইন্সটল
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# FastAPI রান করতে Uvicorn ব্যবহার করা হচ্ছে (মাত্র ১টি ওয়ার্কার দিয়ে র‍্যাম সেভ করার জন্য)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]