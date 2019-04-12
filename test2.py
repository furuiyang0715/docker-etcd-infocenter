import time
import etcd
# 创建一个运行在本机 2379 端口的client
client = etcd.Client(host='127.0.0.1', port=2379)

print(client.read('/nodes/n1').value)
res = client.read("/nodes/n1")
print(res)
res.value = 22
client.update(res)