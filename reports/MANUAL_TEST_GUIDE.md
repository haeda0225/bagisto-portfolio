# Manual Test Guide

기준일: 2026-04-19

이 문서는 자동화가 아니라 사람이 직접 웹과 앱을 확인할 때 따라가는 수동 테스트 절차입니다.

## 공통 대상
- 웹 storefront: `https://api-demo.bagisto.com`
- 모바일 앱 backend: `https://api-demo.bagisto.com/api/graphql`
- Android app package: `com.webkul.bagisto.mobikul`

## 사전 준비
### 웹
- 브라우저 실행
- `https://api-demo.bagisto.com` 접속 가능 상태

### 앱
- 에뮬레이터 또는 안드로이드 기기 실행
- 설치 앱 실행 가능 상태
- 앱이 최신 설치본인지 확인

## 웹 수동 테스트
### 1. 홈 진입
절차:
1. `https://api-demo.bagisto.com` 접속
2. 홈 메인 화면이 열리는지 확인

기대 결과:
- 홈 페이지가 정상 렌더링된다
- 카테고리, 상품 목록 또는 배너 영역이 보인다

실패 시 체크:
- URL 오타 여부
- 데모 서버 접속 가능 여부
- 브라우저 캐시 문제면 새로고침

### 2. 상품 상세 진입
절차:
1. 홈 또는 카테고리에서 임의 상품 클릭
2. 상품 상세 화면으로 이동하는지 확인

기대 결과:
- 상품명, 가격, 설명 또는 이미지가 보인다
- URL이 상품 상세 페이지로 바뀐다

실패 시 체크:
- 데모 서버 상품 데이터 변경 여부
- 특정 상품만 깨졌는지 다른 상품도 같은지

### 3. 장바구니 진입
절차:
1. 상품 상세 또는 상단/하단 cart 아이콘으로 장바구니 이동
2. 장바구니 화면이 열리는지 확인

기대 결과:
- 장바구니 페이지가 열린다
- 비어 있으면 empty state, 담겨 있으면 item list가 보인다

실패 시 체크:
- 세션 쿠키 문제
- 상품 옵션 선택이 필요한 상품인지

### 4. 체크아웃 진입
절차:
1. 장바구니에서 checkout 관련 버튼 클릭
2. 체크아웃 페이지가 열리는지 확인

기대 결과:
- checkout 화면 또는 로그인/주소 입력 관련 화면으로 진입한다

실패 시 체크:
- 장바구니가 비어 있는지
- 특정 상품 타입이 체크아웃 불가 상태인지

### 5. 웹 로그인 정책 확인
절차:
1. 신규 계정 또는 기존 계정으로 로그인 시도
2. 메시지 확인

기대 결과:
- 현재 demo storefront 는 신규 API 생성 계정에 대해 이메일 인증 요구 메시지가 나올 수 있다
- `Verify your email account first.` 가 나오면 정책상 정상일 수 있다

실패 시 체크:
- 백엔드 연동 문제와 로그인 정책 문제를 구분
- 웹 로그인 실패가 곧 데이터 연동 실패는 아님

## 앱 수동 테스트
### 1. 앱 실행 및 홈 확인
절차:
1. 앱 실행
2. 홈 화면 로딩 확인

기대 결과:
- `bagisto` 홈이 열린다
- `Featured Products` 또는 카테고리 영역이 보인다

실패 시 체크:
- 앱이 다른 환경 URL을 보고 있지 않은지
- 앱 첫 실행 권한 팝업이 막고 있지 않은지

### 2. 로그인 화면 진입
절차:
1. 하단 `Account` 탭 선택
2. guest 상태면 `Login` 선택

기대 결과:
- `Welcome back!`
- 이메일/비밀번호 입력 필드
- `Login` 버튼이 보인다

실패 시 체크:
- 이미 로그인된 상태인지
- 로그인 상태가 남아 있으면 앱 데이터 초기화 후 재시도

### 3. 상품 상세 진입
절차:
1. 홈 `Featured Products` 에서 상품 선택
2. 상세 화면 이동 확인

기대 결과:
- 상품명과 `Add to Cart` 버튼이 보인다

실패 시 체크:
- 현재 홈에 보이는 상품이 virtual/grouped/bundle 타입인지
- simple product 로 다시 시도

### 4. 장바구니 담기
절차:
1. simple product 상세에서 `Add to Cart`
2. 성공 메시지 확인
3. 하단 `Cart` 탭으로 이동

기대 결과:
- `Product added to cart successfully`
- 장바구니 화면에서 해당 상품이 보인다

실패 시 체크:
- 옵션 선택이 필요한 상품인지
- 추천 상품 목록이 바뀌었는지

### 5. 로그인 후 주문 내역 없음 확인
절차:
1. 새 계정 생성 또는 주문 없는 계정으로 로그인
2. `Account > My Orders` 이동

기대 결과:
- `Orders`
- `No Orders Yet`

실패 시 체크:
- 이전 로그인 상태가 남아 있는지
- 해당 계정이 이미 주문을 가진 계정인지

### 6. 앱 UI 주문 생성
절차:
1. 로그인된 계정으로 simple product 장바구니 추가
2. `Cart > Pay Now` 이동
3. 저장 주소가 있으면 checkout 화면에서 주소 카드가 보이는지 확인
4. `Free Shipping` 선택
5. `Money Transfer` 선택
6. `Place Order` 클릭

기대 결과:
- `Thank you for your order!`
- `Your order No. #...`
- `View Order` 또는 `Continue Shopping`

실패 시 체크:
- 주소가 없으면 checkout 상단에서 주소 입력 또는 주소 저장 필요
- 배송/결제 옵션이 안 보이면 화면을 아래로 스크롤
- 장바구니 상품 타입이 주문 불가능한 타입인지 확인

### 7. 앱 주문 내역 반영 확인
절차:
1. 주문 완료 후 `View Order` 또는 `Account > My Orders` 이동
2. 방금 주문번호 확인

기대 결과:
- 방금 생성한 주문번호가 주문 목록에 보인다
- 상태는 보통 `Processing` 으로 보일 수 있다

실패 시 체크:
- 다른 계정으로 로그인된 건 아닌지
- 네트워크 지연으로 목록 반영이 늦는지

## 추천 수동 회귀 시나리오
짧게 한 번 볼 때:
1. 웹 홈 진입
2. 웹 상품 상세 진입
3. 앱 홈 진입
4. 앱 로그인 화면 진입
5. 앱 simple product 장바구니 추가

좀 더 깊게 볼 때:
1. 새 계정 생성
2. 앱 로그인
3. 앱 주문 생성
4. 앱 `My Orders` 에 주문번호 노출 확인
5. API 또는 웹 쪽 결과와 교차 확인

## 참고 문서
- [README.md](C:/Users/holly/Documents/SwQa/bagisto_qa_portfolio/README.md:1)
- [reports/TEST_RESULTS.md](C:/Users/holly/Documents/SwQa/bagisto_qa_portfolio/reports/TEST_RESULTS.md:1)
