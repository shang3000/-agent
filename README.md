# 抽凭辅助系统

一个基于OCR和大语言模型的智能抽凭辅助系统，能够自动处理财务凭证、检测风险并生成抽凭报告。

## 项目结构

```
sampling_assistant_system/
├── src/                  # 代码目录
│   ├── agent/           # Agent层（大模型调度）
│   ├── config/          # 配置目录
│   ├── core/            # 业务逻辑层
│   └── ocr/             # OCR模块
├── data/                # 数据目录
│   ├── raw/             # OCR输出
│   └── processed/       # 清洗后数据
├── output/              # 输出目录
│   ├── logs/            # 日志
│   └── reports/         # 报告
├── README.md            # 说明文档
├── .gitignore           # Git忽略规则
├── LICENSE              # 开源协议
├── requirements.txt     # 依赖文件
└── run.py               # 主入口
```

## 功能特点

- **OCR识别**：使用GLM-OCR模型自动识别财务凭证
- **智能分析**：集成GLM大语言模型进行深度抽凭分析
- **风险检测**：自动检测异常交易和风险点
- **报告生成**：生成结构化的Markdown抽凭报告
- **批量处理**：支持批量处理多张凭证图片

## 快速开始

### 环境要求

- Python 3.10+
- CUDA 11.7+（推荐，用于GPU加速）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

1. **GLM-OCR模型**：从 [https://hf-mirror.com/zai-org/GLM-OCR/tree/main](https://hf-mirror.com/zai-org/GLM-OCR/tree/main) 下载模型到 `D:/AImodels/GLM-OCR` 目录
2. **GLM API密钥**：在 `src/agent/llm_adapter.py` 中设置API密钥

### 运行

1. 将凭证图片放入 `src/ocr/invoices/` 目录
2. 运行主入口：

```bash
python run.py
```

3. 查看生成的报告：`output/reports/` 目录

## 核心模块

### 1. OCR模块
- **ocr_runner.py**：OCR统一调用入口，处理图片并输出Excel
- **utils.py**：图片处理和OCR结果清洗

### 2. Agent层
- **orchestrator.py**：总流程控制，调度整个抽凭过程
- **llm_adapter.py**：GLM API封装，用于深度分析

### 3. 业务逻辑层
- **data_loader.py**：Excel读取和数据标准化
- **sampler.py**：数据抽凭逻辑
- **risk_engine.py**：风险检测引擎
- **stats.py**：数据统计分析
- **report.py**：报告生成

## 技术栈

- **OCR**：GLM-OCR
- **大语言模型**：GLM-4
- **数据处理**：Pandas, NumPy
- **配置管理**：YAML
- **报告生成**：Markdown

## 注意事项

- 确保GLM-OCR模型已正确下载
- 配置文件中的路径设置正确
- 首次运行可能需要较长时间加载模型

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License
