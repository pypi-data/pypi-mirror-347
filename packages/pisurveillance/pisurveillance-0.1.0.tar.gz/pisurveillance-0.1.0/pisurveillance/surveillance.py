import asyncio
import logging
from datetime import datetime
from io import BytesIO
from typing import Optional

import aiohttp
import cv2

from pisurveillance.config import env

# Configuration
INFERENCE_URL = f"{env.INFERENCE_BASE_URL}/process"


def capture_image(camera_index: Optional[int] = env.CAMERA_INDEX):
    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            raise RuntimeError("Unable to open camera.")
        ret, frame = cap.read()
    finally:
        cap.release()

    if not ret:
        raise RuntimeError("Failed to capture image from camera.")

    # Convert to JPEG bytes for sending
    ret, jpeg = cv2.imencode(".jpg", frame)
    if not ret:
        raise RuntimeError("Failed to encode image to JPEG.")

    return BytesIO(jpeg.tobytes())


async def send_image(image_stream: BytesIO):
    # Send to server
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                INFERENCE_URL,
                data={"image": ("image.jpg", image_stream, "image/jpeg")},
            ) as response:
                if response.status >= 400:
                    message = await response.text()
                    logging.error(f"Inference error {response.status}: {message}")

    except Exception as e:
        logging.error(f"Error sending image: {e}")


async def start_surveillance(
    capture_frequency: Optional[int] = env.CAPTURE_FREQUENCY,
    device_name: Optional[str] = env.DEVICE_NAME,
    camera_index: Optional[int] = env.CAMERA_INDEX,
):
    try:
        logging.info("👀 Starting surveillance 👀")
        logging.info(f"Device name: {device_name}")
        logging.info(f"Camera index: {camera_index}")
        logging.info(f"Inference server: {INFERENCE_URL}\n\n")
        logging.info("Press Ctrl+C to interrupt\n\n")

        while True:
            logging.info(f"Capturing image at {datetime.now()}")
            image = capture_image()
            await send_image(image)
            await asyncio.sleep(capture_frequency)

    except asyncio.CancelledError:
        logging.info("🛑 Surveillance cancelled via asyncio.")
    except KeyboardInterrupt:
        logging.info("🛑 Surveillance interrupted by user (Ctrl+C).")
