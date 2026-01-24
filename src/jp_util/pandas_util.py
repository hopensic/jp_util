from pathlib import Path
import pandas as pd
from pandas import DataFrame


# 读取
def rd_csv_sig(path, index_columns=None):
    return pd.read_csv(
        path,
        encoding="utf-8-sig",
        on_bad_lines="skip",
        engine="python",
        dtype_backend="numpy_nullable",
        index_col=index_columns,
    )


# 带文件夹的读取
def rd_csv_folder_sig(folder, path, index_columns=None):
    return rd_csv_sig(Path(folder, path), index_columns)


# 导出
def to_csv_sig(df, path, need_index=False):
    df.to_csv(path, index=need_index, encoding="utf-8-sig")
    print(f"Saved {len(df)} records → {path}")


# 带文件夹的导出
def to_csv_fold_sig(df, folder, path, need_index=False):
    to_csv_sig(df, Path(folder, path), need_index)


# 导出parquet形式
def to_parquet(df, output_parquet_path):
    df.to_parquet(
        output_parquet_path,
        engine="pyarrow",  # 或 "fastparquet"
        compression="zstd",  # 最高性价比：zstd / snappy(最快) / gzip(体积最小)
        compression_level=6,  # zstd 建议 3~9，越大越小越慢
        index=False  # 通常不需要存索引
    )


# 读取parquet
def rd_parquet(input_parquet_path):
    return pd.read_parquet(
        input_parquet_path,
        engine="pyarrow"
        # columns=["col1","col2"]   # ← 需要时只读部分列，极快
    )


# 连接多个dataframe


def concat_dfs(*dfs: pd.DataFrame, ignore_index: bool = True, **concat_kwargs) -> pd.DataFrame:
    """
    接受任意多个 DataFrame 并拼接

    用法:
        concat_dfs(df1, df2, df3)
        concat_dfs(*df_list)
    """
    if not dfs:
        raise ValueError("至少需要传入一个 DataFrame")

    non_empty_dfs = [df for df in dfs if not df.empty]
    if not non_empty_dfs:
        raise ValueError("所有传入的 DataFrame 都是空的")

    return pd.concat(
        non_empty_dfs,
        ignore_index=ignore_index,
        **concat_kwargs
    )
