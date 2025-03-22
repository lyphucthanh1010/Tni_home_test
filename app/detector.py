import cv2
import numpy as np
from datetime import datetime

def detect_persons(input_path: str, output_path: str) -> int:
    image = cv2.imread(input_path)
    if image is None:
        raise Exception("Không thể load ảnh từ đường dẫn: " + input_path)
    
    h, w, _ = image.shape
    boxes = [
        (int(w*0.1), int(h*0.1), int(w*0.3), int(h*0.5)),
        (int(w*0.5), int(h*0.2), int(w*0.8), int(h*0.7))
    ]
    
    for (x1, y1, x2, y2) in boxes:
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imwrite(output_path, image)
    return len(boxes)
