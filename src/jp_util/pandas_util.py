import pandas as pd


# 读取
def rd_csv_sig(path, index_columns=None):
    return pd.read_csv(
        path,
        encoding="utf-8-sig",
        on_bad_lines="skip",
        engine="python",
        index_col=index_columns,
    )


# 导出
def to_csv_sig(df, path, need_index=False):
    df.to_csv(path, index=need_index, encoding="utf-8-sig")
