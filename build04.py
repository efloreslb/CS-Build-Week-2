import requests
import json
from api_key import API_KEY
import time
import os

# URL
url = "https://lambda-treasure-hunt.herokuapp.com/api"

# Header
headers = {
   "Authorization": API_KEY
}

def init():
   r = requests.get(f'{url}/adv/init/', headers=headers)
   initial_room = r.json()
   # print(f'---INITIAL ROOM---: {initial_room}')
   return initial_room

# def status():
#    r = requests.post(f'{url}/adv/status', headers=headers)
#    data = r.json()
#    print(f'---COOLDOWN---: {data["cooldown"]}')
#    return data

def move(direction):

   action_taken = "MOVED"

   if this_room['terrain'] == "MOUNTAIN":
      r_move = requests.post(f'{url}/adv/fly', data=json.dumps(direction), headers=headers)
      action_taken = "+ FLEW +"
   else: 
      r_move = requests.post(f'{url}/adv/move', data=json.dumps(direction), headers=headers)

   data = r_move.json()

   write_to_text_file(data, "maze.txt")

   print(f' ---------------------- {action_taken} TO --- ')

   for element in data:
      print(f'{element}: {data[element]}')

   return data

def write_to_text_file(data, file_name):
   info = []
   info.append(data)

   with open(file_name, 'a+') as outfile:
         json.dump(info, outfile, indent=2)

# def get_exits(room):
#    directions = room['exits']
#    room_id = room['room_id']
#    print(f'---ROOM ID: {room_id}, ---POSSIBLE EXITS: {directions}')
#    return directions

def print_cooldown(seconds):
   cooldown_done = False

   print('Countdown:', seconds, 'seconds!')
   time.sleep(seconds)

   # while seconds > 0:
   #    print('Countdown:', seconds, 'seconds!')
   #    time.sleep(1)
   #    seconds = seconds - 1

   # Return true instead of just printing seconds
   cooldown_done = True
   return cooldown_done


def take():
   # if len(curr_room['items']) > 0:
   data = {"name": "treasure"}
   r = requests.post(f'{url}/adv/take', headers=headers, data=json.dumps(data))


   #  r = requests.post(f'{url}/adv/take', data=json.dumps(payload), headers=headers)
   #  data = r.json()
   #  info = []
   #  info.append(data)

   #  with open('player_status.txt', 'w') as outfile:
   #      json.dump(info, outfile, indent=2)

   print("waiting to take...", data)
   time.sleep(15)
   return data

def sell(item):
   data = {"name": item}
   r = requests.post(f'{url}/adv/sell', headers=headers, data=json.dumps(data))

   print(f'--------> waiting to sell {item} ...')
   time.sleep(5)

   data = {"name": item, "confirm":"yes"}

   r = requests.post(f'{url}/adv/sell', headers=headers, data=json.dumps(data))

   print(f'-----------> selling {item} now')
   time.sleep(5)
   print("--------> SOLD")

def change_name():
   data = {"name": "[Edgar Flores]"}
   r = requests.post(f'{url}/adv/change_name', headers=headers, data = json.dumps(data))

   print("-----------> CHANGING to TRUE NAME <--------")
   time.sleep(30)

   print("-----------> AYE AYE <--------------------")

   data = {"name": "Edgar Flores", "confirm":"aye"}
   r = requests.post(f'{url}/adv/change_name', headers=headers, data = json.dumps(data))
   time.sleep(30)

   print("-----------> OK CHANGED <--------------------")


def status():
   print("--------------CHECKING STATUS---------------")
   # data = {"name": "Edgar Flores"}
   r = requests.post(f'{url}/adv/status', headers=headers)

   data = r.json()

   print(data)
   time.sleep(20)
   print("-------------STATUS CHECK DONE -------------")

   return data

room_to_mine = ""

