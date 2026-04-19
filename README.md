# Bagisto QA Portfolio

Bagisto 데모 스토어를 기준으로 웹, 모바일, API, 크로스채널 계약 테스트를 묶은 QA 자동화 포트폴리오입니다.

현재 기준 검증 범위는 다음과 같습니다.
- 웹 storefront 스모크
- GraphQL API 스모크 및 주문 생성
- Appium/adb 기반 모바일 스모크
- 웹, 앱, API가 같은 Bagisto 백엔드를 보는지 확인하는 계약 테스트
- 앱 UI에서 실제 주문 생성 후 API 주문 목록과 대조하는 시나리오

자세한 결과는 [reports/TEST_RESULTS.md](C:/Users/holly/Documents/SwQa/bagisto_qa_portfolio/reports/TEST_RESULTS.md) 에 정리했습니다.
수동 확인 절차는 [reports/MANUAL_TEST_GUIDE.md](C:/Users/holly/Documents/SwQa/bagisto_qa_portfolio/reports/MANUAL_TEST_GUIDE.md) 에 정리했습니다.

## 환경

기본 설정은 `config/environments/dev.json`에 정의되어 있으며, 환경 변수로 오버라이드 가능합니다.

### 기본 환경 설정
- 웹 URL: `https://api-demo.bagisto.com`
- GraphQL URL: `https://api-demo.bagisto.com/api/graphql`
- Storefront Key: `pk_storefront_vxLIYv5PIp7jkujPNGLFQoDvIdsh2RMF`
- Android APK: `mobile-app/bagisto.apk` (105MB)
- Android app package: `com.webkul.bagisto.mobikul`
- Android main activity: `com.bagisto.bagisto_flutter.MainActivity`
- Emulator: `emulator-5554`
- Appium Server: `http://127.0.0.1:4723`

### 모바일 앱 설치

테스트 실행 전에 에뮬레이터에 APK를 설치해야 합니다:

```powershell
# 에뮬레이터 실행 후
C:\Users\holly\Documents\SwQa\android-sdk\platform-tools\adb.exe -s emulator-5554 install -r mobile-app/bagisto.apk
```

자세한 내용은 [mobile-app/README.md](mobile-app/README.md)를 참고하세요.

### 환경 변수를 통한 설정 오버라이드
```powershell
# Web/API URL 변경
$env:BAGISTO_WEB_BASE_URL = "https://your-instance.com"
$env:BAGISTO_API_BASE_URL = "https://your-instance.com/api/graphql"
$env:BAGISTO_STOREFRONT_KEY = "your-storefront-key"

# 모바일 설정 변경
$env:APPIUM_SERVER_URL = "http://127.0.0.1:4723"
$env:MOBILE_DEVICE_ID = "emulator-5554"
$env:ADB_PATH = "C:/path/to/adb.exe"

# Playwright headless 모드 변경
$env:PW_HEADLESS = "false"
```

주요 설정 파일:
- [config/environments/dev.json](config/environments/dev.json) - 기본 환경 설정
- [config/settings.py](config/settings.py) - 설정 로더 및 환경 변수 처리

## 디렉터리
```text
bagisto_qa_portfolio/
|-- api/                # GraphQL clients
|   |-- clients/        # API client implementations (auth, cart, checkout, product)
|   `-- schemas/        # GraphQL schema definitions
|-- config/             # 환경 설정
|   |-- environments/   # 환경별 설정 파일 (dev.json)
|   `-- settings.py     # 설정 로더 및 환경 변수 처리
|-- data/               # 테스트 데이터
|   `-- performance/    # JMeter용 CSV 데이터
|-- mobile-app/         # 모바일 앱 APK 및 설치 가이드
|   |-- bagisto.apk     # Bagisto Android 앱 (105MB)
|   `-- README.md       # APK 설치 및 재빌드 가이드
|-- pages/              # Web/Mobile page objects (POM 패턴)
|   |-- web/            # Playwright 웹 페이지 객체
|   `-- mobile/         # Appium 모바일 페이지 객체
|-- performance/        # 성능 테스트
|   `-- jmeter/         # JMeter 테스트 계획
|-- postman/            # Postman collection
|-- reports/            # 결과 문서 및 리포트
|   |-- assets/         # 스크린샷 및 다이어그램
|   |-- portfolio_attachment.html  # HTML 포트폴리오 리포트
|   |-- TEST_RESULTS.md
|   `-- MANUAL_TEST_GUIDE.md
|-- tests/
|   |-- api/            # API 테스트 (8 tests)
|   |-- contract/       # 크로스채널 계약 테스트 (5 tests)
|   |-- mobile/         # 모바일 앱 테스트 (4 tests)
|   |-- web/            # 웹 UI 테스트 (4 tests)
|   `-- conftest.py     # pytest fixtures 및 설정
|-- utils/              # 공통 유틸리티
|   |-- checkout_helper.py      # 체크아웃 공통 로직
|   |-- mobile_adb_helper.py    # ADB 헬퍼 클래스
|   `-- ...
|-- IMPROVEMENTS.md     # 프로젝트 개선사항 요약
|-- pytest.ini
|-- requirements.txt
`-- run_tests.bat
```

