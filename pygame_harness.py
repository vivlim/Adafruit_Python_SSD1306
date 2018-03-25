import pygame

from menu.view_manager import ViewManager
from menu.vertical_list_view import VerticalListView
from menu.root_menu import RootMenu


size = (128, 64)
scale_factor = 4
viewport_size = tuple(i * scale_factor for i in size)
screen = pygame.display.set_mode(viewport_size)
pygame.display.flip()

running = True

root_view = RootMenu(size)

renderer = ViewManager(size, root_view, "RGB")
while running:
    pil_frame = renderer.get_frame()
    frame_bytes = pil_frame.tobytes()
    pygame_frame = pygame.image.frombuffer(frame_bytes, pil_frame.size, pil_frame.mode)

    pygame_scaled_frame = pygame.transform.scale(pygame_frame, viewport_size)

    screen.blit(pygame_scaled_frame, (0, 0) + viewport_size)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                renderer.handle_key('up')
            if event.key == pygame.K_DOWN:
                renderer.handle_key('down')
            if event.key == pygame.K_LEFT:
                renderer.handle_key('left')
            if event.key == pygame.K_RIGHT:
                renderer.handle_key('right')
            if event.key == pygame.K_z or event.key == pygame.K_a:
                renderer.handle_key('a')
            if event.key == pygame.K_x or event.key == pygame.K_b:
                renderer.handle_key('b')
            if event.key == pygame.K_c:
                renderer.handle_key('middle')
