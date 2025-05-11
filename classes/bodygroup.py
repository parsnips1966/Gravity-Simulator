import pygame
import math
from classes.body import Body


class BodyGroup(pygame.sprite.Group):
    """
    Name: BodyGroup
    Purpose: Contains all the bodies in the system and performs actions on all of them.
    Contains variables controlling the function and appearance of the whole simulation.
    Provides the JSON data of the system to be saved to file.
    """
    def __init__(self):
        """
        Name: __init__
        Parameters: -
        Returns: BodyGroup
        Purpose: Initialises super class and all the parameters to their default values.
        """
        super().__init__()
        self.__time: float = 0
        self.__dt: float = 2 ** 16
        self.__big_g: float = 6.674e-11
        self.__scaling: float = 10 ** 9
        self.__shift: tuple[int, int] = (400, 400)
        self.__minimum_radius: float = 0
        self.__radius_scaling: float = 0
        self.__velocity_arrows: bool = False
        self.__force_arrows: bool = False
        self.__com: bool = False
        self.__central_body: str | None = None
        self.__com_coord: list[float] = [0.0, 0.0]
        self.__total_mass: float = 0

    def add_bodies(self, *bodies: Body) -> None:
        """
        Name: add_bodies
        Parameters: *bodies: Body
        Returns: None
        Purpose: Calls add function from the super class to add bodies to the group.
        Adds the bodies' mass to the total mass of the system and recalculates the radii of the bodies on screen in
        case one of the new bodies has greater or smaller radius than any of the others.
        """
        super().add(*bodies)
        for body in bodies:
            self.__total_mass += body.get_mass()
        self.calculate_visual_radii()

    def remove_bodies(self, *bodies: Body) -> None:
        """
        Name: remove_bodies
        Parameters: *bodies: Body
        Returns: None
        Purpose: Passes the bodies to the super class's remove function. The remove function isn't called directly from
        main as it was not recognising the bodies as subclasses of Sprite and throwing an error.
        """
        super().remove(*bodies)

    def get_json(self) -> dict:
        """
        Name: get_json
        Parameters: -
        Returns: dictionary
        Purpose: Retrieves the data for each body and saves each body as a JSON object within a list of all bodies.
        This is placed into another object along with all the other system variables that is returned.
        """
        return {"velocity_arrows": self.__velocity_arrows, "force_arrows": self.__force_arrows,
                "com": self.__com, "time": self.__time, "dt": self.__dt, "big_g": self.__big_g,
                "scaling": self.__scaling, "shift": self.__shift, "central_body": self.__central_body,
                "bodies": [{"name": body.get_name(), "mass": body.get_mass(), "radius": body.get_radius(),
                            "position": body.get_position(), "velocity": body.get_velocity(),
                            "acceleration": body.get_acceleration(), "colour": body.get_colour()}
                           for body in self.sprites()]}

    def set_velocity_arrows(self, value: bool) -> None:
        """
        Name: set_velocity_arrows
        Parameters: value: boolr
        Returns: None
        Purpose: velocity_arrows_setter
        """
        self.__velocity_arrows = value

    def toggle_velocity_arrows(self) -> bool:
        """
        Name: toggle_velocity_arrows
        Parameters: -
        Returns: boolean
        Purpose: If the velocity arrows are active, they are deactivated and vice versa. Their state is returned.
        """
        self.__velocity_arrows = not self.__velocity_arrows
        return self.__velocity_arrows

    def get_velocity_arrows(self) -> bool:
        """
        Name: get_velocity_arrows
        Parameters: -
        Returns: bool
        Purpose: velocity_arrows getter
        """
        return self.__velocity_arrows

    def set_force_arrows(self, value: bool) -> None:
        """
        Name: set_force_arrows
        Parameters: value: bool
        Returns: None
        Purpose: force_arrows setter
        """
        self.__force_arrows = value

    def toggle_force_arrows(self) -> bool:
        """
        Name: toggle_force_arrows
        parameters: -
        Returns: boolean
        Purpose: If the force arrows are active, they are deactivated and vice versa. Their state is returned.
        """
        self.__force_arrows = not self.__force_arrows
        return self.__force_arrows

    def get_force_arrows(self) -> bool:
        """
        Name: get_force_arrows
        Parameters: -
        Returns: bool
        Purpose: force_arrows getter
        """
        return self.__force_arrows

    def set_com(self, value: bool) -> None:
        """
        Name: set_com
        Parameters: value: bool
        Returns: None
        Purpose: com setter
        """
        self.__com = value

    def toggle_com(self) -> bool:
        """
        Name: toggle_com
        Parameters: -
        Returns: boolean
        Purpose: If the centre of mass is active, it is deactivated and vice versa. Its state is returned.
        """
        self.__com = not self.__com
        return self.__com

    def get_com(self) -> bool:
        """
        Name: get_com
        parameters: -
        Returns: bool
        Purpose: com getter
        """
        return self.__com

    def get_com_coord(self) -> list[float]:
        """
        Name: get_com_coord
        Parameters: -
        Returns: list[float]
        Purpose: com_coord getter
        """
        return self.__com_coord

    def get_time(self) -> float:
        """
        Name: get_time
        Parameters: -
        Returns: float
        Purpose: time getter
        """
        return self.__time

    def increment_time(self) -> None:
        """
        Name: increment_time
        Parameters: -
        Returns: None
        Purpose: Increases the universal time by the time interval used in the simulation calculations.
        """
        self.__time += self.__dt

    def set_time(self, time: float) -> None:
        """
        Name: set_time
        Parameters: time: float
        Returns: None
        Purpose: time setter
        """
        self.__time = time

    def get_dt(self) -> float:
        """
        Name: get_dt
        Parameters: -
        Returns: float
        Purpose: dt getter
        """
        return self.__dt

    def change_dt(self, sign: int) -> None:
        """
        Name: change_dt
        Parameters: sign: integer
        Returns: None
        Purpose: Doubles or halves the time interval used in calculations, depending on which button the user clicked.
        """
        self.__dt *= (2 ** sign)

    def set_dt(self, dt: float) -> None:
        """
        Name: set_dt
        Parameters: dt: float
        Returns: None
        Purpose: dt setter
        """
        self.__dt = dt

    def get_big_g(self) -> float:
        """
        Name: get_big_g
        Parameters: -
        Returns: float
        Purpose: big_g getter
        """
        return self.__big_g

    def set_big_g(self, big_g: float) -> None:
        """
        Name: set_big_g
        Parameters: big_g: float
        Returns: None
        Purpose: big_g setter
        """
        self.__big_g = big_g

    def get_scaling(self) -> float:
        """
        Name: get_scaling
        Parameters: -
        Returns: float
        Purpose: scaling getter
        """
        return self.__scaling

    def change_scaling(self, sign: int) -> None:
        """
        Name: change_scaling
        Parameters: sign: integer
        Returns: None
        Purpose: Changes the on-screen size of the simulation by a factor of the fourth root of 2.It either increases
        or decreases depending on which way the user scrolled, or whether they clicked the plus or minus.
        """
        self.__scaling *= 2 ** (0.25 * sign)

    def set_scaling(self, scaling: float) -> None:
        """
        Name: set_scaling
        Parameters: scaling: float
        Returns: None
        Purpose: scaling setter
        """
        self.__scaling = scaling

    def get_shift(self) -> tuple[int, int]:
        """
        Name: get_shift
        Parameters: -
        Returns: tuple[int, int]
        Purpose: shift getter
        """
        return self.__shift

    def set_shift(self, shift: tuple[int, int]) -> None:
        """
        Name: set_shift
        Parameters: shift: tuple[int, int]
        Returns: None
        Purpose: shift setter
        """
        self.__shift = shift

    def calculate_visual_radii(self) -> None:
        """
        Name: calculate_visual_radii
        Parameters: -
        Returns: None
        Purpose: Finds the largest and smallest radii of the bodies.
        Calculates the minimum on-screen radius using a base 10 logarithm of the ratio between the largest radius and
        the difference between largest and smallest radii. This means the on-screen sizes are more similar if the
        difference in real size is small compared to the real sizes. The real sizes are scaled by how they are
        distributed between the largest and smallest radii, and then added onto the minimum radius.
        These values are saved to each body.
        The largest possible range of on-screen radii is 5-25 pixels.
        """
        largest_radius = 0
        smallest_radius = 9e99
        for body in self.sprites():
            if body.get_radius() > largest_radius:
                largest_radius = body.get_radius()
            if body.get_radius() < smallest_radius:
                smallest_radius = body.get_radius()
        minimum_radius = 5 * math.log(20 * largest_radius / (2 * largest_radius - smallest_radius), 10)
        radius_scaling = 20 / (2 * largest_radius - smallest_radius + 1)
        for body in self.sprites():
            body.set_visual_radius((2 * body.get_radius() - smallest_radius) * radius_scaling + minimum_radius)

    def set_central_body(self, body: str) -> None:
        """
        Name: set_central_body
        Parameters: body: str
        Returns: None
        Purpose: central_body setter
        """
        self.__central_body = body

    def get_central_body(self) -> str:
        """
        Name: get_central_body
        Parameters: -
        Returns: str
        Purpose: central_body getter
        """
        return self.__central_body

    def get_names(self) -> list[str]:
        """
        Name: get_names
        Parameters: -
        Returns: list[str]
        Purpose: Retrieves the name of each body and returns a list of them.
        """
        return [body.get_name() for body in self.sprites()]

    def get_masses(self) -> list[float]:
        """
        Name: get_masses
        Parameters: -
        Returns: list[float]
        Purpose: Retrieves the mass of each body and returns a list of them.
        """
        return [body.get_mass() for body in self.sprites()]

    def get_radii(self) -> list[float]:
        """
        Name: get_radii
        Parameters: -
        Returns: list[float]
        Purpose: Retrieves the radius of each body and returns a list of them.
        """
        return [body.get_radius() for body in self.sprites()]

    def get_positions(self) -> list[list[float]]:
        """
        Name: get_positions
        Parameters: -
        Returns: list[list[float]]
        Purpose: Retrieves the position of each body and returns a list of them.
        """
        return [body.get_position() for body in self.sprites()]

    def update_positions(self) -> None:
        """
        Name: update_positions
        Parameters: -
        Returns: None
        Purpose: Calls the update_position function for each body, passing in the timestep.
        """
        for body in self.sprites():
            body.update_position(self.__dt)

    def get_velocities(self) -> list:
        """
        Name: get_velocities
        Parameters: -
        Returns: list
        Purpose: Retrieves the velocity of each body and returns a list of them.
        """
        return [body.get_velocity() for body in self.sprites()]

    def update_velocities(self, save: bool = False) -> None:
        """
        Name: update_velocities
        Parameters: save: bool
        Returns: None
        Purpose: Calls the update_velocity function for each body, passing in the timestep and whether the velocity
        should be saved.
        """
        for body in self.sprites():
            body.update_velocity(self.__dt, save)

    def get_accelerations(self) -> list[list[float]]:
        """
        Name: get_accelerations
        Parameters: list[list[float]]
        Returns: list
        Purpose: Retrieves the acceleration of each body and returns a list of them.
        """
        return [body.get_acceleration() for body in self.sprites()]

    def reset_accelerations(self) -> None:
        """
        Name: reset_accelerations
        Parameters: -
        Returns: None
        Purpose: Calls the reset_acceleration function for each body.
        """
        for body in self.sprites():
            body.reset_acceleration()

    def update_accelerations(self) -> None:
        """
        Name: update_accelerations
        Parameters: -
        Returns: None
        Purpose: Calculates the acceleration of each body due to every other body using Newton's Law of Universal
        Gravitation and calls the update_acceleration function for both bodies in every pair interaction.
        Calls the save_acceleration function for each body after its net acceleration has been calculated.
        """
        for body1 in self.sprites():
            for body2 in self.sprites()[self.sprites().index(body1) + 1:]:
                force_mag = self.__big_g * body1.get_mass() * body2.get_mass() / (
                        (body2.get_position()[0] - body1.get_position()[0]) ** 2 + (
                         body2.get_position()[1] - body1.get_position()[1]) ** 2 + 1) ** 1.5
                body1.update_acceleration([
                    force_mag * (body2.get_position()[0] - body1.get_position()[0]) / (body1.get_mass() + 1),
                    force_mag * (body2.get_position()[1] - body1.get_position()[1]) / (body1.get_mass() + 1)])
                body2.update_acceleration([
                    force_mag * (body1.get_position()[0] - body2.get_position()[0]) / (body2.get_mass() + 1),
                    force_mag * (body1.get_position()[1] - body2.get_position()[1]) / (body2.get_mass() + 1)])
            body1.save_acceleration()
            # print("Force on ", body1.get_name(), ": ", [body1.get_acceleration()[0] * body1.get_mass(),
            #                                             body1.get_acceleration()[1] * body1.get_mass()])
            # print("Magnitude: ", ((body1.get_acceleration()[0] * body1.get_mass()) ** 2 +
            #                       (body1.get_acceleration()[1] * body1.get_mass()) ** 2) ** 0.5)

    def get_all_previous_positions(self) -> list[list[list[float]]]:
        """
        Name: get_all_previous_positions
        Parameters: -
        Returns: list[list[list[float]]]
        Purpose: Retrieves previous positions list from each body and returns a list of those.
        """
        return [body.get_previous_positions() for body in self.sprites()]

    def get_all_previous_velocities(self) -> list[list[list[float]]]:
        """
        Name: get_all_previous_velocities
        Parameters: -
        Returns: list[list[list[float]]]
        Purpose: Retrieves previous velocities list from each body and returns a list of those.
        """
        return [body.get_previous_velocities() for body in self.sprites()]

    def get_all_previous_accs(self) -> list[list[list[float]]]:
        """
        Name: get_all_previous_accs
        Parameters: -
        Returns: list[list[list[float]]]
        Purpose: Retrieves previous accelerations list from each body and returns a list of those.
        """
        return [body.get_previous_accelerations() for body in self.sprites()]

    def get_momenta(self) -> list[list[float]]:
        """
        Name: get_momenta
        Parameters: -
        Returns: list[list[float]]
        Purpose: Retrieves momentum of each body and returns them in a list.
        """
        return [body.get_momentum() for body in self.sprites()]

    def get_kinetic_energies(self) -> list[float]:
        """
        Name: get_kinetic_energies
        Parameters: -
        Returns: list[float]
        Purpose: Retrieves kinetic energy of each body and returns them in a list.
        """
        return [body.get_kinetic_energy() for body in self.sprites()]

    def get_potential_energies(self) -> list[float]:
        """
        Name: get_potential_energies
        Parameters: -
        Returns: list[float]
        Purpose: Calculates the potential energy of each pair of bodies using E = -GMm/r (integral of Newton's
        Universal Law of Gravitation from infinity to r with respect to r). All energies involving one body are summed
        and this is done for each body. The sums are returned in a list.
        """
        return [sum([-self.__big_g * body1.get_mass() * body2.get_mass() /
                     ((body2.get_position()[0] - body1.get_position()[0]) ** 2 +
                      (body2.get_position()[1] - body1.get_position()[1]) ** 2 + 1) ** 0.5
                     for body2 in (self.sprites()[:self.sprites().index(body1)] +
                                   self.sprites()[self.sprites().index(body1) + 1:])]) for body1 in self.sprites()]

    def get_total_mass(self) -> float:
        return self.__total_mass

    def reset_total_mass(self) -> None:
        self.__total_mass = 0

    def check_collisions(self) -> list[Body]:
        """
        Name: check_collisions
        Parameters: -
        Returns: list[Body]
        Purpose: Checks if any bodies have collided with each other and returns a list of ones which have.
        """

        # initialises empty list for collided bodies and iterates through each pair of bodies
        destroyed = []
        for body1 in self.sprites():
            for body2 in self.sprites()[self.sprites().index(body1) + 1:]:
                # initialises variables to detect whether bodies are close enough in either axis to collide
                x_proximity = False
                y_proximity = False
                # maximum separation at which bodies would collide
                radii_sum = body1.get_radius() + body2.get_radius()
                # detects if bodies are within maximum separation in x and y directions
                if body1.get_position()[0] > body2.get_position()[0]:
                    if body1.get_position()[0] - radii_sum < body2.get_position()[0]:
                        x_proximity = True
                else:
                    if body1.get_position()[0] + radii_sum > body2.get_position()[0]:
                        x_proximity = True
                if body1.get_position()[1] > body2.get_position()[1]:
                    if body1.get_position()[1] - radii_sum < body2.get_position()[1]:
                        y_proximity = True
                else:
                    if body1.get_position()[1] + radii_sum > body2.get_position()[1]:
                        y_proximity = True
                # If they are close enough in both axes, they are appended to destroyed list
                # They are treated as squares rather than circles but this makes almost no difference
                if x_proximity and y_proximity:
                    destroyed += [body1, body2]
        # destroyed bodies' masses subtracted from total mass of system. They are removed from the group and returned
        for body in destroyed:
            self.__total_mass -= body.get_mass()
        super().remove(*destroyed)
        return destroyed

    def draw_bodies(self, surface: pygame.Surface) -> None:
        """
        Name: draw_bodies
        Parameters: surface: pygame.Surface
        Returns None
        Purpose: Calculates position of the centre of mass. Calls the draw function for each body and the
        draw_force_arrows and draw_velocity_arrows functions if necessary.
        Draws the centre of mass if the user has selected for it to be displayed.
        """
        com = [0, 0]
        for body in self.sprites():
            com[0] += body.get_position()[0] * body.get_mass()
            com[1] += body.get_position()[1] * body.get_mass()
            body.draw(surface, self.__scaling, self.__shift)
            if self.__velocity_arrows:
                body.draw_velocity_arrow(surface, self.__scaling, self.__shift)
            if self.__force_arrows:
                body.draw_force_arrow(surface, self.__scaling, self.__shift)
        if self.__total_mass != 0 and self.__com:
            self.__com = [com[0] / self.__total_mass, com[1] / self.__total_mass]
            print(self.__com)
            pygame.draw.circle(surface, (0, 0, 0),
                               (com[0] / self.__total_mass / self.__scaling + self.__shift[0],
                                com[1] / self.__total_mass / self.__scaling + self.__shift[1]), 5)
            pygame.draw.circle(surface, (255, 255, 255),
                               (com[0] / self.__total_mass / self.__scaling + self.__shift[0],
                                com[1] / self.__total_mass / self.__scaling + self.__shift[1]), 4)

    def calculate_data(self) -> None:
        """
        Name: calculate_data
        Parameters: -
        Returns: None
        Purpose: If a central body is designated, then orbital data is calculated for each body except the central body.
        """
        if self.__central_body:
            for body in self.sprites():
                if body.get_name() != self.__central_body:
                    body.calculate_data(
                        self.sprites()[self.get_names().index(self.__central_body)], self.__time, self.__dt)
