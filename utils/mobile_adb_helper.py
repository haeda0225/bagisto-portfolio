from __future__ import annotations

import re
import subprocess
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path


class MobileAdbHelper:
    def __init__(self, adb_path: str, device_id: str) -> None:
        self.adb_path = adb_path
        self.device_id = device_id

    def _run(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(
            [self.adb_path, "-s", self.device_id, *args],
            check=check,
            capture_output=True,
            text=True,
        )

    def force_stop(self, package_name: str) -> None:
        self._run("shell", "am", "force-stop", package_name, check=False)

    def clear_app_data(self, package_name: str) -> None:
        self._run("shell", "pm", "clear", package_name)
        time.sleep(2)

    def start_app(self, package_name: str, activity_name: str) -> None:
        self._run("shell", "am", "start", "-n", f"{package_name}/{activity_name}")
        time.sleep(4)

    def back(self) -> None:
        self._run("shell", "input", "keyevent", "4")
        time.sleep(2)

    def tap(self, x: int, y: int) -> None:
        self._run("shell", "input", "tap", str(x), str(y))
        time.sleep(2)

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration_ms: int = 300) -> None:
        self._run(
            "shell",
            "input",
            "swipe",
            str(start_x),
            str(start_y),
            str(end_x),
            str(end_y),
            str(duration_ms),
        )
        time.sleep(2)

    def dump_ui(self) -> ET.Element:
        remote_path = "/sdcard/window_dump.xml"
        last_exc = None
        for _ in range(4):
            try:
                self._run("shell", "uiautomator", "dump", remote_path)
                with tempfile.TemporaryDirectory() as temp_dir:
                    local_path = Path(temp_dir) / "window_dump.xml"
                    self._run("pull", remote_path, str(local_path))
                    return ET.fromstring(local_path.read_text(encoding="utf-8"))
            except Exception as exc:
                last_exc = exc
                time.sleep(2)
        raise AssertionError(f"Failed to dump UI hierarchy: {last_exc}")

    def all_content_descs(self) -> list[str]:
        root = self.dump_ui()
        return [
            node.attrib["content-desc"]
            for node in root.iter()
            if node.attrib.get("content-desc")
        ]

    def find_bounds_by_desc(self, text: str, contains: bool = False) -> tuple[int, int, int, int]:
        root = self.dump_ui()
        available_descs = []
        for node in root.iter():
            desc = node.attrib.get("content-desc", "")
            if not desc:
                continue
            available_descs.append(desc)
            if (contains and text in desc) or (not contains and desc == text):
                return self._parse_bounds(node.attrib["bounds"])

        error_msg = f"Could not find content-desc: '{text}'"
        if contains:
            error_msg += " (partial match)"
        error_msg += f"\nAvailable content-desc values ({len(available_descs)} total):\n"
        error_msg += "\n".join(f"  - {d[:100]}" for d in available_descs[:10])
        if len(available_descs) > 10:
            error_msg += f"\n  ... and {len(available_descs) - 10} more"
        raise AssertionError(error_msg)

    def tap_desc(self, text: str, contains: bool = False) -> None:
        left, top, right, bottom = self.find_bounds_by_desc(text, contains=contains)
        self.tap((left + right) // 2, (top + bottom) // 2)

    def find_bounds_by_resource_id(self, resource_id: str) -> tuple[int, int, int, int]:
        root = self.dump_ui()
        available_ids = []
        for node in root.iter():
            rid = node.attrib.get("resource-id", "")
            if rid:
                available_ids.append(rid)
            if rid == resource_id:
                return self._parse_bounds(node.attrib["bounds"])

        error_msg = f"Could not find resource-id: '{resource_id}'"
        error_msg += f"\nAvailable resource-id values ({len(available_ids)} total):\n"
        error_msg += "\n".join(f"  - {rid}" for rid in sorted(set(available_ids))[:15])
        if len(set(available_ids)) > 15:
            error_msg += f"\n  ... and {len(set(available_ids)) - 15} more unique IDs"
        raise AssertionError(error_msg)

    def tap_resource_id(self, resource_id: str) -> None:
        left, top, right, bottom = self.find_bounds_by_resource_id(resource_id)
        self.tap((left + right) // 2, (top + bottom) // 2)

    def input_text(self, text: str) -> None:
        sanitized = text.replace(" ", "%s")
        self._run("shell", "input", "text", sanitized)
        time.sleep(1)

    def fill_resource_id(self, resource_id: str, text: str) -> None:
        self.tap_resource_id(resource_id)
        self.input_text(text)

    def wait_for_desc(self, text: str, contains: bool = False, timeout: int = 20) -> None:
        end = time.time() + timeout
        while time.time() < end:
            try:
                self.find_bounds_by_desc(text, contains=contains)
                return
            except AssertionError:
                time.sleep(1)
        raise AssertionError(f"Timed out waiting for content-desc: {text}")

    def ensure_home_loaded(self, timeout: int = 30) -> None:
        end = time.time() + timeout
        while time.time() < end:
            descs = self.all_content_descs()
            if "Featured Products" in descs:
                return

            if any(desc == "Home" or desc.endswith("\nHome") for desc in descs):
                try:
                    self.tap_desc("Home", contains=True)
                except AssertionError:
                    pass

            time.sleep(1)

        raise AssertionError("Timed out waiting for the mobile home screen to load.")

    @staticmethod
    def _parse_bounds(bounds: str) -> tuple[int, int, int, int]:
        nums = [int(n) for n in re.findall(r"\d+", bounds)]
        return nums[0], nums[1], nums[2], nums[3]
