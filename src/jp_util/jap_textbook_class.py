from . import common_path as cp
from .pandas_util import rd_csv_sig


class JapTextbookClass():
    # 出版社
    df_press = None
    # 书本
    df_book = None
    # 单元
    df_unit = None

    # 词汇
    df_word = None

    def __init__(self):
        pass

    @staticmethod
    # 获取出版社数据
    def get_press():
        return rd_csv_sig(cp.r_synctrain_press)

    @staticmethod
    # 获取图书数据
    def get_book():
        return rd_csv_sig(cp.r_synctrain_book)

    @staticmethod
    # 获取单元数据
    def get_unit():
        return rd_csv_sig(cp.r_synctrain_unit)

    @staticmethod
    # 获取同步训练单词
    def get_word():
        return rd_csv_sig(cp.r_synctrain_word)
