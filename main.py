import os
import pygame
import button
import random

pygame.init()
#for sound
pygame.mixer.init()
correct_sound = pygame.mixer.Sound(os.path.join('335908__littlerainyseasons__correct.mp3'))
wrong_sound = pygame.mixer.Sound(os.path.join('648462__andreas__wrong-answer.mp3'))
hint_sound = pygame.mixer.Sound(os.path.join('265387__b_lamerichs__sound-effects-01-03-2015-9-click-4.wav'))


# update the points score
def update_score(current_score, is_correct):
    if is_correct:
        return current_score + 1
    else:
        return current_score

# recursion for points
def recursive_update_score(score, is_correct, attempts):
    if attempts == 0:
        return score
    else:
        updated_score = update_score(score, is_correct)
        return recursive_update_score(updated_score, is_correct, attempts - 1)

# Create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("apcsa final")

# game variables
scrambled_word = ""
correct_word = ""
input_text = ""
hints_used = 0
max_hints = 3
revealed_letters = []
points = 0
game_mode = "menu"
definition_pair = ("", "", "")

#fonts
font = pygame.font.SysFont("Consolas", 40)
small_font = pygame.font.SysFont("Consolas", 30)

#colors
TEXT_COL = (255, 255, 255)

#buttons
hint_img = pygame.image.load("button_hint.png").convert_alpha()
mode1_img = pygame.image.load("button_mode1.png").convert_alpha()
mode2_img = pygame.image.load("button_mode2.png").convert_alpha()
hint_button = button.Button(230, 100, hint_img, 0.07)
mode1_button = button.Button(200, 200, mode1_img, 0.15)
mode2_button = button.Button(200, 300, mode2_img, 0.15)

#print to screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# to make the text fit
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = words[0]
    for word in words[1:]:
        if font.size(current_line + ' ' + word)[0] <= max_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

# randomizes the word letters
def scramble_word(word):
    word_list = list(word)
    random.shuffle(word_list)
    scrambled_word = ''.join(word_list)
    return scrambled_word

# randomize the words
def scramble_words_from_list(words):
    scrambled_list = [scramble_word(word) for word in words]
    return scrambled_list

# i tried finding a way to randomize filtered words on pydictionary but it was too much so i asked ai for help (chatgpt)
words = [
    "apple", "banana", "carrot", "dolphin", "elephant", "flower", "guitar", "happiness",
    "island", "jungle", "kitten", "lemon", "mountain", "notebook", "ocean", "pencil",
    "quilt", "rainbow", "sunshine", "tiger", "umbrella", "violet", "whistle",
    "xylophone", "yogurt", "zebra", "breeze", "candle", "donut", "feather"
]
words2 = [
    "ascertain",
    "corroborate","extrapolate","juxtapose","elucidate",
    "ameliorate","propagate","sublimate","delineate",
    "expedite","circumvent","enumerate","instantiate",
    "perpetuate","exacerbate","ostracize","vindicate",
    "consolidate","relinquish","amalgamate"
]
definitions = {
    "ascertain": ("To find something with certainty", "To ignore  details"),
    "corroborate": ("To confirm a statement", "To refute a claim"),
    "extrapolate": ("To conclude with known information", "To discard known information"),
    "juxtapose": ("To place things side by side for comparison", "To blend different things together"),
    "elucidate": ("To make something clear by explaining it", "To obscure the meaning of something"),
    "ameliorate": ("To make something unsatisfactory better", "To make a situation worse"),
    "propagate": ("To promote an idea, or theory widely", "To keep an idea secret"),
    "sublimate": ("To modify an impulse to be socially acceptable", "To do an impulse directly"),
    "delineate": ("To describe or portray something precisely", "To describe something vaguely"),
    "expedite": ("To make a process more quickly", "To delay the progress of something"),
    "circumvent": ("To find a way around something in a clever way", "To confront something"),
    "enumerate": ("To mention a number of things one by one", "To summarize without specifics"),
    "perpetuate": ("To make something an unfounded belief", "To stop something"),
    "exacerbate": ("To make a problem worse", "To fix a bad situation"),
    "ostracize": ("To exclude someone from a group", "To welcome someone"),
    "vindicate": ("To clear someone of blame", "To accuse someone "),
    "consolidate": ("To make something stronger", "To separate into parts"),
    "relinquish": ("To voluntarily let something go", "To hold onto something"),
    "amalgamate": ("To combine to form a structure", "To break into separate parts")
}
scrambled_words = scramble_words_from_list(words)

# random functions for words and definitions for both modes
def get_random_scrambled_word():
    global scrambled_word, correct_word, hints_used, revealed_letters
    correct_word = random.choice(words)
    scrambled_word = scramble_word(correct_word)
    hints_used = 0
    revealed_letters = ["_"] * len(correct_word)

