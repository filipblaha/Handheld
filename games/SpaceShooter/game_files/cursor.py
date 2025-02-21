import pygame
from screensetup import ScreenSetup


class Cursor(pygame.sprite.Sprite):
    """
    Class for cursor and crosshair.

    Calling the constructor makes the mouse invisible and creates a custom cursor in its position.
    """
    def __init__(self):
        super().__init__()
        # cursor
        self.cursor_image = pygame.image.load("assets/images/cursor.png")
        self.cursor_image = pygame.transform.scale_by(self.cursor_image, ScreenSetup.width / 960)
        self.cursor_image = pygame.Surface.convert_alpha(self.cursor_image)
        # crosshair
        self.crosshair_image = pygame.image.load("assets/images/crosshair.png")
        self.crosshair_image = pygame.transform.scale_by(self.crosshair_image, ScreenSetup.width / 960)
        self.crosshair_image = pygame.Surface.convert_alpha(self.crosshair_image)
        self.is_crosshair = False
        # setting up
        pygame.mouse.set_visible(False)
        self.image = self.cursor_image
        self.rect = self.image.get_rect()

    def update(self) -> None:
        """
        Updates the position of the cursor and crosshair
        :return: None
        """
        if self.is_crosshair:
            self.rect.center = pygame.mouse.get_pos()
        else:
            self.rect.topleft = pygame.mouse.get_pos()

    def set_cursor(self) -> None:
        """
        Sets the mouse image to the cursor
        :return: None
        """
        self.image = self.cursor_image
        self.rect = self.image.get_rect()
        self.is_crosshair = False

    def set_crosshair(self) -> None:
        """
        Sets the mouse image to the crosshair
        :return: None
        """
        self.image = self.crosshair_image
        self.rect = self.image.get_rect()
        self.is_crosshair = True

    def destroy(self) -> None:
        """
        Kills the object and sets the mouse visible
        :return: None
        """
        pygame.mouse.set_visible(True)
        self.kill()
