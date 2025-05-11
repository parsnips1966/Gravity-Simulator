import pygame
import time
from classes.togglebutton import ToggleButton


class TextBox(ToggleButton):
    """
    Name: TextBox
    Purpose: A subclass of ToggleButton so it can be clicked to be activated. When activated, it allows users to type
    inside it and the input is then used for a purpose.
    """
    def __init__(self, name: str, dimensions: tuple[int, int], position: tuple[int, int], font: pygame.font.SysFont,
                 font_width: int, contents_type: str, contents: str = ""):
        """
        Name: __init__
        Parameters: name: string, dimension: tuple[int, int], position: tuple[int, int], font: pygame.font.SysFont,
        font_width: integer, contents: string, contents_type: string
        Returns: None
        Purpose: Initialises the super class, passing in the name, dimensions and position of the text box.
        Sets contents to a list of characters from the contents string passed in. The default cursor position is the end
        of the contents. The text and its rect are created and positioned.
        The rect of the text box is created from its position and dimensions
        """
        super().__init__(name, dimensions, position)
        self.__contents: list[str] = [ch for ch in contents]
        self.__cursor_position: int = len(contents)
        self.__position: tuple[int, int] = position
        self.__contents_type: str = contents_type
        self.__text = font.render(contents, True, (0, 0, 0))
        self.__text_rect = self.__text.get_rect()
        self.__text_rect.left = self.__position[0] + 2
        self.__text_rect.top = self.__position[1] + 2
        self.__rect: tuple[int, int, int, int] = (position[0], position[1], dimensions[0], dimensions[1])
        self.__font = font
        self.__font_width: int = font_width

    def draw_text_box(self, surface: pygame.Surface) -> None:
        """
        Name: draw_text_box
        Parameters: surface: pygame.Surface
        Returns: None
        Purpose: Draws the box to the screen and blits the text on top of it. The cursor is displayed every other half
        second.
        """
        pygame.draw.rect(surface, "#FFFFFF", self.__rect)
        surface.blit(self.__text, self.__text_rect)
        if self.get_active() and time.time() % 1 > 0.5:
            cursor = pygame.Rect((self.__text_rect.topright[0] - self.__font_width * (
                    len(self.__contents) - self.__cursor_position), self.__text_rect.topright[1]),
                                 (3, self.__text_rect.height))
            pygame.draw.rect(surface, (0, 0, 0), cursor)

    def key_pressed(self, surface: pygame.Surface, event: pygame.event.Event) -> list[str] | None:
        """
        Name: key_pressed
        Parameters: surface: pygame.Surface, event: pygame.event.Event
        Returns: list[str] | None
        Purpose: Takes in an event which is a key press. Performs an action depending on the key and contents type of
        the text box. Returns contents of the textbox as a list of characters if enter key pressed.
        """

        # If the user presses backspace and the cursor isn't at the start, the character behind the cursor is removed
        # from the contents and the cursor moves back
        if event.key == pygame.K_BACKSPACE:
            if self.__cursor_position > 0:
                del self.__contents[self.__cursor_position - 1]
                self.__cursor_position -= 1
        # if the user presses enter, the text box is deactivated, cursor reset and its contents are returned
        elif event.key == pygame.K_RETURN:
            self.deactivate()
            self.__cursor_position = len(self.__contents)
            return self.__contents
        # if the user presses an arrow key and the cursor is able to move in that direction, it does so
        elif event.key == pygame.K_LEFT:
            if self.__cursor_position > 0:
                self.__cursor_position -= 1
        elif event.key == pygame.K_RIGHT:
            if self.__cursor_position < len(self.__contents):
                self.__cursor_position += 1
        # only certain characters are allowed to be entered into the text box depending on the data type of its contents
        # If an allowed character is entered, it inserts into the contents at the cursor and the cursor increments
        elif len(self.__contents) < 24:
            if self.__contents_type == "float":
                if (event.unicode.isdigit() or event.unicode == "e" or event.unicode == "+" or event.unicode == "-" or
                        event.unicode == "."):
                    self.__contents.insert(self.__cursor_position, event.unicode)
                    self.__cursor_position += 1
            elif self.__contents_type == "str":
                if event.unicode.isalnum() or event.unicode == "-":
                    self.__contents.insert(self.__cursor_position, event.unicode)
                    self.__cursor_position += 1
            elif self.__contents_type == "list":
                if (event.unicode.isdigit() or event.unicode == "," or event.unicode == " " or event.unicode == "e" or
                    event.unicode == "." or event.unicode == "*" or event.unicode == "^" or event.unicode == "-" or
                        event.unicode == "+"):
                    self.__contents.insert(self.__cursor_position, event.unicode)
                    self.__cursor_position += 1
        # text is remade with the new contents and draw to the screen
        self.__text = self.__font.render("".join(self.__contents), True, (0, 0, 0))
        self.__text_rect = self.__text.get_rect()
        self.__text_rect.left = self.__position[0] + 2
        self.__text_rect.top = self.__position[1] + 2
        self.draw_text_box(surface)

    def update_contents(self, text: str) -> None:
        """
        Name: update_contents
        Parameters: text: string
        Returns: None
        Purpose: Resets contents, text objects and cursor position with the new text.
        """
        self.__text = self.__font.render(text, True, (0, 0, 0))
        self.__text_rect = self.__text.get_rect()
        self.__text_rect.left = self.__position[0] + 2
        self.__text_rect.top = self.__position[1] + 2
        self.__contents = [ch for ch in text]
        self.__cursor_position = len(self.__contents)
