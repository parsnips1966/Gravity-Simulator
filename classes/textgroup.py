import pygame
from classes.text import Text


class TextGroup(pygame.sprite.Group):
    """
    Name: TextGroup
    Purpose: Contains all the Text objects on screen and calls their draw functions.
    """
    def __init__(self):
        """
        Name: __init__
        Parameters: -
        Returns: None
        Purpose: Initialises the super class.
        """
        super().__init__()

    def add_texts(self, *texts: Text) -> None:
        """
        Name: add_texts
        Parameters: *texts: Text
        Returns: None
        Purpose: Calls the super class' add function to add the texts to the group. Add not called directly from main as
        it throws an error.
        """
        super().add(*texts)

    def remove_texts(self, *texts: Text) -> None:
        """
        Name: remove_texts
        Parameters: *texts: Text
        Returns: None
        Purpose: Calls the super class' remove function to remove texts from the group. Remove not called directly from
        main as it throws an error.
        """
        super().remove(*texts)

    def draw_texts(self, surface: pygame.Surface) -> None:
        """
        Name: draw_texts
        Parameters: surface: pygame.Surface
        Returns: None
        Purpose: Calls the draw function of each Text object.
        """
        for text in self.sprites():
            text.draw_text(surface)
