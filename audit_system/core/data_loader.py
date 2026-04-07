import pandas as pd

class DataLoader:
    """Excel读取/标准化"""
    
    def load_excel(self, file_path):
        """加载Excel文件
        
        Args:
            file_path: Excel文件路径
            
        Returns:
            pd.DataFrame: 加载的数据
        """
        try:
            df = pd.read_excel(file_path)
            # 标准化数据
            df = self._standardize_data(df)
            return df
        except Exception as e:
            print(f"加载Excel文件失败: {str(e)}")
            return pd.DataFrame()
    
    def _standardize_data(self, df):
        """标准化数据
        
        Args:
            df: 原始数据
            
        Returns:
            pd.DataFrame: 标准化后的数据
        """
        # 处理缺失值
        df = df.fillna('')
        
        # 标准化列名
        df.columns = [col.strip() for col in df.columns]
        
        # 标准化金额列
        if '金额' in df.columns:
            df['金额'] = pd.to_numeric(df['金额'], errors='coerce')
        
        # 标准化日期列
        for col in ['开票日期', '日期']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        return df
