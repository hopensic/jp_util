"""
DataFrame 通用验证框架
======================
设计要点:
1. 全部基于向量化布尔运算,百万级数据无压力
2. 规则即对象,可组合、可复用、可扩展
3. 校验结果以报告形式返回,不直接抛异常
4. 支持 error / warning 两级严重程度
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Iterable, List, Optional, Sequence, Union

import numpy as np
import pandas as pd


# ---------- 1. 基础类型 ----------

class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass
class RuleResult:
    """单条规则的校验结果"""
    rule_name: str
    columns: List[str]
    severity: Severity
    passed: bool                  # 是否全部通过
    failed_mask: pd.Series        # 行级布尔 mask: True 表示该行失败
    failed_count: int
    message: str = ""

    def __repr__(self) -> str:
        status = "✓" if self.passed else "✗"
        return (f"[{status}] {self.severity.value.upper():7s} "
                f"{self.rule_name:30s} cols={self.columns} "
                f"failed={self.failed_count}")


@dataclass
class ValidationReport:
    """整体校验报告"""
    results: List[RuleResult] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """没有任何 error 级别失败即视为通过"""
        return all(r.passed for r in self.results if r.severity == Severity.ERROR)

    @property
    def errors(self) -> List[RuleResult]:
        return [r for r in self.results if not r.passed and r.severity == Severity.ERROR]

    @property
    def warnings(self) -> List[RuleResult]:
        return [r for r in self.results if not r.passed and r.severity == Severity.WARNING]

    def failed_rows(self, df: pd.DataFrame, severity: Severity = Severity.ERROR) -> pd.DataFrame:
        """返回所有失败的行,并附加一个 `_failed_rules` 列说明违反了哪些规则"""
        if not self.results:
            return df.iloc[0:0].copy()

        all_mask = pd.Series(False, index=df.index)
        rule_tags = pd.Series([[] for _ in range(len(df))], index=df.index)

        for r in self.results:
            if r.passed or r.severity != severity:
                continue
            all_mask |= r.failed_mask.reindex(df.index, fill_value=False)
            for idx in df.index[r.failed_mask.reindex(df.index, fill_value=False)]:
                rule_tags.loc[idx] = rule_tags.loc[idx] + [r.rule_name]

        out = df.loc[all_mask].copy()
        out["_failed_rules"] = rule_tags.loc[all_mask]
        return out

    def summary(self) -> pd.DataFrame:
        return pd.DataFrame([{
            "rule": r.rule_name,
            "columns": ",".join(r.columns),
            "severity": r.severity.value,
            "passed": r.passed,
            "failed_count": r.failed_count,
            "message": r.message,
        } for r in self.results])

    def __repr__(self) -> str:
        head = f"ValidationReport: {'PASS' if self.is_valid else 'FAIL'} " \
               f"(errors={len(self.errors)}, warnings={len(self.warnings)})"
        body = "\n".join(repr(r) for r in self.results)
        return f"{head}\n{body}"


# ---------- 2. 规则基类 ----------

class Rule(ABC):
    def __init__(
        self,
        columns: Union[str, Sequence[str]],
        severity: Severity = Severity.ERROR,
        name: Optional[str] = None,
    ):
        self.columns = [columns] if isinstance(columns, str) else list(columns)
        self.severity = severity
        self.name = name or self.__class__.__name__

    @abstractmethod
    def _check(self, df: pd.DataFrame) -> pd.Series:
        """返回 pass_mask:True=通过,False=失败,长度等于 df"""

    def validate(self, df: pd.DataFrame) -> RuleResult:
        # 列存在性检查
        missing = [c for c in self.columns if c not in df.columns]
        if missing:
            return RuleResult(
                rule_name=self.name, columns=self.columns, severity=self.severity,
                passed=False,
                failed_mask=pd.Series(True, index=df.index),
                failed_count=len(df),
                message=f"列不存在: {missing}",
            )
        pass_mask = self._check(df).reindex(df.index, fill_value=False).astype(bool)
        failed_mask = ~pass_mask
        failed = int(failed_mask.sum())
        return RuleResult(
            rule_name=self.name, columns=self.columns, severity=self.severity,
            passed=(failed == 0), failed_mask=failed_mask, failed_count=failed,
            message=f"违反规则的行数: {failed}" if failed else "OK",
        )


# ---------- 3. 内置常用规则 (全部向量化) ----------

class NotNull(Rule):
    """指定列不允许为空"""
    def _check(self, df):
        return df[self.columns].notna().all(axis=1)


class IsNumeric(Rule):
    """指定列必须是数值 (含可被转换的字符串数值)"""
    def __init__(self, columns, allow_str_number=False, **kw):
        super().__init__(columns, **kw)
        self.allow_str_number = allow_str_number

    def _check(self, df):
        mask = pd.Series(True, index=df.index)
        for c in self.columns:
            s = df[c]
            if pd.api.types.is_numeric_dtype(s):
                col_mask = s.notna()
            elif self.allow_str_number:
                col_mask = pd.to_numeric(s, errors="coerce").notna()
            else:
                col_mask = pd.Series(False, index=df.index)
            mask &= col_mask
        return mask


class InRange(Rule):
    """数值范围 [min, max]"""
    def __init__(self, columns, min_value=None, max_value=None,
                 inclusive=True, **kw):
        super().__init__(columns, **kw)
        self.min_value, self.max_value, self.inclusive = min_value, max_value, inclusive

    def _check(self, df):
        mask = pd.Series(True, index=df.index)
        for c in self.columns:
            s = pd.to_numeric(df[c], errors="coerce")
            col_mask = s.notna()
            if self.min_value is not None:
                col_mask &= (s >= self.min_value) if self.inclusive else (s > self.min_value)
            if self.max_value is not None:
                col_mask &= (s <= self.max_value) if self.inclusive else (s < self.max_value)
            mask &= col_mask
        return mask


class InSet(Rule):
    """值必须落在给定集合内"""
    def __init__(self, columns, allowed: Iterable, **kw):
        super().__init__(columns, **kw)
        self.allowed = set(allowed)

    def _check(self, df):
        mask = pd.Series(True, index=df.index)
        for c in self.columns:
            mask &= df[c].isin(self.allowed)
        return mask


class MatchRegex(Rule):
    """字符串列正则匹配"""
    def __init__(self, columns, pattern: str, **kw):
        super().__init__(columns, **kw)
        self.pattern = re.compile(pattern)

    def _check(self, df):
        mask = pd.Series(True, index=df.index)
        for c in self.columns:
            s = df[c].astype(str)
            mask &= s.str.match(self.pattern).fillna(False)
        return mask


class Unique(Rule):
    """单列或多列联合唯一"""
    def _check(self, df):
        return ~df.duplicated(subset=self.columns, keep=False)


class IsDateTime(Rule):
    """可被解析为日期时间"""
    def __init__(self, columns, fmt: Optional[str] = None, **kw):
        super().__init__(columns, **kw)
        self.fmt = fmt

    def _check(self, df):
        mask = pd.Series(True, index=df.index)
        for c in self.columns:
            parsed = pd.to_datetime(df[c], format=self.fmt, errors="coerce")
            mask &= parsed.notna()
        return mask


class Custom(Rule):
    """自定义函数:接受 df,返回 pass_mask Series"""
    def __init__(self, columns, func: Callable[[pd.DataFrame], pd.Series],
                 name: str = "Custom", **kw):
        super().__init__(columns, name=name, **kw)
        self.func = func

    def _check(self, df):
        return self.func(df).astype(bool)


# ---------- 4. 验证器 ----------

class DataFrameValidator:
    def __init__(self, rules: Optional[List[Rule]] = None):
        self.rules: List[Rule] = list(rules or [])

    def add(self, rule: Rule) -> "DataFrameValidator":
        self.rules.append(rule)
        return self

    def validate(self, df: pd.DataFrame, raise_on_error: bool = False) -> ValidationReport:
        report = ValidationReport(results=[r.validate(df) for r in self.rules])
        if raise_on_error and not report.is_valid:
            raise ValueError(f"DataFrame 校验失败:\n{report}")
        return report


# ---------- 5. 使用示例 ----------

if __name__ == "__main__":
    df = pd.DataFrame({
        "id":     [1, 2, 3, 4, 4, None],
        "name":   ["Tom", "Jerry", "", "Alice", "Bob", "Eve"],
        "age":    [25, 30, "abc", 17, 200, 40],
        "email":  ["a@x.com", "b@x.com", "bad", "d@x.com", "e@x.com", "f@x.com"],
        "gender": ["M", "F", "M", "X", "F", "M"],
        "date":   ["2024-01-01", "2024-02-30", "2024-03-15", None, "2024-05-01", "2024-06-01"],
    })

    validator = (DataFrameValidator()
        .add(NotNull(["id", "name"], name="id_name_not_null"))
        .add(Unique("id", name="id_unique"))
        .add(IsNumeric("age", allow_str_number=False, name="age_is_number"))
        .add(InRange("age", min_value=0, max_value=120, name="age_in_range",
                    severity=Severity.WARNING))
        .add(MatchRegex("email", r"^[\w.+-]+@[\w-]+\.[\w.-]+$", name="email_format"))
        .add(InSet("gender", ["M", "F"], name="gender_enum"))
        .add(IsDateTime("date", name="date_parsable"))
        # 跨列规则示例:custom
        .add(Custom(
            columns=["age", "name"],
            func=lambda d: ~((d["age"] == 0) & (d["name"].str.len() > 0)),
            name="age0_only_for_empty_name",
            severity=Severity.WARNING,
        ))
    )

    report = validator.validate(df)

    print(report)
    print("\n--- summary ---")
    print(report.summary())
    print("\n--- failed rows (errors) ---")
    print(report.failed_rows(df, severity=Severity.ERROR))