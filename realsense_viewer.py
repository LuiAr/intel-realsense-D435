import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()

# Enable both streams
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)  # Try rgb8 instead of bgr8

print('Starting pipeline...')
pipeline.start(config)
print('Success! Press Q to quit.')

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        # Convert to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Convert RGB to BGR for OpenCV
        color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)

        # Apply colormap to depth
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_image, alpha=0.03),
            cv2.COLORMAP_JET
        )

        # Show depth at centre
        centre_depth = depth_frame.get_distance(320, 240)
        cv2.putText(color_image, f"Centre depth: {centre_depth:.2f}m", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Stack side by side
        combined = np.hstack((color_image, depth_colormap))
        cv2.imshow('RealSense D435 - RGB | Depth', combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
