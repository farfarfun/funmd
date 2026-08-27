"""Lightweight smoke tests for the ``funmd`` package.

funmd is a tiny, dependency-light utility that converts between Markdown
tables and pandas DataFrames. There is no network/DB/cloud access anywhere
in the package, so these tests exercise the real code paths directly
rather than mocking anything.
"""

import pandas as pd
import pytest


def test_import_top_level_package():
    """The top-level package must import cleanly."""
    import funmd

    assert hasattr(funmd, "to_pandas")
    assert hasattr(funmd, "from_pandas")
    assert set(funmd.__all__) == {"to_pandas", "from_pandas"}


def test_import_submodule():
    """The internal ``_pandas`` submodule must import cleanly too."""
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
    """A standard pipe-delimited Markdown table converts to a DataFrame."""
    import funmd

    df = funmd.to_pandas(MARKDOWN_TABLE)

    assert list(df.columns) == ["foo", "bar"]
    assert df.shape == (2, 2)
    assert df.iloc[0].tolist() == ["1", "2"]
    assert df.iloc[1].tolist() == ["3", "4"]


def test_to_pandas_with_explicit_header():
    """An explicit header overrides any header row detected in the table."""
    import funmd

    body_only = """
| 1 | 2 |
| 3 | 4 |
"""
    df = funmd.to_pandas(body_only, header=["a", "b"])

    assert list(df.columns) == ["a", "b"]
    assert df.shape == (2, 2)


def test_from_pandas_roundtrip():
    """DataFrame -> Markdown -> DataFrame should preserve the data."""
    import funmd

    df = pd.DataFrame({"foo": ["1", "3"], "bar": ["2", "4"]})

    markdown = funmd.from_pandas(df, index=False)
    assert isinstance(markdown, str)
    assert "foo" in markdown
    assert "bar" in markdown

    # And it should be re-parseable by to_pandas.
    df_roundtrip = funmd.to_pandas(markdown)
    assert list(df_roundtrip.columns) == ["foo", "bar"]
    assert df_roundtrip.shape == (2, 2)


def test_is_header_helper():
    """``_is_header`` recognizes Markdown table separator rows."""
    from funmd._pandas import _is_header

    assert _is_header(["---", "---"]) is True
    assert _is_header([":---", "---:", ":---:"]) is True
    assert _is_header([":---", "foo", "bar"]) is False
    assert _is_header(["foo", "bar"]) is False


def test_extract_line_helper():
    """``_extract_line`` parses a single pipe-delimited row."""
    from funmd._pandas import _extract_line

    assert _extract_line("| foo | bar |", False) == (["foo", "bar"], False)
    assert _extract_line("| foo | bar |", True) == (["foo", "bar"], False)
    assert _extract_line("| --- | --- |", False) == (["---", "---"], False)
    assert _extract_line("| --- | --- |", True) == ([], True)


def test_to_pandas_empty_table_returns_empty_dataframe():
    """An empty/blank input should not raise, just yield an empty frame."""
    import funmd

    df = funmd.to_pandas("")
    assert isinstance(df, pd.DataFrame)
    assert df.empty


def test_no_cli_entry_points_declared():
    """funmd currently ships no ``[project.scripts]`` CLI entry points.

    This is a documentation test: if a CLI is ever added, this test should
    be replaced with one that invokes it (e.g. via ``--help``) rather than
    silently passing.
    """
    pytest.skip(
        "funmd 未在 pyproject.toml 的 [project.scripts] 中声明任何 CLI 入口点，"
        "无需测试命令行调用"
    )
