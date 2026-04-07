import os
from pathlib import Path
from datetime import datetime

class Report:
    """报告生成（Markdown/PDF）"""
    
    def generate_report(self, data, risk_results, stats_results, llm_analysis):
        """生成报告
        
        Args:
            data: 数据
            risk_results: 风险检测结果
            stats_results: 统计结果
            llm_analysis: LLM分析结果
            
        Returns:
            str: 报告路径
        """
        # 创建输出目录
        output_dir = Path('output/reports')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成报告文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = output_dir / f'audit_report_{timestamp}.md'
        
        # 生成Markdown报告
        markdown_content = self._generate_markdown(data, risk_results, stats_results, llm_analysis)
        
        # 写入文件
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # 可选：生成PDF报告
        # self._generate_pdf(report_file)
        
        return str(report_file)
    
    def _generate_markdown(self, data, risk_results, stats_results, llm_analysis):
        """生成Markdown报告内容
        
        Args:
            data: 数据
            risk_results: 风险检测结果
            stats_results: 统计结果
            llm_analysis: LLM分析结果
            
        Returns:
            str: Markdown内容
        """
        content = []
        
        # 报告标题
        content.append(f"# 审计报告")
        content.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")
        
        # 数据概览
        content.append("## 数据概览")
        content.append(stats_results)
        content.append("")
        
        # 风险检测结果
        content.append("## 风险检测结果")
        content.append(f"### 风险等级: {risk_results.get('风险等级', '未评估')}")
        
        if risk_results.get('异常交易', []):
            content.append("### 异常交易")
            for item in risk_results['异常交易']:
                content.append(f"- {item}")
        
        if risk_results.get('金额异常', []):
            content.append("### 金额异常")
            for item in risk_results['金额异常']:
                content.append(f"- 图片: {item.get('图片名称', '')}, 金额: {item.get('金额', 0)}, 原因: {item.get('异常原因', '')}")
        
        if risk_results.get('时间异常', []):
            content.append("### 时间异常")
            for item in risk_results['时间异常']:
                content.append(f"- {item}")
        
        content.append("")
        
        # LLM分析
        content.append("## 深度分析")
        content.append(llm_analysis)
        content.append("")
        
        # 审计建议
        content.append("## 审计建议")
        content.append("1. 对金额异常的交易进行进一步核实")
        content.append("2. 检查内部控制流程的有效性")
        content.append("3. 加强财务数据的真实性审核")
        content.append("4. 建立风险预警机制")
        
        return "\n".join(content)
    
    def _generate_pdf(self, markdown_file):
        """生成PDF报告
        
        Args:
            markdown_file: Markdown文件路径
        """
        try:
            import pdfkit
            pdf_file = markdown_file.with_suffix('.pdf')
            pdfkit.from_file(str(markdown_file), str(pdf_file))
        except Exception as e:
            print(f"生成PDF报告失败: {str(e)}")
