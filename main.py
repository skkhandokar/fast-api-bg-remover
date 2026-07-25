import io
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session = None

@app.api_route("/", methods=["GET", "HEAD"])
def home():
    return {"status": "ok", "message": "Background Removal API is Live!"}

@app.post("/api/remove-bg/")
async def remove_background(image: UploadFile = File(...)):
    global session
    
    # স্থানীয়ভাবে (Locally) ইমপোর্ট করা যাতে অ্যাপ চালুর সময় কোনো বাধা না আসে
    from rembg import remove, new_session
    
    if session is None:
        session = new_session("u2netp")
        
    contents = await image.read()
    input_image = Image.open(io.BytesIO(contents))
    
    output_image = remove(input_image, session=session)
    
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    
    return Response(content=img_byte_arr.getvalue(), media_type="image/png")