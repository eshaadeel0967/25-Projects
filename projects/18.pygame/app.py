import random
import time
import os

# Initialize game variables
canvas_width = 50
canvas_height = 20
player_pos = 25
score = 0
aliens = [random.randint(0, canvas_width - 1) for _ in range(5)]
bullets = []
game_over = False

# Game constants
player_speed = 2
bullet_speed = 1
alien_speed = 1


# Game logic functions
def move_player():
    global player_pos
    move = input("Move (a: left, d: right, q: quit): ").strip().lower()
    if move == 'a' and player_pos > 0:
        player_pos -= player_speed
    elif move == 'd' and player_pos < canvas_width - 1:
        player_pos += player_speed
    elif move == 'q':
        return "quit"


def shoot_bullet():
    global bullets
    bullets.append({'x': player_pos, 'y': canvas_height - 2})


def move_bullets():
    global bullets
    for bullet in bullets:
        bullet['y'] -= bullet_speed
    bullets = [bullet for bullet in bullets if bullet['y'] >= 0]
    return bullets


def move_aliens():
    global aliens
    for i in range(len(aliens)):
        if aliens[i] < canvas_width - 1:
            aliens[i] += alien_speed
        else:
            aliens[i] = 0


def check_collisions():
    global bullets, aliens, score
    for bullet in bullets:
        for i, alien in enumerate(aliens):
            if alien - 1 <= bullet['x'] <= alien + 1 and bullet['y'] == 1:
                aliens[i] = random.randint(0, canvas_width - 1)  # Reset alien
                bullets.remove(bullet)  # Remove the bullet
                score += 1
                break


def check_game_over():
    global aliens, game_over
    if any(alien >= canvas_height - 1 for alien in aliens):
        game_over = True


# Drawing the game state
def draw_canvas():
    global player_pos, aliens, bullets, canvas_width, canvas_height

    # Create an empty canvas
    canvas = [[' ' for _ in range(canvas_width)] for _ in range(canvas_height)]

    # Place player
    canvas[canvas_height - 1][player_pos] = '🚀'

    # Place bullets
    for bullet in bullets:
        if bullet['y'] >= 0:
            canvas[bullet['y']][bullet['x']] = '|'

    # Place aliens
    for alien in aliens:
        if alien < canvas_width:
            canvas[0][alien] = '👾'

    # Display canvas
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen for better visualization
    for row in canvas:
        print(''.join(row))

    print(f"Score: {score}")


# Game loop
while not game_over:
    draw_canvas()

    # Move player and shoot
    action = input("Move (a: left, d: right, q: quit) or Shoot (space): ").strip().lower()
    if action == 'a' or action == 'd':
        move_player()
    elif action == ' ':
        shoot_bullet()
    elif action == 'q':
        print("Quitting the game...")
        break

    # Move bullets and aliens
    bullets = move_bullets()
    move_aliens()
    check_collisions()
    check_game_over()

    # Delay for next game loop iteration
    time.sleep(0.1)

# Game over message
if game_over:
    print("\nGame Over! You've been invaded by aliens!")
    print(f"Final Score: {score}")

