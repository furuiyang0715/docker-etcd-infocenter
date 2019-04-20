# register config

import json
import time

from docker.types import RestartPolicy
from docker.types.services import RestartConditionTypesEnum

import etcd


class EtcdConfigMixin(object):

    client = etcd.Client(host='127.0.0.1', port=2379)

    """"全局配置"""
    DOCKER_V_BIND = '/data/strategy_data'
    DOCKER_QUANT_IMAGE = 'cdh1:5000/jzquant:latest'
    JZDATAURI = "192.168.100.78:27017"
    DOCKER_NETWORK = ''
    STRATEGY_SENTRY_DSN = "https://key1:key2@sentry.jingzhuan.cn/x"
    MQ_HOST = "127.0.0.1"
    MQ_PORT = 5672
    STRATEGY_READ_EX = "task_cmd"
    STRATEGY_WRITE_EX = "strategy"
    MQ_VHOST = "quant"
    MQ_USERNAME = "guest"
    MQ_PASSWORD = "guest"
    MOUNTS = ["/etc/localtime:/etc/localtime:ro"]
    LOG_DRIVER = 'json-file'
    LOG_DRIVER_OPTIONS = {"max-size": "10m"}
    INDEX_SERVER_URIS = ''
    INDEX_SWITCH_SERVER = False
    # 策略类型
    BACKTEST = "backtest"
    REALTRADE = "realtrade"
    SIMULATION = "simulation"
    CBACKTEST = "cbacktest"

    """BACKTEST"""
    BACKTEST_RESTARTPOLICY = RestartPolicy(RestartConditionTypesEnum.NONE)
    BACKTEST_LABELS = {"type": "backtest"}
    STRATEGY_MONGO = ''

    """SIMULATION"""
    SIMULATION_LABELS = {'type': "simulation"}

    """REALTRADE"""
    DOCKER_QUANT_TRADE_IMAGE = 'cdh1:5000/jzquant:latest'
    QUANTUSER_SERVER_URL = "http://139.159.148.58/u"
    QUANTUSER_APP_ID = "back"
    QUANTUSER_TOKEN = "ff46fd5a21bf4fc4b3777e3ab4a96273"
    QUANTUSER_REDIS_URI = "redis://127.0.0.1/1"
    TRADE_HOST = "139.198.191.151"
    TRADE_PORT = 9980
    MYSQL_URI = "mysql+cymysql://root:ruiyang@127.0.0.1/trading?charset=utf8"
    FUTURE_QUOTE_HOST = "127.0.0.1"
    FUTURE_QUOTE_PORT = 24444
    FUTURE_TRADE_HOST = "127.0.0.1"
    FUTURE_TRADE_PORT = 9980
    REALTRADE_LABELS = {'type': "realtrade"}

    # - - - - - 配置设置 - - - - -

    def set_default_payload_backtest(self):
        """回测配置"""
        # /payload/backtest/volume
        volume = self.DOCKER_V_BIND

        # /payload/backtest/image
        image = self.DOCKER_QUANT_IMAGE

        # /payload/backtest/envs
        envs = [
            "JZDATAURI={}".format(self.JZDATAURI),
            f"SENTRY_DSN={self.STRATEGY_SENTRY_DSN}",
            f"MQ_HOST={self.MQ_HOST}",
            f"MQ_PORT={self.MQ_PORT}",
            f"STRATEGY_WRITE_EX={self.STRATEGY_WRITE_EX}",
            f"STRATEGY_READ_EX={self.STRATEGY_READ_EX}",
            f"MQ_VHOST={self.MQ_VHOST}",
            f"MQ_USERNAME={self.MQ_USERNAME}",
            f"MQ_PASSWORD={self.MQ_PASSWORD}",
        ]

        # /payload/backtest/labels
        labels = self.BACKTEST_LABELS

        # /payload/backtest/mounts
        mounts = self.MOUNTS

        # /payload/backtest/log_driver
        log_driver = self.LOG_DRIVER

        # /payload/backtest/log_driver_options
        log_driver_options = self.LOG_DRIVER_OPTIONS

        # /payload/backtest/restart_policy
        restart_policy = self.BACKTEST_RESTARTPOLICY

        # /payload/backtest/networks
        networks = self.DOCKER_NETWORK.split(',')

        self.client.write('/payload/backtest/volume', json.dumps(volume))
        self.client.write('/payload/backtest/image', json.dumps(image))
        self.client.write('/payload/backtest/envs', json.dumps(envs))
        self.client.write('/payload/backtest/labels', json.dumps(labels))
        self.client.write('/payload/backtest/mounts', json.dumps(mounts))
        self.client.write('/payload/backtest/log_driver', json.dumps(log_driver))
        self.client.write('/payload/backtest/log_driver_options', json.dumps(log_driver_options))
        self.client.write('/payload/backtest/restart_policy', json.dumps(restart_policy))
        self.client.write('/payload/backtest/networks', json.dumps(networks))


    # def read_default_payload_backtest(self):
    #     """测试"""
    #     volume = json.loads(self.client.read('/payload/backtest/volume').value)
    #     image = json.loads(self.client.read('/payload/backtest/image').value)
    #     envs = json.loads(self.client.read('/payload/backtest/envs').value)
    #     labels = json.loads(self.client.read('/payload/backtest/labels').value)
    #     mounts = json.loads(self.client.read('/payload/backtest/mounts').value)
    #     log_driver = json.loads(self.client.read('/payload/backtest/log_driver').value)
    #     log_driver_options = json.loads(self.client.read('/payload/backtest/log_driver_options').value)
    #     restart_policy = json.loads(self.client.read('/payload/backtest/restart_policy').value)
    #     networks = json.loads(self.client.read('/payload/backtest/networks').value)
    #
    #     return volume, image, envs, labels, mounts, log_driver, log_driver_options, restart_policy, networks


    def set_default_payload_simulation(self):
        """模拟盘配置"""
        # /payload/simulation/volume
        volume = self.DOCKER_V_BIND

        # /payload/simulation/image
        image = self.DOCKER_QUANT_IMAGE

        # /payload/simulation/envs
        envs = [
            "JZDATAURI={}".format(self.JZDATAURI),
            f"SENTRY_DSN={self.STRATEGY_SENTRY_DSN}",
            f"MQ_HOST={self.MQ_HOST}",
            f"MQ_PORT={self.MQ_PORT}",
            f"STRATEGY_WRITE_EX={self.STRATEGY_WRITE_EX}",
            f"STRATEGY_READ_EX={self.STRATEGY_READ_EX}",
            f"MQ_VHOST={self.MQ_VHOST}",
            f"MQ_USERNAME={self.MQ_USERNAME}",
            f"MQ_PASSWORD={self.MQ_PASSWORD}",
        ]

        # /payload/simulation/labels
        labels = self.SIMULATION_LABELS

        # /payload/simulation/mounts
        mounts = self.MOUNTS

        # /payload/simulation/log_driver
        log_driver = self.LOG_DRIVER

        # /payload/simulation/log_driver_options
        log_driver_options = self.LOG_DRIVER_OPTIONS

        # /payload/simulation/networks
        networks = self.DOCKER_NETWORK.split(',')

        self.client.write('/payload/simulation/volume', json.dumps(volume))
        self.client.write('/payload/simulation/image', json.dumps(image))
        self.client.write('/payload/simulation/envs', json.dumps(envs))
        self.client.write('/payload/simulation/labels', json.dumps(labels))
        self.client.write('/payload/simulation/mounts', json.dumps(mounts))
        self.client.write('/payload/simulation/log_driver', json.dumps(log_driver))
        self.client.write('/payload/simulation/log_driver_options', json.dumps(log_driver_options))
        self.client.write('/payload/simulation/networks', json.dumps(networks))


    # def read_default_payload_simulation(self):
    #     """读取测试"""
    #     volume = json.loads(self.client.read('/payload/simulation/volume').value)
    #     image = json.loads(self.client.read('/payload/simulation/image').value)
    #     envs = json.loads(self.client.read('/payload/simulation/envs').value)
    #     labels = json.loads(self.client.read('/payload/simulation/labels').value)
    #     mounts = json.loads(self.client.read('/payload/simulation/mounts').value)
    #     log_driver = json.loads(self.client.read('/payload/simulation/log_driver').value)
    #     log_driver_options = json.loads(self.client.read('/payload/simulation/log_driver_options').value)
    #     networks = json.loads(self.client.read('/payload/simulation/networks').value)
    #
    #     return volume, image, envs, labels, mounts, log_driver, log_driver_options, networks


    def set_default_payload_realtrade(self):
        """实盘配置"""
        # /payload/realtrade/volume
        volume = self.DOCKER_V_BIND

        # /payload/realtrade/image
        # 注意，使用的是实盘的镜像
        image = self.DOCKER_QUANT_TRADE_IMAGE

        # /payload/realtrade/envs
        envs = [
            "JZDATAURI={}".format(self.JZDATAURI),
            'MYSQL_URI={}'.format(self.MYSQL_URI),
            "QUANTUSER_URL={}".format(self.QUANTUSER_SERVER_URL),
            "QUANTUSER_APP_ID={}".format(self.QUANTUSER_APP_ID),
            "QUANTUSER_TOKEN={}".format(self.QUANTUSER_TOKEN),
            "QUANTUSER_REDIS_URI={}".format(self.QUANTUSER_REDIS_URI),
            "TRADE_HOST={}".format(self.TRADE_HOST),
            "TRADE_PORT={}".format(self.TRADE_PORT),
            f"SENTRY_DSN={self.STRATEGY_SENTRY_DSN}",
            f"MQ_HOST={self.MQ_HOST}",
            f"MQ_PORT={self.MQ_PORT}",
            f"STRATEGY_WRITE_EX={self.STRATEGY_WRITE_EX}",
            f"STRATEGY_READ_EX={self.STRATEGY_READ_EX}",
            f"MQ_VHOST={self.MQ_VHOST}",
            f"MQ_USERNAME={self.MQ_USERNAME}",
            f"MQ_PASSWORD={self.MQ_PASSWORD}",
            f"FUTURE_QUOTE_HOST={self.FUTURE_QUOTE_HOST}",
            f"FUTURE_QUOTE_PORT={self.FUTURE_QUOTE_PORT}",
            f"FUTURE_TRADE_HOST={self.FUTURE_TRADE_HOST}",
            f"FUTURE_TRADE_PORT={self.FUTURE_TRADE_PORT}",
        ]

        # /payload/realtrade/labels
        labels = self.REALTRADE_LABELS

        # /payload/realtrade/mounts
        mounts = self.MOUNTS

        # /payload/realtrade/log_driver
        log_driver = self.LOG_DRIVER

        # /payload/realtrade/log_driver_options
        log_driver_options = self.LOG_DRIVER_OPTIONS

        # /payload/realtrade/networks
        networks = self.DOCKER_NETWORK.split(',')

        self.client.write('/payload/realtrade/volume', json.dumps(volume))
        self.client.write('/payload/realtrade/image', json.dumps(image))
        self.client.write('/payload/realtrade/envs', json.dumps(envs))
        self.client.write('/payload/realtrade/labels', json.dumps(labels))
        self.client.write('/payload/realtrade/mounts', json.dumps(mounts))
        self.client.write('/payload/realtrade/log_driver', json.dumps(log_driver))
        self.client.write('/payload/realtrade/log_driver_options', json.dumps(log_driver_options))
        self.client.write('/payload/realtrade/networks', json.dumps(networks))

    # def read_default_payload_realtrade(self):
    #     """读取测试"""
    #     volume = json.loads(self.client.read('/payload/realtrade/volume').value)
    #     image = json.loads(self.client.read('/payload/realtrade/image').value)
    #     envs = json.loads(self.client.read('/payload/realtrade/envs').value)
    #     labels = json.loads(self.client.read('/payload/realtrade/labels').value)
    #     mounts = json.loads(self.client.read('/payload/realtrade/mounts').value)
    #     log_driver = json.loads(self.client.read('/payload/realtrade/log_driver').value)
    #     log_driver_options = json.loads(self.client.read('/payload/realtrade/log_driver_options').value)
    #     networks = json.loads(self.client.read('/payload/realtrade/networks').value)
    #
    #     return volume, image, envs, labels, mounts, log_driver, log_driver_options, networks

    def set_base_config(self):
        """对于所有策略 其基础配置项"""
        config = []

        config.extend(['--mod-config', 'messaging__enabled', "true"])

        self.client.set("/strategy/config/base/", json.dumps(config))
        return config

    # def read_base_config(self):
    #     """读取测试"""
    #     base = json.loads(self.client.read("/strategy/config/base/").value)
    #     return base

    def set_guide_config(self):
        """对于向导式策略 其默认配置"""
        config = []
        code = """
def init(context):
   logger.info('向导式策略启动')
def handle_bar(context, bar_dict):
   pass
        """
        config.extend(['--source-code', code])
        config.extend(['--mod-config', "guide_buy_sell__enabled", 'true'])
        config.extend(['--mod-config', "guide_stockpool__enabled", 'true'])

        self.client.set("/strategy/config/guide/", json.dumps(config))
        return config

    # def read_guide_config(self):
    #     """读取测试"""
    #     guide = json.loads(self.client.read("/strategy/config/guide/").value)
    #     return guide

    def set_codes_config(self):
        """对于编码式配置 其默认配置"""
        config = []
        self.client.set("/strategy/config/codes/", json.dumps(config))
        return config

    # def read_codes_config(self):
    #     """读取测试"""
    #     codes = json.loads(self.client.read("/strategy/config/codes/").value)
    #     return codes

    def set_backtest_config(self):
        """对于回测策略 其默认配置"""
        config = ['--run-type', 'b']
        config.extend(['--mod-config', 'trade_message__enabled', 'true'])
        config.extend(['--mod-config', 'storeDB__enabled', 'true'])
        config.extend(['--mod-config', 'storeDB__host', self.STRATEGY_MONGO])
        config.extend(['--mod-config', "messaging__rw", "1"])

        self.client.set("/strategy/config/backtest/", json.dumps(config))
        return config

    # def read_backtest_config(self):
    #     """读取测试"""
    #     back = json.loads(self.client.read("/strategy/config/backtest/").value)
    #     return back

    def set_simulation_config(self):
        """对于模拟策略 其默认配置"""
        config = ['--run-type', 'p']
        config.extend(['--log-level', "verbose"])
        config.extend(['--mod-config', "realtime__enabled", 'true'])
        config.extend(['--mod-config', "messaging__rw", "3"])

        self.client.set("/strategy/config/simulation/", json.dumps(config))
        return config

    # def read_simulation_config(self):
    #     """读取测试"""
    #     simulation = json.loads(self.client.read("/strategy/config/simulation/").value)
    #     return simulation

    def set_realtrade_config(self):
        """对于实盘策略 其默认配置"""
        config = ['--run-type', 'r']
        config.extend(['--log-level', "verbose"])

        config.extend(['--mod-config', "sys_simulation__enabled", "false"])
        config.extend(["--mod-config", "sys_progress__enabled", "false"])
        config.extend(['--mod-config', "sys_analyser__enabled", "false"])

        config.extend(['--mod-config', "messaging__rw", "3"])
        config.extend(['--mod-config', "realtrade__enabled", "true"])

        config.extend(['--mod-config', "sys_risk__enabled", "true"])
        config.extend(['--mod-config', 'mongodb__enabled', 'true'])
        config.extend(['--mod-config', 'mongodb__mongouri', 'JZDATAURI'])
        config.extend(['--mod-config', "terminator__enabled", "true"])

        self.client.set("/strategy/config/realtrade/", json.dumps(config))
        return config

    # - - - - - 配置生成 - - - - -
    # 一个策略的启动配置项分为两部分： （1）是从 etcd 中读取到 （2） 是根据具体用户和策略的个性化生成
    def gen_baseconfig(self, run_type="b"):
        config_atr = ('start_date', 'end_date', 'stock_starting_cash', 'frequency', 'benchmark')

        configs = ['--run-type', run_type]
        for attr in config_atr:
            attr = str(attr)
            configs.append('--' + attr.replace('_', '-'))
            configs.append(str(getattr(self, attr)))

        configs.extend(['--user-id', str(self.user_id)])
        configs.extend(['--user-account', str(self.user_account)])
        configs.extend(['--strategy-id', str(self.id)])
        configs.extend(['--strategy-name', self.name])
        configs.extend(['--code-type', self.type])

        # ====== 使用固定配置 ======
        # configs.extend(['--mod-config', 'messaging__enabled', "true"])
        config = json.loads(self.client.read("/strategy/config/base/").value)
        configs.extend(config)
        # =========================

        uris = self.INDEX_SERVER_URIS.split(",")
        server_list = []
        for group in uris:
            server = group.split(":")
            server_list.append((server[0].strip(), server[1].strip()))

        if self.INDEX_SWITCH_SERVER:
            seed = int(time.time())
            selected = server_list[seed % len(server_list)]
        else:
            selected = server_list[0]

        configs.extend(["--index-server", selected[0]])
        configs.extend(["--index-port", str(selected[1])])

        # 根据 run_type 来确定 mod_enabled
        if run_type == "b":
            mod_enabled = True

        elif run_type == "p":
            pass

        elif run_type == "r":
            pass

        if mod_enabled:
            configs.extend(['--mod-config', 'mongodb__enabled', 'true'])
            configs.extend(['--mod-config', 'exception__enabled', "true"])
            configs.extend(['--mod-config', 'mongodb__mongouri', self.JZDATAURI])

        return configs

    def gen_buysellconfig(self, run_type):
        """针对向导策略的生成"""

        configs = []
        guide = self.guide
        stock_pool = guide.pop('stock', {})
        hedge = guide.pop('hedge', {})
        configs.extend(['--mod-config', 'guide_buy_sell__kwarg', json.dumps(guide)])
        configs.extend(['--mod-config', "guide_stockpool__kwarg", json.dumps(stock_pool)])

        # ====== 使用固定配置 ======
