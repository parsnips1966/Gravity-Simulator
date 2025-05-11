import pygame
from classes.bodygroup import BodyGroup
from classes.buttongroup import ButtonGroup
from classes.textbutton import TextButton
from classes.textgroup import TextGroup
from classes.shapegroup import ShapeGroup


def evolve_system(bodies: BodyGroup) -> None:
    """
    Name: evolve_system
    Parameters: bodies: BodyGroup
    Returns: None
    Purpose: Calls the bodies methods in the order which carries out the Euler-Richardson leapfrog integration method.
    Passes in True on the second update_velocities method as each one updates the velocity half-way and only one needs
    to be saved. Calls increment_time to record that the system has evolved over some time.
    """
    bodies.update_positions()
    bodies.update_velocities()
    bodies.reset_accelerations()
    bodies.update_accelerations()
    bodies.update_velocities(True)
    bodies.increment_time()


def draw_screen(screen: pygame.Surface, clock: pygame.time.Clock, bodies: BodyGroup, buttons: ButtonGroup,
                text_box_buttons: ButtonGroup, texts: TextGroup, shapes: ShapeGroup) -> None:
    """
    Name: draw_screen
    Parameters: screen: pygame.Surface, clock: pygame.time.Clock, bodies: BodyGroup, buttons: ButtonGroup,
    text_box_buttons: ButtonGroup, texts: TextGroup, shapes: ShapeGroup
    Returns: None
    Purpose: Resets the screen to black draws the objects which have been passed in, in the right order so that the
    correct ones are on top. Calls clock.tick so the simulation is capped at 128 fps.
    """
    screen.fill((0, 0, 0))
    bodies.draw_bodies(screen)
    shapes.draw_sprites(screen)
    texts.draw_texts(screen)
    buttons.draw(screen)
    text_box_buttons.draw_text_boxes(screen)
    pygame.display.update()
    clock.tick(2 ** 7)


def create_body_buttons(bodies: BodyGroup, font: pygame.font.SysFont) -> ButtonGroup:
    """
    Name: create_body_buttons
    Parameters: bodies: BodyGroup, font: pygame.font.SysFont
    Returns: ButtonGroup
    Purpose: Creates a text button for each body passed in which are added to a button group and returned.
    """
    body_buttons = ButtonGroup()
    for i in range(len(bodies.sprites())):
        body_buttons.add_buttons(TextButton(bodies.sprites()[i].get_name(), (100, 20),
                                            (410 + i % 4 * 100, 100 + 30 * (i // 4)),
                                            font, bodies.sprites()[i].get_name(), bodies.sprites()[i].get_colour()))
    return body_buttons
