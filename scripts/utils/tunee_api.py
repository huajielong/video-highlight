"""
Tunee API utilities for video-highlight skill
Copied and adapted from free-music-generator
"""

import os
import sys
from dataclasses import dataclass
from enum import IntEnum
import requests

API_BASE = "https://open.tunee.ai"
API_GENERATE = f"{API_BASE}/open-apis/v1/music/gen"
API_MODELS = f"{API_BASE}/open-apis/v1/models"
API_CREDITS = f"{API_BASE}/open-apis/v1/credits"

CACHE_FILE = os.path.join(os.path.expanduser("~"), ".tunee", "models.json")
TTL_SECONDS = 86400  # 24 hours

SUPPORTED_MUSIC_TYPE = ("Text-to-Music",)
BIZ_TYPE_INSTRUMENTAL = "Instrumental"


def _raw_message(raw: dict) -> str | None:
    """parser msg"""
    return raw.get("msg")


@dataclass
class TuneeErrorResponse:
    """Structured representation of a Tunee API error response."""
    message: str
    status: int
    request_id: str | None


@dataclass
class TuneeResponse:
    """Tunee API unified response; business data in the data field."""
    status: int
    message: str
    request_id: str | None
    data: dict
    raw: dict

    @classmethod
    def from_json(cls, raw: dict) -> "TuneeResponse":
        """Parse raw JSON into a unified response."""
        return cls(
            status=raw.get("status", 0),
            message=_raw_message(raw) or "ok",
            request_id=raw.get("request_id"),
            data=raw.get("data") or {},
            raw=raw,
        )


class TuneeStatus(IntEnum):
    """Tunee API business status codes."""
    SUCCESS = 200000

    @classmethod
    def is_success(cls, code: int) -> bool:
        """Whether the code indicates success."""
        return code == cls.SUCCESS


class TuneeAPIError(Exception):
    """Tunee API call failed."""
    def __init__(self, http_status: int, error: TuneeErrorResponse):
        self.http_status = http_status
        self.error = error
        super().__init__(f"[{http_status}] {error.message} (status={error.status})")


def parse_tunee_error(status_code: int, data: dict) -> TuneeErrorResponse | None:
    """Parse Tunee error response."""
    if status_code != 200:
        return TuneeErrorResponse(
            message=_raw_message(data) or str(data) or f"HTTP {status_code}",
            status=data.get("status", status_code),
            request_id=data.get("request_id"),
        )
    if not TuneeStatus.is_success(data.get("status")):
        return TuneeErrorResponse(
            message=_raw_message(data) or str(data) or "Unknown error",
            status=data.get("status", -1),
            request_id=data.get("request_id"),
        )
    return None


def format_tunee_error(e: TuneeAPIError) -> str:
    """Format error for user feedback."""
    lines = [
        f"HTTP status: {e.http_status}",
        f"Business status: {e.error.status}",
        f"Message: {e.error.message}",
    ]
    if e.error.request_id:
        lines.append(f"request_id: {e.error.request_id}")
    return "\n".join(lines)


def request_tunee_api(url: str, access_key: str, json_payload: dict, timeout: int = 30) -> TuneeResponse:
    """POST request to Tunee API."""
    headers = {
        "Authorization": f"Bearer {access_key}",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, json=json_payload, headers=headers, timeout=timeout)
    raw = resp.json() if resp.content else {}
    err = parse_tunee_error(resp.status_code, raw)
    if err is not None:
        raise TuneeAPIError(resp.status_code, err)
    return TuneeResponse.from_json(raw)


def fetch_models(access_key: str) -> dict:
    """Fetch available models from Tunee API."""
    return request_tunee_api(API_MODELS, access_key, {"modelTypeList": ["music"]}, timeout=30).raw


def resolve_access_key(cli_key: str | None) -> str:
    """Resolve API Key: CLI argument > TUNEE_API_KEY env var."""
    for key in (cli_key, os.environ.get("TUNEE_API_KEY")):
        if key and key.strip() and key != "your-access-key-here":
            return key.strip()
    raise ValueError("No API Key detected. Set TUNEE_API_KEY or pass --api-key")


def check_credits(access_key: str) -> dict:
    """Check remaining credits."""
    return request_tunee_api(API_CREDITS, access_key, {}, timeout=30).data
