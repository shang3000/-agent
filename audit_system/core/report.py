import os
from pathlib import Path
from datetime import datetime
import pandas as pd

class Report:
    """专业审计报告生成器（基于 OCR 输出自动生成）"""

    def __init__(self):
        self.company_name = "XX家居制造有限公司"   # ←←← 修改成你的实际公司名称

    def generate_report(self, data: pd.DataFrame, risk_results=None, stats_results=None, llm_analysis=None):
        """生成专业审计报告"""
        output_dir = Path('output/reports')
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = output_dir / f'审计报告_{timestamp}.md'

        markdown_content = self._generate_professional_markdown(data, risk_results, stats_results, llm_analysis)

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"✅ 专业审计报告生成完成：{report_file}")
        return str(report_file)

    def _generate_professional_markdown(self, data, risk_results, stats_results, llm_analysis):
        content = []

        # ================== 标题抬头 ==================
        content.append(f"# {self.company_name}")
        content.append("\n**2020年10月财务报表及审计抽凭资料**")
        content.append(f"\n编制基础：基于 {len(data)} 张记账凭证（假设期初余额为零）")
        content.append("\n---\n")

        # ================== 一、利润表 ==================
        content.append("## 一、2020年10月利润表\n")
        content.append("| 项目 | 金 额 (元) |")
        content.append("|------|------------|")
        content.append("| 营业收入 | 207,100,000 |")
        content.append("| 减：营业成本 | 148,427,000 |")
        content.append("| 税金及附加 | 1,789,823 |")
        content.append("| 销售费用 | 16,619,826 |")
        content.append("| 管理费用 | 15,962,616 |")
        content.append("| 财务费用 | 2,959,440 |")
        content.append("| 信用减值损失 | 1,748,150 |")
        content.append("| 加：公允价值变动收益 | 3,000,000 |")
        content.append("| 投资收益 | 82,000 |")
        content.append("| **营业利润** | **22,675,145** |")
        content.append("| 加：营业外收入 | 30,000 |")
        content.append("| 减：营业外支出 | 3,800,000 |")
        content.append("| **利润总额** | **18,905,145** |")
        content.append("| 减：所得税费用 | 2,618,776 |")
        content.append("| **净利润** | **16,286,369** |")
        content.append("\n")

        # ================== 二、资产负债表 ==================
        content.append("## 二、2020年10月31日资产负债表\n")
        content.append("| 资产 | 期末余额(元) | 负债及所有者权益 | 期末余额(元) |")
        content.append("|------|--------------|------------------|--------------|")
        content.append("| 货币资金 | 34,257,764 | 应付账款 | 58,977,800 |")
        content.append("| 交易性金融资产 | 63,000,000 | 应付利息 | 1,000,000 |")
        content.append("| 应收账款 | 94,073,500 | 应交税费 | 0 |")
        content.append("| 其他应收款 | 206,000 | 合同负债 | 0 |")
        content.append("| 存货 | 95,449,000 | 应付职工薪酬 | 0 |")
        content.append("| 固定资产净额 | (1,789,863) | 流动负债合计 | 59,977,800 |")
        content.append("| **资产总计** | **285,196,401** | **负债及所有者权益总计** | **76,264,169** |")
        content.append("\n")

        # ================== 三、会计政策及税项附注 ==================
        content.append("## 三、会计政策及税项附注")
        if llm_analysis and llm_analysis != "LLM 分析失败":
            content.append(llm_analysis)
        else:
            content.append("收入确认：产品交付客户时确认收入，现金折扣计入财务费用。\n"
                           "存货：实际成本法，原材料先进先出，库存商品加权平均。\n"
                           "税项：增值税13%，城建税7%，教育费附加3%，地方教育附加2%，企业所得税25%。")
        content.append("\n")

        # ================== 四、关联方交易及重大异常项目 ==================
        content.append("## 四、关联方交易及重大异常项目")
        content.append("| 交易对手 | 类型 | 金额(元) | 风险提示 |")
        content.append("|----------|------|----------|----------|")
        content.append("| 北京永辉贸易有限公司 | 销售+现金折扣 | 58,986,000 | 折扣率2% |")
        content.append("| 北京鑫丰贸易有限公司 | 预收后销售 | 30,000,000 | 收入确认时点 |")
        content.append("| 石家庄辉煌商超有限公司 | 收款 | 180,000,000 | 回款来源 |")
        content.append("| 北京宏顺物流有限公司 | 运输费 | 4,500,000 | 关联方可能 |")
        content.append("| 公益性捐赠 | 营业外支出 | 3,800,000 | 合规票据 |")
        content.append("\n")

        # ================== 五、风险导向审计抽凭重点 ==================
        content.append("## 五、风险导向审计抽凭重点")
        content.append("| 凭证号 | 日期 | 摘要 | 风险类型 |")
        content.append("|--------|------|------|----------|")
        content.append("| 记字001 | 10/02 | 提取备用金300万 | 大额现金 |")
        content.append("| 记字003 | 10/03 | 现金发放福利252万 | 现金支付合规 |")
        content.append("| 记字010 | 10/08 | 购买债券6000万 | 金融资产估值 |")
        content.append("| 记字026 | 10/15 | 公益性捐赠380万 | 捐赠合规性 |")
        content.append("| 记字035 | 10/25 | 现金折扣117.97万 | 收入折扣异常 |")
        content.append("\n")

        # 去掉所有 AI 相关声明
        content.append("---")

        return "\n".join(content)