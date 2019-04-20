import docker

docker_client = docker.from_env()

# 查看当前集群中的所有服务
services = docker_client.services.list()

# print(services)

# 挑选其中的一个服务：
service = services[0]

# print(service)

# 服务名
name = service.name

# print(name)

# 查看服务有哪些属性
features = service.attrs

# print(features)

# 有关服务的注册 service对象主要有以下属性：
features = {
    'ID': '4bag7a7d2o7vuvoinhp22ykzu',
    'Version': {'Index': 328},
    'CreatedAt': '2019-04-12T07:56:02.279361917Z',
    'UpdatedAt': '2019-04-12T07:56:02.348543611Z',

    'Spec': {
        'Name': 'nginx',
        'Labels': {},   # 主要用来记录服务启动的内容
        'TaskTemplate': {
            'ContainerSpec': {
                'Image': 'nginx:1.13.7-alpine@sha256:34aa80bb22c79235d466ccbbfa3659ff815100ed21eddb1543c6847292010c4d',
                'Init': False,
                'DNSConfig': {},
                'Isolation': 'default'
            },
            'Resources': {
                'Limits': {},
                'Reservations': {}
            },
            'Placement': {
                'Platforms': [{'Architecture': 'amd64', 'OS': 'linux'}]
            },
            'ForceUpdate': 0,
            'Runtime': 'container'
        },

        'Mode': {
            'Replicated': {'Replicas': 3}
        },
        'EndpointSpec': {
            'Mode': 'vip',
            'Ports': [{'Protocol': 'tcp', 'TargetPort': 80, 'PublishedPort': 80, 'PublishMode': 'ingress'}]
        }},

    'Endpoint': {

        'Spec': {
            'Mode': 'vip',
            'Ports': [{'Protocol': 'tcp', 'TargetPort': 80, 'PublishedPort': 80, 'PublishMode': 'ingress'}]},

        'Ports': [{'Protocol': 'tcp', 'TargetPort': 80, 'PublishedPort': 80, 'PublishMode': 'ingress'}],
        'VirtualIPs': [{'NetworkID': '6fiijend7xuverqkvcnhwei3u', 'Addr': '10.255.0.38/16'}]}}

