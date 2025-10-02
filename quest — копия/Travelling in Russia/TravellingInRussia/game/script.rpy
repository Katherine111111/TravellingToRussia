# -------------------------------
# Characters
# -------------------------------
default guide_name = "Guide"
define guide = DynamicCharacter("guide_name", color="#3289bb")
define player = Character("[player_name]", color="#10661e")

# -------------------------------
# Defaults (игровые переменные)
# -------------------------------
default player_name = "Игрок"
default transport_order = ["train", "plane", "bus"]
default current_transport_index = 0
default transport = None
default cities_visited = 0
default score = 0
default transport_completed = {"train": False, "plane": False, "bus": False}

# -------------------------------
# Images (спрайты и фоны)
# -------------------------------
# --- Guide sprites ---
# Уменьшение всех изображений гида пропорционально высоте экрана (90% высоты)
# Функция для масштабирования по высоте экрана (с сохранением пропорций)
init python:
    def scale_by_height(path, percent=0.9):
        target_height = int(config.screen_height * percent)
        return Transform(path, fit="contain", yalign=1.0, xalign=0.5, size=(config.screen_width, target_height))

# Спрайты гида (все будут масштабироваться одинаково и не растягиваться)
image guide pointing  = scale_by_height("images/characters/guidepointing.png")
image guide sad       = scale_by_height("images/characters/guidesad.png")
image guide standing  = scale_by_height("images/characters/guidestanding.png")
image guide standing2 = scale_by_height("images/characters/guidestanding2.png")
image guide thinking  = scale_by_height("images/characters/guidethinking.png")
image guide thumbsup  = scale_by_height("images/characters/guidethumbsup.png")

# --- Backgrounds ---
image bg travel = "images/backgrounds/russia_background.png"
image bg moscow = "images/backgrounds/moscow.webp"
image bg saint_petersburg = "images/backgrounds/saint_petersburg.webp"
image bg kazan = "images/backgrounds/kazan.jpg"
image bg baikal = "images/backgrounds/winter_palace.jpg"   # финальный фон, можно заменить

# -------------------------------
# City data
# -------------------------------
default cities = [
    {
        "name": "Moscow",
        "facts": "Welcome to Moscow! The capital of Russia. Here you can see the Red Square and the Kremlin.",
        "train_question": "The Kremlin ___ (build) in the 15th century.",
        "train_answer": "was built",
        "mc_question": "How do you say 'Кремль' in English?",
        "mc_options": ["The Kremlin", "The Red Palace", "The Moscow Fort"],
        "correct_mc": 0
    },
    {
        "name": "Saint Petersburg",
        "facts": "Now you're in Saint Petersburg! The city of museums and canals.",
        "plane_question": "Right now, tourists ___ (take) photos near the Winter Palace.",
        "plane_answer": "are taking",
        "mc_question": "What is 'Зимний дворец' in English?",
        "mc_options": ["Winter Palace", "Summer Palace", "Ice Castle"],
        "correct_mc": 0
    },
    {
        "name": "Kazan",
        "facts": "Welcome to Kazan, the city where Europe meets Asia!",
        "bus_question": "The guide says we ___ try 'эчпочмак' (local dish).",
        "bus_answer": "should",
        "mc_question": "Which river is near Kazan?",
        "mc_options": ["Volga", "Don", "Yenisei"],
        "correct_mc": 0
    }
]

# -------------------------------
# START
# -------------------------------
label start:
    scene bg travel
    show guide standing at left

    guide "Hello! My name is Alex. You won a trip across Russia. What's your name?"
    $ player_name = renpy.input("My name is...", default="Traveler", length=12).strip()
    $ guide_name = "Alex"

    show guide pointing at left
    guide "Nice to meet you, [player_name]! You'll travel by train, plane and bus - in that order."

    $ current_transport_index = 0
    $ transport = transport_order[current_transport_index]
    call transport_intro from _call_transport_intro

    jump city_visit

# -------------------------------
# TRANSPORT INTRO
# -------------------------------
label transport_intro:
    if transport == "train":
        show guide thinking at left
        guide "First leg of your journey: by train! Get ready for verb tense challenges."
    elif transport == "plane":
        show guide pointing at left
        guide "Next, you'll travel by plane! Vocabulary tasks await you."
    else:
        show guide thumbsup at left
        guide "Final part of your trip: by bus! You'll practice modal verbs."
    return

