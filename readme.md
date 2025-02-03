# **StoryMap_Client 프로젝트**

## 📌 1. 목적 

**StoryMap_Client**는 Tokamak Network의 **GemSTON Fantasy** 세계관에서 **스토리 크리에이터들이 자신의 이야기를 StoryMap 프로젝트에 자동 등록할 수 있도록 돕는 클라이언트 애플리케이션**입니다.  

### 🔹 **StoryMap 프로젝트와의 관계**
✅ **사용자는 자신의 GitHub 저장소에 md 파일을 작성**하기만 하면, GemSTON Fantasy의 StoryMap에 **스토리 요약본 및 원본 읽기 URL이 자동 등록**됩니다.  
✅ **StoryMap 프로젝트는 Firestore를 활용하여 StoryMap_Client에서 전송된 데이터를 저장하고, Tokamak Network의 커뮤니티 맴버들이 쉽게 접근할 수 있도록 관리**합니다.  
✅ **결과적으로, GemSTON Fantasy StoryMap에서 모든 스토리가 하나의 세계관으로 통합**되며, 사용자들은 서로의 이야기에 쉽게 접근할 수 있습니다.  

---

## 📌 2. 설치 방법 (Command Line)

이 프로젝트를 실행하려면 **Python 3.10 이상**이 필요합니다.  

### **1️⃣ Conda 가상 환경 설정**
```bash
# Conda가 설치되어 있는지 확인
conda --version

# Conda 환경 생성 (Python 3.10 기반)
conda create --name storymap_client python=3.10

# 가상 환경 활성화
conda activate storymap_client
```

### **2️⃣ StoryMap_Client 프로젝트 클론**
```bash
git clone https://github.com/username/StoryMap_Client.git
cd StoryMap_Client
```

### **3️⃣ 필수 패키지 설치**
```bash
pip install -r requirements.txt
```

### **4️⃣ 환경 변수 설정 (`.env` 파일 생성)**
프로젝트 루트에 `.env` 파일을 생성하고, 아래와 같이 설정합니다.
```ini
GITHUB_TOKEN=your_github_token
OPENAI_API_KEY=your_openai_api_key
STORYMAP_API_URL=https://storymap-api.yourservice.com
FIREBASE_CREDENTIALS_PATH=path_to_your_firebase_credentials.json
```

---

## 📌 3. 파일 구조 및 각 파일 간의 연계 흐름

```
📦 StoryMap_Client
├── 📂 scripts                      # 서비스 기능별 주요 파일
│   ├── fetch_github.py            # ✅ GitHub에서 md 파일 목록을 가져옴 (사용자 인증 포함)
│   ├── process.py                 # ✅ md 파일을 OpenAI API로 요약 및 첫 번째 이미지 URL 추출
│   ├── upload_to_firestore.py      # ✅ StoryMap 프로젝트 API로 데이터 전송
├── 📂 config                       # 환경 설정 관련 파일
│   ├── .env                        # ✅ API 키 및 환경 변수 저장
│   ├── firebase_credentials.json   # ✅ Firestore 인증 키 (선택 사항)
├── 📂 tests                        # 각 기능별 테스트 코드
│   ├── test_github_fetch.py        # ✅ GitHub API 및 사용자 인증 테스트
│   ├── test_openai_summary.py      # ✅ OpenAI 요약 기능 테스트
│   ├── test_firestore_upload.py    # ✅ StoryMap API 전송 테스트
├── 📜 register.py                   # ✅ Entry Point (스토리 등록 프로세스 실행)
├── 📜 requirements.txt              # ✅ 필수 Python 패키지 목록
├── 📜 .gitignore                    # ✅ 업로드 제외 파일 (.env, credentials 등)
├── 📜 README.md                     # ✅ 프로젝트 설명 문서
```

---

### 📌 **각 파일 간 연계 흐름**  
사용자가 `python register.py`를 실행하면 다음과 같은 흐름으로 데이터가 처리됩니다.

1️⃣ **`register.py` 실행**  
- 사용자가 **GitHub 저장소 URL, 저장소 소유자 ID, 스토리 제목을 입력**  

2️⃣ **`fetch_github.py` 실행**  
- 사용자의 **GitHub 저장소에서 `MyStory` 폴더 내 md 파일 목록을 가져옴**  
- **GitHub 저장소 소유자 인증을 수행하여 불법적인 데이터 입력 방지**  

3️⃣ **`process.py` 실행**  
- 가져온 **md 파일을 OpenAI API로 요약**하고 **첫 번째 이미지 URL을 추출**  

4️⃣ **`upload_to_firestore.py` 실행**  
- **StoryMap 프로젝트의 API에 정제된 데이터를 전송**  
- StoryMap 프로젝트가 **Firestore에 저장하고, 프론트엔드에서 UI로 표시**  

---

## 📌 4. 실행 방법 (Command Line)

```bash
python register.py
```

✅ **실행 후, GitHub 저장소 URL 및 정보를 입력하면 StoryMap 프로젝트로 자동 등록됩니다.**

📌 실행 과정(예):
```
등록할 스토리 제목을 입력하세요: [사용자 입력 대기]
귀하의 스토리(md 파일 형식)가 담긴 MyStory 폴더가 Github에 업로드 되어 있어야 합니다.
해당 폴더의 URL을 입력하세요: [사용자 입력 대기]
GitHub 저장소의 소유자 ID를 입력하세요: [사용자 입력 대기]
```

✅ 이후, **Tokamak Network의 GemSTON Fantasy StoryMap에 자동 등록되며, StoryMap을 통해 커뮤니티 맴버들이 손쉽게 접근 가능**합니다.  

---

## 📌 5. 장점 (StoryMap과 Tokamak Network의 연계 장점)

### 🌟 **스토리 자동 등록 시스템**
✅ 사용자가 자신의 **GitHub 저장소 내 `MyStory` 폴더에 md 파일을 추가**하기만 하면, StoryMap 프로젝트로 **자동 등록**됩니다.  
✅ **스토리를 매번 직접 등록할 필요 없이** 새로운 챕터를 추가하면 **자동으로 StoryMap이 업데이트**됩니다.  

### 🌟 **Tokamak Network 커뮤니티와의 연결**
✅ **GemSTON Fantasy StoryMap에 자동 반영**되므로 커뮤니티 맴버들이 편리하게 접근 가능  
✅ 여러 크리에이터들이 **각자의 GitHub 저장소에서 작성한 이야기들이 하나의 StoryMap에 연결**  

### 🌟 **OpenAI API를 활용한 자동 요약 생성**
✅ **스토리 요약본이 자동으로 생성**되어 StoryMap에서 미리보기를 제공  
✅ 전체 내용은 **GitHub 원본 링크를 통해 열람 가능**  
✅ 커뮤니티 맴버들이 **스토리의 주요 내용을 빠르게 파악할 수 있도록 도움**  

### 🌟 **사용자의 스토리 관리 부담 최소화**
✅ **사용자는 자신의 GitHub 저장소만 관리**하면 됨  
✅ StoryMap 프로젝트에서 **자동으로 Firestore에 저장 및 StoryMap UI에서 표시**  
✅ **스토리 버전 관리, 업데이트, 링크 공유 등이 간편**  