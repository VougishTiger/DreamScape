import random

player_stats= {
  "Courage": 0,
  "Fear": 0,
  "Creativity": 0,
  "Doubt":0
}

dream_scenes= [
  "You stand in a hallway where doors float in midair.",
  "A shadow whispers your name from behind.",
  "You find a staircase that loops back into itself.",
  "An old friend speaks in reversed sentences."
]

choices= {
  "face it": {"Courage": 2, "Fear": -1},
  "avoid it": {"Doubt": 2, "Fear": 1},
  "imagine a new path": {"Creativity": 2},
  "scream": {"Fear": 2}
}

def apply_choice(player_choice):
  effects= choices.get(player_choice, {})
  for stat, change in effects.items():
    player_stats[stat]+= change

def get_random_scene():
  return random.choice(dream_scenes)

def check_wake_up():
  return any(value >= 5 for value in player_stats.values())

print("🌙 Welcome to Dreamscape RPG 🌙")
print("Your drift into sleep...")

while True:
  print("\n"+ get_random_scene())

  print("Choices: face it | avoid it | imagine a new path | scream")
  choice= input("What do you do?").strip().lower()

  apply_choice(choice)

  print(f"Your subsconscious stats: {player_stats}")

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

