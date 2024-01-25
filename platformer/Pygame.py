import pygame
from sys import exit
from random import randint

def display_score():
  current_time = int(pygame.time.get_ticks() / 1000) - start_time
  score_surf = my_Font.render(f'Score: {current_time}',False,(64,64,64))
  score_rect = score_surf.get_rect(center = (400,50))
  screen.blit(score_surf,score_rect)
  return current_time

def obstacle_movement(obstacle_list):
  if obstacle_list:
    for obstacle_rect in obstacle_list:
      obstacle_rect.x -= 7
      
      if obstacle_rect.bottom == 310: 
        screen.blit(enemy_surf,obstacle_rect) 
      else: 
        screen.blit(enemy_2_surf,obstacle_rect)

    obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

    return obstacle_list
  else: return []

def collisions(player, obstacles):
  if obstacles:
    for obstacle_rect in obstacles:
      if player.colliderect(obstacle_rect): 
        return False
  return True

pygame.init()
#display surface w/ a width of 800 and a length of 400
screen = pygame.display.set_mode((800,400))
#name of game
pygame.display.set_caption("Blocked")

#used to set fps
clock = pygame.time.Clock()
my_Font = pygame.font.Font('platformer/Pixel Font/Minecraft.ttf',45)
game_active = False
start_time = 0
score = 0


#backgrounds surfaces
Sky = pygame.image.load("platformer/Backgrounds/Sky.png").convert()
Floor = pygame.image.load("platformer/Backgrounds/ground.png").convert()


#player
player = pygame.image.load("platformer/Standing player.png").convert_alpha()
player_rect = player.get_rect(midbottom = (40,310))
player_gravity = 0

#intro screen
player_stand = pygame.image.load("platformer/Standing player.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,45,2.5)
player_stand_rect = player_stand.get_rect(center = (400,300))
game_name = my_Font.render("Blocked" , False, 'Yellow')
game_name_rect = game_name.get_rect(center = (400,50))
game_message = my_Font.render("press 'r' to run  ", False, 'Yellow')
game_message_rect = game_message.get_rect(center = (400,100))


#obstacles
enemy_surf = pygame.image.load("platformer/Enemy.png").convert_alpha()
enemy_2_surf = pygame.image.load("platformer/Obstacle.png").convert_alpha()

obstacle_rect_list = []

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1400)

#while loop that includes all code
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    if game_active:
      if event.type == pygame.KEYDOWN and player_rect.bottom >= 310:
        if event.key == pygame.K_SPACE:
          player_gravity = -20
      if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 310:
        if player_rect.collidepoint(event.pos):
          player_gravity = -20
          start_time = int(pygame.time.get_ticks() / 1000)
      if event.type == obstacle_timer:
          if randint(0,2):
            obstacle_rect_list.append(enemy_surf.get_rect(midbottom = (randint(900,1100),310)))
          else:
            obstacle_rect_list.append(enemy_2_surf.get_rect(midbottom = (randint(900,1100),210)))
    else:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        game_active = True
        start_time = int(pygame.time.get_ticks() / 1000)
  
  #background
  if game_active:
    screen.blit(Sky, (0,0))
    screen.blit(Floor, (0,300))
    score = display_score()
    
    #player
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 310: player_rect.bottom = 310
    screen.blit(player, player_rect)

    # Obstacle movement
    obstacle_rect_list = obstacle_movement(obstacle_rect_list)

    game_active = collisions(player_rect,obstacle_rect_list)
  else:
    screen.fill((94,129,162))
    screen.blit(game_name,game_name_rect)
    screen.blit(player_stand,player_stand_rect)
    current_score = my_Font.render(f"score: {score}", False, 'Yellow')
    current_score_rect = current_score.get_rect(center = (400,110))
    if score == 0:
      screen.blit(game_message,game_message_rect)
    else:
      screen.blit(current_score, current_score_rect)
    obstacle_rect_list.clear()
    player_rect.midbottom = (80,310)
    player_gravity =  0

  pygame.display.update()
  clock.tick(60)
  
  