def reveal_letter():
    global hints_used
    if hints_used < max_hints:
        indices = [i for i, letter in enumerate(correct_word) if revealed_letters[i] == "_"]
        if indices:
            reveal_index = random.choice(indices)
            revealed_letters[reveal_index] = correct_word[reveal_index]
            hints_used += 1

def get_random_definition():
    global definition_pair
    word = random.choice(words2)
    correct_def, incorrect_def = definitions[word]
    if random.choice([True, False]):
        definition_pair = (word, correct_def, incorrect_def)
    else:
        definition_pair = (word, incorrect_def, correct_def)

# get scrambled word
get_random_scrambled_word()

# game loop
run = True
while run:
    screen.fill((100, 78, 91))

    if game_mode == "menu":
        draw_text("Pick a game mode", font, TEXT_COL, 210, 100)
        draw_text("Guess the word", small_font, TEXT_COL, 290, 220)
        draw_text("Pick the definition", small_font, TEXT_COL, 290, 320)
        if mode1_button.draw(screen):
            game_mode = "scramble"
            get_random_scrambled_word()
        if mode2_button.draw(screen):
            game_mode = "definition"
            get_random_definition()

    elif game_mode == "scramble":
        draw_text(f"Points: {points}", font, TEXT_COL, 300, 50)
        draw_text(f"Hints used: {hints_used}/{max_hints}", small_font, TEXT_COL, 275, 105)
        draw_text(f"Scrambled Word: {scrambled_word}", small_font, TEXT_COL, 160, 200)
        draw_text(f"Your Guess: {input_text}", small_font, TEXT_COL, 160, 250)
        draw_text(f"Revealed Letters: {' '.join(revealed_letters)}", small_font, TEXT_COL, 160, 350)
        draw_text("Press SPACE to quit", small_font, TEXT_COL, 410, 550)

        #hint button
        if hints_used < max_hints and hint_button.draw(screen):
            hint_sound.play()
            reveal_letter()

    elif game_mode == "definition":
        word, def1, def2 = definition_pair
        draw_text(f"Points: {points}", font, TEXT_COL, 300, 50)
        draw_text("Press SPACE to quit", small_font, TEXT_COL, 410, 550)
        draw_text(f"Word: {word}", font, TEXT_COL, 150, 180)

        def1_lines = wrap_text(def1, small_font, 600)
        def2_lines = wrap_text(def2, small_font, 600)

        y_offset = 250
        draw_text("1. ", small_font, TEXT_COL, 150, y_offset)
        for line in def1_lines:
            draw_text(f"{line}", small_font, TEXT_COL, 200, y_offset)
            y_offset += 40

        y_offset += 10

        draw_text("2. ", small_font, TEXT_COL, 150, y_offset)
        for line in def2_lines:
            draw_text(f"{line}", small_font, TEXT_COL, 200, y_offset)
            y_offset += 40

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
                draw_text("GAME OVER", font, TEXT_COL, 290, 250)
                draw_text(f"Total Points: {points}", small_font, TEXT_COL, 270, 300)
                pygame.display.update()
                pygame.time.delay(2000)
                run = False
            elif game_mode == "scramble":
                if event.key == pygame.K_RETURN:
                    if input_text.lower() == correct_word.lower():
                        points += 1
                        pygame.draw.rect(screen, (175, 225, 175), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
                        draw_text("Correct!", font, TEXT_COL, 300, 300)
                        correct_sound.play()
                        pygame.display.update()
                        pygame.time.delay(500)
                        input_text = ""
                        get_random_scrambled_word()
                    else:
                        pygame.draw.rect(screen, (255, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
                        draw_text("nah", font, TEXT_COL, 290, 300)
                        wrong_sound.play()
                        pygame.display.update()
                        pygame.time.delay(1000)
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            elif game_mode == "definition":
                if event.unicode == "1":
                    if def1 == definitions[word][0]:
                        points += 1
                        pygame.draw.rect(screen, (175, 225, 175), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
                        correct_sound.play()
                        draw_text("Correct!", font, TEXT_COL, 300, 300)

                    else:
                        pygame.draw.rect(screen, (255, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
                        draw_text("Incorrect!", font, TEXT_COL, 290, 300)
                        wrong_sound.play()
                    pygame.display.update()
                    pygame.time.delay(500)
                    get_random_definition()
                elif event.unicode == "2":
                    if def2 == definitions[word][0]:
                        points += 1
                        pygame.draw.rect(screen, (175, 225, 175), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
                        draw_text("Correct!", font, TEXT_COL, 300, 300)
                    else:
                        pygame.draw.rect(screen, (255, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
                        draw_text("Incorrect!", font, TEXT_COL, 290, 300)
                    pygame.display.update()
                    pygame.time.delay(500)
                    get_random_definition()
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()