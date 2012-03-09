import pygame, sys
from random import randint

def load_image(image_name):
	''' The proper way to load an image '''
	try:
		image = pygame.image.load(image_name)
	except pygame.error, message:
		print "Cannot load image: " + image_name
		raise SystemExit, message
	return image.convert_alpha()


def load_sound(sound_name):
	''' Loads sound '''
	try:
		sound = pygame.mixer.Sound(sound_name)
	except pygame.error, message:
		print "Cannot load sound: " + sound_name
		raise SystemExit, message
	return sound

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X1 = 70
PADDLE_START_Y1 = 250
PADDLE_START_X2 = 720
PADDLE_START_Y2 = 250
PADDLE_WIDTH = 5
PADDLE_HEIGHT = 100
SPEED = 12
COMP_SPEED = 11
BALL_WIDTH_HEIGHT = 16
HL_WIDTH = 6
HL_HEIGHT = SCREEN_HEIGHT
HL_X = 397
HL_Y = 0

# Initializes
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# This is a rect that contains the ball at the beginning it is set in the center of the screen
pygame.Rect((SCREEN_WIDTH / 2, randint(1, SCREEN_HEIGHT/2)), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [SPEED,SPEED]

# Your paddle vertically centered on the left side
paddle_rect1 = pygame.Rect((PADDLE_START_X1, PADDLE_START_Y1), (PADDLE_WIDTH, PADDLE_HEIGHT))
paddle_rect2 = pygame.Rect((PADDLE_START_X2, PADDLE_START_Y2), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Half way line
halfway_line = pygame.Rect((HL_X, HL_Y), (HL_WIDTH, HL_HEIGHT)) 

# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
score_player = 0
score_comp = 0

# Load the font for displaying the score
font = pygame.font.Font(None, 50)

# Used for direction of padddle
direction = -1

# Represents what screen to go to
screen_id = 0

# Who is the winner of the game
winner = 0

# Game loop
while True:
	# Used to change screens and quit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				quit()
			elif event.key == pygame.K_RETURN:
				screen_id = 1
	
	if screen_id == 0:
		# Clear screen
		screen.fill((34, 139, 34))

		# Render the ball, the paddle, text, and the score
		pygame.draw.rect(screen, (184, 134, 11), paddle_rect1) # Your paddle
		pygame.draw.rect(screen, (64, 224, 208), paddle_rect2) # Your paddle
		pygame.draw.circle(screen, (255, 215, 0), ball_rect.center, ball_rect.width / 2) # The ball
		pygame.draw.rect(screen, (255, 255, 255), halfway_line) # Halfway line

		score_text_player = font.render("Player 1: " + str(score_player), True, (184, 134, 11))
		score_text_comp = font.render("Player 2: " + str(score_comp), True, (64, 224, 208))
		screen.blit(score_text_player, (100, 5)) # The score
		screen.blit(score_text_comp, (520, 5))

		instructions = font.render("Press ENTER/RETURN to begin", 1, (255, 215, 0))
		screen.blit(instructions, (122, 50))
		pygame.display.flip()

	elif screen_id == 1:
		# This test if up or down keys are pressed; if yes, move the paddle
		if pygame.key.get_pressed()[pygame.K_UP] and paddle_rect1.top > 0:
			paddle_rect1.top -= SPEED
		elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle_rect1.bottom < SCREEN_HEIGHT:
			paddle_rect1.top += SPEED

		if pygame.key.get_pressed()[pygame.K_w] and paddle_rect1.top > 0:
			paddle_rect1.top -= SPEED
		elif pygame.key.get_pressed()[pygame.K_s] and paddle_rect1.bottom < SCREEN_HEIGHT:
			paddle_rect1.top += SPEED

		# Update ball position
		ball_rect.left += ball_speed[0]
		ball_rect.top += ball_speed[1]

		# Ball collision with rails
		if ball_rect.top <= 0:
			ball_speed[1] = -ball_speed[1]
		if ball_rect.bottom >= SCREEN_HEIGHT:
			ball_speed[1] = -ball_speed[1]
		if ball_rect.right >= SCREEN_WIDTH:
			ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
			rand_ball_dir = randint(1,2) # Makes the direction of where the ball will travel (up/down) when reset random
			if rand_ball_dir == 1:				
				ball_speed[1] = -ball_speed[1]
			score_player += 1
		if ball_rect.left <= 0:
			ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
			rand_ball_dir = randint(1,2) # Makes the direction of where the ball will travel (up/down) when reset random
			if rand_ball_dir == 1:
				ball_speed[1] = -ball_speed[1]
			score_comp += 1

		# Test if the ball is hit by the paddle; if yes reverse speed and add a point
		if paddle_rect1.colliderect(ball_rect):
			sound = load_sound("laser.wav")
			sound.play()
			ball_speed[0] = -ball_speed[0]
		if paddle_rect2.colliderect(ball_rect):
			sound = load_sound("laser.wav")
			sound.play()
			ball_speed[0] = -ball_speed[0]

		#Switch direction if ball is moving up, it is above paddle, and paddle is moving down
		if ball_speed[1] < 0 and ball_rect.top <= paddle_rect2.top and direction == 1:
			direction *= -1
		#Switch direction if ball is moving down, it is below paddle, and paddle is moving up
		if ball_speed[1] > 0 and ball_rect.bottom >= paddle_rect2.bottom and direction == -1:
			direction *= -1
		#Switch direction if ball is moving down, it is above the paddle, and the paddle is moving down
		if ball_speed[1] > 0 and ball_rect.top <= paddle_rect2.top and direction == 1:
			direction *= -1
		#Switch direction if ball is moving up, it is below the paddle, and the paddle is moving up
		if ball_speed[1] < 0 and ball_rect.bottom >= paddle_rect2.bottom and direction == -1:
			direction *= -1
		#IT IS POSSIBLE TO WIN, just very hard

		# Move second paddle
		if paddle_rect2.top >= 0 and direction == -1:
			paddle_rect2.top -= COMP_SPEED
		else:
			paddle_rect2.top += COMP_SPEED
		if paddle_rect2.top <= 0 or paddle_rect2.bottom >= SCREEN_HEIGHT:
			direction *= -1

		# Clear screen
		screen.fill((34, 139, 34))

		# Render the ball, the paddle, and the score
		pygame.draw.rect(screen, (184, 134, 11), paddle_rect1) # Your paddle
		pygame.draw.rect(screen, (64, 224, 208), paddle_rect2) # Your paddle
		pygame.draw.circle(screen, (255, 215, 0), ball_rect.center, ball_rect.width / 2) # The ball
		pygame.draw.rect(screen, (255, 255, 255), halfway_line) # Halfway line

		score_text_player = font.render("Player 1: " + str(score_player), True, (184, 134, 11))
		score_text_comp = font.render("Player 2: " + str(score_comp), True, (64, 224, 208))
		screen.blit(score_text_player, (100, 5)) # The score
		screen.blit(score_text_comp, (520, 5))

		# Checks if anyone has won
		if score_player == 11:
			winner = 1
			score_player = 0
			score_comp = 0
			screen_id += 1
		if score_comp == 11:
			winner = 2
			score_player = 0
			score_comp = 0
			screen_id += 1

		# Update screen and wait 20 milliseconds
		pygame.display.flip()
		pygame.time.delay(20)

	else:
		# Clear screen
		screen.fill((34, 139, 34))
		
		paddle_rect1 = pygame.Rect((PADDLE_START_X1, PADDLE_START_Y1), (PADDLE_WIDTH, PADDLE_HEIGHT))
		paddle_rect2 = pygame.Rect((PADDLE_START_X2, PADDLE_START_Y2), (PADDLE_WIDTH, PADDLE_HEIGHT))

		# Render the ball, the paddle, and the score
		pygame.draw.rect(screen, (184, 134, 11), paddle_rect1) # Your paddle
		pygame.draw.rect(screen, (64, 224, 208), paddle_rect2) # Your paddle
		pygame.draw.circle(screen, (255, 215, 0), ball_rect.center, ball_rect.width / 2) # The ball
		pygame.draw.rect(screen, (255, 255, 255), halfway_line) # Halfway line

		# Shows important text
		score_text_player = font.render("Player 1: " + str(score_player), True, (184, 134, 11))
		score_text_comp = font.render("Player 2: " + str(score_comp), True, (64, 224, 208))
		screen.blit(score_text_player, (100, 5)) # The score
		screen.blit(score_text_comp, (520, 5))

		instructions = font.render("Press ENTER/RETURN to begin", 1, (255, 215, 0))
		screen.blit(instructions, (122, 50))

		win_text = font.render("Player " + str(winner) + " won!", 1, (255, 215, 0))
		screen.blit(win_text, (280, 100))

		pygame.display.flip()


