from typing import Optional

class BaseBye:
    """This is a base class"""
    def __init__(self, name:Optional[str]="James", message:Optional[str]="Base") -> None:
        self.name = name
        self.message = message
    def say_bye(self)->str:
        """This is a function to say bye to a person
        
        Return:
            str : a bye message
        """
        return "Bye {message}: {name}!".format(message=self.message, name=self.name)

class ByeWorld(BaseBye):
    """This is a class for saying good bye
    Args:
        name (str) : a name to say good bye to, default is James
    """
    def __init__(self, name:Optional[str]="James") -> None:
        super().__init__(name=name, message="World")
    
class ByeEarth(BaseBye):
    """This is a class for saying good bye to earth
    Args:
        name (str) : a name to say good bye to, default is James
    """
    def __init__(self, name:Optional[str]="James") -> None:
        super().__init__(name=name, message="Earth")