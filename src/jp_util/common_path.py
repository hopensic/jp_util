import re

# ---------------------------正则---------------------------------
# 解析书面语正则
pattern_table_written = re.compile(r"<table[\s\S]+?>[\s\S]+?<\/table>")
pattern_td_written = re.compile(r"<td><span class=\"\w+\">(.+?)[\s]?</span></td>")

# 解析口头语正则
pattern_table_spoken = re.compile(r"<table[\s\S]+?>[\s\S]+?<\/table>")
pattern_td_spoken = re.compile(r"<td><span class=\"\w+\">(.+?)[\s]?</span></td>")

# 解析音频文件正则
pattern_voice = re.compile(r"<table[\s\S]+?>[\s\S]+?<\/table>")

# \u2460-\u2473 ①-⑳（1-20 带圈数字）
# \uFF21-\uFF3A 全角的A-Z
# \uFF41-\uFF5A 全角的a-z
# \u0391-\u03A9  大写希腊字母
# \u03B1-\u03C9  小写希腊字母

# 用于过滤单词中的各种符号，数字，字母，等非日语字符
filter_pattern = re.compile(
    r"[［］˚О○〇◯◎◇✖✕аА▽△▲♪☆★●|。∙｡･￥\"＂〞〝＇＊ ̊＃#ⅭK₂ⅡⅢⅣ()\-－─−←（）〔〕｛｝〒〈〉／;；<=>@＜＞＠、､_【】％+＋！!&＆'%→？…·・“”」～~※℃\/「｢｣『』{}\u2460-\u2473＝×÷（，＿:：,．\d\[\]\.\?\*a-zA-Z\uFF21-\uFF3A\uFF41-\uFF5A\u0391-\u03A9\u03B1-\u03C9]")

# ---------------------------base_url---------------------------------
base_url = "D:/Dropbox/06.wanjuan/02.jp/freq/"
jlpt_url = "D:/Dropbox/06.wanjuan/02.jp/pos/"
course_map_url = "D:/Dropbox/06.wanjuan/02.jp/course_map/"
article_map_url = "D:/Dropbox/06.wanjuan/02.jp/article/"
meaning_url = "D:/Dropbox/06.wanjuan/02.jp/meaning/"

# ---------------------------base_structure---------------------------------
# 基础词频表 (102306条记录)
r_base_freq_csv = base_url + "r_base_freq.csv"
# 基础词频表第2版 (133638条记录)
r_base_freq_csv_v2 = base_url + "r_base_freq_v2.csv"
# 基础词频表第3版 (81707条记录)
r_base_freq_csv_v3 = base_url + "r_base_freq_v3.csv"
# 基础词频表第4版 (81289条记录) 词条合并后
r_base_freq_csv_v4 = base_url + "r_base_freq_v4.csv"

# 发音词频表 (104097条记录)
r_pron_freq_csv = base_url + "r_pron_freq.csv"
# 发音词频表 (135406条记录)
r_pron_freq_csv_v2 = base_url + "r_pron_freq_v2.csv"

# 词义表(7371条记录)
r_base_meaning_csv = base_url + "r_base_meaning.csv"

# 词性表(条记录)
r_base_pos_csv_v2 = base_url + "r_base_pos_v2.csv"

r_synonyms_mapping = base_url + "synonyms_mapping.csv"



# 2400 word
r_word_2400_xlsx = base_url + "r_word_2400.xlsx"
r_word_2400_v2_csv = base_url + "r_word_2400_v2.csv"
w_word_2400_csv = base_url + "w_word_2400.csv"
w_word_2400_with_guide_csv = base_url + "w_word_2400_with_guide.csv"
w_word_2400_without_guide_csv = base_url + "w_word_2400_without_guide.csv"
r_final_word_2400_with_freq_csv = base_url + "final/r_final_word_2400_with_freq.csv"
w_final_word_2400_with_freq_and_level_csv = base_url + "final/w_final_word_2400_with_freq_and_level.csv"

r_word_2400_v3_csv = base_url + "2400_v3_raw.csv"  # 大绝有2600

# JLPT 难易度词汇
r_jlpt_csv = base_url + "r_jlpt.csv"
r_jlpt_v2_csv = base_url + "r_jlpt_v2.csv"
w_jlpt_csv = base_url + "w_jlpt.csv"
w_jlpt_word_csv = base_url + "w_jlpt_word.csv"
w_jlpt_multiidx_agg_csv = base_url + "w_jlpt_multiidx_agg.csv"

# 12000JLPT词汇
r_jlpt_12000_csv = jlpt_url + "r_jlpt_12000.csv"
w_jlpt_12000_csv = jlpt_url + "w_jlpt_12000.csv"

# 词性字典表
r_pos_dict_csv = jlpt_url + "r_pos_dict.csv"