#         code = """
# def init(context):
#     logger.info('向导式策略启动')
# def handle_bar(context, bar_dict):
#     pass
#                 """
#         configs.extend(['--source-code', code])
#         configs.extend(['--mod-config', "guide_buy_sell__enabled", 'true'])
#         configs.extend(['--mod-config', "guide_stockpool__enabled", 'true'])
        guide = json.loads(self.client.read("/strategy/config/guide/").value)
        configs.extend(guide)
        # =========================

        if run_type == "p":
            configs.extend(['--mod-config', "realtime__fps", '30'])

        elif run_type == "r":
            configs.extend(['--mod-config', "realtime__fps", '30'])

        return configs

    def gen_codesconfig(self, run_type):
        """针对编码式策略的生成"""
        configs = []

        if run_type == "p":
            return configs

        elif run_type == "r":
            return configs

        configs.extend(['--source-code', self.strategy_code])

        codes = json.loads(self.client.read("/strategy/config/codes/").value)
        configs.extend(codes)

        return configs

    def gen_strategy_config(self, run_type):
        configs = []
        if run_type == "b":
            # 个性化配置
            configs.extend(['--log-level', self.log_level])
            configs.extend(['--mod-config', "sys_simulation__matching_type", self.matching_type])
            configs.extend(['--mod-config', "sys_simulation__slippage", str(self.slippage)])
            configs.extend(['--mod-config', "sys_simulation__commission_multiplier",
                        str(self.commission_multiplier)])
            configs.extend(['--mod-config', "sys_simulation__stock_min_commision",
                        str(self.stock_min_commision)])

            configs.extend(['--task-id', self.task_id])

            if self.debug:
                configs.extend(['--mod-config', 'trade_message__debug', 'true'])

            # ====== 使用固定配置 ======
            # configs.extend(['--mod-config', 'trade_message__enabled', 'true'])
            # configs.extend(['--mod-config', 'storeDB__enabled', 'true'])
            # configs.extend(['--mod-config', 'storeDB__host', self.STRATEGY_MONGO])
            # configs.extend(['--mod-config', "messaging__rw", "1"])

            configs.extend(json.loads(self.client.read("/strategy/config/backtest").value))

            return configs

        elif run_type == "p":
            configs.extend(['--task-id', str(self.id)])
            configs.extend(['--mod-config', "sys_simulation__matching_type", self.matching_type])
            configs.extend(['--mod-config', "sys_simulation__slippage", str(self.slippage)])
            configs.extend(['--mod-config', "sys_simulation__commission_multiplier",
                            str(self.commission_multiplier)])
            configs.extend(['--mod-config', "realtime__simulation_id", str(self.simulation_id)])

            # 配置项替换
            # configs.extend(['--log-level', "verbose"])
            # configs.extend(['--mod-config', "realtime__enabled", 'true'])
            # configs.extend(['--mod-config', "messaging__rw", "3"])
            configs.extend(json.loads(self.client.read("/strategy/config/simulation/").value))

            return configs

        elif run_type == "r":
            configs.extend(['--task-id', str(self.id)])
            configs.extend(['--mod-config', 'mongodb__mongouri', self.JZDATAURI])

            # 配置项替换
            # configs.extend(['--log-level', "verbose"])
            # configs.extend(['--mod-config', "sys_simulation__enabled", "false"])
            # configs.extend(["--mod-config", "sys_progress__enabled", "false"])
            # # configs.extend(["--mod-config", "zmq_message__enabled", "false"])
            # configs.extend(['--mod-config', "sys_analyser__enabled", "false"])
            # configs.extend(['--mod-config', "messaging__rw", "3"])
            # configs.extend(['--mod-config', "realtrade__enabled", "true"])
            # # configs.extend(['--mod-config', "async_zmq__enabled", "true"])
            # configs.extend(['--mod-config', "sys_risk__enabled", "true"])
            # configs.extend(['--mod-config', 'mongodb__enabled', 'true'])
            # configs.extend(['--mod-config', "terminator__enabled", "true"])
            configs.extend(json.loads(self.client.read("/strategy/config/realtrade/").value))
            return configs

    def gen_spaw_config(self):
        ori = ['JZquant', 'run']

        # step 1
        ori.extend(self.gen_baseconfig(self.run_type))

        # step 2
        if self.type == "向导式":
            ori.extend(self.gen_buysellconfig(self.run_type))
        elif self.type == "编码式":
            ori.extend(self.gen_codesconfig(self.run_type))

        # step 3
        ori.extend(self.gen_strategy_config(self.run_type))

        return ori

    def gen_spaw_env(self):
        if self.run_type == "b":
            env = json.loads(self.client.read("").value)
        # elif type == self.SIMULATION:
        #     env = json.loads(self.client.read("").value)
        # elif type == self.REALTRADE:
        #     env = json.loads(self.client.read("").value)
        # elif type == self.CBACKTEST:
        #     env = json.loads(self.client.read("").value)
        return env

    def service_args(self, user):
        service_args = {}
        config = self.gen_spaw_config()
        (volume, image, envs, labels, mounts, log_driver, log_driver_options,
         restart_policy, networks) = self.gen_spaw_env()

        service_args.update({
            "image": image,
            "labels": labels.update({"user": user}),
            "mounts": mounts,
            "envs": envs,
            "lod_driver": log_driver,
            "log_driver_options": log_driver_options,
            "restart_policy": restart_policy,
            "networks": networks,
            "name": self.task_name,
        })
        return service_args


