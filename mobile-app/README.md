# Bagisto Mobile App

이 폴더에는 테스트용 Bagisto 모바일 앱 APK 파일이 포함되어 있습니다.

## APK 다운로드

APK 파일이 GitHub 파일 크기 제한(100MB)을 초과하여 repository에 포함되지 않았습니다.

### 방법 1: 직접 빌드 (권장)
아래 "APK 재빌드" 섹션을 참고하여 직접 빌드하세요.

### 방법 2: 에뮬레이터에 이미 설치된 앱 사용
에뮬레이터에 Bagisto 앱이 이미 설치되어 있다면 그대로 사용 가능합니다.

## APK 정보

- **파일명**: `bagisto.apk`
- **크기**: 105MB
- **빌드 날짜**: 2026-04-18
- **패키지명**: `com.webkul.bagisto.mobikul`
- **메인 액티비티**: `com.bagisto.bagisto_flutter.MainActivity`

## 사용 방법

### 에뮬레이터에 설치
```powershell
# ADB를 사용하여 에뮬레이터에 설치
C:\Users\holly\Documents\SwQa\android-sdk\platform-tools\adb.exe -s emulator-5554 install -r mobile-app/bagisto.apk
```

### 실제 기기에 설치
```powershell
# USB 디버깅이 활성화된 기기에 설치
C:\Users\holly\Documents\SwQa\android-sdk\platform-tools\adb.exe install -r mobile-app/bagisto.apk
```

## 테스트 자동화

이 APK는 `tests/mobile/` 및 `tests/contract/`의 모바일 테스트에서 사용됩니다.

테스트 실행 전에 앱이 에뮬레이터에 설치되어 있어야 합니다.

## APK 재빌드

만약 새로운 버전의 APK가 필요하다면:

1. Bagisto 모바일 앱 소스 코드 클론
   ```bash
   git clone https://github.com/bagisto/bagisto-mobile-app.git
   ```

2. Flutter SDK 설치 (https://flutter.dev)

3. 빌드
   ```bash
   flutter build apk --release
   ```

빌드된 APK는 `build/app/outputs/flutter-apk/app-release.apk`에 생성됩니다.
