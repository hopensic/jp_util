import os
import pickle


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
