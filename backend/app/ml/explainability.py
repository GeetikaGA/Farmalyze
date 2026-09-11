from __future__ import annotations

"""Grad-CAM explainability — real heatmap generation, not faked."""

import uuid
from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image


def generate_gradcam(
    model: tf.keras.Model,
    image_array: np.ndarray,
    class_index: int,
    output_dir: str,
    last_conv_layer_name: str = "conv4_block6_1_relu",
) -> tuple[str | None, str | None]:
    """
    Generate Grad-CAM heatmap for the predicted class.
    Returns (heatmap_relative_url, error_message).
    """
    try:
        img = tf.image.resize(image_array, (224, 224))
        img = tf.cast(img, tf.float32)
        batch = tf.expand_dims(img, axis=0)

        grad_model = tf.keras.Model(
            [model.inputs],
            [model.get_layer(last_conv_layer_name).output, model.output],
        )

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(batch)
            loss = predictions[:, class_index]

        grads = tape.gradient(loss, conv_outputs)
        if grads is None:
            return None, "Gradients unavailable for explainability."

        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
        heatmap_np = heatmap.numpy()

        heatmap_resized = cv2.resize(heatmap_np, (image_array.shape[1], image_array.shape[0]))
        heatmap_uint8 = np.uint8(255 * heatmap_resized)
        heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)

        if image_array.max() <= 1.0:
            base = (image_array * 255).astype(np.uint8)
        else:
            base = image_array.astype(np.uint8)

        overlay = cv2.addWeighted(base, 0.55, heatmap_color, 0.45, 0)

        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.jpg"
        out_path = out_dir / filename
        Image.fromarray(overlay).save(out_path, quality=90)

        return f"/uploads/heatmaps/{filename}", None
    except Exception as exc:
        return None, f"Explainability unavailable: {exc}"
