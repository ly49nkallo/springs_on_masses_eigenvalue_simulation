import pygame as pg
import numpy as np
import render

NUM_MASSES = 3
WIDTH, HEIGHT = 1280, 720
FRAMERATE = 60

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(f"Mass-Spring-Ring System Simulation v.1.4.23, TARGET FPS:{FRAMERATE}")
clock = pg.time.Clock()
running = True
frame_count = 0
scale = 200. # How many pixels are in one unit length

X0 = np.linspace(0, 2 * np.pi, NUM_MASSES, endpoint=False)
X = np.zeros_like(X0)
dX0dt = np.array([1] + [0] * (NUM_MASSES - 1))  # Initial velocities, first and last masses have velocity 1, others are 0
k = 1
M = np.zeros((NUM_MASSES, NUM_MASSES), dtype=float)
for i in range(NUM_MASSES):
    M[i, i] = 2.0
    M[(i+1)%NUM_MASSES, i] = -1.
    M[(i-1)%NUM_MASSES, i] = -1.

eigenvalues, eigenvectors = np.linalg.eigh(M)
C_inv = np.linalg.inv(eigenvectors)
dydt = C_inv @ dX0dt

print("Eigenvalues:\n", eigenvalues)
print("Eigenvectors:\n", eigenvectors)
while running:
    # poll for events
    # pg.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
    

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    y = [0] * NUM_MASSES
    t = frame_count / FRAMERATE
    for i, ev in enumerate(eigenvalues):
        if np.abs(ev) < 1e-6:
            y[i] = dydt[i] * t
        else:
            y[i] = 1 / np.sqrt(ev) / np.sqrt(k) * np.sin(np.sqrt(ev) * t)
    X = eigenvectors @ np.array(y)
    # RENDER CODE
    render.render_circle(screen, scale)
    render.render_springs(screen, scale, X, X0)
    render.render_masses(screen, scale, X, X0)


    frame_count += 1
    if frame_count % FRAMERATE == 0:
        print(f"FPS: {clock.get_fps()}")
    pg.display.flip()

    clock.tick(FRAMERATE)

pg.quit()
