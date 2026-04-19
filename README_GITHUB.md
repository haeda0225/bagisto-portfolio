# GitHub 업로드 가이드

이 프로젝트를 GitHub에 업로드하는 방법입니다.

## 준비 사항

1. GitHub 계정
2. Git 설치 완료
3. GitHub repository 생성

## 업로드 절차

### 1. GitHub에 새 Repository 생성

1. https://github.com/new 접속
2. Repository 이름: `bagisto-qa-portfolio` (또는 원하는 이름)
3. Description: `Bagisto E-commerce QA Automation Portfolio - Web, Mobile, API, Cross-channel Testing`
4. Public 또는 Private 선택
5. **"Add a README file" 체크 해제** (이미 README.md가 있음)
6. "Create repository" 클릭

### 2. Git Repository 초기화 및 업로드

```powershell
# bagisto_qa_portfolio 폴더로 이동
cd bagisto_qa_portfolio

# Git repository 초기화
git init

# 모든 파일 추가 (.gitignore가 자동으로 제외할 파일 처리)
git add .

# 첫 커밋 생성
git commit -m "Initial commit: Bagisto QA automation portfolio

- Web UI tests with Playwright (4 tests)
- API tests with GraphQL (8 tests)
- Mobile app tests with Appium (4 tests)
- Cross-channel contract tests (5 tests)
- Total: 21 passing tests
- POM pattern, fixture-based data generation, error handling"

# GitHub repository와 연결 (YOUR_USERNAME을 본인 GitHub 계정으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/bagisto-qa-portfolio.git

# main 브랜치로 이름 변경 (필요시)
git branch -M main

# GitHub에 push
git push -u origin main
```

### 3. GitHub에서 확인

https://github.com/YOUR_USERNAME/bagisto-qa-portfolio 에서 업로드된 파일들을 확인할 수 있습니다.

## 주의사항

### APK 파일 (105MB)
- APK 파일은 GitHub 파일 크기 제한(100MB)으로 인해 `.gitignore`에 포함되어 업로드되지 않습니다
- `mobile-app/README.md`에 APK 빌드 방법이 안내되어 있습니다
- 필요시 별도로 Google Drive, Dropbox 등에 APK를 업로드하고 링크를 공유할 수 있습니다

### 제외되는 파일들
`.gitignore`에 의해 다음이 제외됩니다:
- `__pycache__/` - Python 캐시
- `.venv/` - 가상환경
- `.pytest_cache/` - pytest 캐시
- `reports/screenshots/` - 생성된 스크린샷
- `mobile-app/*.apk` - APK 파일

### 포함되는 파일들
- 모든 소스 코드 (`.py` 파일)
- 설정 파일 (`pytest.ini`, `requirements.txt`, `config/`)
- 문서 (`README.md`, `IMPROVEMENTS.md`, 리포트)
- 테스트 파일 (`tests/`)
- Page Objects (`pages/`)
- 유틸리티 (`utils/`)
- 정적 자산 (`reports/assets/` - SVG, PNG)

## Git LFS를 사용하여 APK 포함하기 (선택사항)

만약 APK를 포함하고 싶다면:

```powershell
# Git LFS 설치 (https://git-lfs.github.com/)
# 설치 후:

git lfs install
git lfs track "*.apk"
git add .gitattributes
git add mobile-app/bagisto.apk
git commit -m "Add APK file with Git LFS"
git push
```

## 나중에 프로젝트 클론하기

다른 컴퓨터에서 작업하려면:

```powershell
# Repository 클론
git clone https://github.com/YOUR_USERNAME/bagisto-qa-portfolio.git
cd bagisto-qa-portfolio

# 가상환경 생성 및 활성화
python -m venv .venv
.venv\Scripts\Activate.ps1

# 의존성 설치
pip install -r requirements.txt
playwright install

# 테스트 실행
pytest tests/web
```

## 문제 해결

### "fatal: not a git repository"
→ `git init`을 먼저 실행하세요

### "remote origin already exists"
→ `git remote remove origin` 후 다시 시도

### "failed to push some refs"
→ GitHub repository를 비어있는 상태로 만들었는지 확인 (README 자동 생성 체크 해제)

### APK를 꼭 포함하고 싶은데 Git LFS가 복잡하다면?
→ GitHub Releases 기능을 사용하여 APK를 별도로 업로드할 수 있습니다
