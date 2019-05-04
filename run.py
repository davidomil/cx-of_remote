import asyncio
import datetime
import sys

import pygame as pygame

from DroneControl import DroneControl
from configuration import *


def clamp(n, minn, maxn): return max(min(maxn, n), minn)


async def controller():
    pygame.init()
    screen = pygame.display.set_mode((576, 720))

    dc = DroneControl()
    asyncio.create_task(dc.loop())

    speed = 30
    jump = 60
    fast_multiplier = 2

    r = 127
    p = 127
    t = 127
    y = 127

    r_speed = 0
    p_speed = 0
    y_speed = 0

    r_speed_added = 0
    p_speed_added = 0
    y_speed_added = 0

    multiplier = 1

    last = datetime.datetime.now()
    while True:

        drone_cmd = SOME_DATA[:]

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                key = event.key
                if event.type == pygame.KEYDOWN:
                    direction = 1
                else:
                    direction = -1

                if key == pygame.K_ESCAPE or key == pygame.K_q:  # ESC
                    dc.disconnect()
                    pygame.quit()
                    return
                elif key == pygame.K_SEMICOLON:
                    drone_cmd = FLY_UP
                    print("UP")
                elif key == pygame.K_QUOTE:
                    print("LAND")
                    drone_cmd = LAND
                elif key == pygame.K_BACKSPACE:
                    print("DIE")
                    t = 0
                elif key == pygame.K_KP_ENTER:
                    print("Enter")
                elif key == pygame.K_LSHIFT:
                    multiplier = multiplier * (fast_multiplier ** direction)
                elif key == pygame.K_w:
                    p_speed += speed
                    if direction == -1:
                        p_speed = 0
                        p -= p_speed_added
                        p_speed_added = 0
                    p += direction * jump
                elif key == pygame.K_LEFT:
                    r_speed -= speed
                    if direction == -1:
                        r_speed = 0
                        r -= r_speed_added
                        r_speed_added = 0
                    r -= direction * jump
                elif key == pygame.K_s:
                    p_speed -= speed
                    if direction == -1:
                        p_speed = 0
                        p -= p_speed_added
                        p_speed_added = 0
                    p -= direction * jump
                elif key == pygame.K_RIGHT:
                    r_speed += speed
                    if direction == -1:
                        r_speed = 0
                        r -= r_speed_added
                        r_speed_added = 0
                    r += direction * jump
                elif key == pygame.K_DOWN and pygame.KEYDOWN:
                    t -= 5
                elif key == pygame.K_UP and pygame.KEYDOWN:
                    t += 5
                elif key == pygame.K_d:
                    y_speed += speed
                    if direction == -1:
                        y_speed = 0
                        y -= y_speed_added
                        y_speed_added = 0
                    y += direction * jump
                elif key == pygame.K_a:
                    y_speed -= speed
                    if direction == -1:
                        y_speed = 0
                        y -= y_speed_added
                        y_speed_added = 0
                    y -= direction * jump

        elapsed = (datetime.datetime.now() - last).total_seconds()
        last = datetime.datetime.now()
        r_speed_added += elapsed * r_speed * multiplier
        p_speed_added += elapsed * p_speed * multiplier
        y_speed_added += elapsed * y_speed * multiplier

        r += elapsed * r_speed * multiplier
        p += elapsed * p_speed * multiplier
        y += elapsed * y_speed * multiplier

        print(f"Roll: {r}; Pitch: {p}, Yaw: {y}, Throttle: {t}")
        print(f"Roll Speed: {r_speed}; Pitch Speed: {p_speed}; Yaw Speed: {y_speed}")
        print(f"Multiplier: {multiplier}; Elapsed: {elapsed}")

        r = clamp(r, 0, 255)
        p = clamp(p, 0, 255)
        t = clamp(t, 0, 255)
        y = clamp(y, 0, 255)

        drone_cmd[1] = int(r)
        drone_cmd[2] = int(p)
        drone_cmd[3] = int(t)
        drone_cmd[4] = int(y)

        dc.data = drone_cmd

        await asyncio.sleep(0.01)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(controller())
