import pygame


class Rectangle(pygame.sprite.Sprite):
    """
    Name: Rectangle
    Purpose: Represents any rectangles on screen.
    """
    def __init__(self, colour: tuple[int, int, int], rect: tuple[int, int, int, int], width: int = 0) -> None:
        """
        Name: __init__
        Parameters: colour: tuple[int, int, int], rect: tuple[int, int, int, int], width: integer
        Returns: None
        Purpose: Initialises the super class and the variables associated wih the rectangle
        """
        super().__init__()
        self.__colour: tuple[int, int, int] = colour
        self.__rect: tuple[int, int, int, int] = rect
        self.__width: int = width
        
    def draw_self(self, surface: pygame.Surface) -> None:
        """
        Name: draw_self
        Parameters: surface: pygame.Surface
        Returns: None
        Purpose: Draws the rectangle to the screen
        """
        pygame.draw.rect(surface, self.__colour, self.__rect, self.__width)
