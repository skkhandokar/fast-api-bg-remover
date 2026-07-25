import io
from PIL import Image
from rembg import remove, new_session
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ফ্রন্টএন্ড (React/Next.js/HTML) থেকে রিকুয়েস্ট এলাউ করার জন্য CORS কনফিগারেশন
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Render-এর ফ্রি ৫১২MB RAM-এর উপযোগী লাইটওয়েট 'u2netp' মডেল সেশন
session = new_session("u2netp")

@app.get("/")
def home():
    return {"message": "Background Removal API is Running!"}

@app.post("/api/remove-bg/")
async def remove_background(image: UploadFile = File(...)):
    # ১. ফ্রন্টএন্ড থেকে আসা ফাইল বাইট হিসেবে পড়া
    contents = await image.read()
    input_image = Image.open(io.BytesIO(contents))
    
    # ২. ব্যাকগ্রাউন্ড রিমুভ করা
    output_image = remove(input_image, session=session)
    
    # ৩. ট্রান্সপারেন্ট PNG ইমেজ ইন-মেমোরি বাফারে সেভ করা
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    
    # ৪. সরাসরি PNG ইমেজ রেসপন্স রিটার্ন করা
    return Response(content=img_byte_arr.getvalue(), media_type="image/png")