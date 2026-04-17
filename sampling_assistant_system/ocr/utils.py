import cv2
import numpy as np
from PIL import Image


def process_image(image_path):
    """处理图片
    
    Args:
        image_path: 图片路径
        
    Returns:
        str: 处理后的图片路径
    """
    # 读取图片
    img = cv2.imread(image_path)
    
    # 灰度转换
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 二值化
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 保存处理后的图片
    processed_path = image_path.replace('.', '_processed.')
    cv2.imwrite(processed_path, binary)
    
    return processed_path


def clean_ocr_output(ocr_result):
    """清洗OCR输出
    
    Args:
        ocr_result: OCR原始结果
        
    Returns:
        list: 清洗后的结果
    """
    cleaned_result = []
    
    for line in ocr_result:
        for item in line:
            text = item[1][0]
            confidence = item[1][1]
            
            # 过滤低置信度结果
            if confidence > 0.5:
                cleaned_result.append({
                    'text': text,
                    'confidence': confidence
                })
    
    return cleaned_result
