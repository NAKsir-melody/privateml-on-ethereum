from tkinter import *
import os
from web3 import Web3, HTTPProvider
from ens.auto import ns
from eth_utils import decode_hex



trace = 0 

class CanvasEventsDemo: 
    def __init__(self, parent=None):
        canvas = Canvas(width=300, height=300, bg='black') 
        canvas.pack()
        canvas.bind('<ButtonPress-1>', self.onStart) 
        canvas.bind('<B1-Motion>',     self.onGrow)  
        canvas.bind('<Double-1>',      self.onSend) 
        canvas.bind('<ButtonPress-3>', self.onClear)  
        canvas.create_rectangle(0,0,400,400,fill = 'black', outline='black')
        self.canvas = canvas
        self.drawn  = None
        self.kinds = [canvas.create_rectangle]

    def onSend(self, event):
        canvas = event.widget
        canvas.update()
        canvas.postscript(file="mydraw.ps", colormode='mono')
        os.system("convert -resize 28x28 mydraw.ps -alpha off /home/naksir/WORK/cryptonian/ML/MNIST/mydraw.png")
        os.system("rm mydraw.ps")
        #os.system("display /home/naksir/WORK/cryptonian/ML/MNIST/mydraw.png")

        print ("send transaction")
        rpc_url = "http://localhost:8080"
        w3 = Web3(HTTPProvider(rpc_url))
        w3.eth.enable_unaudited_features()
        w3.personal.unlockAccount(w3.eth.accounts[0], "base", 0)
        w3.eth.defaultAccount = w3.eth.accounts[0]
        ''' 
        transaction = {
                'to' : w3.eth.accounts[1],
                'from' : w3.eth.accounts[0],
                'value' : w3.toWei('3','ether'),
                'gas' : 4000000,
                'gasPrice' : w3.toWei('40','gwei'),
                'chainId':33,
                'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0])
                }

        with open('/home/naksir/WORK/cryptonian/node/keystore/UTC--2018-10-19T05-14-59.907760670Z--364b1b4b8369a591765e5db7b1ed9b3e49e42858') as keyfile:
            encrypted_key = keyfile.read()
            private_key = w3.eth.account.decrypt(encrypted_key,'base')
            signed_tx = w3.eth.account.signTransaction(transaction, private_key)
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(tx_hash)
        '''

        abi = '''[{"constant":false,"inputs":[{"name":"a","type":"int256"},{"name":"data","type":"string"}],"name":"setData","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"int256"}],"name":"datastores","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"int256"}],"name":"getData","outputs":[{"name":"data","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]'''
        con_addr = "0x6DAdEAA749aB19AFA14c25e6e4A73c15085b193C"
        cryptonian_contract = w3.eth.contract(address=con_addr, abi=abi)
        filename = "mydraw.png\n"
        ttt = cryptonian_contract.functions.setData( 1, filename.encode('utf-8')).transact({'from': w3.eth.accounts[0], 'gas': 700000} )
        print(ttt)

        print (cryptonian_contract.functions.getData(1).call())

    def onStart(self, event):
        self.shape = self.kinds[0]
        self.start = event
        self.drawn = None
    def onGrow(self, event):                         
        canvas = event.widget
        #if self.drawn: canvas.delete(self.drawn)
        #objectId = self.shape(self.start.x, self.start.y, event.x, event.y)
        objectId = self.shape(event.x-10, event.y-10, event.x+10, event.y+10,fill = 'white', outline='white')
        if trace: print (objectId)
        self.drawn = objectId
    def onClear(self, event):
        event.widget.delete('all')                   
    def onMove(self, event):
        if self.drawn:                               
            if trace: print (self.drawn)
            canvas = event.widget
            diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
            objectId = self.shape(event.x-8, event.y-8, event.x+8, event.y+8,fill = 'white', outline='white')
            canvas.move(self.drawn, diffX, diffY)
            self.start = event

if __name__ == '__main__':
    CanvasEventsDemo()
    mainloop()

