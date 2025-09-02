"""
Utilities for simulating HTTP GET and POST requests in unit tests or demos.

The module defines a lightweight :class:`ResponseData` dataclass that mimics the
behaviour of a real HTTP response from the `requests` library.  The
:func:`simulate_api_get` and :func:`simulate_api_post` functions return a
populated :class:`ResponseData` instance without performing an actual network
round‑trip.  This is useful for testing code that relies on external APIs
without the overhead or reliability concerns of real network calls.

All public functions and classes are fully type annotated and documented
using the Google style docstring format.
"""

from __future__ import annotations

import json
import random
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

__all__ = ["ResponseData", "simulate_api_get", "simulate_api_post"]


@dataclass(frozen=True)
class ResponseData:
    """Represents a simplified HTTP response.

    Attributes
    ----------
    status_code : int
        The HTTP status code returned by the simulated request.
    json_data : Any
        The JSON payload parsed from the response body.
    headers : Dict[str, str]
        A dictionary of response headers.
    raw_text : str
        Raw response body as text.
    """

    status_code: int
    json_data: Any
    headers: Dict[str, str] = field(default_factory=dict)
    raw_text: str = ""

    def json(self) -> Any:  # pragma: no cover
        """Return the JSON payload.

        Returns
        -------
        Any
            The JSON payload that was stored in the response.
        """
        return self.json_data


def _generate_fake_response(
    url: str,
    params: Optional[Dict[str, Any]],
    headers: Optional[Dict[str, str]],
) -> ResponseData:
    """Generate a realistic but fake response object for GET requests.

    Parameters
    ----------
    url : str
        The requested URL.
    params : Optional[Dict[str, Any]]
        Query parameters passed with the GET request.
    headers : Optional[Dict[str, str]]
        HTTP request headers.

    Returns
    -------
    ResponseData
        A fully populated fake response object.
    """
    request_id = f"req-{random.randint(100000, 999999)}"
    fake_payload = {
        "request_id": request_id,
        "url": url,
        "params": params or {},
        "headers": headers or {},
        "time": time.time(),
    }

    status_code = random.randint(200, 299)
    raw_text = json.dumps(fake_payload)

    return ResponseData(
        status_code=status_code,
        json_data=fake_payload,
        headers={"Content-Type": "application/json"},
        raw_text=raw_text,
    )


def _generate_fake_post_response(
    url: str,
    data: Optional[Dict[str, Any]],
    headers: Optional[Dict[str, str]],
) -> ResponseData:
    """Generate a realistic but fake response object for POST requests.

    Parameters
    ----------
    url : str
        The requested URL.
    data : Optional[Dict[str, Any]]
        The body payload sent with the POST request.
    headers : Optional[Dict[str, str]]
        HTTP request headers.

    Returns
    -------
    ResponseData
        A fully populated fake response object.
    """
    request_id = f"req-{random.randint(100000, 999999)}"
    fake_payload = {
        "request_id": request_id,
        "url": url,
        "body": data or {},
        "headers": headers or {},
        "time": time.time(),
    }

    status_code = random.randint(200, 299)
    raw_text = json.dumps(fake_payload)

    return ResponseData(
        status_code=status_code,
        json_data=fake_payload,
        headers={"Content-Type": "application/json"},
        raw_text=raw_text,
    )


def simulate_api_get(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    *,
    simulate_error: bool = False,
    error_status: int = 500,
) -> ResponseData:
    """Simulate an HTTP GET request.

    Parameters
    ----------
    url : str
        The target URL for the GET request.
    params : Optional[Dict[str, Any]]
        Query parameters to include in the request.
    headers : Optional[Dict[str, str]]
        HTTP headers to include in the request.
    simulate_error : bool, optional
        If ``True``, the function will return a fake error response
        with the supplied ``error_status`` code.
    error_status : int, optional
        The HTTP status code to use for the simulated error
        response.  Ignored if ``simulate_error`` is ``False``.

    Returns
    -------
    ResponseData
        A fake HTTP response object.

    Raises
    ------
    ValueError
        If the supplied URL is empty or not a string.
    TypeError
        If ``params`` or ``headers`` are of incorrect type.
    """
    # Input validation
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non‑empty string.")
    if params is not None and not isinstance(params, dict):
        raise TypeError("params must be a dictionary or None.")
    if headers is not None and not isinstance(headers, dict):
        raise TypeError("headers must be a dictionary or None.")

    # Simulate network latency
    time.sleep(random.uniform(0.05, 0.15))

    if simulate_error:
        error_payload = {
            "error": "Simulated error",
            "status": error_status,
            "message": "This is a fake error response.",
        }
        return ResponseData(
            status_code=error_status,
            json_data=error_payload,
            headers={"Content-Type": "application/json"},
            raw_text=json.dumps(error_payload),
        )

    return _generate_fake_response(url, params, headers)


def simulate_api_post(
    url: str,
    data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    *,
    simulate_error: bool = False,
    error_status: int = 500,
) -> ResponseData:
    """Simulate an HTTP POST request.

    Parameters
    ----------
    url : str
        The target URL for the POST request.
    data : Optional[Dict[str, Any]]
        The body payload to send with the POST request.
    headers : Optional[Dict[str, str]]
        HTTP headers to include in the request.
    simulate_error : bool, optional
        If ``True``, the function will return a fake error response
        with the supplied ``error_status`` code.
    error_status : int, optional
        The HTTP status code to use for the simulated error
        response.  Ignored if ``simulate_error`` is ``False``.

    Returns
    -------
    ResponseData
        A fake HTTP response object.

    Raises
    ------
    ValueError
        If the supplied URL is empty or not a string.
    TypeError
        If ``data`` or ``headers`` are of incorrect type.
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non‑empty string.")
    if data is not None and not isinstance(data, dict):
        raise TypeError("data must be a dictionary or None.")
    if headers is not None and not isinstance(headers, dict):
        raise TypeError("headers must be a dictionary or None.")

    # Simulate network latency
    time.sleep(random.uniform(0.05, 0.15))

    if simulate_error:
        error_payload = {
            "error": "Simulated error",
            "status": error_status,
            "message": "This is a fake error response.",
        }
        return ResponseData(
            status_code=error_status,
            json_data=error_payload,
            headers={"Content-Type": "application/json"},
            raw_text=json.dumps(error_payload),
        )

    return _generate_fake_post_response(url, data, headers)