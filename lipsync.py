import wave
import time
import asyncio
import numpy as np
import pygame


def compute_mouth_frames(wav_path, fps=30, boost=1.4):
    """Đọc file WAV, trả về list giá trị mở miệng (0..1), mỗi giá trị ứng với 1 khung 1/fps giây."""
    wf = wave.open(wav_path, "rb")
    sample_rate = wf.getframerate()
    n_frames = wf.getnframes()
    n_channels = wf.getnchannels()
    sample_width = wf.getsampwidth()
    raw = wf.readframes(n_frames)
    wf.close()

    dtype = {1: np.int8, 2: np.int16, 4: np.int32}.get(sample_width)
    if dtype is None:
        return [], sample_rate

    data = np.frombuffer(raw, dtype=dtype).astype(np.float32)
    if n_channels > 1:
        data = data.reshape(-1, n_channels).mean(axis=1)

    max_val = float(np.iinfo(dtype).max) or 1.0
    data /= max_val

    samples_per_frame = max(1, int(sample_rate / fps))
    rms_frames = []
    for i in range(0, len(data), samples_per_frame):
        window = data[i:i + samples_per_frame]
        if len(window) == 0:
            break
        rms_frames.append(float(np.sqrt(np.mean(window ** 2))))

    if rms_frames:
        peak = max(rms_frames)
        if peak > 0:
            rms_frames = [min(1.0, (v / peak) * boost) for v in rms_frames]

    return rms_frames, sample_rate


async def speak_with_lipsync(wav_path, controller, fps=30):
    """Phát WAV không chặn và đẩy MouthOpen vào VTube Studio theo đồng hồ thực."""
    frames, _ = compute_mouth_frames(wav_path, fps=fps)
    frame_dt = 1.0 / fps

    pygame.mixer.init()
    pygame.mixer.music.load(wav_path)
    pygame.mixer.music.play()
    start = time.monotonic()

    try:
        while pygame.mixer.music.get_busy():
            elapsed = time.monotonic() - start
            idx = int(elapsed / frame_dt)
            value = frames[idx] if idx < len(frames) else 0.0
            await controller.set_mouth_open(value)
            await asyncio.sleep(frame_dt)
    finally:
        await controller.set_mouth_open(0.0)
        pygame.mixer.music.stop()
        pygame.mixer.quit()
