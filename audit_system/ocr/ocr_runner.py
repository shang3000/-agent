import os
import json
import re
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import torch
from transformers import AutoProcessor, AutoModelForImageTextToText


class OCRRunner:
    """GLM-OCR 统一调用入口（生产可用版）"""

    def __init__(self, model_path="D:/AImodels/GLM-OCR"):
        print("正在加载 GLM-OCR 模型...")

        self.processor = AutoProcessor.from_pretrained(
            model_path,
            local_files_only=True
        )

        self.model = AutoModelForImageTextToText.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,   # ✅ 修复
            device_map="auto",
            use_safetensors=True,
            local_files_only=True
        )

        print("模型加载完成！")

        self.output_dir = Path("data/raw")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.prompt = self._build_prompt()

    # ================== Prompt ==================
    def _build_prompt(self):
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

        return f"""你是一个极其严谨的会计凭证提取专家。
图片是一张标准的记账凭证。

严格输出JSON，不要任何解释。

JSON格式：
{json.dumps(schema, ensure_ascii=False, indent=2)}

规则：
1. 只提取真实存在的分录行
2. 金额必须是纯数字字符串
3. 借贷只能填一侧
4. 行号从1开始连续
5. 不要补空行
"""

    # ================== 主入口 ==================
    def process_images(self, image_dir="./ocr/invoices"):
        image_files = [
            f for f in os.listdir(image_dir)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp'))
        ]

        if not image_files:
            raise Exception(f"在 {image_dir} 中没有找到图片")

        results = []

        for img_name in tqdm(image_files, desc="OCR处理"):
            img_path = os.path.join(image_dir, img_name)

            try:
                data = self._run_single(img_path)
                data["文件名"] = img_name
                results.append(data)

            except Exception as e:
                print(f"❌ 处理失败 {img_name}: {e}")
                results.append({"文件名": img_name, "错误": str(e)})

        return self._save_to_excel(results)

    # ================== 单张OCR ==================
    def _run_single(self, img_path):
        messages = [{
            "role": "user",
            "content": [
                {"type": "image", "url": img_path},  # ✅ 稳定写法
                {"type": "text", "text": self.prompt}
            ]
        }]

        inputs = self.processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)

        generated_ids = self.model.generate(
            **inputs,
            max_new_tokens=8192,
            do_sample=False,
            temperature=0.0
        )

        output_text = self.processor.decode(
            generated_ids[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=False
        )

        return self._safe_parse_json(output_text)

    # ================== JSON安全解析 ==================
    def _safe_parse_json(self, text):
        try:
            match = re.search(r'\{[\s\S]*\}', text)
            json_str = match.group(0) if match else "{}"
            return json.loads(json_str)
        except Exception:
            print("⚠️ JSON解析失败，截取内容：")
            print(text[:500])
            return {"error": "json_parse_failed"}

    # ================== Excel输出（关键优化） ==================
    def _save_to_excel(self, results):
        rows = []

        for item in results:
            entries = item.get("分录", [])

            if not entries:
                rows.append({
                    "文件名": item.get("文件名"),
                    "错误": item.get("error", "无分录")
                })
                continue

            for entry in entries:
                row = {
                    "文件名": item.get("文件名"),
                    "凭证日期": item.get("凭证日期"),
                    "凭证字号": item.get("凭证字号"),
                    "行号": entry.get("行号"),
                    "摘要": entry.get("摘要"),
                    "总账科目": entry.get("总账科目"),
                    "明细科目": entry.get("明细科目"),
                    "借方金额": entry.get("借方金额"),
                    "贷方金额": entry.get("贷方金额")
                }
                rows.append(row)

        df = pd.DataFrame(rows)

        output_file = self.output_dir / "ocr_output.xlsx"
        df.to_excel(output_file, index=False)

        print(f"\n✅ OCR完成，共处理 {len(results)} 张图片")
        print(f"输出文件: {output_file}")

        return str(output_file)