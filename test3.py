import sys
import time
import json

import etcd

from docker.types import RestartPolicy
from docker.types.services import RestartConditionTypesEnum


class EtcdConfigMixin(object):

    BACKTEST = "backtest"
    REALTRADE = "realtrade"
    SIMULATION = "simulation"
    CBACKTEST = "cbacktest"

    # configs
    INDEX_SERVER_URIS = "139.159.135.96:9802"
    JZDATAURI = "192.168.100.78:27017"
    STRATEGY_MONGO = ''
    INDEX_SWITCH_SERVER = False

    # envs
    DOCKER_QUANT_IMAGE = 'cdh1:5000/jzquant:latest'
    DOCKER_V_BIND = '/data/strategy_data'
    DOCKER_NETWORK = ''
    STRATEGY_SENTRY_DSN = "https://key1:key2@sentry.jingzhuan.cn/x"
    MQ_HOST = "127.0.0.1"
    MQ_PORT = 5672
    STRATEGY_WRITE_EX = "strategy"
    STRATEGY_READ_EX = "task_cmd"
    MQ_VHOST = "quant"
    MQ_USERNAME = "guest"
    MQ_PASSWORD = "guest"

    QUANTUSER_SERVER_URL = "http://139.159.148.58/u"
    QUANTUSER_APP_ID = "back"
    QUANTUSER_TOKEN = ''
    QUANTUSER_REDIS_URI = ''
    DOCKER_QUANT_TRADE_IMAGE = ''
    TRADE_HOST = "ff46fd5a21bf4fc4b3777e3ab4a96273"
    TRADE_PORT = 9980
    MYSQL_URI = "mysql+cymysql://root:ruiyang@127.0.0.1/trading?charset=utf8"

    FUTURE_QUOTE_HOST = "127.0.0.1"
    FUTURE_QUOTE_PORT = 24444
    FUTURE_TRADE_HOST = "127.0.0.1"
    FUTURE_TRADE_PORT = 9980

    MOUNTS = ["/etc/localtime:/etc/localtime:ro"]

    log_driver = 'json-file'
    log_driver_options = {"max-size": "10m"}
    restart_policy = RestartPolicy(RestartConditionTypesEnum.NONE)
    source_code = """
def init(context):
    logger.info('向导式策略启动')
def handle_bar(context, bar_dict):
    pass
        """

    backtest_dir = "/service/config/backtest/"
    simulation_dir = "/service/config/simulation/"
    realtrade_dir = "/service/config/realtrade/"
    backtest_environment_dir = "/service/environment/backtest/"
    simulation_environment_dir = "/service/environment/simulation/"
    realtrade_environment_dir = "/service/environment/realtrade/"


    @property
    def etcd(self):
        return etcd.Client(host='127.0.0.1', port=2379)

    def set_realtrade_args(self):
        realtrade = dict()

        config_atr = ('run_type', 'mod_config'
                      'start_date', 'end_date', 'stock_starting_cash', 'frequency', 'benchmark',
                      'user_id', 'user_account', 'strategy_id', 'strategy_name', 'code_type',
                      'index_server_uris', 'index_switch_server',
                      'source_code',
                      'log_level', 'task_id'
                      )

        mod_atr = ('messaging__enabled', 'mongodb__enabled', 'exception__enabled', 'mongodb__mongouri',
                   'guide_buy_sell__enabled', 'guide_buy_sell__kwarg',
                   'guide_stockpool__enabled', 'guide_stockpool__kwarg', 'realtime__fps',

                   'sys_simulation__enabled', 'sys_progress__enabled', 'sys_analyser__enabled',
                   'messaging__rw', 'realtrade__enabled', 'sys_risk__enabled', 'mongodb__enabled',
                   'mongodb__mongouri', 'terminator__enabled')

        for atr in config_atr:
            realtrade.update({atr: ""})

        mod_config = dict()
        for atr in mod_atr:
            mod_config.update({atr: ''})

        mod_config.update({'messaging__enabled': "true"})

        mod_config.update({'guide_buy_sell__enabled': 'true'})
        mod_config.update({'guide_stockpool__enabled': 'true'})

        mod_config.update({'realtime__fps': 'true'})

        mod_config.update({'sys_simulation__enabled': 'false'})
        mod_config.update({'sys_progress__enabled': 'false'})
        mod_config.update({'sys_analyser__enabled': 'false'})
        mod_config.update({'messaging__rw': '3'})
        mod_config.update({'realtrade__enabled': 'true'})
        mod_config.update({'sys_risk__enabled': 'true'})
        mod_config.update({'mongodb__enabled': 'true'})
        mod_config.update({'mongodb__mongouri': self.JZDATAURI})
        mod_config.update({'terminator__enabled': 'true'})

        realtrade.update({'run_type': "r"})
        realtrade.update({'source_code': self.source_code})
        realtrade.update({'index_server_uris': self.INDEX_SERVER_URIS})
        realtrade.update({'index_switch_server': self.INDEX_SWITCH_SERVER})
        realtrade.update({'log_level': "verbose"})

        realtrade.update({'mod_config': mod_config})

        self.etcd.set(self.realtrade_dir, json.dumps(realtrade))

    def set_simulation_args(self):
        simulation = dict()
        config_atr = ('run_type', 'mod_config'
                      'start_date', 'end_date', 'stock_starting_cash', 'frequency', 'benchmark',
                      'user_id', 'user_account', 'strategy_id', 'strategy_name', 'code_type',
                      'index_server_uris', 'index_switch_server',
                      'source_code',
                      'log_level', 'task_id'

                      )

        mod_atr = ('messaging__enabled', 'mongodb__enabled', 'exception__enabled', 'mongodb__mongouri',
                   'guide_buy_sell__enabled', 'guide_buy_sell__kwarg',
                   'guide_stockpool__enabled', 'guide_stockpool__kwarg', 'realtime__fps',

                   'sys_simulation__matching_type', 'sys_simulation__slippage',
                   'sys_simulation__commission_multiplier',
                   'realtime__enabled', 'realtime__simulation_id', 'messaging__rw')

        for atr in config_atr:
            simulation.update({atr: ''})

        mod_config = dict()
        for atr in mod_atr:
            mod_config.update({atr: ''})

        mod_config.update({'messaging__enabled': "true"})
        mod_config.update({'mongodb__enabled': "true"})
        mod_config.update({'exception__enabled': "true"})
        mod_config.update({'mongodb__mongouri': self.JZDATAURI})
        mod_config.update({'guide_buy_sell__enabled': 'true'})
        mod_config.update({'guide_stockpool__enabled': 'true'})
        mod_config.update({'realtime__enabled': 'true'})
        mod_config.update({'messaging__rw': "3"})

        simulation.update({'mod_config': mod_config})

        simulation.update({'run_type': "p"})
        simulation.update({'source_code': self.source_code})
        simulation.update({'index_server_uris': self.INDEX_SERVER_URIS})
        simulation.update({'index_switch_server': self.INDEX_SWITCH_SERVER})
        simulation.update({'log_level': "verbose"})

        self.etcd.set(self.simulation_dir, json.dumps(simulation))

    def set_backtest_args(self):
        backtest = dict()
        config_atr = ('run_type', 'mod_config',
                      'start_date', 'end_date', 'stock_starting_cash', 'frequency', 'benchmark',
                      'user_id', 'user_account', 'strategy_id', 'strategy_name', 'code_type',
                      'log_level', 'task_id', 'run_type',
                      # 'index_server', 'index_port',
                      'index_server_uris', 'index_switch_server',
                      'source_code',
                      'log_level', 'task_id',)

        mod_atr = ('messaging__enabled', 'mongodb__enabled', 'exception__enabled','mongodb__mongouri',
                   'guide_buy_sell__enabled', 'guide_buy_sell__kwarg',
                   'guide_stockpool__enabled', 'guide_stockpool__kwarg',

                   'sys_simulation__matching_type', 'sys_simulation__slippage',
                   'sys_simulation__commission_multiplier', 'sys_simulation__stock_min_commision',
                   'trade_message__enabled', 'trade_message__debug', 'storeDB__enabled',
                   'storeDB__host', 'messaging__rw')

        for atr in config_atr:
            backtest.update({atr: ''})

        mod_config = dict()
        for atr in mod_atr:
            mod_config.update({atr: ''})

        mod_config.update({'messaging__enabled': "true"})
        mod_config.update({'mongodb__enabled': "true"})
        mod_config.update({'exception__enabled': "true"})
        mod_config.update({'mongodb__mongouri': self.JZDATAURI})
        mod_config.update({'guide_buy_sell__enabled': 'true'})
        mod_config.update({'guide_stockpool__enabled': 'true'})
        mod_config.update({'trade_message__enabled': 'true'})
        mod_config.update({'trade_message__debug': 'true'})
        mod_config.update({'storeDB__enabled': 'true'})
        mod_config.update({'storeDB__host': self.STRATEGY_MONGO})
        mod_config.update({'messaging__rw': "1"})

        backtest.update({'mod_config': mod_config})
        backtest.update({'run_type': "b"})
        backtest.update({'source_code': self.source_code})
        backtest.update({'index_server_uris': self.INDEX_SERVER_URIS})
        backtest.update({'index_switch_server': self.INDEX_SWITCH_SERVER})

        self.etcd.set(self.backtest_dir, json.dumps(backtest))

    def set_backtest_environment(self):
        environment = dict()

        image = self.DOCKER_QUANT_IMAGE

        labels = {'type': self.BACKTEST, "user": ""}

        mounts = self.MOUNTS

        # volume = self.DOCKER_V_BIND

        jzdatarui = self.JZDATAURI
        strategy_sentry = self.STRATEGY_SENTRY_DSN
        mqhost = self.MQ_HOST
        mqport = self.MQ_PORT
        write_ex = self.STRATEGY_WRITE_EX
        read_ex = self.STRATEGY_READ_EX
        mq_vhost = self.MQ_VHOST
        mq_username = self.MQ_USERNAME
        mq_password = self.MQ_PASSWORD

        envs = [
            "JZDATAURI={}".format(jzdatarui),
            f"SENTRY_DSN={strategy_sentry}",
            f"MQ_HOST={mqhost}",
            f"MQ_PORT={mqport}",
            f"STRATEGY_WRITE_EX={write_ex}",
            f"STRATEGY_READ_EX={read_ex}",
            f"MQ_VHOST={mq_vhost}",
            f"MQ_USERNAME={mq_username}",
            f"MQ_PASSWORD={mq_password}",
        ]

        log_driver = self.log_driver

        log_driver_options = self.log_driver_options

        restart_policy = self.restart_policy

        networks = self.DOCKER_NETWORK
        networks = networks.split(',')

        environment.update({
            "image": image,
            "labels": labels,
            "mounts": mounts,
            "envs": envs,
            "log_driver": log_driver,
            "log_driver_options": log_driver_options,
            "restart_policy": restart_policy,
            "networks": networks
        })

        self.etcd.set(self.backtest_environment_dir, json.dumps(environment))

    def set_simulation_environment(self):
        environment = self.backtest_environment
        labels = environment.get("labels")
        labels.update({'type': self.SIMULATION})
        environment.update({"labels": labels})
        self.etcd.set(self.simulation_environment_dir, json.dumps(environment))

    def set_realtrade_environmet(self):
        environment = dict()

        # volume = self.DOCKER_V_BIND
        image = self.DOCKER_QUANT_TRADE_IMAGE

        labels={'type': self.REALTRADE, "user": ''}

        mounts = self.MOUNTS

        jzdatarui = self.JZDATAURI
        mysql_uri = self.MYSQL_URI
        quantuser_url = self.QUANTUSER_SERVER_URL
        quantuser_app_id = self.QUANTUSER_APP_ID
        quantuser_token = self.QUANTUSER_TOKEN
        quantuser_redis_uri = self.QUANTUSER_REDIS_URI
        trade_host = self.TRADE_HOST
        trade_port = self.TRADE_PORT
        strategy_sentry = self.STRATEGY_SENTRY_DSN
        mqhost = self.MQ_HOST
        mqport = self.MQ_PORT
        write_ex = self.STRATEGY_WRITE_EX
        read_ex = self.STRATEGY_READ_EX
        mq_vhost = self.MQ_VHOST
        mq_username = self.MQ_USERNAME
        mq_password = self.MQ_PASSWORD
        future_quote_host = self.FUTURE_QUOTE_HOST
        future_quote_port = self.FUTURE_QUOTE_PORT
        future_trade_host = self.FUTURE_TRADE_HOST
        future_trade_port = self.FUTURE_TRADE_PORT

        envs = [
            "JZDATAURI={}".format(jzdatarui),
            'MYSQL_URI={}'.format(mysql_uri),
            "QUANTUSER_URL={}".format(quantuser_url),
            "QUANTUSER_APP_ID={}".format(quantuser_app_id),
            "QUANTUSER_TOKEN={}".format(quantuser_token),
            "QUANTUSER_REDIS_URI={}".format(quantuser_redis_uri),
            "TRADE_HOST={}".format(trade_host),
            "TRADE_PORT={}".format(trade_port),
            f"SENTRY_DSN={strategy_sentry}",
            f"MQ_HOST={mqhost}",
            f"MQ_PORT={mqport}",
            f"STRATEGY_WRITE_EX={write_ex}",
            f"STRATEGY_READ_EX={read_ex}",
            f"MQ_VHOST={mq_vhost}",
            f"MQ_USERNAME={mq_username}",
            f"MQ_PASSWORD={mq_password}",
            f"FUTURE_QUOTE_HOST={future_quote_host}",
            f"FUTURE_QUOTE_PORT={future_quote_port}",
            f"FUTURE_TRADE_HOST={future_trade_host}",
            f"FUTURE_TRADE_PORT={future_trade_port}",
        ]

        log_driver = self.log_driver

        log_driver_options = self.log_driver_options

        networks = self.DOCKER_NETWORK
        networks = networks.split(',')

        environment.update({
            "image": image,
            "labels": labels,
            "mounts": mounts,
            "envs": envs,
            "log_driver": log_driver,
            "log_driver_options": log_driver_options,
            "networks": networks
        })

        self.etcd.set(self.realtrade_environment_dir, json.dumps(environment))

    @property
    def simulation_args(self):
        return json.loads(self.etcd.read(self.simulation_dir).value)

    @property
    def backtest_args(self):
        return json.loads(self.etcd.read(self.backtest_dir).value)

    @property
    def realtrade_args(self):
        return json.loads(self.etcd.read(self.realtrade_dir).value)

    @property
    def backtest_environment(self):
        return json.loads(self.etcd.read(self.backtest_environment_dir).value)

    @property
    def simulation_environment(self):
        return json.loads(self.etcd.read(self.simulation_environment_dir).value)

    @property
    def realtrade_environment(self):
        return json.loads(self.etcd.read(self.realtrade_environment_dir).value)


