import redis

# 1. 连接Redis数据库
# method1: 直接连接
# client=redis.Redis(host='127.0.0.1',port=6379,password='123456')

# method2: 连接池连接(预先创建多个连接, 进行redis操作时, 直接获取已经创建的连接进行操作, 完成后,不会释放, 用于后续的其他redis操作)
pool = redis.ConnectionPool(host='localhost', port=6379,password='123456')
client = redis.Redis(connection_pool=pool)

# 2. keys
# results=client.keys('*')
# print("list keys * :",results)

# 3. 基本数据类型操作
# 基本redis的命令名与redis模块中的函数名一致

# 3.1 String
# key -> value
#
# 设置：
# set(key, value, ex=None, px=None, nx=False, xx=False)
# setnx(key, value)　            只有key不存在时设置
# setex(key, value, time)        设置过期时间（秒）
# mset({key:value,...})          批量设置值
#
# 获取：
# get(key)
# mget(key1,key2,...)
# strlen(key)                   key对应值的字节长度
#
# 值追加内容:
# append(key,addValue)
def test_string():
    print("Test String:")
    result=client.set('a',1)
    print(result)                   # True

    result=client.get('a')
    print(result)                   # b'1'

    result=client.append('a',23)
    print(result)                   # 3

    result=client.get('a')
    print(result)                   # b'123'


# 3.2 Hash: 
# 一个name对应一个dic字典
# n1 -> k1:v1,k2,v2
# n2 -> kx:vx,..
#   
# hset(name, key, value)
# hget(name, key)
# hgetall(name)
# hmset(name, mapping)
# hmget(name, keys, *args)
#
# hlen(name)
# hkeys(name)
# hvals(name)
#
# hexists(name, key)
# hdel(name, *keys)
# hincrby(name, key, amount=1)

def test_hash():
    print("Test Hash:")

    result = client.hset('stu-001','name','Tom')
    print(result)                       # 1
    result = client.hmset('stu-001',{'age':19,'gender':'male'})
    print(result)                       # True
    result = client.hgetall('stu-001')
    print(result)                       # {b'name': b'Tom', b'age': b'19', b'gender': b'male'}

    result = client.hmset('stu-002',{'name':'Lucy','age':16,'gender':'Female'})
    print(result)                       # True
    result = client.hgetall('stu-002')
    print(result)                       # {b'name': b'Lucy', b'age': b'16', b'gender': b'Female'}

    result = client.hlen('stu-001')
    print(result)                       # 3
    result = client.hkeys('stu-001')
    print(result)                       # [b'name', b'age', b'gender']
    result = client.hvals('stu-001')
    print(result)                       # [b'Tom', b'19', b'male']

    result = client.hincrby('stu-001','age',amount=5)
    print(result)                       # 24
    result = client.hgetall('stu-001')
    print(result)                       # {b'name': b'Tom', b'age': b'24', b'gender': b'male'}


# 3.3. List
# 一个name对应一个列表存储
# n1 -> [v1,v2,...]
# n2 -> [...]
#
# lpush(name, *values),rpush(name, *values) 
# lpushx(name, *values),rpushx(name, *values)  name存在时，才能加入
# linsert(name, where, refvalue, value)        name对应的列表的refValue值的前或后where插入一个value
#
# llen(name)                        name列表长度
# lindex(name, index)               索引获取元素
# lrange(name, start, end)          分片获取元素
#
# lset(name, index, value)          索引位置重新赋值
# lpop(name)                        移除列表的左侧第一个元素，返回值则是第一个元素
# lrem(name, value, num=0)          删除name对应的list中的指定值
# ltrim(name, start, end)           移除列表内没有在该索引之内的值

def test_list():
    print("Test List:")

    result = client.lpush('group1','stu-A','stu-B','stu-C','stu-D','stu-E')
    print(result)                      # 5
    result = client.lpush('group2','child-A','child-B')
    print(result)                       # 3

    result = client.llen('group1')
    print(result)                       # 5
    result = client.lrange('group1',2,5)
    print(result)                       # [b'stu-C', b'stu-B', b'stu-A']


