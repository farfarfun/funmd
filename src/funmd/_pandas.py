import re

import pandas as pd
from pandas import DataFrame


def _is_header(extracted: list[str], *args, **kwargs) -> bool:
    """判断一组单元格是否为 Markdown 表格的分隔行（如 ``---``、``:---:``）。

    Args:
        extracted: 一行中已切分出的单元格内容列表。

    Returns:
        bool: 全部单元格都符合分隔行格式时返回 True，否则 False。

    >>> _is_header(["---", "---"])
    True
    >>> _is_header([":---", "---:", ":---:"])
    True
    >>> _is_header([":---", "foo", "bar"])
    False
    >>> _is_header(["foo", "bar"])
    False
    """
    partial_pattern = r":*-+:*"
    return all(re.match(partial_pattern, ex) for ex in extracted)


def _extract_line(
    line: str, possible_separator: bool, *args, **kwargs
) -> tuple[list[str], bool]:
    """解析 Markdown 表格中的一行，切分出单元格内容。

    同时兼容 ``| foo | bar |`` 和 ``+-----+-----+`` 两种表格分隔风格。

    Args:
        line: 待解析的一行文本。
        possible_separator: 该行是否可能是表头分隔行（用于判断是否需要
            检查 ``+---+`` 风格的分隔符，并识别分隔行）。

    Returns:
        tuple[list[str], bool]: 第一项是解析出的单元格内容列表；
        第二项标记该行是否为表头分隔行（是则第一项为空列表）。

    >>> _extract_line("| foo | bar |", False)
    (['foo', 'bar'], False)
    >>> _extract_line("| foo | bar |", True)
    (['foo', 'bar'], False)
    >>> _extract_line("| --- | --- |", False)
    (['---', '---'], False)
    >>> _extract_line("| --- | --- |", True)
    ([], True)
    """
    # 需要支持重叠模式的匹配
    vertical_pattern = r"(?=(\|(.*?)\|))"
    plus_pattern = r"(?=(\+(.*?)\+))"
    extracted = [value.strip() for _, value in re.findall(vertical_pattern, line)]
    if possible_separator and not extracted:
        # 检查 +-----+----+ 这种分隔符风格
        extracted = [value.strip() for _, value in re.findall(plus_pattern, line)]

    if not extracted:
        return [], False

    if possible_separator and _is_header(extracted):
        return [], True

    return extracted, False


def to_pandas(
    table: str, header: list[str] | None = None, *args, **kwargs
) -> DataFrame:
    """将 Markdown 表格字符串转换为 pandas DataFrame。

    Args:
        table: 一个 Markdown 表格字符串，支持 ``|`` 和 ``+`` 两种分隔风格。
        header: 显式指定的列名列表；为 None 时会尝试从表格中检测表头行。
        *args: 透传的位置参数（当前未使用，保留以兼容未来扩展）。
        **kwargs: 透传的关键字参数（当前未使用，保留以兼容未来扩展）。

    Returns:
        DataFrame: 解析后的数据表。
    """
    rows = []
    for line in table.split("\n"):
        extracted, is_header = _extract_line(line.strip(), len(rows) == 1)
        if is_header:
            if header is None:
                header = rows[0]
            rows.pop(0)
            continue
        if not extracted:
            continue
        rows.append(extracted)
    return pd.DataFrame(rows, columns=header)


def from_pandas(df: DataFrame, index: bool = True, *args, **kwargs) -> str:
    """将 pandas DataFrame 转换为 Markdown 表格字符串。

    Args:
        df: 待转换的 DataFrame。
        index: 是否在输出的 Markdown 表格中包含索引列。
        *args: 透传给 ``DataFrame.to_markdown`` 的位置参数。
        **kwargs: 透传给 ``DataFrame.to_markdown`` 的关键字参数。

    Returns:
        str: 转换后的 Markdown 表格字符串。
    """
    return df.to_markdown(*args, index=index, **kwargs)
