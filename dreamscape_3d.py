from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app= Ursina()

player= FirstPersonController()
ground= Entity(model= 'plane', collider= 'box', scale= 100, texture= 'white_cube', texture_scale= (100,100))

stats= {"Courage": 0, "Fear": 0, "Creativity": 0, "Doubt": 0}

choice_text= Text("", origin=(0,0), y=-0.35, scale= 1.2)
stats_text= Text(f"Stats: {stats}", origin= (-.5, .5), background= True)

dream_objects= {
  "door": {
    "model": "cube",
    "color": color.azure, 
    "choices": {
      "open it": {"Courage": 2, "Fear": -1},
      "avoid it": {"Doubt": 2, "Fear": 1},
      "imagine a new path": {"Creativity": 2},
      "scream": {"Fear": 2}
    }
  },
  "mask": {
    "model": "sphere",
    "color": color.red,
    "choices": {
      "wear it": {"Creativity": 2},
      "smash it": {"Courage": 2, "Fear": 1},
      "ignore it": {"Doubt": 2}
    }
  },
  "statue": {
    "model": "cube",
    "color": color.gray,
    "choices": {
      "pray": {"Doubt": -1, "Courage": 1},
      "deface": {"Fear": 2, "Creativity": 1},
      "walk away": {"Doubt": 2}
      }
    },
  "clock": {
    "model": "cube",
    "color": color.yellow,
    "choices": {
      "wind it": {"Creativity": 1},
      "smash it": {"Courage": 1, "Fear": 1},
      "ignore it": {"Doubt": 2}
      }
    },
  "book": {
    "model": "cube",
    "color": color.green,
    "choices": {
      "read it": {"Creativity": 2},
      "burn it": {"Courage": 1, "Fear": 1},
      "close it": {"Doubt": 2}
      }
    }
}

spawned_objects= []
current_interaction= None

def spawn_dream_objects(num= 5):
  for name, data in random.sample(list(dream_objects.items()), num):
    x, z= random.randint(-10, 10), random.randint(-10, 10)
    entity= Entity(
      model= data["model"],
      color= data["color"],
      position= (x, 0, z),
      collider= "box", 
      scale= 1.5
    )
    spawned_objects.append({"name": name, "entity": entity})

spawn_dream_objects(num= 5)

def apply_choice(obj_name, choice):
  global stats, current_interaction
  effects= dream_objects[obj_name]["choices"][choice]
  for stat, change in effects.items():
    stats[stat] += change
  stats_text.text= f"Stats: {stats}"
  choice_text.text= f"You chose '{choice}'. The dream shifts..."
  
 
  for obj in spawned_objects:
    if obj["name"] == obj_name and obj["entity"].enabled:
      e= obj["entity"]

      if obj_name == "door":
        if choice == "open it":
          e.animate_rotation((0, 90, 0), duration= 1)
          invoke(e.disable, delay=1.5)
        else: 
          e.animate_scale((0, 0, 0), duration= 1)
          invoke(e.disable, delay= 1.2)

      elif obj_name == "mask":
        if choice == "smash it":
          e.animate_scale((0, 0, 0), duration= 0.8)
          invoke(e.disable, delay=1)
        elif choice == "wear it":
          e.parent= camera
          e.position= (0, 0.5, 1)
          e.scale= 0.5
          invoke(e.disable, delay= 2)
        else:
          e.disable()

      elif obj_name == "statue":
        if choice == "pray":
          e.animate_color(color.gold, duration= 1)
          invoke(e.disable, delay= 1.5)
        elif choice == "deface":
          e.animate_scale((0, 0, 0), duration= 1.2)
          invoke(e.disable, delay=1.5)
        else:
          e.disable()

      elif obj_name == "clock":
        if choice == "smash it":
          e.animate_rotation((720, 720, 720), duration= 1)
          invoke(e.disable, delay= 1.2)
        elif choice == "wind it":
          e.animate_rotation((0, 360, 0), duration= 2)
          invoke(e.disable, delay= 2.2)
        else:
          e.disable()
      
      elif obj_name == "book":
        if choice == "burn it":
          e.animate_color(color.red, duration= 0.5)
          e.animate_scale((0, 0, 0), duration= 1)
          invoke(e.disable, delay=1.2)
        elif choice == "read it":
          e.animate_rotation((0, 180, 0), duration= 1.2)
          invoke(e.disable, delay=1.5)
        elif choice =="close it":
          e.animate_rotation((0, -90, 0), duration= 1)
          invoke(e.disable, delay=1.2)
        else:
          e.disable()
        
      break

  current_interaction = None
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
  stats_text.text = ""
  Text(message, origin= (0,0), scale= 2, color=color.yellow)
  player.disable()

sky = Sky(texture='assets/Sky Paint1.png')


def update():
  global current_interaction
  if current_interaction:
    return

  current_interaction = None
  for obj in spawned_objects:
    e = obj["entity"]

    if not e or not e.enabled:
      continue

    if distance(player, e) < 2:
      current_interaction = obj["name"]
      options = list(dream_objects[obj["name"]]["choices"].keys())
      numbered = [f"[{i+1}] {opt}" for i, opt in enumerate(options)]
      choice_text.text = f"The {obj['name']} shimmers...\n" + "  ".join(numbered)
      break

def input(key):
  if current_interaction:
    options= list(dream_objects[current_interaction]["choices"].keys())
    if key in ["1", "2", "3", "4"] and int(key)-1 < len(options):
      apply_choice(current_interaction,options[int(key)-1])

directional_light= DirectionalLight()
directional_light.look_at(Vec3(1,-1,-1))

camera.clip_plane_far= 50
scene.fog_color= color.rgb(200,200,220)   
scene.fog_density= 0.01

app.run()
