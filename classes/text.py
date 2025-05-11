import pygame


class Text(pygame.sprite.Sprite):
    """
    Name: Text
    Purpose: Represents any text displayed on screen including that inside buttons.
    Text can be changed, and it draws itself to the screen.
    """
    def __init__(self, font: pygame.font.SysFont, text: str, colour: tuple[int, ...],
                 position: tuple[int, int] = (0, 0), outline: bool = False):
        """
        Name: __init__
        Parameters: font: pygame.font.SysFont, text: str, colour: tuple[int, ...], position: tuple[int, int],
        outline: bool
        Returns: None
        Purpose: Initialises the super class and all the attributes of the text to the values passed in.
        Creates a pygame text object and its rect.
        """
        super().__init__()
        self.__font = font
        self.__colour: tuple[int, ...] = colour
        self.__position: tuple[int, int] = position
        self.__text_str: str = text
        self.__text = font.render(text, True, colour)
        self.__text_rect = self.__text.get_rect()
        self.__text_rect.topleft = self.__position
        self.__outline: bool = outline
        if outline:
            self.__outline_text = font.render(text, True, (0, 0, 0))
            self.__outline1_rect = self.__outline_text.get_rect()
            self.__outline1_rect.topleft = (self.__position[0] + 2, self.__position[1])
            self.__outline2_rect = self.__outline_text.get_rect()
            self.__outline2_rect.topleft = (self.__position[0] - 2, self.__position[1])
            self.__outline3_rect = self.__outline_text.get_rect()
            self.__outline3_rect.topleft = (self.__position[0], self.__position[1] + 2)
            self.__outline4_rect = self.__outline_text.get_rect()
            self.__outline4_rect.topleft = (self.__position[0], self.__position[1] - 2)

    def get_text_str(self) -> str:
        """
        Name: get_text_str
        Parameters: -
        Returns: str
        Purpose: text_str getter
        """
        return self.__text_str

    def get_text(self) -> pygame.surface.Surface:
        """
        Name: get_text
        Parameters: -
        Returns: -
        Purpose: text getter
        """
        return self.__text

    def get_font(self) -> pygame.font.SysFont:
        """
        Name: get_font
        Parameters: -
        Returns: pygame.font.SysFont
        Purpose: font getter
        """
        return self.__font

    def update_text(self, text: str) -> None:
        """
        Name: update_text
        Parameters: text: string
        Returns: None
        Purpose: Creates a new pygame text object with the passed in text.
        Creates its rect and sets it to the correct position.
        """
        self.__text = self.__font.render(text, True, self.__colour)
        self.__text_rect = self.__text.get_rect()
        self.__text_rect.topleft = self.__position
        if self.__outline:
            self.__outline_text = self.__font.render(self.__text_str, True, (0, 0, 0))
            self.__outline1_rect = self.__outline_text.get_rect()
            self.__outline1_rect.topleft = (self.__position[0] + 2, self.__position[1])
            self.__outline2_rect = self.__outline_text.get_rect()
            self.__outline2_rect.topleft = (self.__position[0] - 2, self.__position[1])
            self.__outline3_rect = self.__outline_text.get_rect()
            self.__outline3_rect.topleft = (self.__position[0], self.__position[1] + 2)
            self.__outline4_rect = self.__outline_text.get_rect()
            self.__outline4_rect.topleft = (self.__position[0], self.__position[1] - 2)

    def draw_text(self, surface: pygame.Surface) -> None:
        """
        Name: draw_text
        Parameters: surface: pygame.Surface
        Returns: None
        Purpose: Blits the text to the screen
        """
        if self.__outline:
            surface.blit(self.__outline_text, self.__outline1_rect)
            surface.blit(self.__outline_text, self.__outline2_rect)
            surface.blit(self.__outline_text, self.__outline3_rect)
            surface.blit(self.__outline_text, self.__outline4_rect)
        surface.blit(self.__text, self.__text_rect)