# ---------------------------书面语---------------------------------
# 原始解压的nlt书面语词频文件
r_written_freq_nlt_with_enter_txt = base_url + "r_written_freq_nlt_with_enter.txt"
# 格式化后的的书面语词频文件
w_written_freq_nlt_with_enter_csv = base_url + "w_written_freq_nlt_with_enter.csv"
# 格式化后分组汇总后的书面语词频文件(因为词语有重复)
w_written_freq_nlt_sumed_csv = base_url + "w_written_freq_nlt_sumed.csv"

# ---------------------------口语---------------------------------
# 原始解压的nlb口语词频文件
r_spoken_freq_nlb_with_enter_txt = base_url + "r_spoken_freq_nlt_with_enter.txt"
# 格式化后的的口语词频文件
w_spoken_freq_nlb_with_enter_csv = base_url + "w_spoken_freq_nlb_with_enter.csv"
# 过滤后的的口语词频文件
w_spoken_freq_nlb_with_enter_filtered_csv = base_url + "w_spoken_freq_nlb_with_enter_filtered.csv"
# 增加headword-reading-type字段后的的口语词频文件
w_spoken_freq_nlb_with_enter_filtered_hrt_csv = base_url + "w_spoken_freq_nlb_with_enter_filtered_hrt.csv"
# 对headword, reading字段分组后的语词频文件
w_spoken_freq_nlb_with_enter_filtered_hr_csv = base_url + "w_spoken_freq_nlb_with_enter_filtered_hr.csv"
# 格式化后分组汇总后的口语词频文件
w_spoken_freq_nlb_sumed_csv = base_url + "w_spoken_freq_nlb_sumed.csv"

# ---------------------------合并书面语和口语---------------------------------
# 书面语和口语词汇汇总数据
w_merged_freq_sumed_csv = base_url + "w_merged_freq_sumed.csv"
# 原始--书面语和口语词汇汇总数据
w_raw_merged_freq_sumed_csv = base_url + "w_raw_merged_freq_sumed.csv"
# 原始--书面语和口语词汇汇总数据-以word作为分组
w_word_raw_merged_freq_sumed_csv = base_url + "w_word_raw_merged_freq_sumed.csv"

# 临时文件
w_tmp_csv = base_url + "w_tmp_csv.csv"

# ---------------------------course_map(课程地图)---------------------------------
# 课程地图单元主表（course_map_unit)
w_course_map_unit_csv = course_map_url + "w_course_map_unit.csv"
# 关卡表(course_stage)
w_course_stage_csv = course_map_url + "w_course_stage.csv"
# 五十音表(fifty tones)
w_fifty_tones_csv = course_map_url + "w_fifty_tones.csv"
# 生词表(new_words)
w_new_words_csv = course_map_url + "w_new_words.csv"
# 组句句子表(sentence_formation
w_sentence_formation_csv = course_map_url + "w_sentence_formation.csv"
# 组句句子单词表(sentence_word_formation)
w_sentence_word_formation_csv = course_map_url + "w_sentence_word_formation.csv"
# 阅读文章表(需要和文章主表关联，通过主键关联)(article_stage_rel)
w_article_stage_rel_csv = course_map_url + "w_article_stage_rel.csv"
# 闯关问题关联表(需要和问题主表关联，通过主键关联)(question_stage_rel)
w_question_stage_rel_csv = course_map_url + "w_question_stage_rel.csv"
# 闯关问题表
w_breakthrough_question_csv = course_map_url + "w_breakthrough_question.csv"
# 闯关问题选项表
w_breakthrough_question_option_csv = course_map_url + "w_breakthrough_question_option.csv"

# ---------------------------文章句子问题选项---------------------------------
# 日语文章表(article_jap)
w_article_jap_csv = article_map_url + "w_article_jap.csv"
# 日语文章句子表(article_sentence_jap)
w_article_sentence_jap_csv = article_map_url + "w_article_sentence_jap.csv"
# 问题表(question_jap)
w_question_jap_csv = article_map_url + "w_question_jap.csv"
# 问题选项表(article_question_option_jap)
w_article_question_option_jap_csv = article_map_url + "w_article_question_option_jap.csv"

# ---------------------------摸底测试问题和选项---------------------------------
# 问题表(modi_question)
w_modi_question_csv = article_map_url + "w_modi_question.csv"
# 问题选项表(modi_question_option)
w_modi_question_option_csv = article_map_url + "w_modi_question_option.csv"

# ---------------------------词义相关---------------------------------
simple_meaning_increase_30000_csv = meaning_url + "simple_meaning_increase_30000.csv"
w_merged_130000_simple_meaning_csv = meaning_url + "w_merged_130000_simple_meaning.csv"
# 第二次增加5000以内的词义
w_incr_meaning_merged_v2_3084 = meaning_url + "w_incr_meaning_merged_v2_3084.csv"
w_incr_meaning_merged_v3_3023 = meaning_url + "w_incr_meaning_merged_v3_3023.csv"

# ---------------------------音频文件---------------------------------
r_voice_txt = base_url + "Forvo-Japanese.txt"
r_voice_csv = base_url + "final/r_voice.csv"
