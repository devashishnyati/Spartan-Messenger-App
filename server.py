import yaml
from concurrent import futures
import grpc
import time
import proto.spartanmessenger_pb2 as chat
import proto.spartanmessenger_pb2_grpc as rpc

config=yaml.load(open('config.yaml'))
max_messages = config['max_num_messages_per_user'] 
port = config['port']
max_calls = config['max_call_per_30_seconds_per_user']

def rate_decorator(func):
    def rate(*args, **kwargs):
        time.sleep(30/max_calls)
        return func(*args, **kwargs)
    return rate

class MessageServer(rpc.MessageServerServicer):

    def __init__(self):
        self.chat_messages = {'bob': [], 'alice': [],'charlie': [],'eve': [],'foo': [],'bar': [],'baz': [],'qux': [], 'group1': [], 'group2': []}
        self.friendname = None


    def MessageStream(self, request_iterator, context):
        lastindex = {'alice': 0, 'bob': 0, 'charlie': 0, 'eve': 0, 'foo': 0, 'bar': 0, 'baz': 0, 'qux': 0, 'group1': 0, 'group2': 0}
        while True:
            while self.friendname != None:
                while len(self.chat_messages[self.friendname]) > lastindex[self.friendname]:
                    n = self.chat_messages[self.friendname][lastindex[self.friendname]]
                    lastindex[self.friendname] += 1
                    yield n

    @rate_decorator
    def SendMessage(self, request: chat.Message, context):
        self.friendname = request.friend
        if len(self.chat_messages[self.friendname]) >= max_messages:
            self.chat_messages[self.friendname].pop(0)
        print("[{}] to [{}] {}".format(request.name, request.friend, request.message))
        self.chat_messages[self.friendname].append(request)
        return chat.Empty()



if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_MessageServerServicer_to_server(MessageServer(), server)
    print('Spartan server started on port {}.'.format(port))
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    while True:
        time.sleep(64 * 64 * 100)
