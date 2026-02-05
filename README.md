## Intel RealSense D435 High-FPS Viewer

This project delivers a full-stack dashboard that streams Intel RealSense D435 RGB + depth video at the camera’s peak throughput and surfaces live telemetry for Master Thesis RISE experiments.

### Features
- 90 FPS stereo depth + RGB capture at 848×480 using `pyrealsense2`.
- FastAPI backend that exposes an MJPEG feed (`/video_feed`) and status endpoint (`/data`) with live FPS measurements.
- React/Vite frontend that visualizes the fused stream, monitors connection/stream mode, and prepares for burst captures.

### Getting Started
1. **Backend**
   ```bash
   cd backend
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
   The backend boots the RealSense pipeline in high-speed mode and begins serving frames immediately.

2. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Open the Vite dev server (default http://localhost:5173) to view the dashboard. The Stream View overlay displays the measured FPS reported by the backend.

### Notes
- This repository targets the Intel RealSense D435 exclusively; no fallback camera profiles are loaded.
- For standalone debugging, `realsense_viewer.py` provides a quick OpenCV window that mirrors the 90 FPS settings.
- Ensure your USB 3.1 connection and lighting allow the D435 to sustain the requested frame rate; the dashboard will show the actual measured FPS for transparency.
