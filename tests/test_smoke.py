"""``funmd`` 包的轻量冒烟测试。

funmd 是一个依赖很轻的小工具，用于在 Markdown 表格与 pandas DataFrame
之间互相转换。包内不涉及任何网络/数据库/云存储访问，因此这些测试直接
执行真实代码路径，无需 mock 任何东西。
"""

import pandas as pd
import pytest


def test_import_top_level_package():
    """顶层包必须能正常导入。"""
    import funmd

    assert hasattr(funmd, "to_pandas")
    assert hasattr(funmd, "from_pandas")
    assert set(funmd.__all__) == {"to_pandas", "from_pandas"}


def test_import_submodule():
    """内部的 ``_pandas`` 子模块同样必须能正常导入。"""
    from funmd import _pandas

    assert hasattr(_pandas, "to_pandas")
    assert hasattr(_pandas, "from_pandas")
    assert hasattr(_pandas, "_is_header")
    assert hasattr(_pandas, "_extract_line")


MARKDOWN_TABLE = """
| foo | bar |
| --- | --- |
| 1   | 2   |
| 3   | 4   |
"""

MARKDOWN_TABLE_PLUS_SEPARATOR = """
+-----+-----+
| foo | bar |
+-----+-----+
| 1   | 2   |
| 3   | 4   |
+-----+-----+
"""


def test_to_pandas_basic_table():
    """标准的竖线分隔 Markdown 表格应能正确转换为 DataFrame。"""
    import funmd

    df = funmd.to_pandas(MARKDOWN_TABLE)

    assert list(df.columns) == ["foo", "bar"]
    assert df.shape == (2, 2)
    assert df.iloc[0].tolist() == ["1", "2"]
    assert df.iloc[1].tolist() == ["3", "4"]


def test_to_pandas_with_explicit_header():
    """显式指定的 header 应覆盖表格中检测到的表头行。"""
    import funmd

    body_only = """
| 1 | 2 |
| 3 | 4 |
"""
    df = funmd.to_pandas(body_only, header=["a", "b"])

    assert list(df.columns) == ["a", "b"]
    assert df.shape == (2, 2)


def test_from_pandas_roundtrip():
    """DataFrame -> Markdown -> DataFrame 转换应保持数据不变。"""
    import funmd

    df = pd.DataFrame({"foo": ["1", "3"], "bar": ["2", "4"]})

    markdown = funmd.from_pandas(df, index=False)
    assert isinstance(markdown, str)
    assert "foo" in markdown
    assert "bar" in markdown

    # 转换出的 Markdown 也应能被 to_pandas 重新解析。
    df_roundtrip = funmd.to_pandas(markdown)
    assert list(df_roundtrip.columns) == ["foo", "bar"]
    assert df_roundtrip.shape == (2, 2)


def test_is_header_helper():
    """``_is_header`` 应能识别 Markdown 表格的分隔行。"""
    from funmd._pandas import _is_header

    assert _is_header(["---", "---"]) is True
    assert _is_header([":---", "---:", ":---:"]) is True
    assert _is_header([":---", "foo", "bar"]) is False
    assert _is_header(["foo", "bar"]) is False


def test_extract_line_helper():
    """``_extract_line`` 应能解析单个竖线分隔的表格行。"""
    from funmd._pandas import _extract_line

    assert _extract_line("| foo | bar |", False) == (["foo", "bar"], False)
    assert _extract_line("| foo | bar |", True) == (["foo", "bar"], False)
    assert _extract_line("| --- | --- |", False) == (["---", "---"], False)
    assert _extract_line("| --- | --- |", True) == ([], True)


def test_to_pandas_empty_table_returns_empty_dataframe():
    """空白输入不应抛出异常，而是返回一个空的 DataFrame。"""
    import funmd

    df = funmd.to_pandas("")
    assert isinstance(df, pd.DataFrame)
    assert df.empty


def test_no_cli_entry_points_declared():
    """funmd 目前未提供任何 ``[project.scripts]`` CLI 入口点。

    这是一条文档性质的测试：如果未来新增了 CLI，应替换为真正调用它的测试
    （例如通过 ``--help``），而不是继续静默跳过。
    """
    pytest.skip(
        "funmd 未在 pyproject.toml 的 [project.scripts] 中声明任何 CLI 入口点，"
        "无需测试命令行调用"
    )
