import re
import unicodedata
from typing import List

def to_nfc(text: str) -> str:
    """Unicode NFC 정규화"""
    return unicodedata.normalize("NFC", text)

def collapse_whitespace(text: str) -> str:
    """공백 정규화"""
    return re.sub(r'\s+', ' ', text).strip()

def is_korean_syllable(char: str) -> bool:
    """한글 음절 문자 판별"""
    return '\uAC00' <= char <= '\uD7A3'

def is_korean_token(token: str) -> bool:
    """토큰이 한글을 포함하는지 판별"""
    return any(is_korean_syllable(ch) for ch in token)

def jamo_decompose(char: str) -> tuple:
    """한글 음절을 자모로 분해"""
    if not is_korean_syllable(char):
        return (char,)
    
    code = ord(char) - 0xAC00
    jong = code % 28
    jung = (code - jong) // 28 % 21
    cho = ((code - jong) // 28 - jung) // 21
    
    cho_list = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
    jung_list = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
    jong_list = ['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
    
    result = [cho_list[cho], jung_list[jung]]
    if jong > 0:
        result.append(jong_list[jong])
    
    return tuple(result)

