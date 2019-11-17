import datetime
import hashlib
import json
from flask import Flask, jsonify

'''
BlockChain Genérica
'''

class BlockChain:

    def __init__(self):
        self.chain = [] # BlockChain
        self.create_block(proof=1, previous_hash='0') # Bloco Gênesis
    
    def create_block(self, proof, previous_hash):
        # Bloco padrão da BlockChain
        # Esta função não minera o bloco
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash 
        }

        self.chain.append(block) # Adiciona bloco na lista
        return block

    def get_previous_block(self):
        return self.chain[-1] # Retorna bloco anterior da BlockChain

    def proof_of_work(self, previous_proof):
        new_proof = 1 # nonce
        check_proof = False # Verificar se o bloco foi minerado
        
        # Mineração do bloco
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - \
                             previous_proof**2).encode()).hexdigest()
                             
            if hash_operation[:4] == '0000':  # Nível de dificuldade
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    # Transforma o bloco em uma estrutura json e gera o seu hash
    def hash(self, block):
        encoded_block = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    # Valida o BlockChain. Verifica cada hash
    def is_chain_valid(self, chain):
        previous_block = chain[0] # Primeiro bloco
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index] # Bloco atual
            if block["previous_hash"] != self.hash(previous_block):
                return False
            
            # Verifica se o proof é válido
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False

            # Caminha pela BlockChain
            previous_block = block
            block_index += 1
        return True


# Iniciar BlockChain
blockchain = BlockChain()

# Iniciar Webserver Flask
app = Flask(__name__)


@app.route('/mine_block', methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    
    response = {
        "message": "Parabéns você minerou um bloco",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"]    
    }    
    return jsonify(response), 200


@app.route('/get_chain', methods=["GET"])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

app.run(host='0.0.0.0', port=5000)