# funmd

`funmd` 是一个 Markdown 表格与 `pandas.DataFrame` 互转的轻量工具，提供 `to_pandas` / `from_pandas` 两个函数，兼容 `|` 和 `+` 两种 Markdown 表格分隔风格。

## 安装

```bash
uv add funmd
# 或
pip install funmd
```

## 快速开始

```python
from funmd import to_pandas, from_pandas

table = """
| foo | bar |
| --- | --- |
| 1   | 2   |
| 3   | 4   |
"""

df = to_pandas(table)
print(df)
#    foo bar
# 0    1   2
# 1    3   4

markdown = from_pandas(df, index=False)
print(markdown)
# | foo   | bar   |
# |:------|:------|
# | 1     | 2     |
# | 3     | 4     |
```

`to_pandas` 也支持 `+-----+-----+` 风格的分隔线，以及通过 `header` 参数显式指定列名（覆盖表格中检测到的表头行）。

---

## 关于 farfarfun

[farfarfun](https://github.com/farfarfun) 是一个专注于实用工具库的开源组织，
涵盖云存储、数据处理、AI、多媒体与开发工具链等方向。

- 🏠 组织主页：<https://github.com/farfarfun>
- 📦 PyPI：<https://pypi.org/user/niuliangtao/>
- 📧 联系：farfarfun@qq.com

本项目基于 [MIT](LICENSE) 协议开源。
