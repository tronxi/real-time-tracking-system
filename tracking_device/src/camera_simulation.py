import numpy as np, time, subprocess, math

W, H, FPS = 640, 480, 15
RTMP_URL = "rtmp://tronxi.ddns.net:1935/live/test"
FFMPEG = "ffmpeg"

ff = subprocess.Popen([
    FFMPEG, "-loglevel","error", "-fflags","nobuffer",
    "-f","rawvideo", "-pix_fmt","rgb24", "-s",f"{W}x{H}", "-r",str(FPS), "-i","-",
    "-c:v","libx264","-preset","veryfast","-tune","zerolatency",
    "-pix_fmt","yuv420p", "-f","flv", RTMP_URL
], stdin=subprocess.PIPE)

x = np.arange(W, dtype=np.uint16)
y = np.arange(H, dtype=np.uint16)
X, Y = np.meshgrid(x, y)

period = 1.0 / FPS
t = 0
try:
    while True:
        t0 = time.time()

        r16 = (X + 2*t)
        g16 = (Y + 3*t)

        cx = int((W/2) + (W/3)*math.sin(t/20.0))
        cy = int((H/2) + (H/3)*math.cos(t/18.0))
        mask = ((X.astype(np.int32)-cx)**2 + (Y.astype(np.int32)-cy)**2) < (40**2)

        b16_bg = (X//2 + Y//2 + t)
        b16 = np.where(mask, 255, b16_bg)

        r = (r16 & 0xFF).astype(np.uint8)
        g = (g16 & 0xFF).astype(np.uint8)
        b = (b16 & 0xFF).astype(np.uint8)

        frame = np.dstack([r, g, b])

        ff.stdin.write(frame.tobytes())
        t += 1

        dt = time.time() - t0
        if dt < period:
            time.sleep(period - dt)
except KeyboardInterrupt:
    pass
finally:
    try:
        ff.stdin.close()
    except Exception:
        pass
    ff.wait()
