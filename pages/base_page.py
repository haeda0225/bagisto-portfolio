class BasePage:
    def __init__(self, page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self, path: str) -> None:
        self.page.goto(f"{self.base_url}{path}")

    def text(self, selector: str) -> str:
        return self.page.locator(selector).text_content().strip()