class DockerSpawnerMixin(object):

    def run_backtest(self, command, env, user, backtest_type="backtest"):


        return self.client.services.create(image,
                                           command=command,
                                           labels={'type': backtest_type, "user": user},
                                           # mounts=['{}:/root/.rqalpha:rw'.format(volume),
                                           mounts=["/etc/localtime:/etc/localtime:ro"],
                                           env=envs,
                                           log_driver='json-file',
                                           log_driver_options={"max-size": "10m"},
                                           restart_policy=restart_policy,
                                           networks=networks,
                                           *args, **kwargs)

    def spawn(self, command, env, user="anonymous"):
        if self.run_type == "b":  # backtest
            return self.run_backtest(command, env, user=user)
        elif self.run_type == "p":  # simulation
            return self.run_simulation(command, env, user=user)
        elif self.run_type == "r":  # realtrade
            return self.run_realtrade(command, env, user=user)
        elif self.run_type == "c":  # cbacktest
            return self.run_backtest(command, env, user=user, backtest_type=self.CBACKTEST)
        else:
            raise NotImplementedError


class StrategyApp(EtcdConfigMixin, DockerSpawnerMixin):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def backtest_strategy(self, user, **kwargs):
        # EtcdConfigMixin
        service_args = self.service_args(user)
        # DockerSpawnerMixin
        service_args.update(kwargs)
        container = self.spawn(service_args)
        # TODO 打印日志
        return container


