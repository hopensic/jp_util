# 判断两个dataframe的键是否有重合
from typing import Set, Any

import pandas as pd
from pandas import DataFrame


def has_overlapping_values(df_a: DataFrame, df_b: DataFrame, col_a: str, col_b: str):
    set_a = set(df_a[col_a])
    set_b = set(df_b[col_b])
    set_c = set_a & set_b
    return len(set_c), set_c


# 判断若干的集合之间是否相互有重叠

from itertools import combinations


def compare_sets(*, show_elements: bool = False, **sets_dict: Set[Any]) -> None:
    """
    两两比较多个集合是否有交集，并可选择显示交集元素

    参数:
        show_elements: 是否打印具体的交集元素，默认 False
        **sets_dict: 关键字参数，key 为集合名称，value 为 set 对象

    示例:
        compare_sets(setA=setA, setB=setB, show_elements=True)
    """
    if len(sets_dict) < 2:
        print("需要至少传入 2 个集合")
        return

    for name1, name2 in combinations(sets_dict.keys(), 2):
        set1 = sets_dict[name1]
        set2 = sets_dict[name2]

        # 类型保护
        if not isinstance(set1, set) or not isinstance(set2, set):
            print(f"警告: {name1} 或 {name2} 不是 set 类型，已跳过")
            continue

        intersection = set1 & set2
        count = len(intersection)

        if count > 0:
            print(f"有交集 → {name1} ↔ {name2}")
            print(f"  交集个数: {count}")

            if show_elements and count > 0:
                # 排序输出更易读（可选）
                elements = sorted(intersection)
                if len(elements) <= 20:
                    print(f"  交集元素: {elements}")
                else:
                    # 元素太多时只显示前几个 + 省略号
                    shown = elements[:10]
                    print(f"  交集元素 (前10个，共{count}个): {shown} ...")
            print("─" * 50)


if __name__ == '__main__':
    df1 = pd.DataFrame([1, 2, 3], columns=['aa'])
    df2 = pd.DataFrame([2, 3, 4], columns=['bb'])
    print(has_overlapping_values(df1, df2, 'aa', 'bb'))