## 설치
PowerShell 기준:

```powershell
python -m venv ..\.venv
..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install
```

모바일 테스트는 아래가 추가로 필요합니다.
- Appium 서버 실행 (`appium` 또는 `appium server`)
- Android emulator 실행 (Android Studio 또는 `emulator` 명령)
- APK 설치 (`mobile-app/bagisto.apk` → 에뮬레이터에 설치)
- `android-sdk\platform-tools\adb.exe` 사용 가능 상태

## 실행
전체 실행:

```powershell
run_tests.bat
```

개별 실행:

```powershell
..\.venv\Scripts\python.exe -m pytest tests\web
..\.venv\Scripts\python.exe -m pytest tests\api
..\.venv\Scripts\python.exe -m pytest tests\contract
..\.venv\Scripts\python.exe -m pytest tests\mobile
```

주의:
- `tests\contract` 와 `tests\mobile` 은 같은 에뮬레이터를 공유하므로 직렬 실행을 권장합니다.
- 모바일 테스트는 앱 상태에 영향을 주므로 웹/API와 분리해서 보는 편이 안정적입니다.

## 현재 검증 포인트
- 웹 로그인 화면/상품/장바구니/체크아웃 진입
- 고객 등록, 상품 조회, 장바구니, 주문 목록, 주문 생성
- 모바일 로그인 화면, 카테고리/상품 렌더링, 장바구니 렌더링
- 앱 홈 상품명과 API 상품명 일치
- API 생성 계정으로 앱 로그인 후 `My Orders` 빈 상태 검증
- API로 생성한 주문이 앱 `My Orders` 에 노출되는지 검증
- 앱 UI에서 직접 주문 생성 후 API 주문 목록과 주문번호 대조

## 실행 안정화 원칙
- 웹과 API는 독립 실행 가능
- 계약과 모바일은 직렬 실행
- 모바일 로그인/주문 시나리오는 앱 데이터 초기화 후 시작
- 주문/회원가입 시나리오는 매번 고유 이메일을 생성 (UUID 기반)
- 하드코딩된 경로 제거: 모든 경로는 설정 파일이나 환경 변수로 관리
- 에러 메시지 개선: ADB 기반 모바일 테스트 실패 시 사용 가능한 요소 목록 표시
- 공통 로직 추출: 체크아웃 흐름은 `utils/checkout_helper.py`에서 재사용

## 주요 개선사항

### 1. 설정 관리 개선
- 하드코딩된 경로를 `config/environments/dev.json`으로 이동
- 환경 변수를 통한 설정 오버라이드 지원
- ADB 경로, Appium 서버 URL, 디바이스 ID 등 환경별로 변경 가능

### 2. 코드 품질 향상
- 공통 체크아웃 로직을 `utils/checkout_helper.py`로 추출
- `complete_checkout_flow()`, `add_product_to_cart()` 헬퍼 함수로 중복 제거
- 테스트 코드 가독성 및 유지보수성 향상

### 3. 에러 핸들링 강화
- `mobile_adb_helper.py`의 `find_bounds_by_desc()` 개선
- 요소를 찾지 못했을 때 사용 가능한 요소 목록 표시 (최대 10개)
- 디버깅 시간 단축 및 문제 해결 용이성 증대

### 4. HTML 리포트 보완
- `reports/portfolio_attachment.html` 시각 자료 및 설명 개선
- 모바일 이미지 경로 수정 (SVG 다이어그램으로 대체)
- 체크마크(✓) 추가로 완료된 테스트 명확히 표시
- 기술 스택 및 프로젝트 범위 설명 구체화

### 5. 불필요한 파일 정리
- 사용되지 않는 `data/test_users.json`, `data/products.json`, `data/addresses.json` 제거
- 테스트 데이터는 fixture에서 동적 생성하여 충돌 방지

## 참고
- [tests/api](tests/api) - GraphQL API 테스트
- [tests/contract](tests/contract) - 크로스채널 계약 테스트
- [tests/mobile](tests/mobile) - 모바일 앱 테스트
- [tests/web](tests/web) - 웹 UI 테스트
- [utils/checkout_helper.py](utils/checkout_helper.py) - 체크아웃 공통 로직
- [reports/portfolio_attachment.html](reports/portfolio_attachment.html) - HTML 포트폴리오 리포트
