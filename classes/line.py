import pygame


class Line(pygame.sprite.Sprite):
    """
    Name: Line
    Purpose: Represents any lines on screen.
    """
    def __init__(self, colour: tuple[int, int, int], start_pos: tuple[int, int], end_pos: tuple[int, int], width: int):
        """
        Name: __init__
        Parameters: colour: tuple[int, int, int], start_pos: tuple[int, int], end_pos: tuple[int, int], width: integer
        Returns: None
        Purpose: Initialises super class and variables associated with the line
        """
        super().__init__()
        self.__colour: tuple[int, int, int] = colour
        self.__start_pos: tuple[int, int] = start_pos
        self.__end_pos: tuple[int, int] = end_pos
        self.__width: int = width

    def draw_self(self, surface: pygame.Surface) -> None:
        """
        Name: draw_self
        Parameters: surface: pygame.Surface
        Returns: None
        Purpose: Draws the line to the screen.
        """
        pygame.draw.line(surface, self.__colour, self.__start_pos, self.__end_pos, self.__width)