# -------------------------------
# CITY VISIT
# -------------------------------
label city_visit:
    python:
        while cities_visited < len(cities):
            current_city = cities[cities_visited]
            has_task = False

            if transport == "train" and "train_question" in current_city:
                has_task = True
            elif transport == "plane" and "plane_question" in current_city:
                has_task = True
            elif transport == "bus" and "bus_question" in current_city:
                has_task = True

            if has_task:
                break
            else:
                cities_visited += 1

    if cities_visited >= len(cities):
        $ transport_completed[transport] = True
        $ cities_visited = 0

        if current_transport_index < len(transport_order) - 1:
            $ current_transport_index += 1
            $ transport = transport_order[current_transport_index]
            call transport_intro from _call_transport_intro_1
            jump city_visit
        else:
            jump finale

    $ current_city = cities[cities_visited]
    $ bg_name = "bg " + current_city["name"].lower().replace(" ", "_")
    scene expression bg_name

    if transport == "train":
        show guide thinking at left
    elif transport == "plane":
        show guide pointing at left
    else:
        show guide thumbsup at left

    guide "You've arrived at [current_city['name']] by [transport]!"
    guide "[current_city['facts']]"

    if transport == "train":
        call train_task from _call_train_task
    elif transport == "plane":
        call plane_task from _call_plane_task
    else:
        call bus_task from _call_bus_task

    $ question_text = current_city["mc_question"]
    $ option1 = current_city["mc_options"][0]
    $ option2 = current_city["mc_options"][1]
    $ option3 = current_city["mc_options"][2]
    $ correct_index = current_city["correct_mc"]

    show guide standing at left
    guide "Now answer this question:"

    menu:
        "[question_text]"

        "[option1]":
            if correct_index == 0:
                show guide thumbsup at left
                guide "That's right!"
                $ score += 1
            else:
                show guide sad at left
                guide "Sorry, that's incorrect."

        "[option2]":
            if correct_index == 1:
                show guide thumbsup at left
                guide "That's right!"
                $ score += 1
            else:
                show guide sad at left
                guide "Sorry, that's incorrect."

        "[option3]":
            if correct_index == 2:
                show guide thumbsup at left
                guide "That's right!"
                $ score += 1
            else:
                show guide sad at left
                guide "Sorry, that's incorrect."

    $ cities_visited += 1

    if cities_visited < len(cities):
        show guide pointing at left
        guide "Here's your ticket to the next city!"
        jump city_visit
    else:
        $ transport_completed[transport] = True
        $ cities_visited = 0

        if current_transport_index < len(transport_order) - 1:
            $ current_transport_index += 1
            $ transport = transport_order[current_transport_index]
            call transport_intro from _call_transport_intro_2
            jump city_visit
        else:
            jump finale

# -------------------------------
# TASKS
# -------------------------------
label train_task:
    $ question = current_city["train_question"]
    $ answer = current_city["train_answer"]

    show guide thinking at left
    guide "Verb tense task:"
    guide "[question]"
    $ user_answer = renpy.input("Your answer:", default="", length=40).strip().lower()

    if user_answer == answer.lower():
        show guide thumbsup at left
        guide "Correct! +1 point."
        $ score += 1
    else:
        show guide sad at left
        guide "Oops! Right answer: [answer]."
    return

label plane_task:
    $ question = current_city["plane_question"]
    $ answer = current_city["plane_answer"]

    show guide standing at left
    guide "Vocabulary task:"
    guide "[question]"
    $ user_answer = renpy.input("Your answer:", default="", length=40).strip().lower()

    if user_answer == answer.lower():
        show guide thumbsup at left
        guide "Correct! +1 point."
        $ score += 1
    else:
        show guide sad at left
        guide "Oops! Right answer: [answer]."
    return

label bus_task:
    $ question = current_city["bus_question"]
    $ answer = current_city["bus_answer"]

    show guide standing2 at left
    guide "Modal verb task:"
    guide "[question]"
    $ user_answer = renpy.input("Your answer:", default="", length=40).strip().lower()

    if user_answer == answer.lower():
        show guide thumbsup at left
        guide "Correct! +1 point."
        $ score += 1
    else:
        show guide sad at left
        guide "Oops! Right answer: [answer]."
    return

# -------------------------------
# FINALE
# -------------------------------
label finale:
    python:
        max_points = 0
        for c in cities:
            if "train_question" in c:
                max_points += 1
            if "plane_question" in c:
                max_points += 1
            if "bus_question" in c:
                max_points += 1
            if "mc_question" in c:
                max_points += 1

    scene bg baikal with fade
    show guide standing2 at left

    guide "Congratulations, [player_name]! You've completed all three journeys!"
    guide "Your final score is [score] out of [max_points] possible points."

    show guide pointing at left
    guide "Would you like to try again?"

    menu:
        "Play again":
            $ cities_visited = 0
            $ score = 0
            $ current_transport_index = 0
            $ transport = transport_order[current_transport_index]
            $ transport_completed = {"train": False, "plane": False, "bus": False}
            jump start
        "Quit":
            return
