import pygame as pg
import numpy as np

def render_circle(surface:pg.Surface, scale:float):
    pg.draw.circle(
        surface=surface,
        color=[100, 100, 100],
        center = (surface.get_width() // 2, surface.get_height() // 2),
        radius = int(scale) + int(0.05 * scale) // 2,
        width = int(0.05 * scale)
    )
    pg.draw.line(
        surface=surface,
        color=[0, 0, 0],
        start_pos=(surface.get_width() // 2, surface.get_height() // 2),
        end_pos=(surface.get_width() // 2 + scale, surface.get_height() // 2),
        width=int(0.02 * scale)
    )

def render_masses(surface:pg.Surface, scale:float, X, X0):
    for S_theta, theta_0 in zip(X, X0):
        pos = pg.Vector2(surface.get_width() // 2, surface.get_height() // 2)
        pos += pg.Vector2(scale, 0.).rotate_rad(S_theta + theta_0)
        pg.draw.circle(
            surface=surface,
            color=[0, 0, 0],
            center = pos,
            radius = int(0.1 * scale),
            width=0 # filled in
        )

def render_springs(surface:pg.surface, scale:float, X:np.ndarray, X0:np.ndarray):
    num_of_turns = 10
    l = len(X)
    center = pg.Vector2(surface.get_width() / 2, surface.get_height() / 2)
    for i, (S_theta, theta_0) in enumerate(zip(X, X0)):
        # figure out the mass immediately to the left
        S_theta_left = X[(i+1)%l]
        theta_0_left = X0[(i+1)%l]
        delta_S_theta = S_theta_left - S_theta
        delta_theta_0 = theta_0_left - theta_0
        delta_theta = delta_S_theta + delta_theta_0
        if delta_theta < 0:
            delta_theta += 2 * np.pi
        spacing = delta_theta / num_of_turns / 2
        for j in range(num_of_turns * 2):
            # calculate the position of the current segment
            pos1 = pg.Vector2(scale, 0.).rotate_rad(S_theta + theta_0 + (j) * spacing)
            pos2 = pg.Vector2(scale, 0.).rotate_rad(S_theta + theta_0 + (j + 1) * spacing)
            # displace
            if j % 4 == 0:
                pos2 *= 1.1
            elif j % 4 == 1:
                pos1 *= 1.1
            elif j % 4 == 2:
                pos2 *= 0.9
            else:
                pos1 *= 0.9
            # translate to the center of the screen
            pos1 += center
            pos2 += center
            pg.draw.line(
                surface=surface,
                color=[255 * int(j % 2 == 0), 0, 0],
                start_pos=pos1,
                end_pos=pos2,
                width=int(max(0.01 * scale, 1))
            )
