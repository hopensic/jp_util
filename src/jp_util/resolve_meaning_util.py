import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

from jp_util.jap_base_class import JapBaseWordClass
from jp_util.pandas_util import to_csv_sig

pos_dic = {'動1': '动1',
           '動2': '动2',
           '動3': '动3',
           '副詞': '副词',
           '感動詞': '感叹词',
           '接頭詞': '接头词',
           '接尾詞': '接尾词',
           '接続詞': '连词',
           '連詞': '连词',
           '連体詞': '连体词',
           '代名詞': '代词',
           '代詞': '代词',
           '連語': '惯用句',
           '名詞': '名词',
           '助詞': '助词',
           '助動詞': '助动词',
           '量詞': '量词'
           }

df_base_pos = JapBaseWordClass.gen_df_base_pos()
df_base_pron = JapBaseWordClass.gen_df_base_pron_latest()
df_base_word = JapBaseWordClass.gen_df_base_word_latest()


class GeneratedMeaningParser:
    def __init__(self):
        self.rows = []  # Will store flat records for DataFrame

    def _parse_desc_list(self, s: Optional[str]) -> List[tuple[str, str]]:
        """Parse [(描述:百分比%), ...] → [('描述', '百分比'), ...]"""
        if not s or not s.strip():
            return []
        pattern = r'\(([^:)]+):([^)]+)%\)'
        matches = re.findall(pattern, s)
        return [(desc.strip(), pct.strip()) for desc, pct in matches]

    def _parse_pos_block(self, spell: str, pron: str, pron_per: str, block: str):
        """Parse {词性:百分比%[描述列表], ...} and append flat rows"""
        pos_pattern = r'([^,:{}]+):(\d+)%(\[[^\]]*\])?'
        for match in re.finditer(pos_pattern, block):
            pos, pos_percent, desc_list_str = match.groups()
            pos = pos.strip()
            pos_percent = pos_percent.strip()
            desc_list_str = desc_list_str.strip() if desc_list_str else None

            # Append one row per pos
            self.rows.append({
                "spell": spell,
                "pron": pron,
                "pron_per": pron_per,
                "pos": pos,
                "pos_per": pos_percent,
                "meaning_desc": desc_list_str  # keep raw for now, or parse further if needed
            })

    def _parse_pronunciation_block(self, spell: str, pron_part: str):
        """Parse single pronunciation entry: あいだ:60%{...}"""
        match = re.match(r'^([^:]+):(\d+)%\{([^{}]*)\}$', pron_part.strip())
        if not match:
            raise ValueError(f"Invalid pronunciation format: {pron_part}")

        pron, pron_per, pos_block = match.groups()
        pron = pron.strip()
        pron_per = pron_per.strip()

        self._parse_pos_block(spell, pron, pron_per, pos_block)

    def parse_line(self, line: str) -> Dict[str, Any]:
        """Parse one full line and append flattened rows internally"""
        line = line.strip()
        if not line:
            return {}

        try:
            spelling_part, rest = line.split("|", 1)
        except ValueError:
            raise ValueError(f"Line missing '|' separator: {line}")

        spell = spelling_part.strip()

        # Clear previous pronunciation rows for this word (in case of reuse)
        pron_parts = [p.strip() for p in rest.split("|") if p.strip()]

        for pron_part in pron_parts:
            self._parse_pronunciation_block(spell, pron_part)

        return {"spelling": spell, "pronunciations_count": len(pron_parts)}

    def parse_file(self, filepath: Path) -> pd.DataFrame:
        """Parse entire file and return flattened DataFrame"""
        self.rows.clear()  # Reset
        failed_lines = []

        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    self.parse_line(line)
                except Exception as e:
                    failed_lines.append((line_num, line, str(e)))

        df = pd.DataFrame(self.rows)
        if not df.empty:
            df = df[['spell', 'pron', 'pron_per', 'pos', 'pos_per', 'meaning_desc']]
            df['pos'] = df['pos'].str.strip()

        if failed_lines:
            print(f"Warning: {len(failed_lines)} lines failed to parse:")
            for num, ln, err in failed_lines[:10]:  # Show first 10 errors
                print(f"  Line {num}: {err}\n    {ln.rstrip()}")
            if len(failed_lines) > 10:
                print(f"  ... and {len(failed_lines) - 10} more")

        return df

    def to_csv(self, df: pd.DataFrame, output_path: str):
        """Save with UTF-8-SIG encoding (Excel friendly)"""
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Saved {len(df)} records → {output_path}")

    # 生成最终可导入系统的词义
    def gen_available_meaning_df(selfs, df: pd.DataFrame):
        df['pos'] = df['pos'].map(pos_dic).fillna(df['pos'])

        # 关联词性ID
        df["pos_id"] = (
            df["pos"]
            .map(df_base_pos.set_index("pos")["pos_id"])
            .astype("Int64")
        )

        df.set_index(["spell", "pron"], inplace=True)
        df_base_pron.set_index(["spell", "pron"], inplace=True)
        df_base_word.set_index(["spell"], inplace=True)
        # 关联发音数据集
        df_merged = pd.merge(df, df_base_pron[["pron_id"]],
                             left_index=True,
                             right_index=True,
                             how="left",
                             indicator="check_pron",
                             )
        replace_dict = {"both": "normal", "left_only": "pron_missing"}
        df_merged["check_pron"] = df_merged["check_pron"].map(replace_dict)
        df_merged = df_merged.reset_index()

        # 关联基础词频数据集
        df_merged.set_index(["spell"], inplace=True)
        df_meaning = df_merged.merge(
            df_base_word[["word_id"]],
            left_index=True,
            right_index=True,
            how="left",
            indicator="check_spell",
        )
        # 字符串替换，把拼写找不到的标识一下
        replace_dict_2 = {"both": "normal", "left_only": "spell_missing"}
        df_meaning["check_spell"] = df_meaning["check_spell"].map(replace_dict_2)
        df_meaning = df_meaning.reset_index()
        # to_csv_sig(df_meaning, "D:/Dropbox/06.wanjuan/99.tmp/normal_merged_20251202.csv")

        # 将单行的词义转为多行的词义
        extracted = df_meaning["meaning_desc"].str.extractall(r"\(([^:)]+):([^)]+)%\)")
        extracted = extracted.reset_index(level=1, drop=True).rename(
            columns={0: "meaning", 1: "meaning_per"}
        )
        # to_csv_sig(extracted, 'd:/tmp/extracted_tmp.csv')

        extracted["meaning_per"] = extracted["meaning_per"].astype(float)
        result = df_meaning.drop(columns=["meaning_desc"]).join(extracted)
        # to_csv_sig(result, "D:/Dropbox/06.wanjuan/99.tmp/result_20251202.csv")

        result["pron_per"] = result["pron_per"].astype(float)
        result["pos_per"] = result["pos_per"].astype(float)

        result["pron_per"] = round(result["pron_per"] / 100, 2)
        result["pos_per"] = round(result["pos_per"] / 100, 2)
        result["meaning_per"] = round(result["meaning_per"] / 100, 2)

        result["meaning_per"] = round(
            result["pron_per"] * result["pos_per"] * result["meaning_per"], 2
        )

        column_order = [
            "spell",
            "pron",
            "pos",
            "meaning",
            "meaning_per",
            "pos_per",
            "pron_per",
            "word_id",
            "pron_id",
            "check_spell",
            "check_pron",
            "pos_id"
        ]
        result = result.reset_index(drop=True)

        start_index = 10000
        result.index = range(
            start_index, start_index + len(result)
        )

        result.index.name = "meaning_id"
        return result[column_order]


# ================================
# Usage Example
# ================================

if __name__ == "__main__":
    parser = GeneratedMeaningParser()

    input_path = Path(r'D:\03.bigfile\word_meaning\tmp256\256.txt')
    output_path = r'D:\Dropbox\06.wanjuan\99.tmp\meaning_merged_1202.csv'

    df = parser.parse_file(input_path)
    to_csv_sig(df, output_path)
    # parser.to_csv(df, output_path)
    print(f"\nTotal records: {len(df)}")
    print("Sample:")
    print(df.head(10))

    result = parser.gen_available_meaning_df(df)
    to_csv_sig(result, 'd:/tmp/abc_tmp.csv')
