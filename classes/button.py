import pygame


class Button(pygame.sprite.Sprite):
    """
    Name: Button
    Purpose: Represents a button that detects if the user clicks on it
    """
    def __init__(self, name: str, dimensions: tuple[int, int], position: tuple[int, int], image: str = ""):
        """
        Name: __init__
        Parameters: name: string, dimensions: tuple[int, int], position: tuple[int, int], image: string
        Returns: None
        Purpose: Initialises the super class and variables relating to the button. If a file path is provided in the
        image parameter, the image at that location is saved to the image attribute.
        The button hit-box is created from the position and dimensions.
        """
        super().__init__()
        self.__name: str = name
        self.__dimensions: tuple[int, int] = dimensions
        self.__position: tuple[int, int] = position
        if image:
            self.image = pygame.transform.scale(pygame.image.load("images/" + image), dimensions)
        self.rect = pygame.Rect(position[0], position[1], dimensions[0], dimensions[1])

    def set_name(self, name: str) -> None:
        """
        Name: set_name
        Parameters: name: str
        Returns: None
        Purpose: name setter
        """
        self.__name = name

    def get_rect(self) -> pygame.Rect:
        """
        Name: get_rect
        Parameters: -
        Returns: pygame.Rect
        Purpose: rect getter
        """
        return self.rect

    def get_name(self) -> str:
        """
        Name: get_name
        Parameters: -
        Returns: str
        Purpose: name getter
        """
        return self.__name

    def click(self, position: tuple) -> str:
        """
        Name: click
        Parameters: position: tuple
        Returns: string
        Purpose: Detects if the button has been clicked and returns its name if it has.
        """
        if self.rect.collidepoint(position):
            return self.__name
        return ""

    def set_position(self, value: tuple) -> None:
        """
        Name: set_position
        Parameters: value: tuple
        Returns: None
        Purpose: Sets position to the value provided and recalculates the hit-box
        """
        self.__position = value
        self.rect = pygame.Rect(value[0], value[1], self.__dimensions[0], self.__dimensions[1])
