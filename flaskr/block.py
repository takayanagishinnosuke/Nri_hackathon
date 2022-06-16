import hashlib
import json
import datetime

from numpy import block

class Block:
  def __init__(self,index,timestamp,transaction,previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.transaction = transaction
    self.previous_hash = previous_hash
    self.property_dict = {str(i): j for i, j in self.__dict__.items()}
    self.now_hash = self.calc_hash()

  def calc_hash(self):
    block_string = json.dumps(self.property_dict, sort_keys=True).encode('ascii')

    return hashlib.sha256(block_string).hexdigest()

def new_transaction(id, user):
  transaction = {
    'ID': id,
    'USER': user,
  }
  return transaction

block_chain = []

gensis_block = Block(0, 0, 0, "-")
block_chain.append(gensis_block)

transaction = new_transaction('1','admin')
new_block = Block(1,str(datetime.datetime.now()),transaction, block_chain[0].now_hash)
block_chain.append(new_block)

for key, value in gensis_block.__dict__.items():
  print(key, ':', value)

print("")

for key, value in new_block.__dict__.items():
  print(key, ':', value)


