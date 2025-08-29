import random

player_stats= {
  "Courage": 0,
  "Fear": 0,
  "Creativity": 0,
  "Doubt":0
}

adjectives = ["glowing", "shattered", "endless", "floating", "dark", "melting", "whispering"]
locations = ["hallway", "forest", "corridor", "room", "staircase", "mirror chamber", "ocean"]
objects = ["door", "shadow", "mirror", "clock", "book", "statue", "mask"]
actions = ["breathes softly", "whispers your name", "loops back on itself", "melts into the floor", "screams silently", "shifts colors", "vanishes suddenly"]


choices= {
  "face it": {"Courage": 2, "Fear": -1},
  "avoid it": {"Doubt": 2, "Fear": 1},
  "imagine a new path": {"Creativity": 2},
  "scream": {"Fear": 2}
}

dream_puzzles= [
  {
    "question": "You see a clock with no hands. Do you: add hands | smash it | walk away?",
    "answers": {
      "add hands": {"Creativity": 2},
      "smash it": {"Courage": 2, "Fear": 1},
      "walk away": {"Doubt": 2}
    }
  },
  {
    "question": "A mirror shows your reflection smiling without you. Do you: smile back | shatter mirror | run?",
    "answers": {
      "smile back": {"Creativity": 1, "Fear": -1},
      "shatter mirror": {"Courage": 2, "Fear": 1},
      "walk away": {"Doubt": 2, "Fear": 1}
    }
  },
  {
        "question": "A staircase stretches endlessly upward. Do you: climb | jump off | sit down?",
        "answers": {
            "climb": {"Courage": 2},
            "jump off": {"Fear": 2},
            "sit down": {"Doubt": 2, "Creativity": 1}
        }
    }
]

def apply_choice(player_choice, effects):
  for stat, change in effects.items():
    player_stats[stat] += change


def generate_dream_scene():
    adj = random.choice(adjectives)
    loc = random.choice(locations)
    obj = random.choice(objects)
    act = random.choice(actions)
    return f"You see a {adj} {obj} inside a {loc} that {act}."

def check_wake_up():
  return any(value >= 5 for value in player_stats.values())

print("🌙 Welcome to Dreamscape RPG 🌙")
print("You drift into sleep...")

while True:
  if random.random()< 0.25:
    puzzle= random.choice(dream_puzzles)
    print("\n"+ puzzle["question"])
    choice= input("what do you do").strip().lower()
    if choice not in puzzle["answers"]:
      print("That choice fades away like a forgotten dream...")
      continue
      apply_choice(choice, puzzle["answers"][choice])
    else:
        print("\n" + generate_dream_scene())
        print("Choices: face it | avoid it | imagine a new path | scream")
        choice = input("What do you do? ").strip().lower()
        if choice not in choices:
            print("That action dissolves into dream static... (try again!)")
            continue
        apply_choice(choice, choices[choice])

    print(f"Your subconscious stats: {player_stats}")

    if check_wake_up():
        print("\n✨ You wake up from the dream...")
        break
if player_stats["Fear"] >= 5:
  print("😱 You wake in terror, sweating in the dark...")
elif player_stats["Creativity"] >= 5:
  print("🎨 You wake inspired, sketches already forming in your mind.")
elif player_stats["Courage"] >= 5:
  print("🦁 You wake with newfound strength and determination.")
elif player_stats["Doubt"] >= 5:
  print("🤔 You wake uncertain, questioning what was real.")
else:
  print("You wake... but something feels unfinished.")

