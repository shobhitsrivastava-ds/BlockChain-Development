


import hashlib
import json
from time import time
from uuid import uuid4
from textwrap import dedent

from flask import Flask


class Blockchain(object):
	def __init__(self):
		self.chain= []
		self.current_transaction= []

		# Creating the genesis block
		self.new_block(previous_hash=1, proof= 100)

	def new_block(self, proof, previous_hash= None):
		block= {
		"index": len(self.chain)+1,
		"timestamp": time(),
		"transactions": self.current_transaction,
		"proof": proof,
		"previous_hash": previous_hash or self.hash(self.chain[-1]),
		}

		# Reset the current transaction
		self.current_transaction= []
		self.chain.append(block)
		return(block)

	def new_transaction(self, sender, recipient, amount):
		self.current_transaction.append({
			"sender":sender,
			"recipient": recipient,
			"amount": amount
			})
		return(self.last_block["index"]+1)

	def proof_of_work(self, last_proof):
		proof= 0
		while(self.valid_proof(last_proof, proof) is False):
			proof+=1
		return(proof)
 

	@staticmethod
	def valid_proof(last_proof, proof):
		guess= f"{last_proof}{proof}".encode()
		guess_hash= hashlib.sha256(guess).hexdigest()
		return(guess_hash[:4]=="0000")

	@staticmethod
	def hash(block):

		#hashes a block
		pass

	@property
	def last_block(self):
		# returns the last block in the chain
		pass


# Intitate out node

app= Flask(__name__)

# Generate a globally unique address for this node

node_identifier= str(uuid4()).replace("-","")

# Instantiate the blockchain

blockchain= Blockchain()

@app.route("/mine", method= ["GET"])
def mine():
	# We run the proof of work algorithm to get the next proof...
	last_block= blockchain.last_block
	last_proof= last_block["proof"]
	proof= blockchain.proof_of_work(last_proof)

	# We must receive the reward for finding th proof.
	# The sender is "0" to signify that this node has mind a new coin

	blockchain.new_transaction(
		"sender":"0",
		recipient= node_identifier,
		amount= 1,
		)

		# Forge the new block by adding it to the chain

		previous_block= blockchain.hash(last_block)
		block= blockchain.next_block(proof, previous_hash)

		response= {
		"message": "New Block Forged",
		"index": block["index"],
		"transaction": block["transactions"],
		"proof": block["proof"],
		"previous_hash": block["previous_hash"],

		}
		return(jsonify(response), 200)

@app.route("/transaction/new", method= ["POST"])
def new_transaction():
	values= request.get_json()

	# Check the required field are in the posted data
	required= ["sender", "recipient", "amount"]

	if not all(k in values for k in required):
		return("Missing values", 400)

	# Create a new transaction
	index= blockchain.new_transaction(values["sender"], values["recipient"],
		values["amount"])
	response= {"message": f"Transaction will be addes to Block {index}"}
	return(jsonify(response), 201)



@app.route("/chain", method= ["GET"])
def full_chain():
	response= {
	"chain": block.chain,
	"length": len(blockchain.chain),
	}
	return(json(response), 200)


# RUNNGING THE API

if __name__=="__main__":
	app.run(host= "0.0.0.0", port= 5000)

# Here's an example of how a simple block would look like
"""
block= {
	"index":1,
	"timestamp": 1506057125.900785,
	"transactions": [
	{
	"sender": "8527147fe1f5426f9dd545de4b27ee00",
	"recipient": "a77f5cdfa2934df3954a5c7c7da5df1f"
	"amount": 5,
	} 
	],
	"proof":  324984774000,
	"previous_hash": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}

"""
























