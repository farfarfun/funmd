# Changelog

本文件记录 `funmd` 的版本变更，按版本倒序排列。

## [未发布]

### 修复

- README 补充一句话简介、安装命令、最小可运行示例，并追加组织统一的「关于 farfarfun」区块
- `pyproject.toml` 补充真实的 `description`、`license = "MIT"`，以及 `pandas`/`tabulate` 依赖的版本下限
- `uv.lock` 重新生成，清理与当前 `pyproject.toml` 不一致的残留依赖（`funutil`）
- `src/funmd/_pandas.py` 公开函数 `to_pandas`/`from_pandas` 补齐中文 docstring 与完整类型标注
- `.gitignore` 补充 `*.db`、`*.rar`、`.run/`、`logs/`、`.idea/` 规则

## [0.1.3] - 2026-09-01

### 新增

- `tests/` 目录，补充冒烟测试覆盖 `to_pandas`/`from_pandas` 及内部辅助函数
- `src/funmd/py.typed` 标记（PEP 561）

### 修复

- 升级 `pytest` 版本，修复 Dependabot 提示的 tmpdir 处理相关告警

### 变更

- `requires-python` 下限提升，移除已停止安全更新的旧版本支持
- 移除未使用的 `funutil` 依赖声明

## [0.1.2] - 2024-12-02

### 新增

- 首次发布，提供 Markdown 表格与 `pandas.DataFrame` 互转能力（`to_pandas` / `from_pandas`），兼容 `|` 与 `+` 两种表格分隔风格
