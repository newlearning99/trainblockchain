from flask import Flask, jsonify, request
import hashlib, json
from time import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        self.chain.append(Block(0, time(), "Genesis Block", "0"))

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), time(), data, last_block.hash)
        self.chain.append(new_block)
        return new_block

blockchain = Blockchain()

app = Flask(__name__)

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify([vars(b) for b in blockchain.chain]), 200

@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.get_json()
    block = blockchain.add_block(data.get('data', 'No data'))
    return jsonify(vars(block)), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
