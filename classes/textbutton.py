from classes.togglebutton import ToggleButton
from classes.text import Text


class TextButton(ToggleButton):
    """
    Name: TextButton
    Purpose: A subclass of ToggleButton so it activates or deactivates when clicked. A button which contains text and
    has cases for specific buttons to change the text when clicked.
    """
    def __init__(self, name: str, dimensions: tuple[int, int], position: tuple[int, int], font, text: str, colour: tuple
                 ):
        """
        Name: __init__
        Parameters: name: string, dimension: tuple[int, int], position: tuple[int, int], text: Text
        Returns: None
        Purpose: Initialises the super class, passing in the text button's name, dimensions and position.
        Sets the inbuilt image attribute to the image of the text, so it can be drawn automatically by pygame.
        """
        super().__init__(name, dimensions, position)
        self.__text = Text(font, text, colour)
        self.image = self.__text.get_text()

    def set_text(self, text: Text) -> None:
        """
        Name: set_text
        Parameters: text: Text
        Returns: None
        Purpose: Sets the text attribute and sets the inbuilt image attribute to the image of the text.
        """
        self.__text = text
        self.image = text.get_text()

    def toggle_text(self) -> bool:
        """
        Name: toggle_text
        Parameters: -
        Returns: Boolean
        Purpose: If the text is 'More Data' it is changed to 'Less Data' and vice versa, for the toggle_data button
        Returns whether the button is active or not.
        """
        if self.__text.get_text_str() == "More Data":
            self.set_text(Text(self.__text.get_font(), "Less Data", (255, 255, 255)))
        elif self.__text.get_text_str() == "Less Data":
            self.set_text(Text(self.__text.get_font(), "More Data", (255, 255, 255)))
        return self.toggle()
