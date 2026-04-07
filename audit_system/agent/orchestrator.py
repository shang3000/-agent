"""
审计总流程控制器（Orchestrator）
负责协调 OCR 输出 → 数据处理 → 风险分析 → 报告生成
"""

from core.data_loader import DataLoader
from core.sampler import Sampler
from core.risk_engine import RiskEngine
from core.stats import Stats
from core.report import Report
from .llm_adapter import LLMAdapter


class Orchestrator:
    """审计流程总控制器"""

    def __init__(self):
        """初始化各个核心模块"""
        self.data_loader = DataLoader()
        self.sampler = Sampler()
        self.risk_engine = RiskEngine()
        self.stats = Stats()
        self.report = Report()
        self.llm = LLMAdapter()

        print("✅ Orchestrator 初始化完成，所有模块已加载")

    def run_audit(self, ocr_output_path: str = None):
        """
        执行完整审计流程

        Args:
            ocr_output_path: OCR输出的Excel文件路径，默认为 data/raw/ocr_output.xlsx
        """
        if ocr_output_path is None:
            ocr_output_path = "data/raw/ocr_output.xlsx"

        print(f"🚀 开始审计流程，输入文件: {ocr_output_path}")

        # 1. 读取 OCR 输出数据
        data = self.data_loader.load_excel(ocr_output_path)
        if data.empty:
            print("❌ 错误：读取 OCR 数据失败或数据为空，请检查文件路径")
            return None

        print(f"✅ 成功加载 {len(data)} 条凭证记录")

        # 2. 数据抽样（可调整比例，0.3~1.0）
        sampled_data = self.sampler.sample(data, sample_rate=0.5)

        # 3. 风险检测（建议对全量数据检测）
        risk_results = self.risk_engine.detect_risk(data)

        # 4. 数据统计
        stats_results = self.stats.calculate_stats(data)

        # 5. LLM 深度分析
        llm_analysis = self._analyze_with_llm(data, risk_results, stats_results)

        # 6. 生成最终报告
        report_path = self.report.generate_report(
            data=data,
            risk_results=risk_results,
            stats_results=stats_results,
            llm_analysis=llm_analysis
        )

        print(f"🎉 审计流程执行完成！报告路径：{report_path}")
        return report_path

    def _analyze_with_llm(self, data, risk_results, stats_results):
        """使用 GLM-4 进行深度智能分析"""
        prompt = f"""你是一位经验丰富的财务审计专家，请基于以下信息给出专业、客观的审计分析报告：

【数据概览】
{stats_results}

【风险检测结果】
{risk_results}

请按以下结构输出：
1. 主要审计发现（列出3-5条关键点）
2. 风险评估（整体风险等级及理由）
3. 具体审计建议（可操作性强）
4. 总体结论

语言要专业、简洁、具有建设性。"""

        try:
            response = self.llm.generate(prompt, model="glm-4")
            return response
        except Exception as e:
            print(f"⚠️ LLM 分析调用失败: {e}")
            return "LLM 深度分析暂不可用（请检查 API Key 或网络）。"
