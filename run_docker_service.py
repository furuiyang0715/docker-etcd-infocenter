import subprocess

env_debug = False
env_uwsgi_accept_http = True
env_mysql_user = 'test'
env_mysql_password = 'ruiyang'
env_mysql_host = '192.168.66.128'
env_redis_host = '192.168.66.128'
env_redis_password = ''
service_port = 7788
service_network = 'jingzhuannetwork'
service_name = 'test_service'
image_name = 'registry.cn-shenzhen.aliyuncs.com/jzdev/jzuser'
image_tag = '0.4.0'


def run():
    cmd = f'''
    docker service create --with-registry-auth \
    -e DEBUG={env_debug} \
    -e UWSGI_HTTP={env_uwsgi_accept_http} \
    -e MYSQL_USER={env_mysql_user} \
    -e MYSQL_PASSWORD={env_mysql_password} \
    -e MYSQL_HOST={env_mysql_host} -e REDIS_HOST={env_redis_host} \
    -p {service_port}:80 \
    --network {service_network} \
    --name {service_name} {image_name}:{image_tag}
    '''
    print(cmd)
    print(subprocess.getoutput(cmd))


if __name__ == '__main__':
    run()

