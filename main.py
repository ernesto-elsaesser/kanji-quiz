import pygame
import random
import json
import os

# --- Configuration ---
KANJI_FILE = 'kanji_dictionary.json'
FONT_NAME = 'dejavusansmono'
FONT_SIZE_KANJI = 100
FONT_SIZE_OPTIONS = 40
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
CORRECT_COLOR = (0, 200, 0)
INCORRECT_COLOR = (200, 0, 0)
SELECTED_COLOR = (100, 100, 255)
FEEDBACK_DURATION_MS = 1500

# --- Pygame Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kanji Trainer")

# Load custom font if available, otherwise use default
try:
    font_kanji = pygame.font.Font(FONT_NAME, FONT_SIZE_KANJI)
    font_options = pygame.font.Font(FONT_NAME, FONT_SIZE_OPTIONS)
except:
    font_kanji = pygame.font.SysFont("dejavusans", FONT_SIZE_KANJI) # Fallback to a common system font
    font_options = pygame.font.SysFont("dejavusans", FONT_SIZE_OPTIONS)

# --- Load Kanji Dictionary ---
def load_kanji_dictionary(filename):
    if not os.path.exists(filename):
        # Create a dummy file if it doesn't exist
        dummy_data = {
            "日": "day, sun",
            "月": "month, moon",
            "火": "fire",
            "水": "water",
            "木": "tree, wood",
            "金": "gold, money",
            "土": "earth, soil",
            "山": "mountain",
            "川": "river",
            "田": "rice field"
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dummy_data, f, ensure_ascii=False, indent=4)
        print(f"Created a dummy '{filename}' as it was not found. Please modify it with your kanji data.")

    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

kanji_dict = load_kanji_dictionary(KANJI_FILE)
kanji_list = list(kanji_dict.keys())

if not kanji_list:
    print("Error: Kanji dictionary is empty. Please add kanji entries to 'kanji_dictionary.json'.")
    pygame.quit()
    exit()

# --- Game State ---
current_kanji = ""
current_options = []
correct_answer_index = -1
selected_option_index = 0
show_feedback = False
feedback_text = ""
feedback_color = TEXT_COLOR
feedback_timer = 0

# --- Game Functions ---
def get_new_question():
    global current_kanji, current_options, correct_answer_index, selected_option_index
    current_kanji = random.choice(kanji_list)
    correct_meaning = kanji_dict[current_kanji]

    # Generate wrong options
    wrong_options = []
    other_meanings = [v for k, v in kanji_dict.items() if k != current_kanji]
    
    # Ensure we don't pick the same meaning multiple times if some kanji share meanings
    unique_other_meanings = list(set(other_meanings) - {correct_meaning})

    # Pick 3 wrong options, or fewer if not enough unique meanings exist
    num_wrong_options = min(3, len(unique_other_meanings))
    wrong_options = random.sample(unique_other_meanings, num_wrong_options)

    # Combine and shuffle options
    current_options = wrong_options + [correct_meaning]
    random.shuffle(current_options)

    correct_answer_index = current_options.index(correct_meaning)
    selected_option_index = 0  # Reset selection

def display_question():
    screen.fill(BACKGROUND_COLOR)

    # Display Kanji
    kanji_text_surface = font_kanji.render(current_kanji, True, TEXT_COLOR)
    kanji_rect = kanji_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(kanji_text_surface, kanji_rect)

    # Display Options
    option_y_start = SCREEN_HEIGHT // 2
    option_spacing = FONT_SIZE_OPTIONS + 10
    
    for i, option in enumerate(current_options):
        color = TEXT_COLOR
        if i == selected_option_index:
            color = SELECTED_COLOR
        
        option_text_surface = font_options.render(f"{i+1}. {option}", True, color)
        option_rect = option_text_surface.get_rect(midleft=(SCREEN_WIDTH // 8, option_y_start + i * option_spacing))
        screen.blit(option_text_surface, option_rect)

    # Display Feedback
    if show_feedback:
        feedback_surface = font_options.render(feedback_text, True, feedback_color)
        feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 7 // 8))
        screen.blit(feedback_surface, feedback_rect)

    pygame.display.flip()

# --- Game Loop ---
get_new_question()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not show_feedback:
                if event.key == pygame.K_UP:
                    selected_option_index = (selected_option_index - 1) % len(current_options)
                elif event.key == pygame.K_DOWN:
                    selected_option_index = (selected_option_index + 1) % len(current_options)
                elif event.key == pygame.K_a or event.key == pygame.K_RETURN:  # A button or Enter for PC testing
                    if selected_option_index == correct_answer_index:
                        feedback_text = "Correct!"
                        feedback_color = CORRECT_COLOR
                    else:
                        feedback_text = f"Incorrect. The correct answer was: {current_options[correct_answer_index]}"
                        feedback_color = INCORRECT_COLOR
                    show_feedback = True
                    feedback_timer = pygame.time.get_ticks()

    if show_feedback:
        if pygame.time.get_ticks() - feedback_timer > FEEDBACK_DURATION_MS:
            show_feedback = False
            get_new_question()

    display_question()
    pygame.time.Clock().tick(60) # Limit frame rate

pygame.quit()