class BaseConfigMixin(EtcdConfigMixin):
    def base_update(self):
        pass

    def realtrade_commond(self):
        configs = self.realtrade_args
        mod_config = configs.get("mod_config", {})

        configs.update({
            "start_date": self.start_date,
            "end_date": self.end_date,
            "stock_starting_cash": self.stock_starting_cash,
            "frequency": self.frequency,
            "benchmark": self.benchmark,
            "user_id": self.user_id,
            "user_account": self.user_account,
            "strategy_id": self.id,
            "strategy_name": self.name,
            "code_type": self.type,

            "task_id": self.id,

        })

        uris = configs.get("index_server_uris").split(",")
        server_list = []
        for group in uris:
            server = group.split(":")
            server_list.append((server[0].strip(), server[1].strip()))
        if configs.get("index_switch_server"):
            seed = int(time.time())
            selected = server_list[seed % len(server_list)]
        else:
            selected = server_list[0]
        configs.pop("index_server_uris")
        configs.pop("index_switch_server")

        configs.update({
            "index_server": selected[0],
            "index_port": str(selected[1])
        })

        mod_config.pop('mongodb__enabled')
        mod_config.pop('exception__enabled')
        mod_config.pop('mongodb__mongouri')

        if self.type == "向导式":
            guide = self.guide
            stock_pool = guide.pop('stock', {})
            # hedge = guide.pop('hedge', {})
            mod_config.update({
                "guide_buy_sell__kwarg": json.dumps(guide),
                "guide_stockpool__kwarg": json.dumps(stock_pool)
            })
        elif self.type == "编码式":
            configs.update({
                "source_code": self.strategy_code,
            })
            mod_config.pop("guide_buy_sell__kwarg")
            mod_config.pop("guide_stockpool__kwarg")
            #
            mod_config.pop("realtime__fps")

        configs.update({"mod_config": mod_config})
        return self.commond(configs)

    def simulation_commond(self):
        configs = self.simulation_args
        mod_config = configs.get("mod_config", {})

        configs.update({
            "start_date": self.start_date,
            "end_date": self.end_date,
            "stock_starting_cash": self.stock_starting_cash,
            "frequency": self.frequency,
            "benchmark": self.benchmark,
            "user_id": self.user_id,
            "user_account": self.user_account,
            "strategy_id": self.id,
            "strategy_name": self.name,
            "code_type": self.type,

            "task_id": self.id   #

        })

        mod_config.update({
            "sys_simulation__matching_type": self.matching_type,
            "sys_simulation__slippage": str(self.slippage),
            "sys_simulation__commission_multiplier": str(self.commission_multiplier),
            "realtime__simulation_id": str(self.simulation_id),   #
        })

        uris = configs.get("index_server_uris").split(",")
        server_list = []
        for group in uris:
            server = group.split(":")
            server_list.append((server[0].strip(), server[1].strip()))
        if configs.get("index_switch_server"):
            seed = int(time.time())
            selected = server_list[seed % len(server_list)]
        else:
            selected = server_list[0]
        configs.pop("index_server_uris")
        configs.pop("index_switch_server")

        configs.update({
            "index_server": selected[0],
            "index_port": str(selected[1])
        })

        if self.type == "向导式":
            guide = self.guide
            stock_pool = guide.pop('stock', {})
            # hedge = guide.pop('hedge', {})
            mod_config.update({
                "guide_buy_sell__kwarg": json.dumps(guide),
                "guide_stockpool__kwarg": json.dumps(stock_pool)
            })
        elif self.type == "编码式":
            configs.update({
                "source_code": self.strategy_code,
            })
            mod_config.pop("guide_buy_sell__kwarg")
            mod_config.pop("guide_stockpool__kwarg")
            #
            mod_config.pop("realtime__fps")

        configs.update({"mod_config": mod_config})
        return self.commond(configs)

    def backtest_commond(self, task_id, debug):
        configs = self.backtest_args
        mod_config = configs.get("mod_config", {})

        configs.update({
            "start_date": self.start_date,
            "end_date": self.end_date,
            "stock_starting_cash": self.stock_starting_cash,
            "frequency": self.frequency,
            "benchmark": self.benchmark,
            "user_id": self.user_id,
            "user_account": self.user_account,
            "strategy_id": self.id,
            "strategy_name": self.name,
            "code_type": self.type,
            "log_level": self.log_level,

            "task_id": task_id,

        })

        mod_config.update({
            "sys_simulation__matching_type": self.matching_type,
            "sys_simulation__slippage": str(self.slippage),
            "sys_simulation__commission_multiplier": str(self.commission_multiplier),
            "sys_simulation__stock_min_commision": str(self.stock_min_commision)
        })

        uris = configs.get("index_server_uris").split(",")
        print(uris)
        # sys.exit(0)
        server_list = []
        for group in uris:
            server = group.split(":")
            server_list.append((server[0].strip(), server[1].strip()))
        if configs.get("index_switch_server"):
            seed = int(time.time())
            selected = server_list[seed % len(server_list)]
        else:
            selected = server_list[0]
        configs.pop("index_server_uris")
        configs.pop("index_switch_server")

        configs.update({
            "index_server": selected[0],
            "index_port": str(selected[1])
        })

        if self.type == "向导式":
            guide = self.guide
            stock_pool = guide.pop('stock', {})
            # hedge = guide.pop('hedge', {})
            mod_config.update({
                "guide_buy_sell__kwarg": json.dumps(guide),
                "guide_stockpool__kwarg": json.dumps(stock_pool)
            })
        elif self.type == "编码式":
            configs.update({
                "source_code": self.strategy_code,
            })
            mod_config.pop("guide_buy_sell__kwarg")
            mod_config.pop("guide_stockpool__kwarg")

        configs.update({"mod_config": mod_config})

        return self.commond(configs)

    def commond(self, configs):
        commond = []
        for key, value in configs.items():
            if key == "mod_config":
                continue
            commond.append('--' + key.replace('_', '-'))
            commond.append(value)

        for key, value in configs.get("mod_config", {}).items():
            commond.extend(['--mod-config', key, value])
        return commond


if __name__ == "__main__":
    class Strategy(BaseConfigMixin):
        def __init__(self, **kwargs):
            self.__dict__ = kwargs

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

    import bson
    id = str(bson.ObjectId())

    strategy.__dict__.update({
        "id": id,
    })

    task = str(bson.ObjectId())

    task_name = "{}_{}_{}".format('b', user_uid, task)

    debug = True  #

    strategy.set_backtest_args()
    try:
        strategy.backtest_commond(task, debug)
    except Exception as e:
        print(e)

    # j = BaseConfigMixin()
    # j.backtest_commond(None, None)
    # j.simulation_commond()

    # rundemo = EtcdConfigMixin()
    # rundemo.set_backtest_args()
    # print(rundemo.backtest_args)
    # rundemo.set_simulation_args()
    # print(rundemo.simulation_args)
    # rundemo.set_realtrade_args()
    # print(rundemo.realtrade_args)
    # rundemo.set_backtest_environment()
    # print(rundemo.backtest_environment)
    # rundemo.set_simulation_environment()
    # print(rundemo.simulation_environment)
    # rundemo.set_realtrade_environmet()
    # print(rundemo.realtrade_environment)

