# -*- coding: UTF-8 -*-
import zmq  


def send_request(header,q):
  SERVER_ENDPOINT = "tcp://localhost:5555"
  CLIENT_IDENTITY = "AD_Client_pyzmq" 
  c=zmq.Context()
  s=c.socket(zmq.REQ)
  #s.set(zmq.IDENTITY,CLIENT_IDENTITY)
  s.connect(SERVER_ENDPOINT)
  m=[header,q]
  s.send_multipart(m)
  return s.recv()


#request='{ "action" : "searchJob" , "q" : { "keyword" : ".net"} , "filter" : { } ,"sort" : 1 , "output" : { "format" : "json", "offset" : 0 , "size" : 10}}'

#print send_request('search',request)


#f = open('./data/jobs.txt')
#re_jobs=re.compile('{"action":"updateDoc".*{"format":"json","offset":0,"size":10}}')
#for i in f:
#    m = re_jobs.search(i)
#    if m:
#        request = m.group()
#        print request
#        break
#        print send_request('update',request)

#request = '{"action":"removeDoc","name":"job","keyId":"67943"}'
#print send_request('remove',request)
#
#
#request='{"action":"adv","q":{"referurl":"http://blog.csdn.net/zhangchaoyangsun/article/details/8879615","keyword":[""]},"filter":{"city":[""],"province":[""]},"sort":1,"output":{"format":"json","offset":0,"size":6}}'
#print send_request('search',request)

#import sys
#f = open('skill.txt')
#for k in f:
#    request='{ "action" : "searchJob" , "q" : { "keyword" : "'+k+'"} , "sort" : 1 , "output" : { "format" : "json" , "offset" : 0 , "size" : 10}}'
#    print k
#    print send_request('search',request)
#    ch = sys.stdin.read(1)

k='python'

request='{ "action" : "searchJob" , "q" : { "keyword" : "'+k+'"} , "sort" : 1 , "output" : { "format" : "json" , "offset" : 0 , "size" : 10}}'
print k
print send_request('search',request)
