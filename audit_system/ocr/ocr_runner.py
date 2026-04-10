import os
import json
import re
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import torch
from transformers import AutoProcessor, AutoModelForImageTextToText
from PIL import Image


class OCRRunner:
    """GLM-OCR 统一调用入口（已优化记账凭证提取）"""

    def __init__(self, model_path="D:/AImodels/GLM-OCR"):
        print("正在加载 GLM-OCR 模型...")
        self.processor = AutoProcessor.from_pretrained(model_path, local_files_only=True)

        self.model = AutoModelForImageTextToText.from_pretrained(
            model_path,
            dtype=torch.bfloat16,
            device_map="auto",
            use_safetensors=True,
            local_files_only=True
        )
        print("模型加载完成！")

        self.output_dir = Path("data/raw")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.prompt = self._build_strong_prompt()

    def _build_strong_prompt(self):
        schema = {
            "凭证类型": "记账凭证",
            "凭证日期": "",
            "凭证字号": "",
            "附件张数": "",
            "分录": [
                {
                    "行号": "",
                    "摘要": "",
                    "总账科目": "",
                    "明细科目": "",
                    "借方金额": "",
                    "贷方金额": ""
                }
            ],
            "借方合计": "",
            "贷方合计": "",
            "会计主管": "",
            "记账": "",
            "出纳": "",
            "审核": "",
            "制单": "",
            "备注": ""
        }

        return f"""你是一个极其严谨的会计分录提取专家。
图片是一张标准的记账凭证表格。请**只提取图片中真实存在的分录行**，不要补空行，不要猜测。

严格按照以下JSON格式输出，不要添加任何解释、代码块或多余文字。

JSON格式：
{json.dumps(schema, ensure_ascii=False, indent=2)}

核心规则：
1. 只提取表格中真正有内容的行（摘要或科目有文字的行）
2. 金额必须是纯数字字符串（如 "30000000"），绝不能带 ¥、逗号、单位
3. 借方金额和贷方金额只能填写有数字的那一列，另一列留空字符串 ""
4. "行号" 从 1 开始连续编号
5. 如果图片中只有 3 行分录，就只输出 3 行，不要多输出空行
6. 签字人姓名要准确提取"""

    def process_images(self, image_dir="./invoices"):
        """批量处理图片文件夹"""
        image_files = [f for f in os.listdir(image_dir)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'))]

        if not image_files:
            raise Exception(f"在 {image_dir} 中没有找到图片")

        results = []

        for img_name in tqdm(image_files, desc="OCR处理"):
            img_path = os.path.join(image_dir, img_name)
            try:
                image = Image.open(img_path).convert("RGB")

                messages = [{
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image},
                        {"type": "text", "text": self.prompt}
                    ]
                }]

                inputs = self.processor.apply_chat_template(
                    messages, tokenize=True, add_generation_prompt=True,
                    return_dict=True, return_tensors="pt"
                ).to(self.model.device)

                generated_ids = self.model.generate(
                    **inputs, max_new_tokens=8192, do_sample=False, temperature=0.0
                )

                output_text = self.processor.decode(
                    generated_ids[0][inputs["input_ids"].shape[1]:], skip_special_tokens=False
                )

                json_match = re.search(r'\{[\s\S]*\}', output_text)
                json_str = json_match.group(0) if json_match else "{}"

                data = json.loads(json_str)
                data["文件名"] = img_name
                results.append(data)

            except Exception as e:
                print(f"处理失败 {img_name}: {e}")
                results.append({"文件名": img_name, "错误": str(e)})

        return self._save_to_excel(results)

    def _save_to_excel(self, results):
        """保存为 Excel"""
        df = pd.json_normalize(results)
        output_file = self.output_dir / "ocr_output.xlsx"
        df.to_excel(output_file, index=False)

        print(f"\nOCR 处理完成！共处理 {len(results)} 张图片")
        print(f"输出文件: {output_file}")
        return str(output_file)