import string

NEWLINE = '\n'
OUTPUT_FOLDER = "output"
INPUT_FOLDER = "input"
ARCHIVE_FOLDER = "archive"

'''
string.punctuation 包含这32个ASCII标点符号：
'''
# !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
japanese_punctuation = '。、！？・…「」『』【】〔〕〈〉《》〖〗〘〙〚〛ー～―‥•◦※♪♫〜'
chinese_punctuation = '，。！？；：""''（）【】《》、…—～·'

##总共73个标点符号
punctuation_set = set(string.punctuation) | set(chinese_punctuation) | set(japanese_punctuation)

# print(f"共 {len(punctuation_set)} 个标点符号")