def examine(thing):
   data = {"name": thing}
   r = requests.post(f'{url}/adv/examine', headers=headers, data=json.dumps(data))

   print("------------ EXAMINING --------------")
   
   result = r.json()
   room_to_mine = result["description"][-3:]

   print("-------------------------------------------")
   print(f"NEW MINE ROOM: {room_to_mine}")
   print("-------------------------------------------")
   time.sleep(3)


# def fly(direction):
#    r_move = requests.post(f'{url}/adv/move', data=json.dumps(direction), headers=headers)
#    data = r_move.json()

#    write_to_text_file(data, "maze.txt")

#    print(f' ----- FLEW TO ----- {data}')
#    for el in data:
#       prin(el)

#    new_room = json.loads(r_move.text)
#    return data

traversal_path = []
reversal_path = []
rooms = {}
maze = {} 
visited = set()

this_room = init()
# print(f"------------INITIAL ROOM------------: {this_room}")

# Set up inverse relationship with directions
inverse_directions = { "n": "s", "e": "w", "w": "e", "s": "n" }

# move({"direction": "e"})
# time.sleep(30)
# move({"direction": "e"})
# time.sleep(30)
# move({"direction": "e"})
# time.sleep(30)
# move({"direction": "s"})
# time.sleep(30)
# move({"direction": "e"})
# time.sleep(30)
# move({"direction": "n"})
# time.sleep(30)
# move({"direction": "n"})
# time.sleep(30)
# move({"direction": "w"})
# time.sleep(30)

