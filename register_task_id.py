import json
import time

import etcd
from docker.types import RestartPolicy
from docker.types.services import RestartConditionTypesEnum


class EtcdConfigMixin(object):

    BACKTEST = "backtest"
    REALTRADE = "realtrade"
    SIMULATION = "simulation"
    CBACKTEST = "cbacktest"

    SPAWN_TYPE = (BACKTEST, REALTRADE, SIMULATION, CBACKTEST)

    # configs
    INDEX_SERVER_URIS = "139.159.135.96:9802"
    JZDATAURI = "192.168.100.78:27017"
    STRATEGY_MONGO = ''
    INDEX_SWITCH_SERVER = True

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
    QUANTUSER_TOKEN = "ff46fd5a21bf4fc4b3777e3ab4a96273"
    QUANTUSER_REDIS_URI = "redis://127.0.0.1/1"
    DOCKER_QUANT_TRADE_IMAGE = 'cdh1:5000/jzquant:latest'
    TRADE_HOST = "139.198.191.151"
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

    # 在etcd的存储路径
    backtest_dir = "/config/backtest/"
    simulation_dir = "/config/simulation/"
    realtrade_dir = "/config/realtrade/"
    backtest_environment_dir = "/environment/backtest/"
    simulation_environment_dir = "/environment/simulation/"
    realtrade_environment_dir = "/environment/realtrade/"

    # 存储 task_id 的根目录
    service_base_dir = "/services/{}"

    # 不管是实盘,模拟盘还是回测,其共有的config atr
    base_config_atr = {
        'index_server_uris', 'strategy_id',
        'run_type', 'code_type',
        'start_date', 'stock_starting_cash',
        'index_switch_server', 'log_level',
        'task_id', 'frequency',
        'user_id', 'end_date',
        'benchmark', 'mod_config',
        'strategy_name', 'user_account'
    }

    # 实盘,模拟盘,回测的共有的mod config atr
    base_mod_atr = {
        'guide_buy_sell__enabled', 'messaging__rw',
        'guide_stockpool__enabled', 'mongodb__mongouri',
        'guide_buy_sell__kwarg', 'messaging__enabled',
        'guide_stockpool__kwarg', 'mongodb__enabled'
    }

    @property
    def etcd(self):
        # etcd_url = current_app.config.get('ETCD_URL', ('127.0.0.1', 2379))
        etcd_url = ('127.0.0.1', 2379)
        host, port = etcd_url[0], etcd_url[1]
        return etcd.Client(host=host, port=port)

    def _checkonly(self, mydict, myset):
        """尽量不在 etcd 中保存多余的数据"""
        only_dict = {key: value for key, value in mydict.items() if key in myset}
        return only_dict

    def set_realtrade_args(self):
        """配置实盘参数"""
        config_atr = self.base_config_atr

        # 实盘需特殊配置的 mod_atr
        r_mod_atr = {
            'realtime__fps', 'sys_analyser__enabled', 'terminator__enabled',
            'sys_risk__enabled', 'sys_simulation__enabled', 'realtrade__enabled',
            'sys_progress__enabled'
        }
        mod_atr = self.base_mod_atr.union(r_mod_atr)

        # 配置默认值  TODO ugly
        realtrade = dict()
        for atr in config_atr:
            realtrade.update({atr: ""})

        mod_config = dict()
        for atr in mod_atr:
            mod_config.update({atr: ''})

        # 设置实盘mod atr的相对固定配置
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
        mod_config.update({'realtime__fps': "30"})

        self._checkonly(mod_config, mod_atr)

        # 配置实盘config的相对固定值
        realtrade.update({'mod_config': mod_config})

        realtrade.update({'run_type': "r"})
        realtrade.update({'index_server_uris': self.INDEX_SERVER_URIS})
        realtrade.update({'index_switch_server': self.INDEX_SWITCH_SERVER})
        realtrade.update({'log_level': "verbose"})
        self._checkonly(realtrade, config_atr)

        self.etcd.set(self.realtrade_dir, json.dumps(realtrade))

    def set_simulation_args(self):
        config_atr = self.base_config_atr

        # 针对模拟盘,需要特殊配置的mod_atr
        s_mod_atr = {
            'sys_simulation__slippage', 'realtime__enabled',
            'sys_simulation__commission_multiplier', 'realtime__simulation_id',
            'sys_simulation__matching_type', 'realtime__fps',
            'exception__enabled'
        }
        mod_atr = self.base_mod_atr.union(s_mod_atr)

        simulation = dict()
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
        mod_config.update({'realtime__fps': "30"})

        self._checkonly(mod_config, mod_atr)
        simulation.update({'mod_config': mod_config})

        simulation.update({'run_type': "p"})
        simulation.update({'index_server_uris': self.INDEX_SERVER_URIS})
        simulation.update({'index_switch_server': self.INDEX_SWITCH_SERVER})
        simulation.update({'log_level': "verbose"})
        self._checkonly(simulation, config_atr)

        self.etcd.set(self.simulation_dir, json.dumps(simulation))

    def set_backtest_args(self):
        # 回测时，启动参数 + source_code
        config_atr = self.base_config_atr.union({"source_code"})

        # 针对回测，其需要特殊配置的mod atr
        b_mod_atr = {
            'trade_message__enabled', 'sys_simulation__slippage',
            'sys_simulation__commission_multiplier',
            'sys_simulation__matching_type', 'storeDB__enabled',
            # 'trade_message__debug',
            'storeDB__host',
            'sys_simulation__stock_min_commision', 'exception__enabled'
        }
        mod_atr = self.base_mod_atr.union(b_mod_atr)

        backtest = dict()
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
        # mod_config.update({'trade_message__debug': 'true'})   # 根据 debug 判断
        mod_config.update({'storeDB__enabled': 'true'})
        mod_config.update({'storeDB__host': self.STRATEGY_MONGO})
        mod_config.update({'messaging__rw': "1"})
        self._checkonly(mod_config, mod_atr)
        backtest.update({'mod_config': mod_config})

        backtest.update({'run_type': "b"})
        backtest.update({'source_code': self.source_code})
        backtest.update({'index_server_uris': self.INDEX_SERVER_URIS})
        backtest.update({'index_switch_server': self.INDEX_SWITCH_SERVER})
        self._checkonly(backtest, config_atr)

        self.etcd.set(self.backtest_dir, json.dumps(backtest))

    def set_backtest_environment(self):
        environment = dict()

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

        environment.update({
            "image": self.DOCKER_QUANT_IMAGE,
            "labels": {'type': self.BACKTEST, "user": ""},
            "mounts": self.MOUNTS,
            "envs": envs,
            "log_driver": self.log_driver,
            "log_driver_options": self.log_driver_options,
            "restart_policy": self.restart_policy,
            "networks": self.DOCKER_NETWORK.split(',')
        })

        self.etcd.set(self.backtest_environment_dir, json.dumps(environment))

    def set_simulation_environment(self):
        environment = self.backtest_environment

        labels = environment.get("labels")
        labels.update({'type': self.SIMULATION})
        environment.update({"labels": labels})

        environment.pop("restart_policy")
        self.etcd.set(self.simulation_environment_dir, json.dumps(environment))

    def set_realtrade_environment(self):
        environment = dict()

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

        environment.update({
            "image": self.DOCKER_QUANT_TRADE_IMAGE,
            "labels": {'type': self.REALTRADE, "user": ''},
            "mounts": self.MOUNTS,
            "envs": envs,
            "log_driver": self.log_driver,
            "log_driver_options": self.log_driver_options,
            "networks": self.DOCKER_NETWORK.split(',')
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
    def _base_update(self):
        self.set_realtrade_environment()
        self.set_simulation_environment()
        self.set_backtest_environment()

        self.set_realtrade_args()
        self.set_simulation_args()
        self.set_backtest_args()

    def realtrade_commond(self):
        configs = self.realtrade_args

        mod_config = configs.get("mod_config", {})

        configs.update({
            "start_date": self.start_date,
            "end_date": self.end_date,
            "stock_starting_cash": str(self.stock_starting_cash),
            "frequency": self.frequency,
            "benchmark": self.benchmark,
            "user_id": self.user_id,
            "user_account": self.user_account,
            "strategy_id": self.id,
            "strategy_name": self.name,
            "code_type": self.type,
            "task_id": self.id,

        })

        # （TODO）共同部分是否可封装
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

        # mod_config.pop('exception__enabled')

        if self.type == "向导式":
            guide = self.guide
            stock_pool = guide.pop('stock', {})
            hedge = guide.pop('hedge', {})
            mod_config.update({
                "guide_buy_sell__kwarg": json.dumps(guide),
                "guide_stockpool__kwarg": json.dumps(stock_pool)
            })
            configs.update({"source_code": self.source_code})
        elif self.type == "编码式":
            # 如果为编码式 就将向导式增加的参数 pop 出去
            mod_config.pop("guide_buy_sell__kwarg")
            mod_config.pop("guide_stockpool__kwarg")
            mod_config.pop("guide_buy_sell__enabled")
            mod_config.pop("guide_stockpool__enabled")

            mod_config.pop("realtime__fps")

        configs.update({"mod_config": mod_config})
        return self.commond(configs)

    def simulation_commond(self):
        configs = self.simulation_args

        mod_config = configs.get("mod_config", {})

        configs.update({
            "start_date": self.start_date,
            "end_date": self.end_date,
            "stock_starting_cash": str(self.stock_starting_cash),
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
            hedge = guide.pop('hedge', {})
            mod_config.update({
                "guide_buy_sell__kwarg": json.dumps(guide),
                "guide_stockpool__kwarg": json.dumps(stock_pool)
            })
            configs.update({"source_code": self.source_code})
        elif self.type == "编码式":
            mod_config.pop("guide_buy_sell__kwarg")
            mod_config.pop("guide_stockpool__kwarg")
            mod_config.pop("guide_buy_sell__enabled")
            mod_config.pop("guide_stockpool__enabled")
            mod_config.pop("realtime__fps")

        configs.update({"mod_config": mod_config})
        return self.commond(configs)

    def backtest_commond(self, task_id, debug):
        configs = self.backtest_args

        mod_config = configs.get("mod_config", {})

        configs.update({
            "start_date": self.start_date,
            "end_date": self.end_date,
            "stock_starting_cash": str(self.stock_starting_cash),
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

        if debug:
            mod_config.update({'trade_message__debug': 'true'})

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
            hedge = guide.pop('hedge', {})
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
            mod_config.pop("guide_buy_sell__enabled")
            mod_config.pop("guide_stockpool__enabled")

        configs.update({"mod_config": mod_config})

        return self.commond(configs)

    def cbacktest_commond(self):
        #
        return []

    def commond(self, configs, *args, **kwargs):
        commond = ['JZquant', 'run']
        for key, value in configs.items():
            if key == "mod_config":
                continue
            commond.append('--' + key.replace('_', '-'))
            commond.append(value)

        for key, value in configs.get("mod_config", {}).items():
            commond.extend(['--mod-config', key, value])
        return commond


class SpawnerEnvMixin(EtcdConfigMixin):

    @property
    def spawn_map(self):
        return {
            self.BACKTEST: self.backtest_environment,
            self.SIMULATION: self.simulation_environment,
            self.REALTRADE: self.realtrade_environment,
            self.CBACKTEST: self.backtest_environment
        }

    def _base_update(self):
        self.set_backtest_environment()
        self.set_simulation_environment()
        self.set_realtrade_environment()

    def spawn_params(self, command, user, type):
        if type not in self.SPAWN_TYPE:
            raise NotImplementedError

        params = self.spawn_map.get(type)
        labels = params.get("labels")

        labels.update({"user": user})
        if type == self.CBACKTEST:
            labels.update({"type": self.CBACKTEST})

        params.update({"labels": labels})
        params.update({"command": command})

        return params


if __name__ == "__main__":

    demo = EtcdConfigMixin()

    demo.set_realtrade_args()
    # print(demo.realtrade_args)

    demo.set_simulation_args()
    # print(demo.simulation_args)

    demo.set_backtest_args()
    # print(demo.backtest_args)

    demo.set_backtest_environment()
    # print(demo.backtest_environment)

    demo.set_simulation_environment()
    # print(demo.simulation_environment)

    demo.set_realtrade_environment()
    # print(demo.realtrade_environment)

    sp = SpawnerEnvMixin()

    # print(sp.spawn_map)

    # print(sp.spawn_params(None, None, "backtest"))

    # print(sp.spawn_params(None, None, "simulation"))

    # print(sp.spawn_params(None, None, "realtrade"))
