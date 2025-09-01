import time
import random
from typing import Any, Dict, Optional


def mock_api(endpoint: str, *, delay: float = 0.1) -> Dict[str, Any]:
    """
    Simulates an HTTP API call.

    This function is useful for unit tests or demonstrations where a real
    network request would be unnecessary or undesirable. It mimics a
    typical JSON‑style response, optionally delaying to emulate network
    latency.

    Args:
        endpoint: The API endpoint to be requested.  Only a handful of
            pre‑defined endpoints are recognised; any other value will
            raise a :class:`ValueError`.
        delay: Optional number of seconds to pause before returning the
            result.  Defaults to ``0.1`` seconds.

    Returns:
        A dictionary containing a ``status`` key with the HTTP status
        code and a ``data`` key with the payload.

    Raises:
        ValueError: If *endpoint* is not one of the supported values.

    Example:
        >>> mock_api("/users")
        {'status': 200, 'data': [{'id': 1, 'name': 'Alice'}, ...]}

    Notes:
        - The function deliberately does **not** perform any I/O.
        - The returned data is randomly generated for realism.
    """
    # Simulate network latency
    time.sleep(delay)

    # Define a small set of supported endpoints
    supported_endpoints = {"/users", "/posts", "/comments"}

    if endpoint not in supported_endpoints:
        raise ValueError(f"Unsupported endpoint: {endpoint!r}")

    # Generate fake data based on the endpoint
    if endpoint == "/users":
        payload = [
            {"id": i, "name": f"User{i}", "email": f"user{i}@example.com"}
            for i in range(1, random.randint(3, 6))
        ]
    elif endpoint == "/posts":
        payload = [
            {
                "id": i,
                "title": f"Post {i}",
                "body": f"This is the body of post {i}.",
                "userId": random.randint(1, 5),
            }
            for i in range(1, random.randint(3, 6))
        ]
    else:  # "/comments"
        payload = [
            {
                "id": i,
                "postId": random.randint(1, 5),
                "name": f"Commenter {i}",
                "email": f"commenter{i}@example.com",
                "body": f"Comment body {i}.",
            }
            for i in range(1, random.randint(3, 6))
        ]

    return {"status": 200, "data": payload}