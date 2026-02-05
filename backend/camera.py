import pyrealsense2 as rs
import numpy as np
import cv2
import threading
import time

class RealSenseCamera:
    """High-FPS RealSense D435 capture helper."""

    FRAME_WIDTH = 848
    FRAME_HEIGHT = 480
    STREAM_FPS = 90

    def __init__(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(
            rs.stream.depth,
            self.FRAME_WIDTH,
            self.FRAME_HEIGHT,
            rs.format.z16,
            self.STREAM_FPS,
        )
        self.config.enable_stream(
            rs.stream.color,
            self.FRAME_WIDTH,
            self.FRAME_HEIGHT,
            rs.format.rgb8,
            self.STREAM_FPS,
        )

        self.device_name = "Unknown"
        self.profile = None

        try:
            self.profile = self.pipeline.start(self.config)
            device = self.profile.get_device()
            self.device_name = device.get_info(rs.camera_info.name)
            print(f"Pipeline started at {self.STREAM_FPS} FPS for {self.device_name}.")
        except RuntimeError as e:
            print(f"Error starting pipeline: {e}")
            # Handle case where device is not connected for testing purposes
            self.pipeline = None

        self.lock = threading.Lock()
        self._last_frame_ts = None
        self._fps_ewma = 0.0

    def get_frame(self):
        if not self.pipeline:
            # Return dummy frames if no camera
            return None, None
            
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        
        if not depth_frame or not color_frame:
            return None, None
            
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        return color_image, depth_image, depth_frame

    def generate_frames(self):
        while True:
            with self.lock:
                if self.pipeline:
                    try:
                        color_image, depth_image, _ = self.get_frame()
                        if color_image is None:
                            continue

                        now = time.time()
                        if self._last_frame_ts is not None:
                            delta = max(now - self._last_frame_ts, 1e-6)
                            instant_fps = 1.0 / delta
                            if self._fps_ewma == 0.0:
                                self._fps_ewma = instant_fps
                            else:
                                self._fps_ewma = 0.9 * self._fps_ewma + 0.1 * instant_fps
                        self._last_frame_ts = now
                            
                        # Convert RGB to BGR for OpenCV
                        color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)
                        
                        # Apply colormap to depth
                        depth_colormap = cv2.applyColorMap(
                            cv2.convertScaleAbs(depth_image, alpha=0.03), 
                            cv2.COLORMAP_JET
                        )
                        
                        # Stack images horizontally
                        images = np.hstack((color_image, depth_colormap))
                        
                        # Encode to JPEG
                        ret, buffer = cv2.imencode('.jpg', images)
                        frame = buffer.tobytes()
                        
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    except Exception as e:
                        print(f"Error generating frame: {e}")
                        time.sleep(0.1)
                else:
                    # Serve a placeholder image if no camera
                    blank_image = np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH * 2, 3), np.uint8)
                    cv2.putText(blank_image, "No Camera Connected", (400, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    ret, buffer = cv2.imencode('.jpg', blank_image)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    time.sleep(1)

    def get_data(self):
        if self.pipeline:
            fps = round(self._fps_ewma, 1) if self._fps_ewma else 0.0
            return {
                "status": "connected",
                "temp": "N/A",
                "fps": fps,
                "depth_resolution": f"{self.FRAME_WIDTH}x{self.FRAME_HEIGHT}",
                "color_resolution": f"{self.FRAME_WIDTH}x{self.FRAME_HEIGHT}",
                "stream_mode": f"{self.STREAM_FPS}fps high-speed",
                "device_name": self.device_name,
            }
        return {
            "status": "disconnected",
            "temp": "N/A",
            "fps": 0.0,
            "depth_resolution": "0x0",
            "color_resolution": "0x0",
            "stream_mode": "offline",
            "device_name": "Intel RealSense D435",
        }

    def release(self):
        if self.pipeline:
            self.pipeline.stop()
