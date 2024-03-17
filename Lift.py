import pygame
import sys
import random
import mediapipe as mp
import cv2
import time


# Initialize Pygame
pygame.init()
gray = (150, 150, 150)
green = (35, 155, 86)
num_floors = 5
# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FLOOR_HEIGHT = 100
FLOOR_COLOR = (200, 200, 200)
LIFT_COLOR = (0, 0, 255)
BUTTON_COLOR_RESET = [gray for i in range(num_floors)]  # Gray color for buttons
BUTTON_COLOR = [gray for i in range(num_floors)]  # Gray color for buttons
FONT_SIZE = 24
BIG_FONT_SIZE = 48
SPACING = 20  # Spacing between components
cap = cv2.VideoCapture(0)
selected_floor = -1
val =0



# Load images
image = pygame.image.load("image.png")  # Replace with your image path
lift_art = pygame.image.load("lift_art.png")  # Replace with your image path
liftinside = pygame.image.load("liftinside.jpg")  # Replace with your image path
floor1 = pygame.image.load("floor.jpeg")  # Replace with your image path
floor2 = pygame.image.load("floor2.jpeg")  # Replace with your image path
floor3 = pygame.image.load("floor3.png")  # Replace with your image path
floor4 = pygame.image.load("floor4.png")  # Replace with your image path
floor5 = pygame.image.load("floor5.png")  # Replace with your image path
floors = {0: floor1, 1: floor2, 2: floor3, 3: floor4, 4: floor5}
# Get image dimensions
image_width, image_height = image.get_size()
lift_width, lift_height = lift_art.get_size()

