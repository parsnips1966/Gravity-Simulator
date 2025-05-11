import pygame
from classes.button import Button


class ToggleButton(Button):
    """
    Name: ToggleButton
    Purpose: Subclass of button which allows buttons to have two states: activated and deactivated. Switches between
    these when clicked
    """
    def __init__(self, name: str, dimensions: tuple[int, int], position: tuple[int, int], image_path: str = ""):
        """
        Name: __init__
        Parameters: name: string, dimension: tuple[int, int], position: tuple[int, int], image_path: string
        Returns: None
        Purpose: Initialises the super class, sets default of deactivated and sets image_path
        """
        super().__init__(name, dimensions, position, image_path)
        self.__active: bool = False
        self.__image_path: str = image_path

    def toggle(self) -> bool:
        """
        Name: toggle
        Parameters: -
        Returns: bool
        Purpose: Changes the image to a pause button if it's a play button and vice versa, for the play_pause button.
        Switches from activated to deactivated or vice versa and returns the state
        """
        if self.__image_path == "play.jpg":
            self.__image_path = "pause.jpg"
            self.image = pygame.transform.scale(pygame.image.load("./images/pause.jpg"), self.rect.size)
        elif self.__image_path == "pause.jpg":
            self.__image_path = "play.jpg"
            self.image = pygame.transform.scale(pygame.image.load("./images/play.jpg"), self.rect.size)
        self.__active = not self.__active
        return self.__active

    def activate(self) -> None:
        """
        Name: activate
        Parameters: -
        Returns: None
        Purpose: set active to True
        """
        self.__active = True

    def deactivate(self) -> None:
        """
        Name: deactivate
        Parameters: -
        Returns: None
        Purpose: set active to False
        """
        self.__active = False

    def get_active(self) -> bool:
        """
        Name: get_active
        Parameters: -
        Returns: bool
        Purpose: active getter
        """
        return self.__active
