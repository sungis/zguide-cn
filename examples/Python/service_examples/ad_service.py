# -*- coding: UTF-8 -*-

from whoosh.analysis import Tokenizer,Token
from whoosh.analysis import RegexTokenizer
from whoosh.index import create_in
from whoosh import index
from whoosh.fields import *
from radix_tree import RadixTree
import pymongo
from ac_trie import Trie
import json

class ADIndex:


    def __init__(self,indexdir):
        exists = index.exists_in(indexdir)
        if exists :
            self.ix =index.open_dir(indexdir)
        else:
            schema = Schema(title=TEXT(stored=True), id=NUMERIC(unique=True,stored=True),
                tags=KEYWORD(stored=True))
            self.ix = create_in(indexdir, self.schema)

        self.conn = pymongo.Connection(host='192.168.4.216', port=19753)
        self.tagsParser = Trie('./skill.txt')
     
    def add_doc(self,jobs):
        writer = self.ix.writer()
        rep = ''
        for j in jobs:
            writer.update_document(id=j[0],title=j[1],tags=j[2])
            rep = 'add doc :'+str(j[0])+'\r\n'
        writer.commit()
        return rep

    def del_doc(self,id):
        self.ix.delete_by_term('id',id)
        return 'del doc :'+str(id)+'\r\n'

    def find(self,query):
        searcher=self.ix.searcher()
        return searcher.find("tags", query)
#state 0  插入 链接
#state 1  插入 正文
#state 2  插入 标签
    def search_by_url(self,url):
        webData = self.conn.pongo.webData
        url = unicode(url)
        one = webData.find_one({"_id": url, "state": 2}, {"tags": 1})
        if one :
            tags = one["tags"]
            return self.search(tags)
        else:
            webData.insert({"_id":url,"state":0})
            return 'insert :'+url
            
    def search(self,query):
        rep = ''
        jobs = self.find(query)
        rep += str(len(jobs)) + '==>' +str(jobs.runtime)
        for j in jobs:
            rep += str(j['id'])+":"+j['title']+"\r\n"
        
        return rep

    def cut(self,value):
        value=value.lower().replace('&nbsp','')
        value = value.encode('UTF-8')
        terms = self.tagsParser.parse(value)
        v = {}
        for i in terms:
            v[i[0]]=i[1]
        return v.values()

    def dispatch_hander(self,worker,frames):
        header = frames[2]
        data = frames[3]
        jdata = json.loads(data.replace("''","0"),strict=False)
        action = jdata ["action"]
        rep = 'request err :'+data
        if header == 'update' and action == "updateDoc":
            jobs=[]
            for j in jdata['fields']:
                tags = self.cut(j['jobname']+' '+j['description'])
                jobid = j['jobid']
                jobname = unicode(j['jobname'])
                tags = ' '.join(tags).decode('UTF-8')
                jobs.append((jobid,jobname,tags))

            rep = self.add_doc(jobs)
        #remove
        #{"action":"removeDoc","name":"job","keyId":"64983"}
        if header == 'remove' and action == "removeDoc":
            keyid = jdata ["keyId"]
            rep =self.del_doc(int(keyid))
        if header == 'search':
            if action == 'adv':
                referurl = jdata['q']["referurl"]
                rep = self.search_by_url(referurl)
            if action == 'searchJob':
                keyword = jdata['q']["keyword"]
                rep = self.search(keyword)
        
        msg = [frames[0],frames[1],rep.encode('UTF-8')]
        worker.send_multipart(msg)
#        worker.send_unicode(msg)

if __name__ == '__main__' :
    aix = ADIndex('indexdir')
    jobs =[
            (1,u'java搜索',u'java linux lucene'),
            (2,u'ruby开发',u'java linux linux ruby'),
            (3,u'python开发',u'java linux linux python')
          ]
    aix.add_doc(jobs)
    aix.del_doc(2)
    jobs = aix.find(u'java linux')
    print jobs
    for j in jobs:
        print j,j.score
