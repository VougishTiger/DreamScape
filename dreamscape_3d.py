from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app= Ursina()

player= FirstPersonController()
ground= Entity(model= 'plane', collider= 'box', scale= 100, texture= 'white_cube', texture_scale= (100,100))
stats= {"Courage": 0, "Fear": 0, "Creativity": 0, "Doubt": 0}

door= Entity(model='cube', color=color.azure, position=(3,0,3), scale=(1.5,3,0.2))
mask= Entity(model= 'sphere', color=color.red, position=(-2,1,4))
statue= Entity(model='cube', color=color.gray, position=(0,0,6), scale=(1,2,1))

choice_text= Text("",  origin=(0,0), y=- 0.35, scale= 1.2)
stats_text = Text(f"Stats: {stats}", origin=(-.5,.5), background=True)

dream_choices= {
  "door": {
    "face it": {"Courage": 2, "Fear": -1},
    "avoid it": {"Doubt": 2, "Fear": 1},
    "imagine a new path": {"Creativity": 2},
    "scream": {"Fear": 2}
  },
  "mask": {
    "wear it": {"Creativity": 2},
    "smash it": {"Courage": 2, "Fear": 1},
    "ignore it": {"Doubt": 2}
  },
  "statue": {
    "pray": {"Doubt": -1, "Courage": 1},
    "deface": {"Fear": 2, "Creativity": 1},
    "walk away": {"Doubt": 2}
  }
}

current_interaction= None

def apply_choice(object_name, choice):
  global stats, current_interaction
  effects= dream_choices[object_name][choice]
  for stat, change in effects.items():
    stats[stat]+= change
  stats_text.text= f"Stats: {stats}"
  choice_text.text= f"You chose '{choice}'. The dream shifts..."

  if object_name == "door":
    door.color= color.lime
  elif object_name == "mask":
    mask.color= color.orange
  elif object_name == "statue":
    statue.color= color.violet  

  current_interaction= None
  check_wake_up()


def check_wake_up():
  if any(value >= 5 for value in stats.values()):
    if stats["Fear"]>= 5:
      end_game("😱 You wake in terror, sweating in the dark...")
    elif stats["Creativity"]>= 5:
      end_game("🎨 You wake inspired, sketches already forming in your mind.")
    elif stats["Courage"]>= 5:
      end_game("🦁 You wake with newfound strength and determination.")
    elif stats["Doubt"]>= 5:
      end_game("🤔 You wake uncertain, questioning what was real.")

def end_game(message):
  choice_text.text= ""
  Text(message, origin= (0,0), scale= 2, color=color.yellow)
  player.disable()

def update():
  global current_interaction

  if distance(player, door)< 2:
    current_interaction= "door"
    choice_text.text= "The door whispers your name...\n[1] face it  [2] avoid it  [3] imagine a new path  [4] scream"
  elif distance(player, mask)< 2:
    current_interaction= "mask"
    choice_text.text= "The mask shifts colors...\n[1] wear it [2] smash it [3] ignore it"
  elif distance(player, statue)< 2:
    current_interaction= "statue"
    choice_text.text= "The statue hums softly...\n[1] pray  [2] deface  [3] walk away"
  else: 
    current_interaction= None

def input(key):
  if current_interaction:
    if current_interaction == "door":
      if key == '1': apply_choice("door", "face it")
      elif key == '2': apply_choice("door", "avoid it")
      elif key == '3': apply_choice("door", "imagine a new path")
      elif key == '4': apply_choice("door", "scream")
    elif current_interaction == "mask":
      if key == '1': apply_choice("mask", "wear it")
      elif key == '2': apply_choice("mask", "smash it")
      elif key == '3' : apply_choice("mask", "ignore it")
    elif current_interaction == "statue":
      if key == '1': apply_choice("statue", "pray")
      elif key == '2': apply_choice("statue", "deface")
      elif key == '3': apply_choice("statue", "walk away")

Sky()
DirectionalLight().look_at(Vec3(1,-1,-1))

app.run()