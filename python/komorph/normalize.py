# python/komorph/normalize.py
from .utils import to_nfc, collapse_whitespace
import re

def normalize_text(text: str) -> str:
    """텍스트 전처리 및 정규화"""
    # Unicode NFC 정규화
    text = to_nfc(text)
    
    # 공백 정규화
    text = collapse_whitespace(text)
    
    # 특수 문자 정규화 (선택사항)
    text = text.replace('·', '.')
    text = text.replace('…', '...')
    
    return text

