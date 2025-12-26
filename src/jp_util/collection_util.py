# 判断两个dataframe的键是否有重合
import pandas as pd
from pandas import DataFrame

def has_overlapping_values(df_a: DataFrame, df_b: DataFrame, col_a: str, col_b: str):
    set_a = set(df_a[col_a])
    set_b = set(df_b[col_b])
    set_c = set_a & set_b
    return len(set_c), set_c


if __name__ == '__main__':
    df1 = pd.DataFrame([1, 2, 3], columns=['aa'])
    df2 = pd.DataFrame([2, 3, 4], columns=['bb'])
    print(has_overlapping_values(df1, df2, 'aa', 'bb'))
