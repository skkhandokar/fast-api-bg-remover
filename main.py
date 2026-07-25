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

# সেশন শুরুতে None থাকবে (Lazy Loading)
session = None

def get_session():
    global session
    if session is None:
        # রিকুয়েস্ট আসলে প্রথমবার মডেল লোড হবে
        session = new_session("u2netp")
    return session

@app.get("/")
def home():
    return {"status": "ok", "message": "Background Removal API is Live!"}

@app.post("/api/remove-bg/")
async def remove_background(image: UploadFile = File(...)):
    contents = await image.read()
    input_image = Image.open(io.BytesIO(contents))
    
    # প্রথমবার কল হলে মডেল লোড হবে
    current_session = get_session()
    output_image = remove(input_image, session=current_session)
    
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    
    return Response(content=img_byte_arr.getvalue(), media_type="image/png")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)