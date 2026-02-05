import pyrealsense2 as rs

# Check for connected devices
ctx = rs.context()
devices = ctx.query_devices()

print(f"Found {len(devices)} device(s)")
for dev in devices:
    print(f"  - {dev.get_info(rs.camera_info.name)}")
    print(f"    Serial: {dev.get_info(rs.camera_info.serial_number)}")