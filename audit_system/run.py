import sys
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('output/logs/audit_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """主入口函数"""
    try:
        logger.info("开始审计系统流程")
        
        # 1. 导入必要模块
        from ocr.ocr_runner import OCRRunner
        from agent.orchestrator import Orchestrator
        
        # 2. 初始化OCR Runner
        ocr_runner = OCRRunner()
        
        # 3. 执行OCR处理
        ocr_output_path = ocr_runner.process_images(image_dir="./ocr/invoices")
        logger.info(f"OCR处理完成，输出路径: {ocr_output_path}")
        
        # 4. 初始化Orchestrator
        orchestrator = Orchestrator()
        
        # 5. 执行审计流程
        orchestrator.run_audit(ocr_output_path)
        
        logger.info("审计系统流程完成")
        
    except Exception as e:
        logger.error(f"系统执行失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
