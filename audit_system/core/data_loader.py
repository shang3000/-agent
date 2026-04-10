import pandas as pd
import ast
import json
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Excel读取与标准化（适配记账凭证 OCR 输出）"""

    def load_excel(self, file_path):
        """加载Excel文件并进行标准化处理"""
        try:
            df = pd.read_excel(file_path)
            logger.info(f"成功读取 Excel 文件: {file_path}，共 {len(df)} 行")

            df = self._standardize_data(df)
            return df

        except Exception as e:
            logger.error(f"加载Excel文件失败: {str(e)}")
            print(f"❌ 加载Excel文件失败: {str(e)}")
            return pd.DataFrame()

    def _standardize_data(self, df):
        """针对记账凭证 OCR 输出进行标准化"""
        if df.empty:
            return df

        # 1. 处理缺失值
        df = df.fillna('')

        # 2. 清理列名（去除空格）
        df.columns = [col.strip() for col in df.columns]

        # 3. 关键处理：分录列（列表嵌套字典）
        if '分录' in df.columns:
            df = self._parse_entry_column(df)

        # 4. 标准化金额列（如果存在）
        for col in ['借方合计', '贷方合计', '借方金额', '贷方金额']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # 5. 标准化日期列
        for col in ['凭证日期', '开票日期', '日期']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        logger.info("数据标准化完成")
        return df

    def _parse_entry_column(self, df):
        """解析 '分录' 列（将字符串形式的列表转为可用的结构）"""

        def safe_parse(entry):
            if pd.isna(entry) or entry == '':
                return []
            try:
                # 如果已经是列表，直接返回
                if isinstance(entry, list):
                    return entry
                # 如果是字符串，尝试解析
                if isinstance(entry, str):
                    # 尝试用 ast.literal_eval（更安全）
                    return ast.literal_eval(entry)
            except:
                pass
            return []

        df['分录'] = df['分录'].apply(safe_parse)

        # 展开分录为多行（可选，后续可根据需要使用）
        # 如果你想把每条分录展开成一行，可以在这里处理，但目前先保持原结构

        return df