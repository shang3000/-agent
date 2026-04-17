"""
抽凭辅助系统主入口 - 一键运行完整流程
OCR处理 → 数据加载 → 风险检测 → LLM分析 → 生成报告
"""

import sys
import logging
from pathlib import Path

# ================== 配置日志 ==================
log_dir = Path("output/logs")
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "sampling_assistant.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    """主入口函数"""
    logger.info("=" * 70)
    logger.info("          财务抽凭智能系统 - 开始运行")
    logger.info("=" * 70)

    try:
        # 1. 导入模块
        from ocr.ocr_runner import OCRRunner
        from agent.orchestrator import Orchestrator

        # 2. 执行 OCR 处理
        logger.info("步骤1: 开始执行 OCR 识别...")
        ocr_runner = OCRRunner()

        # 使用绝对路径，更稳定
        image_dir = Path("ocr/invoices").resolve()
        ocr_output_path = ocr_runner.process_images(str(image_dir))

        logger.info(f"✅ OCR 处理完成，输出文件: {ocr_output_path}")

        # 3. 执行抽凭分析流程
        logger.info("步骤2: 开始执行抽凭分析流程...")
        orchestrator = Orchestrator()

        report_path = orchestrator.run_sampling(ocr_output_path)

        if report_path:
            logger.info("=" * 70)
            logger.info("🎉 完整抽凭流程执行成功！")
            logger.info(f"📄 抽凭报告路径: {report_path}")
            logger.info("=" * 70)
        else:
            logger.warning("抽凭流程执行完成，但报告生成可能有问题")

    except FileNotFoundError as e:
        logger.error(f"❌ 文件或路径不存在: {e}")
        logger.error("请确认以下路径是否存在：")
        logger.error("   - ocr/invoices/ 目录下是否有图片")
        logger.error("   - data/raw/ 目录是否有写入权限")
        sys.exit(1)

    except ImportError as e:
        logger.error(f"❌ 模块导入失败: {e}")
        logger.error("请检查项目结构和 __init__.py 文件是否正确")
        sys.exit(1)

    except Exception as e:
        logger.error(f"❌ 系统执行失败: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()