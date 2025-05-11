import pygame
import math


class Body(pygame.sprite.Sprite):
    """
    Name: Body
    Purpose: Represents a body such as a star or planet and contains the physical parameters of that body.
    Calculates how the body moves due to forces from the other bodies and keeps track of previous values
    Draws itself and any arrows related to it onto the screen
    Calculates many other data regarding itself
    """
    def __init__(self, name: str, mass: int, radius: int, position: list[float], velocity: list[float],
                 colour: list[int]):
        """
        Name: __init__
        Parameters: name: string, mass: integer, radius: integer, position: list[float], velocity: list[float],
        colour: list[int]
        Returns: None
        Purpose: initialise the super class and all the Body object attributes with either values passed in or a default
        """
        super().__init__()
        self.__name: str = name
        self.__mass: float = mass
        self.__radius: float = radius
        self.__position: list[float] = position
        self.__velocity: list[float] = velocity
        self.__acceleration: list[float] = [0.0, 0.0]
        self.__angular_momentum: float = 0
        self.__previous_positions: list[list[float]] = [self.__position]
        self.__previous_velocities: list[list[float]] = [self.__velocity]
        self.__previous_accelerations: list[list[float]] = [[0, 0]]
        self.__colour: list[int] = colour
        self.__visual_radius: float = 0
        self.__initial_position: list[float] = list(position)
        self.__displacement: list[float] = [0, 0]
        self.__delta_x: float = 0
        self.__delta_y: float = 0
        self.__orbit: list[int] = [0, 0]
        self.__initial_time: float = 0
        self.__apocentre: list[float] = list(position)
        self.__apocentre_distance: float = 0
        self.__pericentre: list[float] = list(position)
        self.__pericentre_distance: float = 9e99
        self.__distance_from_apocentre: float = 0
        self.__distance_from_pericentre: float = 0
        self.__co_vertex_1: list[float] = []
        self.__co_vertex_2: list[float] = []
        self.__eccentricity: float = 0
        self.__period: float = 0
        self.__min_rate_of_area: float = 9e99
        self.__max_rate_of_area: float = 0

    def get_name(self) -> str:
        """
        Name: get_name
        Parameters: -
        Returns: str
        Purpose: name getter
        """
        return self.__name

    def set_name(self, name: str) -> None:
        """
        Name: set_name
        Parameters: name: str
        Returns: None
        Purpose: name setter
        """
        self.__name = name

    def get_mass(self) -> float:
        """
        Name: get_mass
        Parameters: -
        Returns: float
        Purpose: mass getter
        """
        return self.__mass

    def set_mass(self, value: float) -> None:
        """
        Name: set_mass
        Parameters: value: float
        Returns: None
        Purpose: mass setter
        """
        self.__mass = value

    def get_radius(self) -> float:
        """
        Name: get_radius
        Parameters: -
        Returns: float
        Purpose: radius getter
        """
        return self.__radius

    def set_radius(self, value: float) -> None:
        """
        Name: set_radius
        Parameters: value: float
        Returns: None
        Purpose: radius setter
        """
        self.__radius = value

    def get_colour(self) -> list[int]:
        """
        Name: get_colour
        Parameters: -
        Returns: list[int]
        Purpose: colour getter
        """
        return self.__colour

    def set_colour(self, value: list[int]) -> None:
        """
        Name: set_colour
        Parameters: value: list[int]
        Returns: None
        Purpose: colour setter
        """
        self.__colour = value

    def set_visual_radius(self, radius: float) -> None:
        """
        Name: set_visual_radius
        Parameters: radius: float
        Returns: None
        Purpose: visual_radius setter
        """
        self.__visual_radius = radius

    def get_position(self) -> list[float]:
        """
        Name: get_position
        Parameters: -
        Returns: list[float]
        Purpose: position getter
        """
        return self.__position

    def set_position(self, position: list[float]) -> None:
        """
        Name: set_position
        Parameters: position: list[float]
        Returns: None
        Purpose: position setter
        """
        self.__position = position
        self.__previous_positions.append(position)

    def update_position(self, dt: float) -> None:
        """
        Name: update_position
        Parameters: dt: float
        Returns: None
        Purpose: Calculates change in x and y coordinates using the equation of motion for constant acceleration:
        s = ut + 0.5at^2, saving it for a later calculation, and updates the position with these changes.
        The new position is saved to the list of previous positions used to display the trail.
        """
        self.__delta_x = self.get_velocity()[0] * dt + self.get_acceleration()[0] * 0.5 * dt * dt
        self.__delta_y = self.get_velocity()[1] * dt + self.get_acceleration()[1] * 0.5 * dt * dt
        self.__position[0] += self.__delta_x
        self.__position[1] += self.__delta_y
        self.__previous_positions.append(list(self.__position))

    def get_velocity(self) -> list[float]:
        """
        Name: get_velocity
        Parameters: -
        Returns: list[float]
        Purpose: velocity getter
        """
        return self.__velocity

    def set_velocity(self, velocity: list) -> None:
        """
        Name: set_velocity
        Parameters: velocity: list
        Returns: None
        Purpose: velocity setter
        """
        self.__velocity = velocity

    def update_velocity(self, dt: float, save: bool) -> None:
        """
        Name: update_velocity
        Parameters: dt: float, save: boolean
        Returns: None
        Purpose: Calculates the new velocity using the equation of motion for constant acceleration: v = u + at.
        The velocity is updated in two 'halves' which is why there is a factor of 0.5, and it is only saved to the
        previous velocities list every other update.
        """
        self.__velocity[0] += self.get_acceleration()[0] * 0.5 * dt
        self.__velocity[1] += self.get_acceleration()[1] * 0.5 * dt
        if save:
            self.__previous_velocities.append(self.__velocity)

    def get_speed(self) -> float:
        """
        Name: get_speed
        Parameters: -
        Returns: float
        Purpose: Uses Pythagoras' theorem to calculate speed from velocity and return it
        """
        return (self.__velocity[0] ** 2 + self.__velocity[1] ** 2) ** 0.5

    def get_acceleration(self) -> list[float]:
        """
        Name: get_acceleration
        Parameters: -
        Returns: list[float]
        Purpose: acceleration getter
        """
        return self.__acceleration

    def reset_acceleration(self) -> None:
        """
        Name: reset_acceleration
        Parameters: -
        Returns: None
        Purpose: resets acceleration back to [0, 0], used after each set of motion calculations
        """
        self.__acceleration = [0, 0]

    def update_acceleration(self, value: list) -> None:
        """
        Name: update_acceleration
        Parameters: value: list
        Returns: None
        Purpose: adds the acceleration due to one other body to the total acceleration
        """
        self.__acceleration[0] += value[0]
        self.__acceleration[1] += value[1]

    def save_acceleration(self) -> None:
        """
        Name: save_acceleration
        Parameters: -
        Returns: None
        Purpose: Saves the current value of acceleration to the list of previous values
        """
        self.__previous_accelerations.append(self.__acceleration)

    def get_previous_positions(self) -> list[list[float]]:
        """
        Name: get_previous_positions
        Parameters: -
        Returns: list[list[float]]
        Purpose: previous_positions getter
        """
        return self.__previous_positions

    def get_previous_velocities(self) -> list[list[float]]:
        """
        Name: get_previous_velocities
        Parameters: -
        Returns: list[list[float]]
        Purpose: previous_velocities getter
        """
        return self.__previous_velocities

    def get_previous_accelerations(self) -> list[list[float]]:
        """
        Name: get_previous_accelerations
        Parameters: -
        Returns: list[list[float]]
        Purpose: previous_accelerations getter
        """
        return self.__previous_accelerations

    def get_momentum(self) -> list[float]:
        """
        Name: get_momentum
        Parameters: -
        Returns: list[float]
        Purpose: Multiplies velocity by mass to obtain and return momentum
        """
        return [self.__velocity[0] * self.__mass, self.__velocity[1] * self.__mass]

    def get_kinetic_energy(self) -> float:
        """
        Name: get_kinetic_energy
        Parameters: -
        Returns: float
        Purpose: Uses KE = 0.5mv^2, obtaining v^2 using Pythagoras, and returns it
        """
        return 0.5 * self.__mass * (self.__velocity[0] ** 2 + self.__velocity[1] ** 2)

    def reset_orbital_data(self) -> None:
        """
        Name: reset_orbital_data
        Parameters: -
        Returns: None
        Purpose: Sets all the orbital data variables back to default values when a body is changed to a central body
        """
        self.__angular_momentum = 0
        self.__apocentre = [0, 0]
        self.__apocentre_distance = 0
        self.__pericentre = [0, 0]
        self.__pericentre_distance = 0
        self.__distance_from_apocentre = 0
        self.__distance_from_pericentre = 0
        self.__co_vertex_1 = []
        self.__co_vertex_2 = []
        self.__eccentricity = 0
        self.__period = 0
        self.__min_rate_of_area: float = 9e99
        self.__max_rate_of_area: float = 0

    def get_angular_momentum(self) -> float:
        """
        Name: get_angular_momentum
        Parameters: -
        Returns: float
        Purpose: angular_momentum getter
        """
        return self.__angular_momentum

    def get_apocentre(self) -> list[float]:
        """
        Name: get_apocentre
        Parameters: -
        Returns: list[float]
        Purpose: apocentre getter
        """
        return self.__apocentre

    def get_apocentre_distance(self) -> float:
        """
        Name: get_apocentre_distance
        Parameters: -
        Returns: float
        Purpose: apocentre_distance getter
        """
        return self.__apocentre_distance

    def set_apocentre(self, value: float) -> None:
        """
        Name: set_apocentre
        Parameters: value: float
        Returns: None
        Purpose: apocentre setter
        """
        self.__apocentre = value

    def get_pericentre(self) -> list[float]:
        """
        Name: get_pericentre
        Parameters: -
        Returns: list[float]
        Purpose: pericentre getter
        :return:
        """
        return self.__pericentre

    def get_pericentre_distance(self) -> float:
        """
        Name: get_pericentre_distance
        Parameters: -
        Returns: float
        Purpose: pericentre_distance getter
        """
        return self.__pericentre_distance

    def set_pericentre(self, value: float) -> None:
        """
        Name: set_pericentre
        Parameters: value: float
        Returns: None
        Purpose: pericentre_setter
        """
        self.__pericentre = value

    def get_semi_major_axis(self) -> float:
        """
        Name: get_semi_major_axis
        Parameters: -
        Returns: float
        Purpose: calculates semi-major axis of the body's elliptical orbit by finding the half distance between its
        closest and furthest points from the central body. This value is then returned.
        """
        return 0.5 * ((self.__apocentre[0] - self.__pericentre[0]) ** 2 + (
                self.__apocentre[1] - self.__pericentre[1]) ** 2) ** 0.5

    def get_semi_minor_axis(self) -> float:
        """
        Name: get_semi_minor_axis
        Parameters: -
        Returns: float
        Purpose: If the body has completed 1.75 orbits (and the co-vertices found), it calculates semi-minor axis of the
        body's elliptical orbit by finding half the distance between the two points which are half-way between its
        closest and furthest points from the central body. This is returned if calculated, otherwise a default of 0 is.
        """
        if self.__co_vertex_2:
            try:
                return 0.5 * ((self.__co_vertex_1[0] - self.__co_vertex_2[0]) ** 2 + (
                    self.__co_vertex_1[1] - self.__co_vertex_2[1]) ** 2) ** 0.5
            except IndexError:
                print("The selected central body is not valid.")
        return 0

    def get_eccentricity(self) -> float:
        """
        Name: get_eccentricity
        Parameters: -
        Returns: float
        Purpose: eccentricity getter
        """
        return self.__eccentricity

    def get_max_rate_of_area(self) -> float:
        """
        Name: get_max_rate_of_area
        Parameters: -
        Returns: float
        Purpose: max_rate_of_area getter
        """
        return self.__max_rate_of_area

    def get_min_rate_of_area(self) -> float:
        """
        Name: get_min_rate_of_area
        Parameters: -
        Returns: float
        Purpose: min_rate_of_area_getter
        """
        return self.__min_rate_of_area

    def get_period(self) -> float:
        """
        Name: get_period
        Parameters: -
        Returns: float
        Purpose: period getter
        """
        return self.__period

    def set_period(self, value: float) -> None:
        """
        Name: set_period
        Parameters: value: float
        Returns: None
        Purpose: period setter
        """
        self.__period = value

    def draw(self, surface: pygame.Surface, scaling: float, shift: list) -> None:
        """
        Name: draw
        Parameters: surface: pygame.Surface, scaling: float, shift: list
        Returns: None
        Purpose: Draws a trail of previous positions and the body to the screen
        The trail is up to 256 positions long and each position is 1 point darker for each RGB value
        When drawing, the true position of each body is first scaled to a pixel value on screen and then shifted
        Zooming and panning change these scaling and shift values. The trail radius is 0.25 times than the body radius.
        """
        if len(self.__previous_positions) < 256:
            trail_length = len(self.__previous_positions)
        else:
            trail_length = 256
        for i in range(trail_length):
            colour = list(self.__colour)
            for j in range(3):
                if self.__colour[j] + (i + 1 - trail_length) < 0:
                    colour[j] = 0
                else:
                    colour[j] -= trail_length - i - 1
            if i == trail_length - 1:
                pygame.draw.circle(surface, colour,
                                   (self.__previous_positions[i - trail_length][0] / scaling + shift[0],
                                    self.__previous_positions[i - trail_length][1] / scaling + shift[1]),
                                   self.__visual_radius)
            else:
                pygame.draw.circle(surface, colour,
                                   (self.__previous_positions[i - trail_length][0] / scaling + shift[0],
                                    self.__previous_positions[i - trail_length][1] / scaling + shift[1]),
                                   self.__visual_radius / 4)

    def draw_velocity_arrow(self, surface: pygame.Surface, scaling: float, shift: tuple) -> None:
        """
        Name: draw_velocity_arrow
        Parameters: surface: pygame.Surface, scaling: float, shift: tuple
        Returns: None
        Purpose: Draws a velocity arrow representing the magnitude and direction of the body's velocity by its length
        and angle. The tip position is calculated adding a multiple of the velocity to the current position and then
        scaling and shifting to the right screen location. A purple line is drawn between here and the body's position.
        The angle of this line from vertical is calculated. Two smaller lines are drawn from the tip to be the arrowhead
        at the angle of the main line plus or minus 45 degrees.
        """
        tip = ((self.__position[0] + self.__velocity[0] * 4 * 10 ** 6) / scaling + shift[0],
               (self.__position[1] + self.__velocity[1] * 4 * 10 ** 6) / scaling + shift[1])
        pygame.draw.line(surface, (255, 0, 255), (self.__position[0] / scaling + shift[0],
                                                  self.__position[1] / scaling + shift[1]), tip)
        if self.__velocity[1] == 0:
            theta = -math.pi / 2
        else:
            theta = math.atan(self.__velocity[0] / -self.__velocity[1])
        if self.__velocity[1] < 0:
            theta += math.pi
        pygame.draw.line(surface, (255, 0, 255), tip,
                         (tip[0] + self.get_speed() * math.sin(theta + math.pi / 4) * 3 * 10 ** 5 / scaling,
                          tip[1] - self.get_speed() * math.cos(theta + math.pi / 4) * 3 * 10 ** 5 / scaling))
        pygame.draw.line(surface, (255, 0, 255), tip,
                         (tip[0] + self.get_speed() * math.sin(theta - math.pi / 4) * 3 * 10 ** 5 / scaling,
                          tip[1] - self.get_speed() * math.cos(theta - math.pi / 4) * 3 * 10 ** 5 / scaling))

    def draw_force_arrow(self, surface: pygame.Surface, scaling: float, shift: list) -> None:
        """
        Name: draw_force_arrow
        Parameters: surface: pygame.Surface, scaling: float, shift: list
        Returns: None
        Purpose: First calculates force vector, scaling acceleration by mass, and the magnitude using Pythagoras
        These are used in place of velocity and speed to draw green force arrows in the same way as the velocity arrows.
        """
        force = [self.__acceleration[0] * self.__mass, self.__acceleration[1] * self.__mass]
        force_magnitude = (force[0] ** 2 + force[1] ** 2) ** 0.5
        tip = ((self.__position[0] + force[0] / (1.5 * 10 ** 12)) / scaling + shift[0],
               (self.__position[1] + force[1] / (1.5 * 10 ** 12)) / scaling + shift[1])
        pygame.draw.line(surface, (0, 255, 0), (self.__position[0] / scaling + shift[0],
                                                self.__position[1] / scaling + shift[1]), tip)
        if force[1] == 0:
            theta = -math.pi / 2
        else:
            theta = math.atan(force[0] / -force[1])
        if force[1] < 0:
            theta += math.pi
        pygame.draw.line(surface, (0, 255, 0), tip,
                         (tip[0] + force_magnitude * math.sin(theta + math.pi / 4) / (2 * 10 ** 13) / scaling,
                          tip[1] - force_magnitude * math.cos(theta + math.pi / 4) / (2 * 10 ** 13) / scaling))
        pygame.draw.line(surface, (0, 255, 0), tip,
                         (tip[0] + force_magnitude * math.sin(theta - math.pi / 4) / (2 * 10 ** 13) / scaling,
                          tip[1] - force_magnitude * math.cos(theta - math.pi / 4) / (2 * 10 ** 13) / scaling))

    def calculate_data(self, central_body, time: float, dt: float) -> None:
        """
        Name: calculate_data
        Parameters: central_body: Body, time: float, dt: float
        Returns: None
        Purpose: Calculates all data for the body in the 'more data' tab in the edit window.
        """

        # if the body's x or y displacement has a different sign to the previous frame, this means the body has crossed
        # its initial x or y position and 1 is added to the corresponding index of the orbit list
        if ((self.__position[0] - self.__initial_position[0]) < 0) == (self.__displacement[0] >= 0):
            self.__orbit[0] += 1
        if (self.__position[1] - self.__initial_position[1]) < 0 == (self.__displacement[1] > 0):
            self.__orbit[1] += 1
        # the current displacement is saved, so it can be compared with displacement on the next frame
        self.__displacement = [self.__position[0] - self.__initial_position[0],
                               self.__position[1] - self.__initial_position[1]]
        # If a body has crossed its original x or y position twice, it has completed a full orbit and more data may be
        # calculated
        if self.__orbit[0] == 2 or self.__orbit[1] == 2:
            # due to slight inaccuracies in the simulation, the body may seem to cross its original x or y position
            # multiple times when it should actually only be once. This can only happen for one coordinate and not on
            # the first period. It results in very small values for period which are clearly anomalous, so I've
            # implemented a check that the period must be no smaller than 50 times the previous period
            if (time - self.__initial_time) * 50 > self.__period:
                # period is calculated from the current time subtract the time it was at the start of the orbit
                # initial position and time variables are set to current values
                self.__period = time - self.__initial_time
                self.__initial_position = list(self.__position)
                self.__initial_time = time
                # eccentricity of the elliptical orbit is calculated using the formula e = c/a where c is the distance
                # a focus to the centre and 'a' is the semi-major axis. An alternate form is the following.
                self.__eccentricity = (self.__apocentre_distance - self.__pericentre_distance) / (
                        self.__apocentre_distance + self.__pericentre_distance)
            # values of orbit are subtracted by 2 if greater than 0 because that's what makes it work
            if self.__orbit[0] > 0:
                self.__orbit[0] -= 2
            if self.__orbit[1] > 0:
                self.__orbit[1] -= 2
        # distance from central body is calculated using pythagoras
        distance_from_centre = ((self.__position[0] - central_body.get_position()[0]) ** 2 + (
                self.__position[1] - central_body.get_position()[1]) ** 2) ** 0.5
        # angular momentum is the product of mass, tangential velocity and distance from centre of rotation
        self.__angular_momentum = self.__mass * self.get_speed() * distance_from_centre
        # if the distance is greater than the current greatest distance from centre, or less than the current smallest
        # distance, they are updated
        if distance_from_centre > self.__apocentre_distance:
            self.__apocentre = list(self.__position)
            self.__apocentre_distance = distance_from_centre
        elif distance_from_centre < self.__pericentre_distance:
            self.__pericentre = list(self.__position)
            self.__pericentre_distance = distance_from_centre
        # if the body has completed one orbit around the central body, it will have correct values for period,
        # apocentre and pericentre so other data can be calculated from these
        if self.__period:
            # current distances from apocentre and pericentre calculated using pythagoras
            # if one distance was greater than the other on the previous frame, and now they have flipped, then the body
            # is very close to half-way between them and its position is assigned to a co-vertex
            distance_from_apocentre = ((self.__position[0] - self.__apocentre[0]) ** 2 + (
                self.__position[1] - self.__apocentre[1]) ** 2) ** 0.5
            distance_from_pericentre = ((self.__position[0] - self.__pericentre[0]) ** 2 + (
                self.__position[1] - self.__pericentre[1]) ** 2) ** 0.5
            if (distance_from_apocentre > distance_from_pericentre and
                    self.__distance_from_apocentre < self.__distance_from_pericentre):
                self.__co_vertex_1 = list(self.__position)
            elif (distance_from_apocentre < distance_from_pericentre and
                  self.__distance_from_apocentre > self.__distance_from_pericentre):
                self.__co_vertex_2 = list(self.__position)
            self.__distance_from_apocentre = distance_from_apocentre
            self.__distance_from_pericentre = distance_from_pericentre
        # rate of area swept out is calculated by approximating (very closely) the area between the current and previous
        # frames as a triangle. Using the change in displacement values from the calculate_position function, 0.5bh is
        # used to obtain area. This is divided by the time for one frame to get a rate.
        rate_of_area = 0.5 * distance_from_centre * (self.__delta_x ** 2 + self.__delta_y ** 2) ** 0.5 / dt
        # if it's greater than the current maximum value or less than the current minimum, those values are updated.
        if rate_of_area > self.__max_rate_of_area:
            self.__max_rate_of_area = rate_of_area
        elif rate_of_area < self.__min_rate_of_area:
            self.__min_rate_of_area = rate_of_area
