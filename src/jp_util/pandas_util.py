from pathlib import Path

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


def rd_csv_folder_sig(folder, path, index_columns=None):
    path = Path(folder, path)
    return rd_csv_sig(path, index_columns)


# 导出
def to_csv_sig(df, path, need_index=False):
    df.to_csv(path, index=need_index, encoding="utf-8-sig")
    print(f"Saved {len(df)} records → {path}")


def to_csv_fold_sig(df, folder, path, need_index=False):
    path = Path(folder, path)
    to_csv_sig(df, path, need_index)
