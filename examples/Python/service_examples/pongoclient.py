import zmq  


def search(q):
  SERVER_ENDPOINT = "tcp://192.168.4.215:5560"
  CLIENT_IDENTITY = "AD_Client_pyzmq" 
  c=zmq.Context()
  s=c.socket(zmq.REQ)
  s.set(zmq.IDENTITY,CLIENT_IDENTITY)
  s.connect(SERVER_ENDPOINT)
  m=['search',q]
  s.send_multipart(m)
  return s.recv()


request='{ "action" : "searchJob" , "q" : { "keyword" : ".net"} , "filter" : { } ,"sort" : 1 , "output" : { "format" : "json", "offset" : 0 , "size" : 10}}'

#print search(request)

SERVER_ENDPOINT = "tcp://192.168.4.215:5560" 
CLIENT_IDENTITY = "AD_Client_pyzmq"

context = zmq.Context(1)
print "I: Connecting to server..."
client = context.socket(zmq.REQ)
client.set(zmq.IDENTITY,CLIENT_IDENTITY)
client.connect(SERVER_ENDPOINT)

poll = zmq.Poller()
poll.register(client, zmq.POLLIN)
m=['search',request]


REQUEST_TIMEOUT = 3000
retries_left=3

client.send_multipart(m)
while retries_left:
  socks = dict(poll.poll(REQUEST_TIMEOUT))
  if socks.get(client) == zmq.POLLIN:
    reply = client.recv()
    if not reply:
      break
    else:
      print reply
      break

  else:
    print "W: No response from server, retrying..."
    client.setsockopt(zmq.LINGER, 0)
    client.close()
    poll.unregister(client)
    if retries_left == 0:
      print "E: Server seems to be offline, abandoning"
      break
    print "I: Reconnecting and resending (%s)" % request
    client = context.socket(zmq.REQ)
    client.set(zmq.IDENTITY,CLIENT_IDENTITY)
    client.connect(SERVER_ENDPOINT)
    poll.register(client, zmq.POLLIN)
    client.send_multipart(m)
    #print client.recv()

#context.term()




#if __name__ == '__main__':
#  q='{ "action" : "searchJob" , "q" : { "keyword" : ".net"} , "filter" : { } ,\
#      "sort" : 1 , "output" : { "format" : "json", "offset" : 0 , "size" : 10}}'
#  print search(q)

