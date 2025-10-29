from . import common_path as cp
from .file_util import get_obj_by_pickle_path, export_to_pickle_path
from .pandas_util import rd_csv_sig


class JapBaseWordClass():
    df_base_word = None
    df_base_pron = None
    df_base_word_pickcle_path = "d:/95.pickle_files/df_base_word.pickle"
    # -----------------
    df_base_word_v3 = None
    df_base_pron_v3 = None
    df_base_word_pickcle_v3_path = "d:/95.pickle_files/df_base_word_v3.pickle"

    # -----------------
    df_base_word_v4 = None
    df_base_pron_v4 = None
    df_base_word_pickcle_v4_path = "d:/95.pickle_files/df_base_word_v4.pickle"

    df_synonyms_mapping = None

    '''
    日语词条基础类
    '''

    def __init__(self):
        pass

    @staticmethod
    def gen_df_base_word():
        df_base_word = get_obj_by_pickle_path(JapBaseWordClass.df_base_word_pickcle_path)
        if df_base_word is None:
            df_base_word = rd_csv_sig(cp.r_base_freq_csv_v2)
            export_to_pickle_path(df_base_word, JapBaseWordClass.df_base_word_pickcle_path)
        return df_base_word

    @staticmethod
    def gen_df_base_word_v3():
        df_base_word = get_obj_by_pickle_path(JapBaseWordClass.df_base_word_pickcle_v3_path)
        if df_base_word is None:
            df_base_word = rd_csv_sig(cp.r_base_freq_csv_v3)
            export_to_pickle_path(df_base_word, JapBaseWordClass.df_base_word_pickcle_v3_path)
        return df_base_word

    @staticmethod
    def gen_df_base_word_v4():
        df_base_word = get_obj_by_pickle_path(JapBaseWordClass.df_base_word_pickcle_v4_path)
        if df_base_word is None:
            df_base_word = rd_csv_sig(cp.r_base_freq_csv_v4)
            export_to_pickle_path(df_base_word, JapBaseWordClass.df_base_word_pickcle_v4_path)
        return df_base_word

    #获取同义词映射表
    @staticmethod
    def gen_df_synonyms_mapping():
        return rd_csv_sig(cp.r_synonyms_mapping)
