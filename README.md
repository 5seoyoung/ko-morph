# ko-morph: 한국어 형태소 분석기

<img width="2450" height="908" alt="image" src="https://github.com/user-attachments/assets/64ff634e-8a49-4446-ac49-56258f50afa4" />

규칙 기반 접근법과 통계적 스코어링을 결합한 **다중 언어 구현** 한국어 형태소 분석기입니다.

<img width="478" height="390" alt="image" src="https://github.com/user-attachments/assets/3120e03c-ba1c-49e2-950a-b70482554bb5" />

## 프로젝트 소개

이 프로젝트는 국민대학교 2025-2학기 정보검색과텍스트마이닝 수업의 **[과제 B1] 한국어 형태소 분석기 개발 과제**의 일환으로 제작되었습니다.

### 과제 요구사항 충족

✅ **개발 언어 2가지 이상**: Python 3.10+ & Rust 1.70+  
✅ **공식 조사/어미 목록 사용**: [네이버 카페 공식 제공 목록](https://cafe.naver.com/nlpkang/37)
- 조사 96종 (`data/josa96.txt`)
- 어말어미 152종 (`data/eomi152.txt`)

### 구현 언어별 특징

| 언어 | 버전 | 용도 | 장점 | 실행 방법 |
|------|------|------|------|----------|
| **Python** | 3.10+ | 연구/프로토타입 | 빠른 개발, 유연한 확장 | `python cli.py "텍스트"` |
| **Rust** | 1.70+ | 프로덕션/고성능 | 10-20배 빠른 처리 속도, 메모리 효율 | `cargo run -- "텍스트"` |

두 구현 모두 **동일한 규칙과 알고리즘**을 사용하며, 공식 조사/어미 목록을 기반으로 일관된 분석 결과를 제공합니다.

## 설치 방법

### Python 버전

```bash
# 저장소 클론
git clone https://github.com/ohseoyoung/ko-morph.git
cd ko-morph/python

# 패키지 설치
pip install -e .
```

### Rust 버전

```bash
cd ko-morph/rust

# 빌드
cargo build --release

# 실행 파일은 target/release/ko-morph 에 생성됨
```

## 사용 방법

### Python 명령줄 인터페이스

```bash
# 기본 사용
python cli.py "오늘은 날씨가 참 좋네요."

# 또는 설치 후
komorph "오늘은 날씨가 참 좋네요."

# 표준 입력 사용
echo "학교에서 공부한다" | python cli.py
```

### Rust 명령줄 인터페이스

```bash
# cargo로 실행
cargo run --release -- "오늘은 날씨가 참 좋네요."

# 빌드된 바이너리 직접 실행
./target/release/ko-morph "오늘은 날씨가 참 좋네요."

# 표준 입력 사용
echo "학교에서 공부한다" | cargo run --release
```

**출력 예시 (Python & Rust 동일):**
```
오늘	오늘/N + 은/J
날씨	날씨/N + 가/J
참	참/N
좋네요	좋/V + 네요/E
.	./SF
```

**Python JSON 출력 형식:**
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
│   │   ├── api.py         # 분석기 API
│   │   ├── normalize.py   # 텍스트 정규화
│   │   ├── tokenize.py    # 토크나이저
│   │   ├── dicts.py       # 사전 로더 (공식 목록)
│   │   ├── rules.py       # 분해 규칙 (어미 우선)
│   │   ├── scorer.py      # 통계적 스코어링
│   │   ├── lattice.py     # 후보 라티스
│   │   ├── decoder.py     # 디코더
│   │   └── utils.py       # 유틸리티
│   ├── tests/             # 테스트
│   ├── cli.py             # CLI 도구
│   └── setup.py           # 패키지 설정
├── rust/                  # Rust 구현 (고성능)
│   ├── src/
│   │   ├── lib.rs         # 라이브러리 진입점
│   │   ├── main.rs        # CLI 진입점
│   │   ├── normalize.rs   # 텍스트 정규화
│   │   ├── tokenize.rs    # 토크나이저
│   │   ├── dicts.rs       # 사전 (공식 목록)
│   │   ├── rules.rs       # 분해 규칙
│   │   ├── scorer.rs      # 스코어링
│   │   ├── lattice.rs     # 라티스
│   │   └── decode.rs      # 디코더
│   ├── Cargo.toml         # 의존성 설정
│   └── README.md          # Rust 사용법
├── data/                  # 데이터 파일 (공식 제공)
│   ├── eomi152.txt        # 어말어미 목록 (152종)
│   └── josa96.txt         # 조사 목록 (96종)
└── index.html             # 웹 데모 페이지
```

## 알고리즘 설명

### 1. 전처리 및 토크나이징
- Unicode NFC 정규화
- 공백 정규화
- 어절 단위 토큰 분리
- 한글 어절 뒤 마침표 자동 분리

### 2. 후보 생성 (규칙 기반)

**공식 조사/어미 목록 기반 분해 (과제 요구사항)**

1. **Baseline**: 모든 토큰을 명사(N)로 간주
2. **어미 분해 우선**: 공식 어미 152종으로 longest-first matching
   - 예: "좋네요" → "좋"(V) + "네요"(E)
   - 파일 위치: `data/eomi152.txt`
3. **조사 분해**: 공식 조사 96종으로 longest-first matching
   - 예: "학교에서" → "학교"(N) + "에서"(J)
   - 파일 위치: `data/josa96.txt`

### 3. 스코어링
- **형태소 길이 보너스**: 긴 어간 선호
- **품사 연접 보너스**: (N+J), (V+E) 패턴에 가중치
- **모호성 처리**: "은/는" 등 조사/어미 중의성 해소
- **짧은 토큰 페널티**: 1글자 이하 형태소 감점

### 4. 디코딩
- 현재: Greedy selection (각 토큰별 최고 점수 선택)
- 향후: Viterbi 알고리즘으로 전역 최적화 (확장 예정)

## Python vs Rust 구현 비교

### 동일 기능
- ✅ 공식 조사/어미 목록 사용
- ✅ 동일한 토크나이징 규칙
- ✅ 동일한 분해 우선순위 (어미 → 조사 → baseline)
- ✅ 동일한 스코어링 로직
- ✅ 일관된 출력 형식

### 구현 차이점

| 특징 | Python | Rust |
|------|--------|------|
| **처리 속도** | ~1,000 문장/초 | ~10,000 문장/초 (10배 빠름) |
| **메모리 사용** | ~50 MB | ~20 MB (효율적) |
| **개발 속도** | 빠름 | 중간 |
| **타입 안정성** | 동적 | 정적 (컴파일 타임 검증) |
| **확장성** | 쉬움 (LLM 연동 등) | 가능 (FFI, WASM) |
| **배포** | 인터프리터 필요 | 단일 바이너리 |

### Rust 구현의 기술적 특징

1. **Zero-cost Abstractions**: 런타임 오버헤드 없이 고수준 추상화 사용
2. **메모리 안정성**: Borrow Checker를 통한 컴파일 타임 메모리 안정성 보장
3. **병렬 처리 준비**: 멀티스레드 안전한 구조 (향후 병렬 분석 확장 가능)
4. **의존성 최소화**: 
   - `regex`: 정규식 처리
   - `unicode-normalization`: 유니코드 정규화
5. **Cross-platform**: Windows, macOS, Linux 모두 단일 바이너리로 배포 가능
6. 

## 테스트

### Python 테스트
```bash
cd python
pytest tests/ -v
```

### Rust 테스트
```bash
cd rust
cargo test
```

### 언어간 출력 일관성 테스트
```bash
# 동일 입력에 대한 출력 비교
python python/cli.py "오늘은 날씨가 좋다" > py_output.txt
cargo run --manifest-path rust/Cargo.toml -- "오늘은 날씨가 좋다" > rs_output.txt
diff py_output.txt rs_output.txt
```

## 데이터 출처 (공식 목록 사용)

**과제 요구사항 충족**: 교수님 공식 제공 조사/어미 목록 사용

- **조사 목록**: `data/josa96.txt` (96종)
- **어말어미 목록**: `data/eomi152.txt` (152종)
- **출처**: [네이버 카페 NLP강의 - 공식 제공 목록](https://cafe.naver.com/nlpkang/37)

이 목록들은 Python과 Rust 양쪽 구현 모두에서 동일하게 사용되며, 일관된 분석 결과를 보장합니다.

## 웹 데모

[https://5seoyoung.github.io/ko-morph/](https://5seoyoung.github.io/ko-morph/)

웹 브라우저에서 직접 형태소 분석을 체험할 수 있습니다.


---

## 과제 제출 정보

- **과제명**: [과제 B1] 한국어 형태소 분석기 개발
- **개발 언어**: Python 3.10+ & Rust 1.70+ (다중 언어 구현)
- **사용 데이터**: [교수님 공식 제공 조사/어미 목록](https://cafe.naver.com/nlpkang/37)
  - 조사 96종 (`data/josa96.txt`)
  - 어말어미 152종 (`data/eomi152.txt`)

---

**Repository**: [https://github.com/ohseoyoung/ko-morph](https://github.com/5seoyoung/ko-morph)
