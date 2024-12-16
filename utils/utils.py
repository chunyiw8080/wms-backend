from datetime import datetime
from functools import wraps
from flask import session, redirect, url_for, flash, jsonify
from pypinyin import pinyin, Style


def convert_name_to_pinyin(name: str) -> str:
    pinyin_result = pinyin(name, style=Style.NORMAL)  # 默认拼音形式
    # 拼接拼音为字符串
    pinyin_string = ''.join([item[0] for item in pinyin_result])
    return pinyin_string


def generate_id(count: int) -> str:
    numeric_part = str(count + 1).zfill(4)
    return f"{numeric_part}"




