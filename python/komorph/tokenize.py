import re
from typing import List

class KoreanTokenizer:
    def __init__(self):
        # 한글, 영문, 숫자, 기본 문장부호 패턴
        self.pattern = re.compile(
            r'[가-힣]+|[A-Za-z]+|\d+|[.!?;:,\"\'()[\]{}/<>@#$%^&*+=|\\~`-]'
        )
    
    def tokenize(self, text: str) -> List[str]:
        """어절 단위 토크나이징"""
        return self.pattern.findall(text)

def tokenize(text: str) -> List[str]:
    """간단한 토크나이징 함수"""
    tokenizer = KoreanTokenizer()
    return tokenizer.tokenize(text)