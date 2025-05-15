from .pyvidplayer import Video
import pygame as pg

class UTNVideoPlayer(Video):
    
    def __init__(self, path, screen: pg.Surface):
        super().__init__(path)
        self.__screen = screen
        self.__video_initial_time = 0
        self.__video_length_time = None
    
    def run_video(self, size: tuple):
        self.set_size((size[0], size[1]))
        self.set_volume(0.3)
        self.__video_initial_time = int(pg.time.get_ticks() / 1000)
        if not self.__video_length_time:
            self.__video_length_time = self.duration
            
        running = True
        while running:
            if self.active:
                
                self.set_volume(0.9)
                self.draw(self.__screen, (0, 0))
            else:
                running = False
                self.close()
            current_time = int(pg.time.get_ticks() / 1000)
            if current_time - self.__video_initial_time >= self.__video_length_time:
                running = False
                self.close()
            
            running = self.check_close_event(running)
            pg.display.update()
        pg.display.update()
    
    def check_close_event(self, running: bool):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.close()
                running = False
                break
        return running