# Calculate screen dimensions
SCREEN_WIDTH = max(SCREEN_WIDTH, image_width + lift_width + SPACING * 3 + (FLOOR_HEIGHT // 2))
SCREEN_HEIGHT = max(SCREEN_HEIGHT, image_height, FLOOR_HEIGHT * 1)  # Adjust as needed

# Calculate positions
image_x = SCREEN_WIDTH - image_width - SPACING
image_y = SPACING
lift_x = image_x - lift_width - SPACING  # Lift to the immediate left of the image
lift_y = image_y

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lift Game")

# Floor properties

floor_buttons = [pygame.Rect(100 * (i%2 + 1), i//2 * FLOOR_HEIGHT + FLOOR_HEIGHT // 4, 50, FLOOR_HEIGHT // 2) for i in range(num_floors)]

# Font setup
font = pygame.font.Font(None, FONT_SIZE)
big_font = pygame.font.Font(None, BIG_FONT_SIZE)

# Stick figure properties
stick_figure_color = (255, 0, 0)
stick_figure_head_radius = 6
stick_figure_body_length = 20

# Generate a random floor number to press
current_floor = random.randint(1, num_floors)
correct_floor_text = big_font.render(str(current_floor), True, (255, 255, 255))

timer_started = False
start_time = 0
duration = 5

def findPose():
    ret, frame = cap.read()
                
    # BGR 2 RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Flip on horizontal
    image = cv2.flip(image, 1)
    
    # Set flag
    image.flags.writeable = False
    
    # Detections
    results = hands.process(image)
    
    # Set flag to true
    image.flags.writeable = True
    
    # RGB 2 BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Detections
    
    # Rendering results
    if results.multi_hand_landmarks:
        landmark = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        return (landmark.x,landmark.y)
    else:
        return(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    
prev_button = 0
go_rect = pygame.draw.rect(screen, 'red', (100 * (num_floors%2 + 1), num_floors//2 * FLOOR_HEIGHT + FLOOR_HEIGHT // 4, 50, FLOOR_HEIGHT // 2))
go_text = font.render('GO', True, (255, 255, 255))  # White text color
go_text_rect = go_text.get_rect(center=(go_rect.centerx, go_rect.centery))
go_clicked = False 
feedback_text = ''
def pointer():
    # pos = pygame.mouse.get_pos()
    
    global timer_started,start_time,prev_button,selected_floor,current_floor,lift_y,go_clicked, feedback_text,val
    pos = findPose()
    pos = (pos[0]*SCREEN_WIDTH,pos[1]*SCREEN_HEIGHT)
    r = 25
    l = 20
    color = (25, 111, 61)
    pointer_ellipse = pygame.draw.ellipse(screen, color, (pos[0] - r/2, pos[1] - r/2, r, r), 4)
    pygame.draw.line(screen, color, (pos[0], pos[1] - l/2), (pos[0], pos[1] - l), 4)
    pygame.draw.line(screen, color, (pos[0] + l/2, pos[1]), (pos[0] + l, pos[1]), 4)
    pygame.draw.line(screen, color, (pos[0], pos[1] + l/2), (pos[0], pos[1] + l), 4)
    pygame.draw.line(screen, color, (pos[0] - l/2, pos[1]), (pos[0] - l, pos[1]), 4)

    for i,button in enumerate(floor_buttons):
        if pointer_ellipse.colliderect(button):
            BUTTON_COLOR[prev_button] = gray   
            prev_button = i
            selected_floor = i+1
            BUTTON_COLOR[i] = green

    if pointer_ellipse.colliderect(go_rect):
        if not go_clicked:
            if selected_floor == -1:
                val = 0
                feedback_text = "Please select a floor!"
            elif selected_floor == current_floor:
                feedback_text = "Yay Good Job!"
                val = selected_floor -1  # Green text color
            else:
                feedback_text = "Try Again"  # Red text color
                val= selected_floor-1
            go_clicked = True
            current_floor = random.randint(1, num_floors)

        result_text = big_font.render(feedback_text, True, (0, 255, 0))
        result_text_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(result_text, result_text_rect)
        lift_y = (selected_floor - 1) * FLOOR_HEIGHT
    else:
        go_clicked= False
        feedback_text = ''

import csv
# Create the font
font = pygame.font.SysFont('arial', 40)

def draw_start_menu():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    global username
    username = ''
    username_active = False

    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
    enter_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 50)
    enter_text = font.render('Enter', True, WHITE)
    enter_text_rect = enter_text.get_rect(center=(enter_button.centerx, enter_button.centery))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    username_active = True
                elif enter_button.collidepoint(event.pos) and username != '':
                    with open('names.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([username])
                    return  # Return to the main application
                else:
                    username_active = False
            elif event.type == pygame.KEYDOWN and username_active:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, input_box, 2)  # White border
        username_text = font.render(username, True, WHITE)  # White text color
        screen.blit(username_text, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, GREEN, enter_button)  # Green button
        screen.blit(enter_text, enter_text_rect)
        pygame.display.flip()

# Call start_screen before the main game loop
draw_start_menu()

# Main game loop
running = True


# Main game loop
running = True
mp_hands = mp.solutions.hands

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                        

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the image on the rightmost side with spacing
        screen.blit(image, (image_x, image_y))
        liftinside_width = (3 * SCREEN_WIDTH) // 4
        liftinside_height = SCREEN_HEIGHT
        liftinside_scaled = pygame.transform.scale(liftinside, (liftinside_width, liftinside_height))
        screen.blit(liftinside_scaled, (0, 0))
        # Draw lift


        floor_width = lift_width*4-30
        floor_height = lift_height*4-20
        floor_scaled = None  # default value
        if val < len(floors):
            floor_scaled = pygame.transform.scale(floors[val], (floor_width, floor_height))
            print(val)
            screen.blit(floor_scaled, (266, 160))
        else:
            print("Error: current_floor is not a valid index in the floors list.")
        # Draw button with text
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(80, 10, 190, 290))
        for i, button in enumerate(floor_buttons):
            button_rect = pygame.draw.rect(screen, BUTTON_COLOR[i], button)
            floor_text = font.render(str(i + 1), True, (255, 255, 255))  # White text color
            floor_text_rect = floor_text.get_rect(center=(button.centerx, button.centery))
            screen.blit(floor_text, floor_text_rect)

        # go buton

        go_text = font.render('GO', True, (0, 0, 0))  # Black text color
        screen.blit(go_text, go_text_rect)



        # Draw result text if available
      
        correct_floor_text = big_font.render("Please go to "+str(current_floor), True, (255, 255, 255))
        # Draw correct floor text
        correct_floor_text_rect = correct_floor_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + FLOOR_HEIGHT // 2))
        screen.blit(correct_floor_text, correct_floor_text_rect)
 
        
        pointer()            
        

        pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
