from __future__ import annotations

"""Modular ML inference layer — MobileNetV2 transfer learning."""

import json
import logging
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image

from app.ml.class_map import CLASS_MAP, CROP_ALIASES
from app.ml.explainability import generate_gradcam
from app.ml.quality import assess_image_quality

logger = logging.getLogger(__name__)

IMG_SIZE = (224, 224)


class DiseaseClassifier:
    def __init__(self, model_path: str, class_map_path: str, heatmap_dir: str) -> None:
        self.model_path = Path(model_path)
        self.class_map_path = Path(class_map_path)
        self.heatmap_dir = heatmap_dir
        self.model: tf.keras.Model | None = None
        self.class_names: list[str] = CLASS_MAP
        self._load()

    def _load(self) -> None:
        if self.class_map_path.exists():
            with open(self.class_map_path) as f:
                self.class_names = json.load(f)

        if self.model_path.exists():
            self.model = tf.keras.models.load_model(self.model_path)
            logger.info("Loaded ML model from %s", self.model_path)
        else:
            logger.warning(
                "Model not found at %s — building prototype model. "
                "Run backend/ml/train_model.py for better weights.",
                self.model_path,
            )
            self.model = self._build_prototype_model()
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            self.model.save(self.model_path)
            with open(self.class_map_path, "w") as f:
                json.dump(self.class_names, f)

    def _build_prototype_model(self) -> tf.keras.Model:
        base = tf.keras.applications.MobileNetV2(
            input_shape=(*IMG_SIZE, 3),
            include_top=False,
            weights="imagenet",
        )
        base.trainable = False
        inputs = tf.keras.Input(shape=(*IMG_SIZE, 3))
        x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
        x = base(x, training=False)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dropout(0.3)(x)
        outputs = tf.keras.layers.Dense(len(self.class_names), activation="softmax")(x)
        model = tf.keras.Model(inputs, outputs)
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
        return model

    def _preprocess(self, image_array: np.ndarray) -> np.ndarray:
        if image_array.max() <= 1.0:
            image_array = (image_array * 255).astype(np.uint8)
        pil = Image.fromarray(image_array).convert("RGB")
        pil = pil.resize(IMG_SIZE)
        arr = np.array(pil, dtype=np.float32)
        return arr

    def _filter_by_crop(self, crop: str, probs: np.ndarray) -> tuple[int, float, str]:
        crop_norm = CROP_ALIASES.get(crop.lower(), crop)
        mask = np.array([1.0 if c.startswith(crop_norm) else 0.0 for c in self.class_names])
        if mask.sum() == 0:
            idx = int(np.argmax(probs))
            return idx, float(probs[idx]), self.class_names[idx]

        masked = probs * mask
        if masked.sum() == 0:
            idx = int(np.argmax(probs))
            return idx, float(probs[idx]), self.class_names[idx]
        masked /= masked.sum()
        idx = int(np.argmax(masked))
        return idx, float(masked[idx]), self.class_names[idx]

    def predict(
        self,
        image_path: str,
        crop: str,
        confidence_high: float,
        confidence_medium: float,
    ) -> dict:
        image = Image.open(image_path).convert("RGB")
        image_array = np.array(image)
        quality = assess_image_quality(image_array)

        if not quality["acceptable"]:
            return {
                "skipped_inference": True,
                "image_quality": quality,
                "disease": "Analysis skipped",
                "confidence": 0.0,
                "confidence_level": "low",
                "class_index": -1,
                "explanation": {"available": False, "heatmap_url": None, "message": quality["message"]},
            }

        preprocessed = self._preprocess(image_array)
        batch = np.expand_dims(preprocessed, axis=0)
        batch_model = tf.keras.applications.mobilenet_v2.preprocess_input(batch.copy())

        probs = self.model.predict(batch_model, verbose=0)[0]
        class_idx, confidence, class_name = self._filter_by_crop(crop, probs)

        if confidence >= confidence_high:
            level = "high"
        elif confidence >= confidence_medium:
            level = "medium"
        else:
            level = "low"

        disease = class_name.split("_", 1)[-1].replace("_", " ")
        heatmap_url, err = generate_gradcam(self.model, preprocessed, class_idx, self.heatmap_dir)

        return {
            "skipped_inference": False,
            "image_quality": quality,
            "disease": disease,
            "confidence": round(confidence, 4),
            "confidence_level": level,
            "class_index": class_idx,
            "raw_class": class_name,
            "explanation": {
                "available": heatmap_url is not None,
                "heatmap_url": heatmap_url,
                "message": err or "Grad-CAM highlights regions that influenced the model prediction.",
            },
        }


_classifier: DiseaseClassifier | None = None


def get_classifier(model_path: str, class_map_path: str, heatmap_dir: str) -> DiseaseClassifier:
    global _classifier
    if _classifier is None:
        _classifier = DiseaseClassifier(model_path, class_map_path, heatmap_dir)
    return _classifier
