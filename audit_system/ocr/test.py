import os
import json
import pandas as pd
import re
from tqdm import tqdm
import torch
from transformers import AutoProcessor, AutoModelForImageTextToText

# ================== 配置区（已优化） ==================
MODEL_PATH = "D:/AImodels/GLM-OCR"
IMAGE_FOLDER = "./invoices/"
OUTPUT_EXCEL = "记账凭证提取结果_优化版.xlsx"

JSON_SCHEMA = {
    "凭证类型": "记账凭证",
    "凭证日期": "",
    "凭证字号": "",
    "附件张数": "",
    "分录": [
        {
            "行号": "",           # 新增：帮助对齐行序
            "摘要": "",
            "总账科目": "",
            "明细科目": "",
            "借方金额": "",       # 强制要求纯数字
            "贷方金额": ""        # 强制要求纯数字
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

PROMPT = f"""你是一个严格的会计凭证信息提取专家。
图片是一张标准的《记账凭证》，请严格按照以下JSON格式提取，不要添加任何解释、代码块或多余文字。
输出必须是合法、可直接解析的JSON。

JSON格式：
{json.dumps(JSON_SCHEMA, ensure_ascii=False, indent=2)}

重要规则：
- "分录" 必须严格按照图片中从上到下的表格行顺序提取
- 每行分录都要提取，即使摘要为空
- 金额必须是纯数字字符串（如 "30000000"），不要带 ¥、逗号或其他单位
- "行号" 请按 1,2,3... 顺序填写，帮助对齐
- 签字人姓名要准确提取
- 如果某字段完全没有，请用空字符串 "" """

# ================== 加载模型 ==================
print("正在从本地加载 GLM-OCR 模型...")

processor = AutoProcessor.from_pretrained(MODEL_PATH, local_files_only=True)

model = AutoModelForImageTextToText.from_pretrained(
    MODEL_PATH,
    dtype=torch.bfloat16,
    device_map="auto",
    use_safetensors=True,
    local_files_only=True
)

print("模型加载完成！")

# ================== 批量处理 ==================
results = []
image_files = [f for f in os.listdir(IMAGE_FOLDER)
               if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'))]

print(f"检测到 {len(image_files)} 张图片，开始处理...")

for img_name in tqdm(image_files, desc="处理图片"):
    img_path = os.path.join(IMAGE_FOLDER, img_name)
    try:
        messages = [{
            "role": "user",
            "content": [
                {"type": "image", "url": img_path},
                {"type": "text", "text": PROMPT}
            ]
        }]

        inputs = processor.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True,
            return_dict=True, return_tensors="pt"
        ).to(model.device)

        generated_ids = model.generate(
            **inputs, max_new_tokens=8192, do_sample=False, temperature=0.0
        )

        output_text = processor.decode(
            generated_ids[0][inputs["input_ids"].shape[1]:], skip_special_tokens=False
        )

        json_match = re.search(r'\{[\s\S]*\}', output_text)
        json_str = json_match.group(0) if json_match else output_text.strip()

        data = json.loads(json_str)
        data["文件名"] = img_name
        results.append(data)

    except Exception as e:
        print(f"\n❌ 处理 {img_name} 失败: {e}")
        results.append({"文件名": img_name, "错误": str(e)})

# ================== 保存 Excel ==================
if results:
    df = pd.json_normalize(results)
    df.to_excel(OUTPUT_EXCEL, index=False, engine="openpyxl")
    print(f"\n✅ 处理完成！共处理 {len(results)} 张图片")
    print(f"结果已保存到：{OUTPUT_EXCEL}")
    print("请检查分录是否按顺序对齐、金额是否为纯数字。")
else:
    print("未找到图片，请检查 invoices 文件夹。")