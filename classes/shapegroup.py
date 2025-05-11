import pygame
from classes.line import Line
from classes.rectangle import Rectangle


class ShapeGroup(pygame.sprite.Group):
    """
    Name: ShapeGroup
    Purpose: Contains all the geometric shapes (lines and rectangles) on screen.
    """
    def __init__(self):
        """
        Name: __init__
        Parameters: -
        Returns: None
        Purpose: Initialises the super class
        """
        super().__init__()

    def add_sprites(self, *sprites: Line | Rectangle) -> None:
        """
        Name: add_sprites
        Parameters: *sprites: Line | Rectangle
        Returns: None
        Purpose: Calls the super class's add method to add shapes to the group. Add method isn't called directly from
        main as it throws an error.
        """
        super().add(*sprites)

    def remove_sprites(self, *sprites) -> None:
        """
        Name: remove_sprites
        Parameters: *sprites: Line or Rectangle
        Returns: None
        Purpose: Calls the super class' remove method to remove shapes from the group. Remove method isn't called
        directly from main as it throws an error.
        """
        super().remove(*sprites)

    def draw_sprites(self, surface: pygame.Surface) -> None:
        """
        Name: draw_sprites
        Parameters: surface: pygame.Surface
        Returns: None
        Purpose: Calls the draw_self method for each shape in the group.
        """
        for shape in self.sprites():
            shape.draw_self(surface)
