"""Optional training script — fine-tune MobileNetV2 on PlantVillage subset."""

import json
from pathlib import Path

# Run manually when dataset is available:
# python -m backend.ml.train_model --data-dir /path/to/plantvillage

if __name__ == "__main__":
    print(
        "Training requires a local PlantVillage dataset directory.\n"
        "Place images in subfolders per class matching class_map.py names.\n"
        "The prototype ships with ImageNet-pretrained MobileNetV2 head for demo inference.\n"
        "Field validation with locally collected images is required before production use."
    )
    artifacts = Path(__file__).parent / "artifacts"
    artifacts.mkdir(exist_ok=True)
    from app.ml.class_map import CLASS_MAP

    with open(artifacts / "class_map.json", "w") as f:
        json.dump(CLASS_MAP, f, indent=2)
    print(f"Wrote class map to {artifacts / 'class_map.json'}")
