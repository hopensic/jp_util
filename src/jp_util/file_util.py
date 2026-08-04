import os
import pickle
from pathlib import Path

base_pkl = Path(r'D:\12.cache\01.pkl')


def get_file_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("文件不存在")
    except IOError:
        print("读取文件时出错")


def write_file_content(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)


# 根据pickle_path 返回对象
def get_obj_by_pickle_path(pickle_path: str):
    if os.path.exists(pickle_path):
        with open(pickle_path, "rb") as f:
            return pickle.load(f)
    else:
        return None


# 将对象导出到 pickle
def export_to_pickle_path(obj, pickle_path: str):
    with open(pickle_path, "wb") as f:
        pickle.dump(obj, f)


def get_obj_from_cache(object_name):
    path = base_pkl / (object_name + '.pkl')
    if path.exists():
        return get_obj_by_pickle_path(path)
    else:
        return None


def export_to_cache(obj, object_name):
    path = base_pkl / (object_name + '.pkl')
    export_to_pickle_path(obj, path)


# 删除指定目录下的所有csv,
def delete_csv_files_pure_python(directory: str, recursive: bool = False):
    """纯 Python 删除 .csv 文件"""
    dir_path = Path(directory)
    pattern = "**/*.csv" if recursive else "*.csv"

    csv_files = list(dir_path.glob(pattern))

    for file in csv_files:
        try:
            file.unlink()
            print(f"已删除: {file}")
        except Exception as e:
            print(f"删除失败 {file}: {e}")

    print(f"共删除 {len(csv_files)} 个 .csv 文件")


def delete_csv_parquet_files_pure_python(directory: str, recursive: bool = False):
    """纯 Python 删除 .csv 和 .parquet 文件"""
    dir_path = Path(directory)

    extensions = ["*.csv", "*.parquet"]
    pattern_prefix = "**/" if recursive else ""

    all_files = []
    for ext in extensions:
        all_files.extend(dir_path.glob(f"{pattern_prefix}{ext}"))

    for file in all_files:
        try:
            file.unlink()
            print(f"已删除: {file}")
        except Exception as e:
            print(f"删除失败 {file}: {e}")

    print(f"共删除 {len(all_files)} 个文件")
