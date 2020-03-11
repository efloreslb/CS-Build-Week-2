import hashlib
import requests
import json
import time
import json
from api_key import API_KEY

headers = {
   "Authorization": API_KEY
}

def last_proof():
   res = requests.get(
      'https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/', headers=headers)

   res = json.loads(res.text)
   print("LAST PROOF", res)
   return res


def proof_of_work(last_proof):

   the_last_proof = last_proof['proof']
   difficulty = last_proof['difficulty']
   last_hash = json.dumps(the_last_proof)
   proof = 0

   while valid_proof(last_hash, proof, difficulty) is False:
      proof += 1

   new_proof = {"proof": int(proof)}
   res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/', headers=headers, data=json.dumps(new_proof))

   res = json.loads(res.text)
   time.sleep(res['cooldown'])
   return res

def valid_proof(last_hash, proof, difficulty):
   guess = f'{last_hash}{proof}'.encode()
   guess_hash = hashlib.sha256(guess).hexdigest()
   return guess_hash[:difficulty] == "0" * difficulty

if __name__ == "__main__":
   while True:
      last_proof = last_proof()
      time.sleep(last_proof['cooldown'])
      new_proof = proof_of_work(last_proof)