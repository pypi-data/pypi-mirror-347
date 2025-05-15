import cv2
import yaml
from pathlib import Path
from typing import Any, Dict
from PIL import Image
import numpy as np
from mmllm_face_refinement.face_detector import YoloFaceDetector

class Detector:
    def __init__(self, model_paths: dict = None, config_path: str = None):
        if config_path is None:
            config_path = str(Path(__file__).parent.parent / 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        # Optionally override model paths
        if model_paths:
            self.config['yolo']['model_path'] = model_paths.get('yolo', self.config['yolo']['model_path'])
        self.detector = YoloFaceDetector(
            model_path=self.config['yolo'].get('model_path'),
            confidence_threshold=self.config['yolo']['confidence_threshold'],
            iou_threshold=self.config['yolo']['iou_threshold'],
            device=self.config['yolo']['device']
        )

    def infer_faces(self, img, model=None, model_config=None):
        """
        Detect faces in an image using YOLO face detector.
        Args:
            img: np.ndarray (BGR or RGB)
            model: ignored (for API compatibility)
            model_config: must have .name (should start with 'yolo')
        Returns:
            faces: list of [x, y, w, h] (int)
        """
        # Convert to RGB if needed
        if isinstance(img, np.ndarray):
            if img.shape[-1] == 3:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                raise ValueError("Input image must have 3 channels (BGR or RGB)")
            pil_img = Image.fromarray(img_rgb)
            temp_path = 'temp/_infer_temp.jpg'
            pil_img.save(temp_path)
            image_path = temp_path
        elif isinstance(img, str):
            image_path = img
        else:
            raise ValueError("img must be a numpy array or image path")
        detections = self.detector.detect(image_path)
        faces = []
        for det in detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            w = x2 - x1
            h = y2 - y1
            faces.append([x1, y1, w, h])
        return faces

def infer_faces(img, model, model_config):
    """
    API-compatible face inference function for external use.
    Args:
        img: np.ndarray (BGR or RGB)
        model: Detector instance
        model_config: must have .name (should start with 'yolo')
    Returns:
        faces: list of [x, y, w, h] (int)
    """
    if hasattr(model, 'infer_faces'):
        return model.infer_faces(img, model, model_config)
    raise ValueError("Model must be an instance of Detector from mmllm_face_refinement.init()") 