# 3.4. Set
# 不允许重复的列表
# n1 -> {v1,v2,...}
# n2 -> {...}
#
# sadd(name, *values)           添加元素
# srem(name,*values)            删除元素
# smembers(name)                列出集合所有元素
# scard(name)                   获取元素个数
# sismember(name, value)        测试素是否在

# spop(name)                    从集合中随机弹出一个元素
# smove(src, dst, value)        将一个元素从集合1移到集合2

# sdiff/sdiffstore(keys, *args) 差集（以前一个集合为标准）
# sinter(keys, *args)           交集
# sunion(keys, *args)           并集

def test_set():
    print("Test Set:")

    result = client.sadd('stdGrp1','stu-A','stu-B','stu-B','stu-C')
    print(result)                       # 3
    result = client.smembers('stdGrp1')
    print(result)                       # {b'stu-B', b'stu-C', b'stu-A'}
    result = client.scard('stdGrp1')
    print(result)                       # 3

    result = client.sadd('stdGrp2',*('stu-A','stu-C','stu-D'))
    print(result)                       # 3

    result = client.sdiff('stdGrp1','stdGrp2')
    print(result)                       # {b'stu-B'}
    result = client.sinter('stdGrp1','stdGrp2')
    print(result)                       # {b'stu-C', b'stu-A'}
    result = client.sunion('stdGrp1','stdGrp2')
    print(result)                       # {b'stu-B', b'stu-C', b'stu-A', b'stu-D'}


# 3.5. ZSet
# 有序集合(set的升级), 每次添加修改元素后会自动重新排序
# 每一个元素有两个值，值value和分数score(专门用来做排序)
# n1 -> {(value1,score1),(value2,score2),...}
# rank: index
# lexicographical: 相同的分值时，有序集合的元素会根据成员的值逐字节对比

# zadd(name, mapping, nx=False, xx=False, ch=False, incr=False) 添加

# zrem(name, values)                                            删除
# zremrangebyrank(name, start, end)
# zremrangebyscore(name, minscore, maxscore)

# zscan(name, cursor=0, match=None, count=None, score_cast_func=float) 查看
# zscan_iter(name, match=None, count=None,score_cast_func=float)

# zrange/zrevrange(name, start, end, desc=False, withscores=False, score_cast_func=float) 获取rank范围内的元素
# zrangebyscore(name,minscore,maxscore,...)   获取score范围内的元素

# zrank/zrevrank(name, value)                  获取元素rank
# zscore(name, value)                          获取元素score

# zcard(name)                         所有元素个数
# zcount(name, minscore, maxscore)    指定score范围内的元素数量

# zincrby(name, value, amount)                自增
# zinterstore(dest, keys, aggregate=None)     交集(相同值不同分数，则按照 aggregate=SUM/MIN/MAX 进行操作)
# zunionstore(dest, keys, aggregate=None)     并集

def test_zset():
    print("Test ZSet:")

    # 创建
    result = client.zadd('car1',{'car-A':10,'car-B':20,'car-C':30,'car-D':40}) 
    print(result)                    # 4

    # 列出
    result = client.zscan('car1')
    print(result)                   # (0, [(b'car-A', 10.0), (b'car-B', 20.0), (b'car-C', 30.0), (b'car-D', 40.0)])

    # 切片，获取元素列表
    result = client.zrange('car1',1,3)
    print(result)                   # [b'car-B', b'car-C', b'car-D']
    result = client.zrangebyscore('car1',15,35)
    print(result)                   # [b'car-B', b'car-C']

    # 统计数量
    result = client.zcard('car1')
    print(result)                   # 4
    result = client.zcount('car1',15,35)
    print(result)                   # 2

    # 获取元素属性：rank,score
    result = client.zrank('car1','car-C')
    print(result)                   # 2
    result = client.zscore('car1','car-C')
    print(result)                   # 30.0

    # 交集
    result = client.zadd('car2',{'car-B':25,'car-D':45,'car-E':55})
    print(result)                   # 3

    result = client.zinterstore('car-inter',('car1','car2'))
    print(result)                   # 2
    result = client.zscan('car-inter')
    print(result)                   # (0, [(b'car-B', 45.0), (b'car-D', 85.0)])

    result = client.zinterstore('car-inter',('car1','car2'),aggregate='MAX')
    print(result)                   # 2
    result = client.zscan('car-inter')
    print(result)                   # (0, [(b'car-B', 25.0), (b'car-D', 45.0)])


