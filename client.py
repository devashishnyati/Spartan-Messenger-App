import yaml
import sys
import threading
import time
import grpc
import proto.spartanmessenger_pb2 as chat
import proto.spartanmessenger_pb2_grpc as rpc
from Crypto.Cipher import AES
from Crypto.Util import Counter

config=yaml.load(open('config.yaml'))
address = 'localhost'
port = config['port']
users = config['users']

nonce = '_2M\xfd\x86\x9fK\x0b'
key = b'\x94:a.\x98\xb6\x06MW\x8f\xdc?\xefB6\xde\x982u\xc8\xf2\xd1\xe5\xc6zj\xcdh\x7fpQ\xe4'
username = sys.argv[1]
groups = config['groups']
group1_names = groups['group1']
group2_names = groups['group2']

class Client:

    def __init__(self, u: str, f: list):
        self.username = u
        self.friendlist = f
        self.friendlist.append('group1')
        self.friendlist.append('group2')
        print('[Spartan] Friend list: {}'.format(self.friendlist))
        self.friend_name = input('[Spartan] Enter a user whom you want to chat with: ')
        if self.friend_name in self.friendlist:
            print('[Spartan] You are now connected with {}'.format(self.friend_name))
            channel = grpc.insecure_channel(address + ':' + str(port))
            self.conn = rpc.MessageServerStub(channel)
            threading.Thread(target=self.__listen_for_messages, daemon=True).start()
            self.__enter_message()


    def __listen_for_messages(self):
        for note in self.conn.MessageStream(chat.Empty()):
            if (note.friend == self.username) & (note.name == self.friend_name):
                countg = Counter.new(64, nonce)
                decrypto = AES.new(key, AES.MODE_CTR, counter=countg)
                self.decryptedmessage = decrypto.decrypt(note.message)
                print("[{}] {}".format(note.name, self.decryptedmessage.decode('utf-8')))
            if (note.friend == 'group1'):
                for note.friend in group1_names:
                    if (note.friend == self.username) & (note.name != self.username):
                        countg = Counter.new(64, nonce)
                        decrypto = AES.new(key, AES.MODE_CTR, counter=countg)
                        self.decryptedmessage = decrypto.decrypt(note.message)
                        print("[{}] {}".format(note.name, self.decryptedmessage.decode('utf-8')))
            if (note.friend == 'group2'):
                for note.friend in group2_names:
                    if (note.friend == self.username) & (note.name != self.username):
                        countg = Counter.new(64, nonce)
                        decrypto = AES.new(key, AES.MODE_CTR, counter=countg)
                        self.decryptedmessage = decrypto.decrypt(note.message)
                        print("[{}] {}".format(note.name, self.decryptedmessage.decode('utf-8')))

                
    
    def send_message(self, event):
        message = self.message
        if message is not '':
            n = chat.Message()
            n.name = self.username
            n.friend = self.friend_name
            n.message =  self.message
            self.conn.SendMessage(n)
    
    
    def __enter_message(self):
            try:
                while (True):
                    self.input = input('Message: ')
                    countf = Counter.new(64, nonce) 
                    encrypto = AES.new(key, AES.MODE_CTR, counter=countf)
                    self.message = encrypto.encrypt(self.input)
                    print("[{}] {}".format(self.username, self.input))
                    self.send_message('<Return>')  
            except KeyboardInterrupt:
                print('\n[Spartan] Enter friend name:')


if __name__ == '__main__':
    print('[Spartan] Connected to Spartan Server at port {}.'.format(port))
    if username in users:
        users.remove(username)
        while (True):
            c = Client(username, users) 
        time.sleep(10)