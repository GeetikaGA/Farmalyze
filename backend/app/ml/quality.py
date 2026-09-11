"""Image quality assessment before ML inference."""

import cv2
import numpy as np


def assess_image_quality(image_array: np.ndarray) -> dict:
    """
    Returns quality score 0-1 and acceptability flag.
    Checks: resolution, blur (Laplacian variance), brightness.
    """
    h, w = image_array.shape[:2]
    min_dim = min(h, w)

    if min_dim < 128:
        return {
            "acceptable": False,
            "score": 0.15,
            "message": "Image resolution is too low. Please capture a closer, clearer photo.",
        }

    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY) if len(image_array.shape) == 3 else image_array
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    brightness = float(np.mean(gray))

    blur_score = min(1.0, lap_var / 120.0)
    if lap_var < 30:
        return {
            "acceptable": False,
            "score": round(blur_score * 0.3, 2),
            "message": (
                "Image quality is too low for reliable analysis. "
                "Please capture a clearer image showing the affected area."
            ),
        }

    brightness_score = 1.0
    if brightness < 40:
        brightness_score = brightness / 40
        if brightness < 25:
            return {
                "acceptable": False,
                "score": round(blur_score * brightness_score * 0.4, 2),
                "message": "Image is too dark. Please retake in better lighting.",
            }
    elif brightness > 220:
        brightness_score = max(0.3, (255 - brightness) / 35)

    resolution_score = min(1.0, min_dim / 512)
    combined = blur_score * 0.5 + brightness_score * 0.25 + resolution_score * 0.25
    acceptable = combined >= 0.45 and lap_var >= 50

    message = None
    if not acceptable:
        message = (
            "Image quality is too low for reliable analysis. "
            "Please capture a clearer image showing the affected area."
        )

        return {
            "acceptable": bool(acceptable),
            "score": round(float(combined), 2),
            "message": message,
        }
