import pygame
import subprocess


class VideoSprite(pygame.sprite.Sprite):
    FFMPEG_BIN = "/usr/bin/ffmpeg"  # Full path to ffmpeg executable

    def __init__(self, rect, filename, FPS=25):
        pygame.sprite.Sprite.__init__(self)
        command = [self.FFMPEG_BIN,
                   '-loglevel', 'quiet',
                   '-i', filename,
                   '-f', 'image2pipe',
                   '-s', '%dx%d' % (rect.width, rect.height),
                   '-pix_fmt', 'rgb24',
                   '-vcodec', 'rawvideo', '-']
        self.bytes_per_frame = rect.width * rect.height * 3
        self.proc = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=self.bytes_per_frame * 3)
        self.image = pygame.Surface((rect.width, rect.height), pygame.HWSURFACE)
        self.rect = self.image.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y
        # Used to maintain frame-rate
        self.last_at = 0  # time frame starts to show
        self.frame_delay = 1000 / FPS  # milliseconds duration to show frame
        self.video_stop = False

    def update(self):
        if (not self.video_stop):
            time_now = pygame.time.get_ticks()
            if (time_now > self.last_at + self.frame_delay):  # has the frame shown for long enough
                self.last_at = time_now
                try:
                    raw_image = self.proc.stdout.read(self.bytes_per_frame)
                    self.image = pygame.image.frombuffer(raw_image, (self.rect.width, self.rect.height), 'RGB')
                    # self.proc.stdout.flush()  - doesn't seem to be necessary
                except:
                    # error getting data, end of file?  Black Screen it
                    self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA, 32)

                    self.image= self.image.convert_alpha()
                    self.video_stop = True

"""
### Create Video Area
video_sprite1 = VideoSprite(pygame.Rect(100, 100, 320, 240), 'd.mp4')
video_sprite2 = VideoSprite(pygame.Rect(100, 100, 160, 90), 'dd.mp4')  # 640x360
# sprite_group = pygame.sprite.GroupSingle()
sprite_group = pygame.sprite.Group()
sprite_group.add(video_sprite2)

# Window size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
WINDOW_SURFACE = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE

DARK_BLUE = (3, 5, 54)

### initialisation
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW_SURFACE)
pygame.display.set_caption("Video Sprite")
### Main Loop
clock = pygame.time.Clock()
done = False
while not done:

    # Handle user-input
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            done = True
        elif (event.type == pygame.MOUSEBUTTONUP):
            # On mouse-click
            pass

    # Movement keys
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP]):
        video_sprite2.rect.y -= 10
    if (keys[pygame.K_DOWN]):
        video_sprite2.rect.y += 10
    if (keys[pygame.K_LEFT]):
        video_sprite2.rect.x -= 10
    if (keys[pygame.K_RIGHT]):
        video_sprite2.rect.x += 10

    # Update the window, but not more than 60fps
    sprite_group.update()
    window.fill(DARK_BLUE)
    sprite_group.draw(window)
    pygame.display.flip()

    # Clamp FPS# matching my video file

pygame.quit()"""