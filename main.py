import os
import io
import uvicorn
from PIL import Image
from rembg import remove, new_session
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS কনফিগারেশন
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# লাইটওয়েট 'u2netp' মডেল সেশন
session = new_session("u2netp")

@app.get("/")
def home():
    return {"message": "Background Removal API is Running!"}

@app.post("/api/remove-bg/")
async def remove_background(image: UploadFile = File(...)):
    contents = await image.read()
    input_image = Image.open(io.BytesIO(contents))
    
    # ব্যাকগ্রাউন্ড রিমুভ করা
    output_image = remove(input_image, session=session)
    
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    
    return Response(content=img_byte_arr.getvalue(), media_type="image/png")

# এই অংশটি সার্ভিসটিকে ডায়নামিক পোর্টে রান করবে
if __name__ == "__main__":
    # Render-এর দেওয়া PORT ধরবে, না পেলে ১০০০০ পোর্টে চলবে
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)