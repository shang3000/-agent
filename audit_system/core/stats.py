import pandas as pd

class Stats:
    """数据统计"""
    
    def calculate_stats(self, data):
        """计算统计信息
        
        Args:
            data: 数据
            
        Returns:
            str: 统计结果
        """
        if data.empty:
            return "无数据"
        
        stats_result = []
        
        # 基本统计
        stats_result.append(f"总记录数: {len(data)}")
        
        # 按类型统计
        if '类型' in data.columns:
            type_counts = data['类型'].value_counts()
            stats_result.append("\n类型分布:")
            for type_name, count in type_counts.items():
                stats_result.append(f"- {type_name}: {count}")
        
        # 金额统计
        if '金额' in data.columns:
            amount_stats = data['金额'].describe()
            stats_result.append("\n金额统计:")
            stats_result.append(f"- 平均值: {amount_stats['mean']:.2f}")
            stats_result.append(f"- 最大值: {amount_stats['max']:.2f}")
            stats_result.append(f"- 最小值: {amount_stats['min']:.2f}")
            stats_result.append(f"- 标准差: {amount_stats['std']:.2f}")
        
        return "\n".join(stats_result)
