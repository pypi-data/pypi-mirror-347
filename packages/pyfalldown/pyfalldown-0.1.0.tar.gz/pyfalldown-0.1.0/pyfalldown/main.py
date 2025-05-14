import asyncio

import pygame

from pyfalldown.ui import UI


async def run() -> None:
    pygame.init()
    ui = UI()
    await ui.run()
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(run())
