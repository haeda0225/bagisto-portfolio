from __future__ import annotations

import requests

from config.settings import API_BASE_URL, API_TIMEOUT, STOREFRONT_KEY


class BaseClient:
    def __init__(self, token: str | None = None) -> None:
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-STOREFRONT-KEY": STOREFRONT_KEY,
                "X-CHANNEL": "default",
            }
        )
        if token:
            self.set_token(token)

    def set_token(self, token: str) -> None:
        self.session.headers["Authorization"] = f"Bearer {token}"

    def execute(self, query: str, variables: dict | None = None):
        payload = {"query": query, "variables": variables or {}}
        return self.session.post(self.base_url, json=payload, timeout=API_TIMEOUT)
