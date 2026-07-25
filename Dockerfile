FROM python:3.10-slim

WORKDIR /app

# সি-লাইব্রেরির জন্য প্রয়োজনীয় ডিপেন্ডেন্সি
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# সরাসরি python main.py দিয়েই অ্যাপ স্টার্ট হবে
CMD ["python", "main.py"]