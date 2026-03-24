# Daily Task Manager - React + Google Drive

Google Drive와 동기화되는 할 일 관리 앱 (React 버전)

## 🚀 설치 및 실행

### 1. 프로젝트 설정

```bash
cd /c/Study-02/todo-react
npm install
```

### 2. Google Cloud 설정

#### Step 1: Google Cloud Console 접속
1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 새 프로젝트 생성
   - 프로젝트 이름: "Daily Task Manager"

#### Step 2: Google Drive API 활성화
1. 왼쪽 메뉴 → "API 및 서비스" → "라이브러리"
2. "Google Drive API" 검색
3. "활성화" 클릭

#### Step 3: OAuth 2.0 클라이언트 ID 생성
1. 왼쪽 메뉴 → "API 및 서비스" → "사용자 인증 정보"
2. "사용자 인증 정보 만들기" → "OAuth 2.0 클라이언트 ID"
3. 애플리케이션 유형: "웹 애플리케이션"
4. 다음 정보 추가:
   - **이름**: "Daily Task Manager"
   - **승인된 JavaScript 출처**:
     ```
     http://localhost:5173
     ```
   - **승인된 리디렉션 URI**:
     ```
     http://localhost:5173
     ```
5. "만들기" 클릭
6. 표시되는 클라이언트 ID 복사

#### Step 4: 환경변수 설정
1. `/c/Study-02/todo-react/.env` 파일 생성 (`.env.example`을 복사):
   ```bash
   cp .env.example .env
   ```

2. `.env` 파일 편집:
   ```
   VITE_GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE
   ```
   - `YOUR_CLIENT_ID_HERE`를 위에서 복사한 클라이언트 ID로 교체

### 3. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 `http://localhost:5173` 접속

## 📋 기능

### Core Features
- ✅ Google 로그인/로그아웃
- ✅ 할 일 추가/수정/삭제
- ✅ 완료 체크박스
- ✅ 카테고리 분류 (업무/개인/공부)
- ✅ 진행률 표시 (그래디언트 바)
- ✅ 다크모드
- ✅ JSON 내보내기/가져오기

### Google Drive 연동
- ✅ 자동 동기화 (1초 debounce)
- ✅ AppData 폴더에 todos.json 저장
- ✅ 동기화 상태 표시 (저장 중, 저장됨, 오류)
- ✅ 파일 ID 캐싱 (localStorage)
- ✅ 재시도 로직 (실패 시 1회 자동 재시도)

## 🏗️ 프로젝트 구조

```
todo-react/
├── public/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── ProgressBar.jsx
│   │   ├── TodoInput.jsx
│   │   ├── TodoItem.jsx
│   │   └── CategorySection.jsx
│   ├── hooks/
│   │   ├── useGoogleDrive.js (Google Drive API)
│   │   └── useGoogleDrive.js와 통합
│   ├── context/
│   │   └── AppContext.jsx (전역 상태)
│   ├── utils/
│   │   └── driveHelper.js (Drive 헬퍼 함수)
│   ├── App.jsx
│   ├── App.css
│   └── main.jsx
├── .env (로컬, .gitignore에 포함)
├── .env.example (템플릿)
├── package.json
└── vite.config.js
```

## 🔄 자동 동기화 흐름

```
할 일 CRUD
  ↓
useState 상태 업데이트
  ↓
useEffect 트리거 (debounce 1초)
  ↓
Google Drive API 요청
  ↓
저장 성공/실패 상태 표시
```

## 🔐 Google Drive 저장 방식

- **위치**: AppData 폴더 (사용자에게 보이지 않음)
- **파일명**: `todos.json`
- **구조**:
  ```json
  {
    "version": "2.0",
    "lastModified": "2026-03-24T...",
    "todos": [
      {
        "id": 1234567890,
        "title": "할 일 제목",
        "category": "work",
        "completed": false,
        "date": "2026. 03. 24."
      }
    ]
  }
  ```

## 🐛 Troubleshooting

### "Google Client ID가 설정되지 않았습니다"
- `.env` 파일을 확인하세요
- `VITE_GOOGLE_CLIENT_ID`가 올바르게 설정되어 있는지 확인하세요
- 개발 서버를 다시 시작하세요 (`npm run dev`)

### "로그인이 실패했습니다"
- Google Cloud Console에서 클라이언트 ID 설정을 확인하세요
- 승인된 출처에 `http://localhost:5173`이 포함되어 있는지 확인하세요
- 브라우저 콘솔에서 CORS 오류를 확인하세요

### "저장 오류 발생"
- Google Drive API가 활성화되어 있는지 확인하세요
- 토큰 만료 시간 확인 (자동으로 재로그인됩니다)
- 브라우저 개발자 도구 → Network 탭에서 요청 확인

## 📦 빌드

```bash
npm run build
```

빌드 결과는 `dist/` 폴더에 생성됩니다.

## 🚀 배포 (Vercel 예시)

```bash
npm install -g vercel
vercel
```

환경 변수 설정:
- `VITE_GOOGLE_CLIENT_ID` 추가
- 배포 환경의 Google Cloud 클라이언트 ID 사용

## 📝 기술 스택

- React 18
- Vite
- @react-oauth/google
- gapi-script
- Context API

## 🎯 향후 개선 사항

- [ ] 우선순위 기능
- [ ] 마감일 설정
- [ ] 반복 작업 (매일, 매주, etc)
- [ ] 협업 기능 (여러 사용자 동기화)
- [ ] 로컬 데이터베이스 (IndexedDB) 캐싱
- [ ] PWA 지원
- [ ] 모바일 앱 (React Native)

## 📄 라이선스

MIT

---

**기본 index.html 버전과의 차이점**:
- 👤 Google 로그인 필수
- 🔄 자동 Google Drive 동기화
- 📊 향상된 UI/UX
- ⚙️ 더 나은 상태 관리 (Context API)
