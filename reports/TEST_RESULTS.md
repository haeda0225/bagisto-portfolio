# Test Results

기준일: 2026-04-19

## 요약
- 웹: `4 passed`
- API: `8 passed`
- 계약: `5 passed`
- 모바일: `4 passed`
- 총합: `21 passed`

## 채널별 결과
### Web
- 로그인 진입 및 정책 메시지 확인
- 상품 상세 진입
- 장바구니 진입
- 체크아웃 진입

### API
- 고객 등록
- 로그인 실패/응답 구조 검증
- 카테고리/상품 조회
- 장바구니 추가
- 고객 주문 목록 조회
- 체크아웃 주소 저장
- 배송/결제 방식 저장
- 주문 생성

### Mobile
- 로그인 화면 진입
- 카테고리/상품 목록 렌더링
- 장바구니 탭 렌더링
- simple product 장바구니 추가

### Contract
- 웹 상품명과 API 상품명 일치
- 앱 홈 상품명과 API 상품명 일치
- API 생성 계정으로 앱 로그인 후 `My Orders` 빈 상태 확인
- API 생성 주문이 앱 `My Orders` 에 노출되는지 확인
- 앱 UI에서 직접 주문 생성 후 API 주문 목록과 주문번호 일치 확인

## 의미 있는 검증 결과
- 웹과 앱은 같은 Bagisto 백엔드를 사용함
- 모바일 앱이 실제 사용하는 GraphQL endpoint 기준으로 API 테스트를 재구성함
- 주문 레벨에서 cross-channel 일관성을 검증함
- 앱 UI 주문 완료 화면의 주문번호와 API `customerOrders` 가 연결됨

## 실행 기준
권장 실행 순서:

```powershell
run_tests.bat
```

직접 실행:

```powershell
..\.venv\Scripts\python.exe -m pytest tests\web
..\.venv\Scripts\python.exe -m pytest tests\api
..\.venv\Scripts\python.exe -m pytest tests\contract
..\.venv\Scripts\python.exe -m pytest tests\mobile
```

## 안정화 메모
- 모바일/계약 테스트는 같은 에뮬레이터를 공유하므로 직렬 실행 기준으로 결과를 관리함
- 모바일 체크아웃은 고객 기본 주소를 API로 먼저 생성해 UI 불확실성을 줄임
- 상품 데이터는 데모 서버에서 바뀔 수 있어 홈 화면 기준으로 현재 노출된 simple product 를 선택함

## 주요 개선사항 (2026-04-19)
- **설정 관리**: 하드코딩된 경로를 `config/environments/dev.json`으로 이동하고 환경 변수 지원 추가
- **코드 품질**: 공통 체크아웃 로직을 `utils/checkout_helper.py`로 추출하여 중복 제거
- **에러 핸들링**: 모바일 테스트 실패 시 사용 가능한 UI 요소 목록을 에러 메시지에 포함
- **리포트 개선**: HTML 리포트의 이미지 경로 수정 및 설명 보완
- **데이터 정리**: 사용되지 않는 테스트 데이터 파일 제거 (fixture 기반 동적 생성으로 전환)
