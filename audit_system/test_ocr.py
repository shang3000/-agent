from ocr.ocr_runner import OCRRunner
import os

# ================== 配置 ==================
# 使用绝对路径，避免相对路径出错
IMAGE_DIR = r"D:\pycharm\AIaplication\audit_system\ocr\invoices"

# 如果你想让程序自动创建文件夹，可以加下面这行
os.makedirs(IMAGE_DIR, exist_ok=True)

# ================== 执行 OCR ==================
ocr = OCRRunner()                    # 使用默认模型路径
result_file = ocr.process_images(IMAGE_DIR)

print(f"\n处理完成！结果文件路径：{result_file}")