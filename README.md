# Gravity Simulator

An interactive 2D N-body gravitational simulator written in Python using Pygame. Users can create arbitrary gravitational systems, simulate their evolution over time, and inspect physical and orbital properties in real time.

## Features

- Simulates arbitrary N-body gravitational systems
- Euler–Richardson/leapfrog numerical integration
- Interactive Pygame interface with zooming and panning
- Create and edit bodies with custom masses, positions and velocities
- Save and reopen gravitational systems
- Visualise trajectories and velocity vectors
- Calculate system properties including energy and momentum
- Calculate orbital parameters including eccentricity, semi-major axis, orbital period, apocentre and pericentre
- Investigate Kepler's laws and conservation laws numerically

## Physics

The simulator evolves each body under Newtonian gravitational forces from the other bodies in the system.

Time evolution uses a leapfrog integration scheme, updating positions and velocities around recalculated gravitational accelerations. This provides substantially better behaviour for orbital simulations than a simple forward-Euler method.

The simulator can be used to investigate quantities including:

- Total energy
- Linear and angular momentum
- Orbital eccentricity
- Apocentre and pericentre
- Semi-major and semi-minor axes
- Orbital period
- Rate of area swept by an orbiting body

## Interface

The Pygame interface allows users to construct systems, alter simulation parameters and inspect individual bodies or the system as a whole while the simulation runs.

## Running the project

Requires Python and Pygame.

```bash
pip install pygame
python main.py
```

## Example

