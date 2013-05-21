zmq 作为服务接口

worker 从 mongoDB 读取 url 对应的 tags

根据tags 从 Whoosh 索引 的 招聘资料 中 按BM25 排序输出 结果集



客户端        lpclient
服务端队列    ppqueue
服务端工作机  ppworker
mongodb操作   mongodbclient 
索引操作      whoosh_test
结果集高亮    radix_tree


