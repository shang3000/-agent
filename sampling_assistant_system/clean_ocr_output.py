import pandas as pd
import ast
import re
from pathlib import Path


def clean_ocr_data(input_path="data/raw/ocr_output.xlsx", output_path="data/raw/ocr_output_clean.xlsx"):
    print("🚀 开始清洗 OCR 导出结果...")
    df = pd.read_excel(input_path)

    # 1. 清洗金额列（去除 ¥ 并转为数字）
    for col in ['借方合计', '贷方合计']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace('¥', '', regex=True).str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # 2. 清洗 '分录' 列（解析 JSON + 去掉空行）
    def clean_entry_list(entry_str):
        if pd.isna(entry_str) or str(entry_str).strip() == '':
            return []
        try:
            entries = ast.literal_eval(str(entry_str))
            if not isinstance(entries, list):
                entries = [entries]
            # 过滤掉完全空的行
            cleaned = []
            for e in entries:
                if isinstance(e, dict):
                    # 如果所有值都为空，则跳过
                    if any(str(v).strip() not in ['', '0', '0.0'] for v in e.values()):
                        cleaned.append(e)
            return cleaned
        except:
            return []

    if '分录' in df.columns:
        df['分录'] = df['分录'].apply(clean_entry_list)

    # 3. 清洗日期格式
    for col in ['凭证日期']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')

    # 保存清洗后的文件
    df.to_excel(output_path, index=False)
    print(f"✅ 清洗完成！共处理 {len(df)} 条记录")
    print(f"📁 清洗后文件已保存至：{output_path}")
    return df


if __name__ == "__main__":
    clean_ocr_data()