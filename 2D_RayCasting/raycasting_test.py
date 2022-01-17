import pygame
from Boundary import Boundary
from Polygon import Polygon
from Player import Player
from Ray import Ray
from Colors import BLACK

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Raycasting Demo")

SIM_RUNNING = True
SIM_PAUSED = False
MAX_FPS = 60


def Draw(window, to_draw, boundaries):
    window.fill(BLACK)
    for item in to_draw:
        item.draw(window)
        if item.tag == "ray":
            item.cast(window, boundaries)
    pygame.display.update()

def main():
    pygame.init()

    global SIM_RUNNING
    global SIM_PAUSED

    clock = pygame.time.Clock()

    b1 = Boundary([10.0, 10.0], [10.0, 590.0])
    b2 = Boundary([10.0, 590.0], [790.0, 590.0])
    b3 = Boundary([790.0, 590.0], [790.0, 10.0])
    b4 = Boundary([790.0, 10.0], [10.0, 10.0])

    boundaries = []
    boundaries.append(b1)
    boundaries.append(b2)
    boundaries.append(b3)
    boundaries.append(b4)

    # r1 = Ray(400, 300, -30.0)
    # r2 = Ray(400, 300, 0.0)
    # r3 = Ray(400, 300, 0.0)
    # r4 = Ray(400, 300, 0.0)
    # r5 = Ray(400, 300, 0.0)
    # r6 = Ray(400, 300, 0.0)
    # r7 = Ray(400, 300, 0.0)
    # r8 = Ray(400, 300, 0.0)
    
    player = Player([400, 300], 20) # upto to 1000 eyes is okay

    to_draw = []
    to_draw.append(b1)
    to_draw.append(b2)
    to_draw.append(b3)
    to_draw.append(b4)

    polys = []
    for i in range(5):
        p = Polygon()
        polys.append(p)
        boundaries += p.sides
        to_draw.append(p)

    to_draw += player.getRays()
    # to_draw.append(r1)
    # to_draw.append(r2)
    # to_draw.append(r3)
    # to_draw.append(r4)
    # to_draw.append(r5)
    # to_draw.append(r6)
    # to_draw.append(r7)
    # to_draw.append(r8)

    while SIM_RUNNING:
        clock.tick(MAX_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SIM_RUNNING = False
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.MOUSEMOTION:
                mousePos = list(pygame.mouse.get_pos())
                # print(mousePos)
                player.setPosition(mousePos)
                # r1.setAngleFromPos(mousePos)
                # r2.setAngle((r1.angle + 45.0) )
                # r3.setAngle((r1.angle + 90.0) )
                # r4.setAngle((r1.angle + 135.0) )
                # r5.setAngle((r1.angle + 180.0) )
                # r6.setAngle((r1.angle + -45.0) )
                # r7.setAngle((r1.angle + -90.0) )
                # r8.setAngle((r1.angle + -135.0) )
            
            Draw(window, to_draw, boundaries)

    print("Terminating Simulation...")
    pygame.quit()


if __name__ == "__main__":
    main()