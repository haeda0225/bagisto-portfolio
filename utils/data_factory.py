from datetime import datetime


def unique_email(prefix: str = "qa") -> str:
    return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
