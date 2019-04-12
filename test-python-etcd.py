# 练习python-etcd 模块的使用'

# 首先要在 macos 上安装 etcd

import time
import etcd
# # 创建一个运行在本机 2379 端口的client
client = etcd.Client(host='127.0.0.1', port=2379)
# 集群的写法 ？？
# client = etcd.Client(host=(('127.0.0.1', 4001), ('127.0.0.1', 4002), ('127.0.0.1', 4003)))
# print(client)

# 简单的写入和读出
# client.write('/nodes/n1', 1)
# client.set('/nodes/n1', 1)  # set 和 write 等效
# print(client.read('/nodes/n1').value)

# # 设置过期时间
# client.write('/nodes/n2', 2, ttl=4)
# print(client.read("/nodes/n2").value)
# time.sleep(5)
# try:
#     print(client.read("/nodes/n2").value)
# except Exception as e:
#     print(e)  # Key not found : /nodes/n2
#
# # 循环获取某个节点的值
# try:
#     print(client.read("/nodes").value)
#     # get all the values of a directory, recursively.
#     print(client.read("/nodes", recursive=True))
# except Exception as e:
#     print(e)

# 删除
# client.delete('/nodes/n1')
# try:
#     print(client.read("/nodes/n1"))
# except Exception as e:
#     print(e)

# Atomic Compare and Swap
# client.set("/nodes/n2", 3)
# try:
#     # 这样会报错出来的 ...
#     client.write('/nodes/n2', 2, prevValue=4)  # will set /nodes/n2 's value to 2 only if its previous value was 4 and
# except Exception as e:
#     print(e)
#
# print(client.read("/nodes/n2").value)

# try:
#     client.write('/nodes/n2', 2, prevExist=False)
#     # will set /nodes/n2 's value to 2 only if the key did not exist before
# except Exception as e:
#     print(e)  # Key already exists : /nodes/n2

# print(client.read("/nodes/n2"))
# try:
#     # 存了一个创建的索引和修改的索引
#     client.write('/nodes/n2', 2, prevIndex=59)
#     # <class 'etcd.EtcdResult'>
#     # ({'action': 'get', 'key': '/nodes/n2', 'value': '3', 'expiration': None, 'ttl': None,
#     # 'modifiedIndex': 59, 'createdIndex': 59, 'newKey': False, 'dir': False, '_children': [],
#     # 'etcd_index': 59, 'raft_index': 156})
# except Exception as e:
#     print(e)
# # will set /nodes/n2 's value to 2 only if the key was last modified at index 30

# client.test_and_set('/nodes/n2', 2, 4)  # equivalent to client.write('/nodes/n2', 2, prevValue = 4)
#
# # 更新值
# result = client.read('/foo')
# print(result.value) # bar
# result.value += u'bar'
# updated = client.update(result) # if any other client wrote '/foo' in the meantime this will fail
# print(updated.value) # barbar

# will wait till the key is changed, and return once its changed
# 这个语句会使程序一直处于一种阻塞状态
# try:
#     print(client.read('/nodes/n1', wait=True))
# except Exception as e:
#     print(e)
#     # 一直未改变回报错： Watch timed out: ReadTimeoutError("HTTPConnectionPool(host='127.0.0.1', port=2379): Read timed out.")
#
# # 设置wait的超时时间
# # client.read('/nodes/n1', wait = True, timeout=30)
# # will wait till the key is changed, and return once its changed, or exit with an exception after 30 seconds.
# client.read('/nodes/n1', wait=True, timeout=30)

# 从某个index之后返回其所有的修改
# print(client.read('/nodes/n1', wait=True, waitIndex=60, timeout=None))
# # get all changes on this key starting from index 10
#
# # watch 和 read
# client.watch('/nodes/n1') #equivalent to client.read('/nodes/n1', wait = True)
# client.watch('/nodes/n1', index=10)
#
#
# """
# (Since etcd 2.3.0) Keys in etcd can be refreshed without notifying current watchers.
#
# This can be achieved by setting the refresh to true when updating a TTL.
#
# You cannot update the value of a key when refreshing it.
# """
#
# client.write('/nodes/n1', 'value', ttl=30)  # sets the ttl to 30 seconds
# client.refresh('/nodes/n1', ttl=600)  # refresh ttl to 600 seconds, without notifying current watchers


# # Locking module
# # Initialize the lock object:
# # NOTE: this does not acquire a lock yet
# import etcd
# client = etcd.Client()
# # Or you can custom lock prefix, default is '/_locks/' if you are using HEAD
# client = etcd.Client(lock_prefix='/my_etcd_root/_locks')
# lock = etcd.Lock(client, 'my_lock_name')
#
# # Use the lock object:
# lock.acquire(blocking=True,  # will block until the lock is acquired
#       lock_ttl=None)  # lock will live until we release it
# print(lock.is_acquired)  # True
# lock.acquire(lock_ttl=60)  # renew a lock
# lock.release()  # release an existing lock
# print(lock.is_acquired)  # False
#
# # The lock object may also be used as a context manager:
# client = etcd.Client()
# with etcd.Lock(client, 'customer1') as my_lock:
#     # do_stuff()
#     print(my_lock.is_acquired)  # True
#     my_lock.acquire(lock_ttl=60)
# print(my_lock.is_acquired)  # False


# Generate a sequential key in a directory
# 在目录中生成顺序的键值
x = client.write("/dir/name", "v1", append=True)
# print("generated key: " + x.key)
# print("stored value: " + x.value)
print(client.read("/dir/name"))
"""
<class 'etcd.EtcdResult'>({'action': 'get', 'key': '/dir/name', 'value': None, 'expiration': None, 'ttl': None, 
'modifiedIndex': 69, 'createdIndex': 69, 'newKey': False, 'dir': True, 
'_children': [{'key': '/dir/name/00000000000000000069', 'value': 'value', 'modifiedIndex': 69, 'createdIndex': 69}, 
{'key': '/dir/name/00000000000000000070', 'value': 'value', 'modifiedIndex': 70, 'createdIndex': 70}, 
{'key': '/dir/name/00000000000000000071', 'value': 'v1', 'modifiedIndex': 71, 'createdIndex': 71}, 
{'key': '/dir/name/00000000000000000072', 'value': 'v1', 'modifiedIndex': 72, 'createdIndex': 72}], 'etcd_index': 72, 
'raft_index': 170})

"""

# 展示目录下内容
#stick a couple values in the directory
# client.write("/dir/name", "value1", append=True)
# client.write("/dir/name", "value2", append=True)

directory = client.get("/dir/name")

# loop through directory children
for result in directory.children:
  print(result.key + ": " + result.value)

# or just get the first child value
print(type(directory.children))
# print(directory.children.next().value)

