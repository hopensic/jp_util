import re
import pykakasi
from jp_util.pandas_util import rd_csv_sig, to_csv_sig

# kanji_range = r"[\u4E00-\u9FCF]"
# hiragana_range = r"[\u3040-\u309F]"
# katakana_range = r"[\u30A0-\u30FF]"

# 定义字符范围
ranges = {
    'kanji': r'[\u4E00-\u9FCF]',
    'hiragana': r'[\u3040-\u309F]',
    'katakana': r'[\u30A0-\u30FF]'
}

kks = pykakasi.kakasi()

value_map = {
    4: 1,  # 1. 汉字：只包含汉字，例如「日本語」。(100)
    6: 2,  # 2. 汉字和平假名：包含汉字和平假名，例如「漢字ひらがな」。(110)
    5: 3,  # 3. 汉字和片假名：包含汉字和片假名，例如「漢字カタカナ」。(101)
    7: 4,  # 4. 汉字、平假名和片假名：包含汉字、平假名和片假名，例如「漢字ひらカタ」。(111)
    2: 5,  # 5. 纯平假名：只包含平假名，例如「ひらがな」。(010)
    1: 6,  # 6. 纯片假名：只包含片假名，例如「カタカナ」。(001)
    3: 7,  # 7. 平假名和片假名混合：包含平假名和片假名，例如「ひらカタ」。(011)
    0: 8,  # 8. 其它 (000)
}


def get_kanji_type(spell: str):
    has_kanji = bool(re.search(ranges['kanji'], spell))
    has_hiragana = bool(re.search(ranges['hiragana'], spell))
    has_katakana = bool(re.search(ranges['katakana'], spell))
    code = (int(has_kanji) * 4) | int(has_hiragana) * 2 | (
        int(has_katakana))
    return value_map[code]


def get_df_col_kanji_type(df):
    for key, pattern in ranges.items():
        df[f'has_{key}'] = df['spell'].str.contains(pattern)
    df['code'] = (
            df['has_kanji'].astype(int) * 4 +
            df['has_hiragana'].astype(int) * 2 +
            df['has_katakana'].astype(int)
    )
    df['kanji_type'] = df['code'].map(value_map)
    del df['has_kanji']
    del df['has_hiragana']
    del df['has_katakana']
    del df['code']


def to_hira(text):
    text_list = kks.convert(text)
    return ''.join([item['hira'] for item in text_list])


if __name__ == '__main__':
    # text
    # text = 'エアコン'
    # ret = get_kanji_type(text)
    # print(ret)

    df = rd_csv_sig("d:/tmp/book_unit_word_202512201057.csv")
    df['old_kanji_type']=df['kanji_type']
    get_df_col_kanji_type(df)
    to_csv_sig(df,"d:/tmp/book_unit_word_new_kanji_type.csv")


