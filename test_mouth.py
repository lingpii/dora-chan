"""Test cô lập: chỉ bơm MouthOpen vào VTube Studio, không dính chat/voice.
Chạy: python test_mouth.py  (trong env có pyvts)
Quan sát: miệng model có mấp máy đều trong ~6 giây không?
"""
import asyncio
import math
from vtube import VTubeController


async def main():
    controller = VTubeController()
    await controller.connect()
    print("[test] đã kết nối. Bắt đầu bơm MouthOpen trong 6 giây...")

    fps = 15
    duration = 6.0
    steps = int(duration * fps)
    errors = 0
    for i in range(steps):
        # hình sin 0..1, ~1.5 chu kỳ/giây
        value = (math.sin(i / fps * 2 * math.pi * 1.5) + 1) / 2
        try:
            await controller.set_mouth_open(value)
        except Exception as e:
            errors += 1
            print(f"[test] lỗi bơm tại bước {i}: {e}")
        await asyncio.sleep(1 / fps)

    await controller.set_mouth_open(0.0)
    print(f"[test] xong. Số lần lỗi: {errors}/{steps}")
    await controller.vts.close()


if __name__ == "__main__":
    asyncio.run(main())
