from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
import json
import time
from camera import RealSenseCamera

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

camera = RealSenseCamera()

@app.on_event("startup")
async def startup_event():
    # Only start if not already running (managed by class)
    pass

@app.on_event("shutdown")
async def shutdown_event():
    camera.release()

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(camera.generate_frames(), 
                             media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/data")
def get_data():
    return camera.get_data()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