while len(maze) < 500:
   # print(f'LENGTH: {len(maze)}')
   # print(f'ROOMS: {rooms}')
   # print(f'TRAVERSAL_PATH: {traversal_path}')

   # print('THIS_ROOM_ID:', this_room['room_id'])
   looping_room = this_room['room_id']

   print(f'------------------- LOOPING ROOM {looping_room} ----------------')
   print_cooldown(this_room['cooldown'])

   curr_room = this_room["room_id"]

   if curr_room not in maze:
      maze[curr_room] = curr_room
      print(f'MAZE ROOM: {maze[curr_room]}')
      curr_room_exits = {}
      print(f'CURR_ROOM_EXITS: {curr_room_exits}')

      # print(f'MAZE: {maze}')
      # print(f'ROOMS: {rooms}')

      # print(curr_room["exits"])

      for room_exit in this_room['exits']:
         # print(f'ROOM_EXITS: {room_exit}')
         curr_room_exits[room_exit] = "?"

      maze[curr_room] = curr_room_exits
      print(f'MAZE ROOM: {maze[curr_room]}')

   curr_room_exits = maze[curr_room]

   # print(f'MAZE: {maze}')

   if curr_room not in rooms:
      rooms[curr_room] = this_room['coordinates']

   # SELL IF AT SHOP
   if this_room["title"] == "Shop":
      my_status = status()

      for item in my_status['inventory']:
         sell(item)

   if this_room["title"] == "Pirate Ry's":
      change_name()


   if this_room["title"] != "A misty room" and this_room["title"] != "Mt. Holloway":
      special_room = this_room["title"]
      os.system(f'say "Found a special room {special_room}"')
   
   ## EXAMINE WISHING WELL
   if this_room["title"] == "Wishing Well":
      print("--------------- FOUND WISHING WELL -------------")
      os.system('say "Found the Wishing Well"')
      examine("Wishing Well")

   # room_to_mine = 433

   print(f'ROOM to MINE: {room_to_mine}')

   # ROOM TO MINE IN
   if this_room["room_id"] == room_to_mine:
      print("--------- MINE HERE NOW! --------")
      os.system('say "Found the Mining Room"')
      break

   # TRANSMOGRIPHER
   # if this_room["room_id"] == 495:
   #    print("---------Found Transmogripher! --------")
   #    os.system('say "Found the Transmogripher"')
   #    break

   # print(f'ROOMS: {rooms}')

   # TAKE ITEM IF ITEM IN ROOM
   if len(this_room['items']) > 0 and this_room['items'][0] == "shiny treasure":
      print("______________ TREASURE ______________")
      os.system('say "Found a Shiny Treasure"')
      take()
      status()
      print("--------------- DONE -----------------")

   # print(f'MAZE CURR ROOM --> {maze[curr_room]}')
   # print(f'CURR ROOM EXITS --> {curr_room_exits}')
   # break

   if 'n' in maze[curr_room] and curr_room_exits['n'] == '?':

      if curr_room_exits['n'] == "?": 
         ## NEED TO FIX MOVE FUNCTION ##
         this_room = move({"direction": "n"})
         traversal_path.append("n")
         
         new_room = this_room['room_id']
         curr_room_exits['n'] = new_room
         new_room_exits = {}

         if new_room not in maze:
            for room_exit in this_room['exits']:
               new_room_exits[room_exit] = "?"
               maze[new_room] = new_room_exits
            new_room_exits['s'] = curr_room
         # reversal_path.append('s')

         room_to_add = str(curr_room)
         print(f'ROOM to ADD: {room_to_add}')
         reversal_path.append({'s': room_to_add})

         print(f'REVERSAL PATH: {reversal_path}')

   elif 'e' in maze[curr_room] and curr_room_exits['e'] == '?':

      if curr_room_exits['e'] == "?":
         this_room = move({"direction": 'e'})
         traversal_path.append('e')
         
         new_room = this_room['room_id']
         curr_room_exits['e'] = new_room
         new_room_exits = {}

         if new_room not in maze:
            for room_exit in this_room['exits']:
               new_room_exits[room_exit] = "?"
               maze[new_room] = new_room_exits
            new_room_exits['w'] = curr_room
         # reversal_path.append('w')

         room_to_add = str(curr_room)
         print(f'ROOM to ADD: {room_to_add}')
         reversal_path.append({'w': room_to_add})

         print(f'REVERSAL PATH: {reversal_path}')

   elif 'w' in maze[curr_room] and curr_room_exits['w'] == '?':

      if curr_room_exits['w'] == "?":
         this_room = move({"direction": 'w'})
         traversal_path.append('w')
         
         new_room = this_room['room_id']
         curr_room_exits['w'] = new_room
         new_room_exits = {}

         if new_room not in maze:
            for room_exit in this_room['exits']:
               new_room_exits[room_exit] = "?"
               maze[new_room] = new_room_exits
            new_room_exits['e'] = curr_room

         room_to_add = str(curr_room)
         print(f'ROOM to ADD: {room_to_add}')
         reversal_path.append({'e': room_to_add})

         print(f'REVERSAL PATH: {reversal_path}')

   elif 's' in maze[curr_room] and curr_room_exits['s'] == '?':
   
      if curr_room_exits['s'] == "?":
         this_room = move({"direction": 's'})
         traversal_path.append('s')
         
         new_room = this_room['room_id']
         curr_room_exits['s'] = new_room
         new_room_exits = {}

         if new_room not in maze:
            for room_exit in this_room['exits']:
               new_room_exits[room_exit] = "?"
               maze[new_room] = new_room_exits
            new_room_exits['n'] = curr_room
         # reversal_path.append('n')

         room_to_add = str(curr_room)
         print(f'ROOM to ADD: {room_to_add}')
         reversal_path.append({'n': room_to_add})

         print(f'REVERSAL PATH: {reversal_path}')

   else:
      print("TURNING BACK.....")

      reverse_room = None

      reverse_data = reversal_path.pop()
      reverse_direction = list(reverse_data.keys())[0]
      reverse_room = list(reverse_data.values())[0]

      ## WISE EXPLORER
      if reverse_room is not None:
         this_room = move({"direction": reverse_direction, "next_room_id": reverse_room})
      else:
         this_room = move({"direction": reverse_direction})

      traversal_path.append(reverse_direction)

   write_to_text_file(rooms, 'mazerooms.txt')