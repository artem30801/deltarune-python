from game_construcor import *


#pygame.time.wait(5000)

chapter1 = Game(kris)

set_current_game(chapter1)
chapter1.main_loop()

print(current_game)

pygame.quit()
