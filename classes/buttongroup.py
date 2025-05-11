import pygame
from classes.button import Button
from classes.togglebutton import ToggleButton
from classes.textbutton import TextButton
from classes.textbox import TextBox


class ButtonGroup(pygame.sprite.Group):
    """
    Name: ButtonGroup
    Purpose: Contains similar buttons such as text boxes and allows actions to be performed on all of them
    """
    def __init__(self):
        """
        Name: __init__
        Parameters: -
        Returns: None
        Purpose: Initialises the super class.
        """
        super().__init__()

    def add_buttons(self, *buttons: Button) -> None:
        """
        Name: add_buttons
        Parameters: *buttons: Button
        Returns: None
        Purpose: Calls the super class' add method to add buttons to the group. Add method isn't called directly from
        main as it throws an error.
        """
        super().add(*buttons)

    def remove_buttons(self, *buttons: Button) -> None:
        """
        Name: remove_buttons
        Parameters: *buttons: Button
        Returns: None
        Purpose: Calls the super class' remove method to remove buttons from the group. Remove method isn't called
        directly from main as it throws an error.
        """
        super().remove(*buttons)

    def get_names(self) -> list[str]:
        """
        Name: get_names
        Parameters: -
        Returns: list[str]
        Purpose: Retrieves the name of each button and returns a list of them
        """
        return [button.get_name() for button in self.sprites()]

    def button_clicked(self, position: list[int]) -> str:
        """
        Name: button_clicked
        Parameters: position: list[int]
        Returns: string
        Purpose: Calls each button's click function with the position provided to find if any of them have been clicked.
        If a button has been clicked, its name is returned.
        """
        for button in self.sprites():
            if button.click(position):
                return button.get_name()
        return ""

    def get_activated(self) -> Button | ToggleButton | TextButton | TextBox:
        """
        Name: get_activated
        Parameters: -
        Returns: Button
        Purpose: Calls get_active on all buttons to find if any ToggleButtons are active and returns them if they are
        """
        for button in self.sprites():
            if button.get_active():
                return button

    def deactivate_all(self) -> None:
        """
        Name: deactivate_all
        Parameters: -
        Returns: None
        Purpose: Calls deactivate on all buttons so no ToggleButtons are active
        """
        for button in self.sprites():
            button.deactivate()

    def draw_text_boxes(self, surface: pygame.Surface) -> None:
        """
        Name: draw_text_boxes
        Parameters: surface: pygame.Surface
        Returns: None
        Purpose: Checks if each button is a TextBox and if they are, their draw_text_box method is called
        """
        for button in self.sprites():
            if button.__class__.__name__ == "TextBox":
                button.draw_text_box(surface)
