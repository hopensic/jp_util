from pathlib import Path

from . import common_path as cp
from .file_util import get_obj_by_pickle_path, export_to_pickle_path
from .pandas_util import rd_csv_sig


class JapBaseWordClass():
    # base_word
    df_base_word, df_base_word_pickcle_path = None, "d:/95.pickle_files/df_base_word.pickle"
    df_base_word_v3, df_base_word_pickcle_v3_path = None, "d:/95.pickle_files/df_base_word_v3.pickle"
    df_base_word_v4, df_base_word_pickcle_v4_path = None, "d:/95.pickle_files/df_base_word_v4.pickle"
    df_base_word_v5, df_base_word_pickcle_v5_path = None, "d:/95.pickle_files/df_base_word_v5.pickle"
    df_base_word_v6, df_base_word_pickcle_v6_path = None, "d:/95.pickle_files/df_base_word_v6.pickle"  # 更新了一批word_id,
    df_base_word_v7, df_base_word_pickcle_v7_path = None, "d:/95.pickle_files/df_base_word_v7.pickle"  # 增加了6个单词: 7週間,8週間,9週間,ご存じだ,しばらくだ,白居易

    df_base_pos = None

    # base_pron
    df_base_pron, df_base_pron_pickcle_path = None, "d:/95.pickle_files/df_base_pron.pickle"
    df_base_pron_v2, df_base_pron_pickcle_v2_path = None, "d:/95.pickle_files/df_base_pron_v2.pickle"
    df_base_pron_v3, df_base_pron_pickcle_v3_path = None, "d:/95.pickle_files/df_base_pron_v3.pickle"
    df_base_pron_v4, df_base_pron_pickcle_v4_path = None, "d:/95.pickle_files/df_base_pron_v4.pickle"

    # base_meaning
    df_base_meaning, df_base_meaning_pickcle_path = None, "d:/95.pickle_files/df_base_meaning.pickle"
    df_base_meaning_v2, df_base_meaning_pickcle_v2_path = None, "d:/95.pickle_files/df_base_meaning_v2.pickle"
    df_base_meaning_v3, df_base_meaning_pickcle_v3_path = None, "d:/95.pickle_files/df_base_meaning_v3.pickle"

    df_synonyms_mapping = None

    '''
    日语词条基础类
    '''

    def __init__(self):
        pass

    @staticmethod
    # 获取单词最新版本的数据
    def gen_df_base_word_latest():
        return JapBaseWordClass.gen_df_base_word_v7()

    @staticmethod
    # 获取单词发音最新版本的数据
    def gen_df_base_pron_latest():
        return JapBaseWordClass.gen_df_base_pron_v4()

    @staticmethod
    # 获取词义表最新版本的数据
    def gen_df_base_meaning_latest():
        return JapBaseWordClass.gen_df_base_meaning_v3()

    # ----------------base_word--------------------------
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

    @staticmethod
    def gen_df_base_word_v5():
        df_base_word = get_obj_by_pickle_path(JapBaseWordClass.df_base_word_pickcle_v5_path)
        if df_base_word is None:
            df_base_word = rd_csv_sig(cp.r_base_freq_csv_v5)
            export_to_pickle_path(df_base_word, JapBaseWordClass.df_base_word_pickcle_v5_path)
        return df_base_word

    @staticmethod
    def gen_df_base_word_v6():
        df_base_word = get_obj_by_pickle_path(JapBaseWordClass.df_base_word_pickcle_v6_path)
        if df_base_word is None:
            df_base_word = rd_csv_sig(cp.r_base_freq_csv_v6)
            export_to_pickle_path(df_base_word, JapBaseWordClass.df_base_word_pickcle_v6_path)
        return df_base_word

    @staticmethod
    def gen_df_base_word_v7():
        df_base_word = get_obj_by_pickle_path(JapBaseWordClass.df_base_word_pickcle_v7_path)
        if df_base_word is None:
            df_base_word = rd_csv_sig(cp.r_base_freq_csv_v7)
            export_to_pickle_path(df_base_word, JapBaseWordClass.df_base_word_pickcle_v7_path)
        return df_base_word

    # ----------------base_pron--------------------------

    @staticmethod
    def gen_df_base_pron():
        df_base_pron = get_obj_by_pickle_path(JapBaseWordClass.df_base_pron_pickcle_path)
        if df_base_pron is None:
            df_base_pron = rd_csv_sig(cp.r_pron_freq_csv_v2)
            export_to_pickle_path(df_base_pron, JapBaseWordClass.df_base_pron_pickcle_path)
        return df_base_pron

    @staticmethod
    def gen_df_base_pron_v2():
        df_base_pron_v2 = get_obj_by_pickle_path(JapBaseWordClass.df_base_pron_pickcle_v2_path)
        if df_base_pron_v2 is None:
            df_base_pron_v2 = rd_csv_sig(cp.r_pron_freq_csv_v3)
            export_to_pickle_path(df_base_pron_v2, JapBaseWordClass.df_base_pron_pickcle_v2_path)
        return df_base_pron_v2

    @staticmethod
    def gen_df_base_pron_v3():
        df_base_pron_v3 = get_obj_by_pickle_path(JapBaseWordClass.df_base_pron_pickcle_v3_path)
        if df_base_pron_v3 is None:
            df_base_pron_v3 = rd_csv_sig(cp.r_pron_freq_csv_v4)
            export_to_pickle_path(df_base_pron_v3, JapBaseWordClass.df_base_pron_pickcle_v3_path)
        return df_base_pron_v3

    @staticmethod
    def gen_df_base_pron_v4():
        df_base_pron_v4 = get_obj_by_pickle_path(JapBaseWordClass.df_base_pron_pickcle_v4_path)
        if df_base_pron_v4 is None:
            df_base_pron_v4 = rd_csv_sig(cp.r_pron_freq_csv_v5)
            export_to_pickle_path(df_base_pron_v4, JapBaseWordClass.df_base_pron_pickcle_v4_path)
        return df_base_pron_v4

    # ----------------base_pos--------------------------

    @staticmethod
    def gen_df_base_pos():
        return rd_csv_sig(cp.r_base_pos_csv_v2)

    # ----------------base_meaning--------------------------
    @staticmethod
    def gen_df_base_meaning():
        df_base_meaning = get_obj_by_pickle_path(JapBaseWordClass.df_base_meaning_pickcle_path)
        if df_base_meaning is None:
            df_base_meaning = rd_csv_sig(cp.r_base_meaning_csv)
            export_to_pickle_path(df_base_meaning, JapBaseWordClass.df_base_meaning_pickcle_path)
        return df_base_meaning

    @staticmethod
    def gen_df_base_meaning_v2():
        df_base_meaning_v2 = get_obj_by_pickle_path(JapBaseWordClass.df_base_meaning_pickcle_v2_path)
        if df_base_meaning_v2 is None:
            df_base_meaning_v2 = rd_csv_sig(cp.r_base_meaning_csv_v2)
            export_to_pickle_path(df_base_meaning_v2, JapBaseWordClass.df_base_meaning_pickcle_v2_path)
        return df_base_meaning_v2

    @staticmethod
    def gen_df_base_meaning_v3():
        df_base_meaning_v3 = get_obj_by_pickle_path(JapBaseWordClass.df_base_meaning_pickcle_v3_path)
        if df_base_meaning_v3 is None:
            df_base_meaning_v3 = rd_csv_sig(cp.r_base_meaning_csv_v3)
            pos_dict=JapBaseWordClass.gen_df_base_pos().set_index('pos_id')['pos']
            df_base_meaning_v3['pos']=df_base_meaning_v3['pos_id'].map(pos_dict)
            export_to_pickle_path(df_base_meaning_v3, JapBaseWordClass.df_base_meaning_pickcle_v3_path)
        return df_base_meaning_v3

    # 获取同义词映射表
    @staticmethod
    def gen_df_synonyms_mapping():
        return rd_csv_sig(cp.r_synonyms_mapping)
