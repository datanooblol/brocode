
# greet.py
from typing import Optional


class BaseGreet:
    """Base class for greeting messages.

    Attributes:
        name (Optional[str]): The name to greet. Defaults to ``"James"``.
        message (Optional[str]): The greeting message prefix. Defaults to ``"Hello"``.
    """

    def __init__(self, name: Optional[str] = "James", message: Optional[str] = "Hello") -> None:
        self.name = name
        self.message = message

    def say_hello(self) -> str:
        """Return a greeting string.

        Returns:
            str: A greeting message formatted as ``"{message} {name}!"``.
        """
        return f"{self.message} {self.name}!"


class GreetWorld(BaseGreet):
    """Greeting class that greets the world.

    Args:
        name (Optional[str]): The name to greet. Defaults to ``"James"``.
    """

    def __init__(self, name: Optional[str] = "James") -> None:
        super().__init__(name=name, message="Hello World")


class GreetEarth(BaseGreet):
    """Greeting class that greets the earth.

    Args:
        name (Optional[str]): The name to greet. Defaults to ``"James"``.
    """

    def __init__(self, name: Optional[str] = "James") -> None:
        super().__init__(name=name, message="Hello Earth")
