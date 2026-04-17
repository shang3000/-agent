import pandas as pd
import random

class Sampler:
    """抽凭逻辑"""
    
    def sample(self, data, sample_rate=0.3):
        """数据抽样
        
        Args:
            data: 原始数据
            sample_rate: 抽样比例
            
        Returns:
            pd.DataFrame: 抽样后的数据
        """
        if data.empty:
            return data
        
        # 计算抽样数量
        sample_size = max(1, int(len(data) * sample_rate))
        
        # 分层抽样（按类型）
        if '类型' in data.columns:
            sampled_data = []
            for type_name, group in data.groupby('类型'):
                group_sample_size = max(1, int(len(group) * sample_rate))
                if len(group) > group_sample_size:
                    group_sample = group.sample(group_sample_size)
                else:
                    group_sample = group
                sampled_data.append(group_sample)
            
            return pd.concat(sampled_data)
        else:
            # 简单随机抽样
            if len(data) > sample_size:
                return data.sample(sample_size)
            else:
                return data