# 4. 其他常用操作
# flushdb(asynchronous=False)
# flushall(asynchronous=False)
# delete( *names)
# exists( name)
# keys( pattern='*')
# expire(name ,time)
# rename( src, dst)
# move( name, db)
# randomkey()
# type(name)

def test_others():
    result = client.keys()
    print(result)
    # [b'car-inter', b'car1', b'car2', b'car', b'stdGrp1', b'stdGrp2', b'stu-001', b'a', b'top:dupefilter', b'stu-002', b'top:items', b'group1', b'tt']

    result = client.delete('car')
    print(result)       # 1

    result = client.exists('car')
    print(result)       # 0

    result = client.type('car-inter')
    print(result)       # b'zset'


# 5. 管道: 批量提交命令,还可用来实现事务transation
# pipeline(transaction=True,shard_hint=None) 默认情况下一次pipline是原子性操作
# pipe.watch(name) -- 乐观锁，watch的对象不可改
# pipe.unwatch()

def test_pipeline():
    import time

    client.set('cnt',10)
    result=client.get('cnt')
    print('initial cnt:',result)

    pipe=client.pipeline(transaction=True)
    pipe.watch('cnt')               # 加锁
    try:
        pipe.multi()
        
        cnt=int(client.get('cnt'))
        pipe.set('a', 1)
        pipe.set('cnt',cnt+1)
        pipe.set('b',2)
        
        print('sleep...')
        time.sleep(5)               # 此时，若另一个客户端修改了cnt，则这段操作提交（执行execute）时会报错

        print('execute...')
        pipe.execute()
    except redis.exceptions.WatchError as ex:
        print("pipe fail:",ex)
    else:
        print("pipe success")
    finally:
        print("finally: a=%s,cnt=%s,b=%s" % (client.get('a'),client.get('cnt'),client.get('b')))
        pipe.unwatch()              # 解锁


# 6. 发布／订阅 －－ 不推荐使用
# 发布： 
#   publish(channel,msg)     
#   => redis client execute : `publish channel msg` 
# 订阅： 
#   pubsub().subscribe(channel).parse_response(block,timeout)  
#   => redis client execute : `subscribe channel` (取消使用命令punsubscribe/unsubscribe)

import random

def test_publish():
    result=client.publish("channel-1","Hello!")
    print("result:",result)     # 0

    while True:
        msg = "This is %.2f" % (random.random()*10)
        print('sending...',msg)
        
        result=client.publish("channel-1",msg)
        if result==1:
            print('send success')
        else:
            print('send fail')

        isCondinue=input("continue?(y/n)")
        if isCondinue=='n':
            break;
    
    print('Done!')

def test_subscribe():
    subscribeObj = client.pubsub()
    result=subscribeObj.subscribe("channel-1")
    print(result)           # None

    while True:
        print('receiving...')
        msg=subscribeObj.parse_response(block=False,timeout=60)
        # 第一次收到：[b'subscribe', b'channel-1', 1]
        # 当另一个客户端向此channel发布消息时（eg: `publish channel-1 "Hello World"`）
        # 这里会收到： [b'message', b'channel-1', b'Hello World']
        print("receive msg:",msg)   
        isCondinue=input("continue?(y/n)")
        if isCondinue=='n':
            break;
    print("Done!")


if __name__=='__main__':

    # test_string()
    # test_hash()
    # test_list()
    # test_set()
    # test_zset()
    # test_others()

    # test_pipeline()

    # test_publish()
    # test_subscribe()

