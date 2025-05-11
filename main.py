import sys
import os
import pygame
import json
import time
from classes.body import Body
from classes.bodygroup import BodyGroup
from classes.button import Button
from classes.buttongroup import ButtonGroup
from classes.line import Line
from classes.rectangle import Rectangle
from classes.shapegroup import ShapeGroup
from classes.text import Text
from classes.textbox import TextBox
from classes.textbutton import TextButton
from classes.textgroup import TextGroup
from classes.togglebutton import ToggleButton
from functions import evolve_system, draw_screen, create_body_buttons


def main() -> None:
    """
    Name: main
    Parameters: -
    Returns: None
    Purpose: Initialises the required modules and creates the pygame window and clock to control the speed.
    Initialises all the variables which are needed to control the system and display.
    Runs an infinite loop to detect user inputs and respond accordingly
    Adds or removes sprites from groups so the necessary ones will be on screen
    Calls display_screen function, and evolve_system and calculate_data if the simulation is running
    """
    pygame.display.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    franklingothicmedium_32 = pygame.font.SysFont("franklingothicmedium", 32)
    franklingothicmedium_20 = pygame.font.SysFont("franklingothicmedium", 20)
    consolas = pygame.font.SysFont("consolas", 22)

    # initialising variables concerned with the entire system
    path: str = ""
    contents_list: list[str]
    contents: str
    name: str
    bodies = BodyGroup()
    buttons = ButtonGroup()
    body_buttons = ButtonGroup()
    text_box_buttons = ButtonGroup()
    edit_window_buttons = ButtonGroup()
    edit_window_texts = TextGroup()
    texts = TextGroup()
    projects_texts = TextGroup()
    shapes = ShapeGroup()
    run: bool = True
    dragging: bool = False
    saved: bool = True
    active_body = Body("", 0, 0, [], [], [])
    new_bodies: int = 0
    mouse_pos: tuple
    initial_mouse_pos: tuple[int, int] = (0, 0)
    initial_shift: tuple = (400, 400)
    collided_bodies: list[Body]

    # creates all the text that will ever be displayed on the screen
    time_text = Text(franklingothicmedium_32, "Time: 0s", WHITE, (520, 720))
    years_text = Text(franklingothicmedium_32, "Earth years: 0.0", WHITE, (520, 750))
    scale_text = Text(franklingothicmedium_20, "50px : {:.2e}m".format(10 ** 9 / 0.026), WHITE, (572, 5))
    timestep_text = Text(franklingothicmedium_20, "Timestep: {}s".format(2 ** 16), WHITE, (10, 710))
    name_text = Text(franklingothicmedium_20, "Name", WHITE, (450, 185))
    mass_text = Text(franklingothicmedium_20, "Mass", WHITE, (450, 245))
    position_text = Text(franklingothicmedium_20, "Position", WHITE, (450, 305))
    velocity_text = Text(franklingothicmedium_20, "Velocity", WHITE, (450, 365))
    speed_text = Text(franklingothicmedium_20, "Speed", WHITE, (450, 425))
    radius_text = Text(franklingothicmedium_20, "Radius", WHITE, (450, 485))
    colour_text = Text(franklingothicmedium_20, "Colour", WHITE, (450, 545))
    mass_text_2 = Text(franklingothicmedium_20, "Mass (kg)", WHITE, (420, 190))
    mass_value_2 = Text(consolas, "", WHITE, (610, 192))
    kinetic_energy_text = Text(franklingothicmedium_20, "Kinetic energy (J)", WHITE, (420, 220))
    kinetic_energy_value = Text(consolas, "", WHITE, (610, 223))
    potential_energy_text = Text(franklingothicmedium_20, "Potential energy (J)", WHITE, (420, 250))
    potential_energy_value = Text(consolas, "", WHITE, (610, 253))
    angular_momentum_text = Text(franklingothicmedium_20, "Angular momentum", WHITE, (420, 280))
    angular_momentum_value = Text(consolas, "", WHITE, (610, 298))
    angular_momentum_units = Text(franklingothicmedium_20, "(kg.m\u00b2/s)", WHITE, (420, 310))
    apocentre_text = Text(franklingothicmedium_20, "Apocentre (m)", WHITE, (420, 340))
    apocentre_value = Text(consolas, "", WHITE, (610, 343))
    pericentre_text = Text(franklingothicmedium_20, "Pericentre (m)", WHITE, (420, 370))
    pericentre_value = Text(consolas, "", WHITE, (610, 373))
    semi_major_axis_text = Text(franklingothicmedium_20, "Semi-major axis (m)", WHITE, (420, 400))
    semi_major_axis_value = Text(consolas, "", WHITE, (610, 403))
    semi_minor_axis_text = Text(franklingothicmedium_20, "Semi-minor axis (m)", WHITE, (420, 430))
    semi_minor_axis_value = Text(consolas, "", WHITE, (610, 433))
    eccentricity_text = Text(franklingothicmedium_20, "Eccentricity (None)", WHITE, (420, 460))
    eccentricity_value = Text(consolas, "", WHITE, (610, 463))
    period_text = Text(franklingothicmedium_20, "Period (m)", WHITE, (420, 490))
    period_value = Text(consolas, "", WHITE, (610, 493))
    max_rate_of_area_text = Text(franklingothicmedium_20, "Max rate of area", WHITE, (420, 520))
    max_rate_of_area_units = Text(franklingothicmedium_20, "swept out (m\u00b2/s)", WHITE, (420, 550))
    max_rate_of_area_value = Text(consolas, "", WHITE, (610, 538))
    min_rate_of_area_text = Text(franklingothicmedium_20, "Min rate of area", WHITE, (420, 580))
    min_rate_of_area_units = Text(franklingothicmedium_20, "swept out (m\u00b2/s)", WHITE, (420, 610))
    min_rate_of_area_value = Text(consolas, "", WHITE, (610, 598))
    force_text = Text(franklingothicmedium_20, "Force (N)", WHITE, (420, 640))
    force_value = Text(consolas, "", WHITE, (610, 643))
    whole_system_text = Text(franklingothicmedium_32, "Whole system data", WHITE, (420, 320))
    x_momentum_text = Text(franklingothicmedium_20, "X momentum(kgm/s)", WHITE, (420, 360))
    x_momentum_value = Text(consolas, "", WHITE, (610, 360))
    y_momentum_text = Text(franklingothicmedium_20, "Y momentum(kgm/s)", WHITE, (420, 390))
    y_momentum_value = Text(consolas, "", WHITE, (610, 390))
    total_kinetic_energy_text = Text(franklingothicmedium_20, "Kinetic energy (J)", WHITE, (420, 420))
    total_kinetic_energy_value = Text(consolas, "", WHITE, (610, 420))
    total_potential_energy_text = Text(franklingothicmedium_20, "Potential energy (J)", WHITE, (420, 450))
    total_potential_energy_value = Text(consolas, "", WHITE, (610, 450))
    total_energy_text = Text(franklingothicmedium_20, "Total energy (J)", WHITE, (420, 480))
    total_energy_value = Text(consolas, "", WHITE, (610, 480))
    big_g_text = Text(franklingothicmedium_20, "Gravitational constant", WHITE, (450, 700))
    saved_text = Text(franklingothicmedium_32, "Saved", WHITE, (357, 420), outline=True)
    check_saved_text = Text(franklingothicmedium_32, "Don't forget to save", WHITE, (270, 300), outline=True)
    project_name_text = Text(franklingothicmedium_20, "Choose a name for your project", WHITE, (260, 270), outline=True)
    open_project_text = Text(franklingothicmedium_20, "Type a project name from the list below", WHITE, (242, 270),
                             outline=True)
    doesnt_exist_text = Text(franklingothicmedium_32, "That project doesn't exist", WHITE, (240, 230), outline=True)
    value_error_text = Text(franklingothicmedium_20, "ValueError: Please enter the value", WHITE,
                            (10, 300), outline=True)
    value_error_text2 = Text(franklingothicmedium_20, "in the correct format.", WHITE, (10, 330), outline=True)
    index_error_text = Text(franklingothicmedium_20, "IndexError: Please enter the correct number", WHITE,
                            (10, 300), outline=True)
    index_error_text2 = Text(franklingothicmedium_20, "of values, separated by commas.", WHITE, (10, 330), outline=True)
    colour_error_text = Text(franklingothicmedium_20, "Colour argument error: Please enter three integer", WHITE,
                             (10, 300), outline=True)
    colour_error_text2 = Text(franklingothicmedium_20, "values between 0 and 255 separated by commas", WHITE, (10, 330),
                              outline=True)

    # adds the ones which are initially on screen
    texts.add_texts(time_text, years_text, scale_text, timestep_text)

    # creates all the geometric shapes which will be displayed on screen
    scale_line = Line(WHITE, (630, 30), (680, 30), 2)
    scale_line_left_edge = Line(WHITE, (630, 27), (630, 33), 1)
    scale_line_right_edge = Line(WHITE, (680, 27), (680, 33), 1)
    edit_window_outline = Rectangle(WHITE, (400, 60, 400, 760))
    edit_window = Rectangle(BLACK, (402, 62, 396, 756))
    shapes.add_sprites(scale_line, scale_line_left_edge, scale_line_right_edge)

    # creates all the buttons which will be displayed with their respective images, texts or contents
    fast_back_button = ToggleButton("fast_back", (50, 50), (10, 740), "fastback.png")
    play_pause_button = ToggleButton("play_pause", (50, 50), (70, 740), "play.jpg")
    fast_forward_button = ToggleButton("fast_forward", (50, 50), (130, 740), "fastforward.png")
    plus_button = Button("plus", (40, 40), (520, 10), "plus.png")
    minus_button = Button("minus", (40, 40), (750, 10), "minus.png")
    edit_button = ToggleButton("edit", (50, 50), (740, 375), "edit.png")
    bodies_button = TextButton("bodies", (100, 30), (450, 60), franklingothicmedium_32, "Bodies", WHITE)
    system_button = TextButton("system", (100, 30), (650, 60), franklingothicmedium_32, "System", WHITE)
    add_new_image_button = Button("add_new_image", (40, 40), (450, 730), "plus.png")
    add_new_text_button = TextButton("add_new_text", (100, 40), (500, 738), franklingothicmedium_20, "Add body", WHITE)
    delete_image_button = Button("delete", (40, 40), (600, 730), "bin.png")
    delete_text_button = TextButton("delete", (40, 40), (650, 738), franklingothicmedium_20, "Delete body", WHITE)
    name_box = TextBox("name_box", (300, 28), (450, 210), consolas, 12, contents_type="str")
    mass_box = TextBox("mass_box", (300, 28), (450, 270), consolas, 12, contents_type="float")
    position_box = TextBox("position_box", (300, 28), (450, 330), consolas, 12, contents_type="list")
    velocity_box = TextBox("velocity_box", (300, 28), (450, 390), consolas, 12, contents_type="list")
    speed_box = TextBox("speed_box", (300, 28), (450, 450), consolas, 12, contents_type="float")
    radius_box = TextBox("radius_box", (300, 28), (450, 510), consolas, 12, contents_type="float")
    colour_box = TextBox("colour_box", (300, 28), (450, 570), consolas, 12, contents_type="list")
    central_body_button = TextButton("central_body", (150, 30), (450, 620), franklingothicmedium_20, "Central body",
                                     WHITE)
    central_body_checkbox_button = Button("central_body_checkbox", (40, 40), (710, 610), "checkbox.png")
    central_body_tick = Button("central_body_tick", (30, 30), (715, 615), "tick.png")
    toggle_data_button = TextButton("toggle_data", (150, 30), (520, 670), franklingothicmedium_32, "More Data", WHITE)
    force_arrows_button = TextButton("force_arrows", (150, 30), (450, 130), franklingothicmedium_20,
                                     "Show force arrows", WHITE)
    force_arrows_checkbox_button = Button("force_arrows_checkbox", (40, 40), (640, 130), "checkbox.png")
    force_arrows_tick = Button("force_arrows_tick", (30, 30), (645, 135), "tick.png")
    velocity_arrows_button = TextButton("velocity_arrows", (150, 30), (450, 190), franklingothicmedium_20,
                                        "Show velocity arrows", WHITE)
    velocity_arrows_checkbox_button = Button("velocity_arrows_checkbox", (40, 40), (640, 190), "checkbox.png")
    velocity_arrows_tick = Button("velocity_arrows_tick", (30, 30), (645, 195), "tick.png")
    com_button = TextButton("com", (150, 30), (450, 250), franklingothicmedium_20, "Show centre of mass", WHITE)
    com_checkbox_button = Button("com_checkbox", (40, 40), (640, 250), "checkbox.png")
    com_tick = Button("com_tick", (30, 30), (645, 255), "tick.png")
    big_g_box = TextBox("big_g_box", (300, 28), (450, 730), consolas, 12, contents=str(6.674e-11), contents_type="float"
                        )
    hamburger_button = ToggleButton("hamburger", (50, 50), (10, 10), "hamburger.jpg")
    new_button = Button("new", (50, 50), (10, 70), "new.png")
    open_button = Button("open", (50, 50), (10, 130), "open.png")
    save_button = Button("save", (50, 50), (10, 190), "save.png")
    save_path_box = TextBox("save_path_box", (200, 30), (300, 300), consolas, 12, contents_type="str")
    open_path_box = TextBox("open_path_box", (200, 30), (300, 300), consolas, 12, contents_type="str")

    # adds the buttons initially on screen to the buttons group
    buttons.add_buttons(fast_back_button, play_pause_button, fast_forward_button, plus_button, minus_button,
                        edit_button, hamburger_button)
    # adds the buttons in the edit window to the edit_window_buttons group
    edit_window_buttons.add_buttons(bodies_button, system_button, add_new_image_button, add_new_text_button,
                                    central_body_button, central_body_checkbox_button, central_body_tick,
                                    delete_image_button, delete_text_button, toggle_data_button, force_arrows_button,
                                    force_arrows_checkbox_button, force_arrows_tick, velocity_arrows_checkbox_button,
                                    velocity_arrows_tick, velocity_arrows_button, com_checkbox_button, com_tick,
                                    com_button, big_g_box)
    # adds the texts in the edit window to the edit_window_texts group
    edit_window_texts.add_texts(name_text, mass_text, position_text, velocity_text, speed_text, radius_text,
                                colour_text, mass_text_2, mass_value_2, kinetic_energy_text, kinetic_energy_value,
                                potential_energy_text, potential_energy_value, angular_momentum_text,
                                angular_momentum_units, apocentre_text, apocentre_value, angular_momentum_value,
                                pericentre_text, pericentre_value, semi_major_axis_text, semi_major_axis_value,
                                semi_minor_axis_text, semi_minor_axis_value, eccentricity_text, eccentricity_value,
                                period_text, period_value, max_rate_of_area_text, max_rate_of_area_units,
                                max_rate_of_area_value, min_rate_of_area_text, min_rate_of_area_units,
                                min_rate_of_area_value, big_g_text, x_momentum_text, x_momentum_value, y_momentum_text,
                                y_momentum_value, total_kinetic_energy_text, total_kinetic_energy_value,
                                total_potential_energy_text, total_potential_energy_value, total_energy_text,
                                total_energy_value, whole_system_text, force_text, force_value)

    # creates dictionary with keys of button names and values of the corresponding button objects
    button_names: dict[str, TextBox] = {"name_box": name_box, "mass_box": mass_box, "position_box": position_box,
                                        "big_g_box": big_g_box, "velocity_box": velocity_box, "speed_box": speed_box,
                                        "radius_box": radius_box, "colour_box": colour_box,
                                        "open_path_box": open_path_box, "save_path_box": save_path_box}

    # start infinite loop
    while run:
        # check for user events
        for event in pygame.event.get():
            # if cross is clicked, check if project has been saved and prompt user if not, otherwise close program
            if event.type == pygame.QUIT:
                if saved:
                    sys.exit()
                else:
                    shapes.remove_sprites(edit_window_outline, edit_window)
                    buttons.remove_buttons(*edit_window_buttons)
                    texts.remove_texts(*edit_window_texts)
                    texts.add_texts(time_text, years_text, check_saved_text)
                    text_box_buttons.empty()
                    edit_button.set_position((740, 375))
                    saved = True
            # check for the user pressing a key and if they are typing in a textbox
            elif event.type == pygame.KEYDOWN and text_box_buttons.get_activated():
                text_box_activated = text_box_buttons.get_activated()
                # get the textbox contents and name, the contents are empty unless the user has pressed enter
                contents_list = text_box_activated.key_pressed(screen, event)
                name = text_box_activated.get_name()
                # if the user has pressed enter, check the name of the box they were typing in
                # for object parameters, save the user's input and
                # sets the saved variable to False to record that a change has been made
                if contents_list:
                    contents = "".join(contents_list)
                    try:
                        if name == "name_box":
                            saved = False
                            body_buttons.get_activated().set_name(contents)
                            body_buttons.get_activated().set_text(Text(franklingothicmedium_20, contents,
                                                                       tuple(active_body.get_colour())))
                            active_body.set_name(contents)
                        if name == "mass_box":
                            saved = False
                            active_body.set_mass(float(contents))
                        elif name == "position_box":
                            saved = False
                            active_body.set_position([float(contents.split(",")[0]), float(contents.split(",")[1])])
                        elif name == "velocity_box":
                            saved = False
                            active_body.set_velocity([float(contents.split(",")[0]), float(contents.split(",")[1])])
                            speed_box.update_contents("{:.2e}".format(active_body.get_speed()))
                        elif name == "speed_box":
                            saved = False
                            scale: float = float(contents) / (abs(active_body.get_speed()) + 0.000001)
                            active_body.set_velocity([scale * active_body.get_velocity()[0],
                                                      scale * active_body.get_velocity()[1]])
                            velocity_box.update_contents("{:.2e}, {:.2e}".format(active_body.get_velocity()[0],
                                                                                 active_body.get_velocity()[1]))
                        elif name == "radius_box":
                            saved = False
                            active_body.set_radius(abs(float(contents)))
                            bodies.calculate_visual_radii()
                        elif name == "colour_box":
                            saved = False
                            colour_list = [int(contents.split(",")[0]), int(contents.split(",")[1]),
                                           int(contents.split(",")[2])]
                            valid = True
                            for value in colour_list:
                                if 255 < value or value < 0:
                                    texts.add_texts(colour_error_text, colour_error_text2)
                                    valid = False
                            if valid:
                                active_body.set_colour([int(contents.split(",")[0]), int(contents.split(",")[1]),
                                                        int(contents.split(",")[2])])
                        elif name == "big_g_box":
                            saved = False
                            bodies.set_big_g(float(contents))
                        # if the system is being saved for the first time, a file is created for it
                        elif name == "save_path_box":
                            # if the input name already exists, the program runs through permutations of the name
                            # with numbers appended to the end until one is free
                            if contents + ".json" in os.listdir("projects"):
                                i = 0
                                while contents + f"({i}).json" in os.listdir("projects"):
                                    i += 1
                                path = contents + f"({i})"
                            else:
                                path: str = contents
                            # the JSON file is created with either the user's input or a permutation of it
                            # textbox and text are removed from screen and saved is set to true
                            with open(f"projects/{path}.json", "w") as file:
                                json.dump(bodies.get_json(), file)
                            texts.remove_texts(project_name_text)
                            text_box_buttons.remove_buttons(save_path_box)
                            saved = True
                        # if a system is being opened and the user's input path exists, the data is read
                        # The data is converted from json into the bodies class and some on-screen changes are made
                        elif name == "open_path_box":
                            if f"{contents}.json" in os.listdir("projects"):
                                path = contents
                                with open(f"projects/{path}.json", "r") as file:
                                    data = json.load(file)
                                bodies.empty()
                                active_body = Body("", 0, 0, [], [], [])
                                bodies.reset_total_mass()
                                for body in data["bodies"]:
                                    bodies.add_bodies(
                                        Body(body["name"], body["mass"], body["radius"], body["position"],
                                             body["velocity"], body["colour"]))
                                bodies.set_velocity_arrows(data["velocity_arrows"])
                                bodies.set_force_arrows(data["force_arrows"])
                                bodies.set_com(data["com"])
                                bodies.set_time(data["time"])
                                bodies.set_dt(data["dt"])
                                bodies.set_big_g(data["big_g"])
                                bodies.set_scaling(data["scaling"])
                                bodies.set_shift(data["shift"])
                                bodies.set_central_body(data["central_body"])
                                bodies.calculate_visual_radii()
                                body_buttons = create_body_buttons(bodies, franklingothicmedium_20)
                                edit_window_buttons.add_buttons(*body_buttons)
                                scale_text.update_text("50px : {:.2e}m".format(bodies.get_scaling() / 0.026))
                                timestep_text.update_text(f"Timestep: {bodies.get_dt()}s")
                                time_text.update_text("Time: {:.2e}s".format(bodies.get_time()))
                                years_text.update_text(
                                    f"Earth years: {round(bodies.get_time() / (3.154 * 10 ** 7), 1)}"
                                )
                                play_pause_button.deactivate()
                                texts.remove_texts(open_project_text, *projects_texts)
                                text_box_buttons.remove_buttons(open_path_box)
                                saved = True
                            else:
                                texts.add_texts(doesnt_exist_text)
                    except IndexError:
                        texts.add_texts(index_error_text, index_error_text2)
                    except ValueError:
                        texts.add_texts(value_error_text, value_error_text2)
            # if the user has clicked, they are not able to type in a textbox (unless they clicked on one)
            # if they have clicked a button, its name is retrieved from either the buttons or text_box_buttons class
            elif event.type == pygame.MOUSEBUTTONDOWN:
                texts.remove_texts(doesnt_exist_text)
                text_box_buttons.deactivate_all()
                button_clicked = buttons.button_clicked(event.pos)
                if not button_clicked:
                    button_clicked = text_box_buttons.button_clicked(event.pos)
                # if they have clicked on a button, its name is checked to determine what functionality occurs
                if button_clicked:
                    # if they were in the middle of opening or saving and clicked on something else,
                    # the opening or saving text boxes and corresponding texts are removed
                    if button_clicked != "open_path_box" and button_clicked != "save_path_box":
                        texts.remove_texts(check_saved_text, project_name_text, open_project_text,
                                           value_error_text, value_error_text2, index_error_text, index_error_text2,
                                           colour_error_text, colour_error_text2)
                        text_box_buttons.remove_buttons(open_path_box, save_path_box)
                        texts.remove_texts(*projects_texts.sprites())
                    # the following 5 buttons perform simple functionality for the system or display
                    if button_clicked == "fast_back":
                        bodies.change_dt(-1)
                        timestep_text.update_text(f"Timestep: {bodies.get_dt()}s")
                    elif button_clicked == "play_pause":
                        play_pause_button.toggle()
                    elif button_clicked == "fast_forward":
                        bodies.change_dt(1)
                        timestep_text.update_text(f"Timestep: {bodies.get_dt()}s")
                    elif button_clicked == "plus":
                        bodies.change_scaling(-1)
                        scale_text.update_text("50px : {:.2e}m".format(bodies.get_scaling() / 0.026))
                    elif button_clicked == "minus":
                        bodies.change_scaling(1)
                        scale_text.update_text("50px : {:.2e}km".format(bodies.get_scaling() / 0.026))
                    elif button_clicked == "hamburger":
                        # hamburger button either removes or adds the buttons in its menu to the screen
                        if hamburger_button.toggle():
                            buttons.add_buttons(new_button, open_button, save_button)
                        else:
                            buttons.remove_buttons(new_button, open_button, save_button)
                    elif button_clicked == "new":
                        # clears the previous simulation so the user can start creating their own,
                        # after prompting the user to save if needed
                        if saved:
                            bodies.empty()
                            buttons.remove_buttons(*edit_window_buttons)
                            buttons.add_buttons(bodies_button, system_button)
                            shapes.add_sprites(edit_window_outline, edit_window)
                            edit_button.set_position((350, 375))
                            body_buttons.empty()
                            text_box_buttons.empty()
                            texts.remove_texts(*edit_window_texts, time_text, years_text)
                            path = ""
                        else:
                            texts.add_texts(check_saved_text)
                            saved = True
                    elif button_clicked == "open":
                        # if the edit window is open, it is cleared from the screen
                        shapes.remove_sprites(edit_window_outline, edit_window)
                        buttons.remove_buttons(*edit_window_buttons)
                        texts.remove_texts(*edit_window_texts)
                        texts.add_texts(time_text, years_text)
                        text_box_buttons.empty()
                        edit_button.set_position((740, 375))
                        if play_pause_button.get_active():
                            play_pause_button.toggle()
                        # Prompts the user to save if needed and then opens the file path textbox
                        if saved:
                            text_box_buttons.add_buttons(open_path_box)
                            texts.add_texts(open_project_text)
                            # displays a list of available projects so the user can see which ones they can open
                            projects_texts.empty()
                            for i in range(len(os.listdir("projects"))):
                                projects_texts.add_texts(Text(franklingothicmedium_20, os.listdir("projects")[i][:-5],
                                                              WHITE, (300, 340 + 30 * i), outline=True))
                            texts.add_texts(*projects_texts)
                            open_path_box.activate()
                        else:
                            texts.add_texts(check_saved_text)
                            saved = True
                    elif button_clicked == "save":
                        # if system has been saved previously, JSON data is retrieved and written to file at the path
                        if path:
                            with open(f"projects/{path}.json", "w") as file:
                                json.dump(bodies.get_json(), file)
                            saved = True
                            texts.remove_texts(check_saved_text)
                            # 'Saved' is displayed for 1 second
                            texts.add_texts(saved_text)
                            draw_screen(screen, clock, bodies, buttons, text_box_buttons, texts, shapes)
                            time.sleep(1)
                            texts.remove_texts(saved_text)
                        # otherwise the user must enter a file name for the system to be saved at
                        else:
                            # if the edit window is open, it is removed from the screen
                            shapes.remove_sprites(edit_window_outline, edit_window)
                            buttons.remove_buttons(*edit_window_buttons)
                            texts.remove_texts(*edit_window_texts)
                            texts.add_texts(time_text, years_text)
                            text_box_buttons.empty()
                            edit_button.set_position((740, 375))
                            texts.add_texts(project_name_text)
                            # text box is added to screen for the user to type the file name in
                            text_box_buttons.add_buttons(save_path_box)
                            save_path_box.activate()
                    elif button_clicked == "edit":
                        # adds or removes the edit window from the screen
                        if edit_button.toggle():
                            shapes.add_sprites(edit_window_outline, edit_window)
                            buttons.add_buttons(bodies_button, system_button)
                            edit_button.set_position((350, 375))
                            texts.remove_texts(time_text, years_text)
                        else:
                            shapes.remove_sprites(edit_window_outline, edit_window)
                            buttons.remove_buttons(*edit_window_buttons)
                            texts.remove_texts(*edit_window_texts)
                            texts.add_texts(time_text, years_text)
                            text_box_buttons.empty()
                            edit_button.set_position((740, 375))
                    elif button_clicked == "bodies":
                        # closes the 'system' tab if it's open and opens the 'bodies' tab, adding the buttons for each
                        # body into the edit window
                        system_button.deactivate()
                        if bodies_button.toggle():
                            buttons.remove_buttons(*edit_window_buttons)
                            buttons.add_buttons(bodies_button, system_button, *body_buttons,
                                                add_new_image_button, add_new_text_button, delete_text_button,
                                                delete_image_button)
                            text_box_buttons.remove_buttons(big_g_box)
                            texts.remove_texts(*edit_window_texts)
                        else:
                            buttons.remove_buttons(*edit_window_buttons)
                            buttons.add_buttons(bodies_button, system_button)
                            texts.remove_texts(*edit_window_texts)
                            text_box_buttons.empty()
                    elif button_clicked in body_buttons.get_names():
                        # if one of the body buttons is clicked, the text and boxes for its modifiable parameters are
                        # put on screen
                        text_box_buttons.add_buttons(name_box, mass_box, position_box, velocity_box, speed_box,
                                                     radius_box, colour_box)
                        buttons.add_buttons(add_new_text_button, add_new_image_button, delete_image_button,
                                            delete_text_button, central_body_button, central_body_checkbox_button,
                                            toggle_data_button)
                        texts.remove_texts(*edit_window_texts)
                        texts.add_texts(name_text, mass_text, position_text, velocity_text, speed_text, radius_text,
                                        colour_text)
                        body_buttons.deactivate_all()
                        body_buttons.sprites()[body_buttons.get_names().index(button_clicked)].activate()
                        active_body = bodies.sprites()[bodies.get_names().index(
                            body_buttons.get_activated().get_name())]
                        if bodies.get_central_body() == active_body.get_name():
                            buttons.add_buttons(central_body_tick)
                        else:
                            buttons.remove_buttons(central_body_tick)
                        if toggle_data_button.get_active():
                            toggle_data_button.toggle_text()
                        # the boxes are updated with the values for each parameter, to 2 decimal places if necessary
                        name_box.update_contents(active_body.get_name())
                        mass_box.update_contents("{:.2e}".format(active_body.get_mass()))
                        position_box.update_contents("{:.2e}, {:.2e}".format(active_body.get_position()[0],
                                                                             active_body.get_position()[1]))
                        velocity_box.update_contents("{:.2e}, {:.2e}".format(active_body.get_velocity()[0],
                                                                             active_body.get_velocity()[1]))
                        speed_box.update_contents("{:.2e}".format(active_body.get_speed()))
                        radius_box.update_contents("{:.2e}".format(abs(active_body.get_radius())))
                        colour_box.update_contents(str(active_body.get_colour())[1:-1])
                    # if any text boxes have been clicked, they are activated which allows the user to type in them
                    if button_clicked in button_names.keys():
                        button_names[button_clicked].activate()
                    elif button_clicked == "toggle_data":
                        # swaps text from 'more data' to 'less data' or vice versa
                        if toggle_data_button.toggle_text():
                            # removes items for the modifiable parameters of a body and displays all the system data
                            # in the edit window
                            texts.remove_texts(name_text, mass_text, position_text, velocity_text, speed_text,
                                               radius_text, colour_text)
                            buttons.remove_buttons(add_new_text_button, add_new_image_button, delete_image_button,
                                                   delete_text_button, central_body_button,
                                                   central_body_checkbox_button, central_body_tick)
                            text_box_buttons.remove_buttons(name_box, mass_box, radius_box, position_box, velocity_box,
                                                            speed_box, colour_box)
                            mass_value_2.update_text("{:.8e}".format(active_body.get_mass()))
                            kinetic_energy_value.update_text("{:.8e}".format(active_body.get_kinetic_energy()))
                            potential_energy_value.update_text("{:.8e}".format(
                                bodies.get_potential_energies()[bodies.sprites().index(active_body)]))
                            angular_momentum_value.update_text("{:.8e}".format(active_body.get_angular_momentum())
                                                               )
                            apocentre_value.update_text("{:.8e}".format(active_body.get_apocentre_distance()))
                            pericentre_value.update_text("{:.8e}".format(active_body.get_pericentre_distance()))
                            semi_major_axis_value.update_text("{:.8e}".format(active_body.get_semi_major_axis()))
                            semi_minor_axis_value.update_text("{:.8e}".format(active_body.get_semi_minor_axis()))
                            eccentricity_value.update_text("{:.8e}".format(active_body.get_eccentricity()))
                            max_rate_of_area_value.update_text("{:.8e}".format(active_body.get_max_rate_of_area()))
                            min_rate_of_area_value.update_text("{:.8e}".format(active_body.get_min_rate_of_area()))
                            period_value.update_text("{:.8e}".format(active_body.get_period()))
                            texts.add_texts(mass_text_2, kinetic_energy_text, potential_energy_text, apocentre_text,
                                            pericentre_text, semi_major_axis_text, semi_minor_axis_text,
                                            max_rate_of_area_text, max_rate_of_area_units, min_rate_of_area_text,
                                            min_rate_of_area_units, eccentricity_text, period_text, eccentricity_value,
                                            mass_value_2, kinetic_energy_value, potential_energy_value, apocentre_value,
                                            pericentre_value, semi_major_axis_value, semi_minor_axis_value,
                                            period_value, angular_momentum_text, angular_momentum_value,
                                            angular_momentum_units, max_rate_of_area_value, min_rate_of_area_value)
                        else:
                            # the data texts are removed and previous texts and text boxes are replaced
                            texts.remove_texts(*edit_window_texts)
                            texts.add_texts(name_text, mass_text, position_text, velocity_text, speed_text, radius_text,
                                            colour_text)
                            buttons.add_buttons(add_new_text_button, add_new_image_button, delete_image_button,
                                                delete_text_button, central_body_button, central_body_checkbox_button)
                            text_box_buttons.add_buttons(name_box, mass_box, radius_box, position_box, velocity_box,
                                                         speed_box, colour_box)
                    elif (button_clicked == "central_body" or button_clicked == "central_body_checkbox"
                          or button_clicked == "central_body_tick"):
                        # if any part of the central body text or box is clicked, the button is toggled
                        if central_body_button.toggle():
                            # tick placed into the box if activated
                            buttons.add_buttons(central_body_tick)
                            bodies.set_central_body(active_body.get_name())
                            active_body.reset_orbital_data()
                        else:
                            # tick removed from box if deactivated
                            buttons.remove_buttons(central_body_tick)
                            bodies.set_central_body("")
                    elif button_clicked == "add_new_image" or button_clicked == "add_new_text":
                        # creates a new body in the system and its tab opens automatically
                        # saved set to false as a change has been made, the visual radii must be recalculated in case
                        # the new body has a larger or smaller radius than any systems
                        saved = False
                        active_body = Body(f"Body{new_bodies}", 10 ** 24, 100000, [0, 0], [0, 0], [255, 255, 255])
                        bodies.add_bodies(active_body)
                        bodies.calculate_visual_radii()
                        buttons.remove_buttons(*body_buttons)
                        body_buttons = create_body_buttons(bodies, franklingothicmedium_20)
                        edit_window_buttons.add_buttons(*body_buttons)
                        buttons.add_buttons(*body_buttons)
                        body_buttons.deactivate_all()
                        body_buttons.sprites()[body_buttons.get_names().index(f"Body{new_bodies}")].activate()
                        new_bodies += 1
                        text_box_buttons.add_buttons(name_box, mass_box, position_box, velocity_box, speed_box,
                                                     radius_box, colour_box)
                        buttons.add_buttons(delete_image_button, delete_text_button, central_body_button,
                                            central_body_checkbox_button, toggle_data_button)
                        texts.remove_texts(*edit_window_texts)
                        texts.add_texts(name_text, mass_text, position_text, velocity_text, speed_text, radius_text,
                                        colour_text)
                        # text boxes updated with the default values for a new body
                        name_box.update_contents(active_body.get_name())
                        mass_box.update_contents("{:.2e}".format(active_body.get_mass()))
                        position_box.update_contents("{:.2e}, {:.2e}".format(active_body.get_position()[0],
                                                                             active_body.get_position()[1]))
                        velocity_box.update_contents("{:.2e}, {:.2e}".format(active_body.get_velocity()[0],
                                                                             active_body.get_velocity()[1]))
                        speed_box.update_contents("{:.2e}".format(active_body.get_speed()))
                        radius_box.update_contents("{:.2e}".format(abs(active_body.get_radius())))
                        colour_box.update_contents(str(active_body.get_colour())[1:-1])
                    elif button_clicked == "delete":
                        # saved set to false as a change has been made, body removed from the system, its tab closed and
                        # the body buttons are remade
                        saved = False
                        bodies.remove_bodies(active_body)
                        buttons.remove_buttons(*body_buttons, central_body_button, central_body_checkbox_button,
                                               central_body_tick)
                        body_buttons = create_body_buttons(bodies, franklingothicmedium_20)
                        edit_window_buttons.add_buttons(*body_buttons)
                        buttons.add_buttons(*body_buttons)
                        text_box_buttons.empty()
                        texts.remove_texts(*edit_window_texts)
                    elif button_clicked == "system":
                        # closes 'bodies' tab if it's open and opens 'system' tab
                        # adds options to toggle force arrows, velocity arrows and centre of mass as well as the
                        # gravitational constant text box and data about the whole system
                        bodies_button.deactivate()
                        if system_button.toggle():
                            buttons.remove_buttons(*edit_window_buttons)
                            buttons.add_buttons(bodies_button, system_button, force_arrows_button,
                                                velocity_arrows_button, force_arrows_checkbox_button,
                                                velocity_arrows_checkbox_button, com_checkbox_button, com_button)
                            if bodies.get_force_arrows():
                                buttons.add_buttons(force_arrows_tick)
                            if bodies.get_velocity_arrows():
                                buttons.add_buttons(velocity_arrows_tick)
                            if bodies.get_com():
                                buttons.add_buttons(com_tick)
                            text_box_buttons.empty()
                            text_box_buttons.add_buttons(big_g_box)
                            texts.remove_texts(*edit_window_texts)
                            texts.add_texts(x_momentum_text, x_momentum_value, y_momentum_text, y_momentum_value,
                                            total_kinetic_energy_text, total_potential_energy_value, total_energy_value,
                                            total_potential_energy_text, total_kinetic_energy_value, total_energy_text,
                                            big_g_text, whole_system_text)
                            # sums the x and y components of all bodies' momenta; kinetic, potential and total energies,
                            # displaying the totals to 8 decimal places
                            x_momentum_value.update_text("{:.8e}".format(sum([lst[0] for lst in bodies.get_momenta()])))
                            y_momentum_value.update_text("{:.8e}".format(sum([lst[1] for lst in bodies.get_momenta()])))
                            total_kinetic_energy_value.update_text("{:.8e}".format(sum(bodies.get_kinetic_energies())))
                            total_potential_energy_value.update_text(
                                "{:.8e}".format(sum(bodies.get_potential_energies()) / 2))
                            total_energy_value.update_text("{:.8e}".format(sum(bodies.get_kinetic_energies()) +
                                                                           sum(bodies.get_potential_energies()) / 2))
                        else:
                            # closes system tab, removing all of the above
                            buttons.remove_buttons(*edit_window_buttons)
                            buttons.add_buttons(bodies_button, system_button)
                            text_box_buttons.remove_buttons(big_g_box)
                            texts.remove_texts(big_g_text)
                    elif (button_clicked == "force_arrows" or button_clicked == "force_arrows_checkbox"
                          or button_clicked == "force_arrows_tick"):
                        # adds or removes tick in force arrows checkbox if they are active or not
                        if bodies.toggle_force_arrows():
                            buttons.add_buttons(force_arrows_tick)
                        else:
                            buttons.remove_buttons(force_arrows_tick)
                    elif (button_clicked == "velocity_arrows" or button_clicked == "velocity_arrows_checkbox"
                          or button_clicked == "velocity_arrows_tick"):
                        # adds or removes tick in velocity arrows checkbox
                        if bodies.toggle_velocity_arrows():
                            buttons.add_buttons(velocity_arrows_tick)
                        else:
                            buttons.remove_buttons(velocity_arrows_tick)
                    elif button_clicked == "com" or button_clicked == "com_checkbox" or button_clicked == "com_tick":
                        # adds or removes tick in centre of mass checkbox
                        if bodies.toggle_com():
                            buttons.add_buttons(com_tick)
                        else:
                            buttons.remove_buttons(com_tick)
                else:
                    # if the user clicks anywhere but a button, they can drag to pan around the system
                    # the mouse position when first clicked is saved to calculate the pan
                    dragging = True
                    initial_shift = tuple(bodies.get_shift())
                    initial_mouse_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                # dragging stops when the user stops holding down a mouse button
                dragging = False
            elif event.type == pygame.MOUSEWHEEL:
                # when scrolling, the screen zooms in or out centred on the mouse position
                mouse_pos = (bodies.get_scaling() * (pygame.mouse.get_pos()[0] - bodies.get_shift()[0]),
                             bodies.get_scaling() * (pygame.mouse.get_pos()[1] - bodies.get_shift()[1]))
                bodies.change_scaling(-event.y)
                bodies.set_shift((pygame.mouse.get_pos()[0] - mouse_pos[0] / bodies.get_scaling(),
                                  pygame.mouse.get_pos()[1] - mouse_pos[1] / bodies.get_scaling()))
                # scale text updated to the new value
                scale_text.update_text("50px : {:.2e}m".format(bodies.get_scaling() / 0.026))
            if dragging:
                # updates shift while the user is holding down the mouse button
                bodies.set_shift((initial_shift[0] + pygame.mouse.get_pos()[0] - initial_mouse_pos[0],
                                  initial_shift[1] + pygame.mouse.get_pos()[1] - initial_mouse_pos[1]))
        if play_pause_button.get_active():
            # if the user has clicked the play button, the next iteration of the system is calculated and any buttons
            # for bodies which have collided are removed
            evolve_system(bodies)
            collided_bodies = bodies.check_collisions()
            if collided_bodies:
                buttons.remove_buttons(*[body_buttons.sprites()[body_buttons.get_names().index(body.get_name())]
                                         for body in collided_bodies], central_body_tick, central_body_button,
                                       central_body_checkbox_button)
                body_buttons.remove_buttons(*[body_buttons.sprites()[body_buttons.get_names().index(body.get_name())]
                                              for body in collided_bodies])
                texts.remove_texts(*edit_window_texts)
                text_box_buttons.empty()
            # times in seconds and earth years are updated
            time_text.update_text("Time: {:.2e}s".format(bodies.get_time()))
            years_text.update_text(f"{round(bodies.get_time() / (3.154 * 10 ** 7), 1)} Earth years")
            if system_button.get_active():
                # data about the whole system is updated if the user is viewing it on the 'system' tab
                x_momentum_value.update_text("{:.8e}".format(sum([lst[0] for lst in bodies.get_momenta()])))
                y_momentum_value.update_text("{:.8e}".format(sum([lst[1] for lst in bodies.get_momenta()])))
                total_kinetic_energy_value.update_text("{:.8e}".format(sum(bodies.get_kinetic_energies())))
                total_potential_energy_value.update_text("{:.8e}".format(sum(bodies.get_potential_energies()) / 2))
                total_energy_value.update_text("{:.8e}".format(sum(bodies.get_kinetic_energies()) +
                                                               sum(bodies.get_potential_energies()) / 2))
            if toggle_data_button.get_active():
                # data about a body is calculated and updated if the user is viewing it after clicking 'more data'
                bodies.calculate_data()
                mass_value_2.update_text("{:.8e}".format(active_body.get_mass()))
                kinetic_energy_value.update_text("{:.8e}".format(active_body.get_kinetic_energy()))
                potential_energy_value.update_text("{:.8e}".format(
                    bodies.get_potential_energies()[bodies.sprites().index(active_body)]))
                angular_momentum_value.update_text("{:.8e}".format(active_body.get_angular_momentum()))
                apocentre_value.update_text("{:.8e}".format(active_body.get_apocentre_distance()))
                pericentre_value.update_text("{:.8e}".format(active_body.get_pericentre_distance()))
                semi_major_axis_value.update_text("{:.8e}".format(active_body.get_semi_major_axis()))
                semi_minor_axis_value.update_text("{:.8e}".format(active_body.get_semi_minor_axis()))
                eccentricity_value.update_text("{:.8e}".format(active_body.get_eccentricity()))
                period_value.update_text("{:.8e}".format(active_body.get_period()))
                max_rate_of_area_value.update_text("{:.8e}".format(active_body.get_max_rate_of_area()))
                min_rate_of_area_value.update_text("{:.8e}".format(active_body.get_min_rate_of_area()))
            elif active_body.get_name():
                # otherwise if the user is viewing the main page for a body, the position, velocity and speed are
                # updated every frame while the system is playing
                position_box.update_contents("{:.2e}, {:.2e}".format(active_body.get_position()[0],
                                                                     active_body.get_position()[1]))
                velocity_box.update_contents("{:.2e}, {:.2e}".format(active_body.get_velocity()[0],
                                                                     active_body.get_velocity()[1]))
                speed_box.update_contents("{:.2e}".format(active_body.get_speed()))
        # draws all items onto the screen
        draw_screen(screen, clock, bodies, buttons, text_box_buttons, texts, shapes)


# constants: screen size and colours
WIDTH: int = 800
HEIGHT: int = 800
WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0)

if __name__ == "__main__":
    main()