if __name__ == "__main__":
    import sys
    # 生成一个策略对象
    class Strategy(object):
        def __init__(self, **kwargs):
            self.__dict__ = kwargs

    # 生成一个策略的输入部分
    args = {
        "name": '符瑞阳的策略001',
        "type": "向导式",
        "strategy_code": "abcdefg",
        "start_date": "2016-01-01",
        "end_date": "2017-09-01",
        "stock_starting_cash": 100000,
        "frequency": "1d",
        "benchmark": '000001.XSHG',
        "matching_type": "current_bar",
        "slippage": 0,
        "commission_multiplier": 1,
        "stock_min_commision": 5,
        "log_level": "info",
        "guide": {}

    }
    strategy = Strategy(**args)
    # sys.exit(0)
    # 生成 MongoJStrategies 对象增加参数部分
    user_uid = "1"  # request.user.uid
    user_username = "ruiyang"  # request.user.username
    timestamp = time.time()
    strategy.__dict__.update({
        'modified_time': timestamp,
        'create_time': timestamp,
        'user_id': user_uid,
        'user_account': user_username,
        'task_names': []
    })
    # print(strategy.__dict__)
    # print(strategy.name)
    # print(strategy.task_names)
    # sys.exit(0)

    # 开始回测
    # id为创建MongoJStrategies数据库生产的id
    import bson
    id = str(bson.ObjectId())
    # print(id)
    # sys.exit(0)

    # task 为随机随机生成的 ObjectId，表示生成了一个任务对象
    task = str(bson.ObjectId())

    # 生成一个 task_name 作为 每个策略的唯一标识
    task_name = "{}_{}_{}".format('b', user_uid, task)

    # 增加参数 生成启动回测的 StrategyApp 对象
    debug = True   # 根据启动的时候输入的 action 决定的
    strategy.__dict__.update({
        "id": id,
        "task": task,
        "task_name": task_name,
        "debug": debug,
        "run_type": "b"
    })

    # 生层回测所需的 commonds 参数
    ori = ['JZquant', 'run']
    # 增加 base_config 参数
    # (1) 回测类型
    base = ['--run-type', strategy.run_type]
    # print(base)
    # sys.exit(0)
    # (2) 起止时间 起始资金 频率 基准
    # 用户id 用户账户
    config_atr = ('start_date', 'end_date', 'stock_starting_cash', 'frequency', 'benchmark')
    for attr in config_atr:
        attr = str(attr)
        base.append('--' + attr.replace('_', '-'))
        base.append(str(getattr(strategy, attr)))
    base.extend(['--user-id', str(strategy.user_id)])
    base.extend(['--user-account', str(strategy.user_account)])
    base.extend(['--strategy-id', str(strategy.id)])
    base.extend(['--strategy-name', strategy.name])
    base.extend(['--code-type', strategy.type])
    # print(base)
    # sys.exit(0)

    if strategy.type == "向导式":
        guide = strategy.guide
        stock_pool = guide.pop('stock', {})
        hedge = guide.pop('hedge', {})
        code = """
def init(context):
    logger.info('向导式策略启动')
def handle_bar(context, bar_dict):
    pass
        """
        base.extend(['--source-code', code])
        base.extend(['--mod-config', "guide_buy_sell__enabled", 'true'])
        base.extend(['--mod-config', 'guide_buy_sell__kwarg', json.dumps(guide)])

        base.extend(['--mod-config', "guide_stockpool__enabled", 'true'])
        base.extend(['--mod-config', "guide_stockpool__kwarg", json.dumps(stock_pool)])

        # print(base)
        # sys.exit(0)

    elif strategy.type == "编码式":
        ori.extend(['--source-code', strategy.strategy_code])

    base.extend(['--log-level', strategy.log_level])
    base.extend(['--task-id', strategy.task])

    base.extend(['--mod-config', "sys_simulation__matching_type", strategy.matching_type])
    base.extend(['--mod-config', "sys_simulation__slippage", str(strategy.slippage)])
    base.extend(['--mod-config', "sys_simulation__commission_multiplier",
                 str(strategy.commission_multiplier)])
    base.extend(['--mod-config', "sys_simulation__stock_min_commision",
                 str(strategy.stock_min_commision)])

    # print(base)
    # sys.exit(0)
    # ---------------------非动态部分——-------------------------------------------------------
    # 当回测类型是 'b' 设置 mod_enabled 为 True
    if strategy.run_type == "b":
        mod_enabled = True
    # 可能会放在 etcd 中的一部分
    etcd = {
        "JZDATAURI": '',
        "STRATEGY_MONGO": "",
        "INDEX_SERVER_URIS": "",
        "INDEX_SWITCH_SERVER": ""
    }

    if mod_enabled:
        base.extend(['--mod-config', 'mongodb__enabled', 'true'])
        base.extend(['--mod-config', 'exception__enabled', "true"])
        base.extend(['--mod-config', 'mongodb__mongouri', etcd.get("JZDATAURI")])  # TODO

    if strategy.debug:
        ori.extend(['--mod-config', 'trade_message__debug', 'true'])

    base.extend(['--mod-config', 'storeDB__host', etcd.get("STRATEGY_MONGO")])
    base.extend(['--mod-config', 'trade_message__enabled', 'true'])
    base.extend(['--mod-config', 'storeDB__enabled', 'true'])
    base.extend(['--mod-config', "messaging__rw", "1"])


    # 与具体策略无关的非动态配置 在 etcd 中获取
    base.extend(['--mod-config', 'messaging__enabled', "true"])
    uris = etcd.get("INDEX_SERVER_URIS").split(",")
    server_list = []
    for group in uris:
        server = group.split(":")
        server_list.append((server[0].strip(), server[1].strip()))

    if etcd.get("INDEX_SWITCH_SERVER"):
        seed = int(time.time())
        selected = server_list[seed % len(server_list)]
    else:
        selected = server_list[0]

    base.extend(["--index-server", selected[0]])
    base.extend(["--index-port", str(selected[1])])

    print(base)
    sys.exit(0)

    task_name, container = start_backtest(user_uid, id)


