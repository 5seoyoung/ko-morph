# ko-morph: 한국어 형태소 분석기
<img width="2450" height="908" alt="image" src="https://github.com/user-attachments/assets/64ff634e-8a49-4446-ac49-56258f50afa4" />

규칙 기반 접근법과 통계적 스코어링을 결합한 한국어 형태소 분석기입니다.

<img width="478" height="390" alt="image" src="https://github.com/user-attachments/assets/3120e03c-ba1c-49e2-950a-b70482554bb5" />


## 프로젝트 소개

이 프로젝트는 국민대학교 2025 2학기 정보검색과텍스트마이닝 수업의 **[과제 B1] 한국어 형태소 분석기 개발 과제**의 일환으로 제작되었습니다.

### 개발 환경
- **언어**: Python 3.10+
- **조사/어미**: 교수님 공식 제공 목록 사용 (조사 96종, 어말어미 152종)

### 주요 특징

- **규칙 기반 분해**: 공식 조사/어미 목록을 사용한 정확한 형태소 분리
- **통계적 스코어링**: 형태소 길이, 품사 연접 확률 기반 점수 계산
- **확장 가능한 구조**: LLM 재랭킹, 불규칙 활용 처리 등 추가 기능 확장 용이

## 설치 방법

```bash
# 저장소 클론
git clone https://github.com/ohseoyoung/ko-morph.git
cd ko-morph/python

# 패키지 설치
pip install -e .
```

## 사용 방법

### 명령줄 인터페이스 (CLI)

```bash
# 기본 사용
komorph "오늘은 날씨가 참 좋네요."

# 또는
python cli.py "오늘은 날씨가 참 좋네요."

# 표준 입력 사용
echo "학교에서 공부한다" | komorph
```

**출력 예시:**
```
오늘	오늘/N + 은/J
날씨	날씨/N + 가/J
참	참/N
좋네요	좋/V + 네요/E
.	./SF
```

**결과 형식:**
```python
[
    [
        {'morph': '오늘', 'pos': 'N', 'original': '오늘은'},
        {'morph': '은', 'pos': 'J', 'original': '오늘은'}
    ],
    [
        {'morph': '날씨', 'pos': 'N', 'original': '날씨가'},
        {'morph': '가', 'pos': 'J', 'original': '날씨가'}
    ],
    # ...
]
```

## 품사 태그셋

| 태그 | 설명 | 예시 |
|------|------|------|
| N | 명사 | 학교, 책, 사람 |
| V | 동사 어간 | 가, 먹, 공부하 |
| J | 조사 | 은, 는, 이, 가, 을, 를 |
| E | 어미 | 다, 네요, 습니다, 고 |
| NUM | 숫자 | 123, 2024 |
| ENG | 영문 | Python, AI |
| SF | 문장 부호 | . ! ? |
| SP | 구두점 | , ; : |

## 프로젝트 구조

```
ko-morph/
├── python/                 # Python 구현
│   ├── komorph/           # 메인 패키지
│   │   ├── __init__.py
│   │   ├── api.py         # 분석기 API
│   │   ├── normalize.py   # 텍스트 정규화
│   │   ├── tokenize.py    # 토크나이저
│   │   ├── dicts.py       # 사전 로더
│   │   ├── rules.py       # 분해 규칙
│   │   ├── scorer.py      # 스코어링
│   │   ├── lattice.py     # 후보 라티스
│   │   ├── decoder.py     # 디코더
│   │   └── utils.py       # 유틸리티
│   ├── tests/             # 테스트
│   ├── cli.py             # CLI 도구
│   └── setup.py           # 패키지 설정
├── data/                  # 데이터 파일
│   ├── eomi152.txt        # 어말어미 목록 (152종)
│   └── josa96.txt         # 조사 목록 (96종)
├── docs/                  # 문서
└── index.html             # 웹 데모 페이지
```

## 알고리즘 설명

### 1. 전처리 및 토크나이징
- Unicode NFC 정규화
- 공백 정규화
- 어절 단위 토큰 분리
- 한글 어절 뒤 마침표 자동 분리

### 2. 후보 생성 (규칙 기반)
1. **Baseline**: 모든 토큰을 명사(N)로 간주
2. **어미 분해**: 공식 어미 목록으로 longest-first matching
   - 예: "좋네요" → "좋"(V) + "네요"(E)
3. **조사 분해**: 공식 조사 목록으로 longest-first matching
   - 예: "학교에서" → "학교"(N) + "에서"(J)

### 3. 스코어링
- **형태소 길이 보너스**: 긴 어간 선호
- **품사 연접 보너스**: (N+J), (V+E) 패턴에 가중치
- **짧은 토큰 페널티**: 1글자 이하 형태소 감점

### 4. 디코딩
- 현재: Greedy selection (각 토큰별 최고 점수 선택)
- 향후: Viterbi 알고리즘으로 전역 최적화

## 테스트

```bash
cd python

# 단위 테스트 실행
pytest tests/

# 특정 테스트
pytest tests/test_smoke.py -v
```

## 데이터 출처

- **조사 목록**: `data/josa96.txt` (96종)
- **어말어미 목록**: `data/eomi152.txt` (152종)
- [공식 제공 목록 사용](https://cafe.naver.com/nlpkang/37)



## 웹 데모

[https://5seoyoung.github.io/ko-morph/](https://5seoyoung.github.io/ko-morph/)

웹 브라우저에서 직접 형태소 분석을 체험할 수 있습니다.


---

**과제 제출 정보**
- 과제명: [과제 B1] 한국어 형태소 분석기 개발

---
- 개발 언어: Python 3.10+
- 사용 데이터: 교수님 공식 제공 조사/어미 목록
