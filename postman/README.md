# Postman Guide

## 목적
이 폴더는 `pytest` API 자동화를 대체하는 용도가 아니라, 수동 확인과 데모용 보조 산출물로 사용합니다.

주 용도:
- 빠른 수동 smoke check
- 환경 변수 확인
- 데모 시연
- Newman 기반 CI 확장

주 자동화 레이어는 여전히 `pytest + requests`입니다.

## 현재 기준 대상
- Base URL: `https://api-demo.bagisto.com`
- Shop API 문서: `https://api-demo.bagisto.com/api/shop`
- API 루트 문서: `https://api-demo.bagisto.com/api`

## 주의사항
- 공개 demo는 시점에 따라 응답 데이터가 바뀔 수 있습니다.
- Swagger에는 보이지만 실제 호출 시 404/500이 나는 엔드포인트가 있습니다.
- 현재 `pytest` 기준으로는 `categories`, `customer registration`, `add-product-in-cart`, `customer-orders` 흐름이 실제 검증 대상으로 맞춰져 있습니다.

## 권장 사용 방식
1. Postman 환경값에 base URL을 `https://api-demo.bagisto.com`으로 설정
2. 필요한 경우 `X-STOREFRONT-KEY` 헤더를 추가
3. 실제로 동작 확인된 엔드포인트부터 우선 검증

권장 우선 엔드포인트:
- `GET /api/shop/categories`
- `POST /api/shop/customers`
- `POST /api/shop/add-product-in-cart`
- `GET /api/shop/customer-orders`

## 비고
공개 demo의 Shop Swagger 페이지는 요청 시 `X-STOREFRONT-KEY`를 자동 주입합니다.
Postman에서는 이 헤더를 직접 넣어야 할 수 있습니다.