# 一个策略执行过程中的属性变化

# （1） 新增一个策略
"""
输入部分：
name  # 策略名称 
type  # 类型 -->  向导式 编码式
strategy_code  # 策略代码 
start_date  # 开始日期 默认是"2016-01-01"
end_date  # 结束日期  默认是 "2017-09-01"
stock_starting_cash  # 起始资金  默认是 100000
frequency  # 回测频率 默认是 '1d'
benchmark  # 回测基准 默认是 '000001.XSHG'
matching_type  # 撮合方式 默认 current_bar
slippage  # 滑点 默认是 0
commission_multiplier  # 交易费用设置 默认是 1
stock_min_commision  # 股票最低佣金费用 默认是 5
log_level   # 日志等级 默认是 info
guide  # 向导式策略的一些默认的参数 


更新进入部分：
args.update({
    'modified_time': timestamp,   # 更新时间 
    'create_time': timestamp,  # 创建时间 
    'user_id': request.user.uid,  # 用户 id
    'user_account': request.user.username,  # 用户账户 
    'task_names': []  # task 列表 
})

以上，创建出一个 MongoJStrategies 对象 
new_strategy = MongoJStrategies.create_new(**args)

"""

# （2） 启动回测
"""
action   # backtest 和 backtest_debug
如果是backtest：
task_name, container = self.start_backtest(request.user.uid, id)
如果是 backtest_debug：
task_name, container = self.start_backtest(request.user.uid, id, debug=True)

start_backtest 是在 JStrategyMixin 实现 
在其中新增参数如下：
strategy.update({
    "task": task, 
    "task_name": task_name, 
    "debug": debug,  # 根据 action 为 backtest 还是 backtest_debug 来确定 
    "run_type": "b"
    
})

用以上参数生成 strategy = StrategyApp(**strategy) 对象 
开启回测：
def backtest_strategy(self, user):
    env, commonds = self.config_args()
    return self.spawn(user=user, command=commonds, env=env)

"""
