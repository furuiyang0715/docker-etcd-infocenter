base_config_atr = {
        'index_server_uris',
        'strategy_id',
        'run_type',
        'code_type',
        'start_date',
        'stock_starting_cash',
        'index_switch_server',
        'log_level',
        'task_id',
        'frequency',
        'user_id',
        'end_date',
        'benchmark',
        'mod_config',
        'strategy_name',
        'user_account'
    }


base_mod_atr = {
    'guide_buy_sell__enabled',
    'guide_stockpool__enabled',
    'guide_buy_sell__kwarg',
    'guide_stockpool__kwarg',
    'mongodb__enabled',
    'messaging__rw',
    'mongodb__mongouri',
    'messaging__enabled',
}


r_mod_atr = {
            'realtime__fps',
            'sys_analyser__enabled',
            'terminator__enabled',
            'sys_risk__enabled',
            'sys_simulation__enabled',
            'realtrade__enabled',
            'sys_progress__enabled'
        }

config_atr = base_config_atr


# 具有给定的键值 给字典赋默认值
import time
num = 1000000

"""第一种方法："""      # 2.852492094039917
t1 = time.time()
for j in range(num):
    r1 = dict(list(zip(config_atr, ["" for i in range(len(config_atr))])))
t2 = time.time()

"""第二种方法：遍历赋默认值"""  # 4.651882886886597
for j in range(num):
    r2 = dict()
    for atr in config_atr:
        r2.update({atr: ''})
t3 = time.time()

"""第三种：使用具有默认值的字典"""  # 2.7060930728912354
for j in range(num):
    r3 = dict()
    for atr in config_atr:
        r3.setdefault(atr, "")
t4 = time.time()

# print(t2-t1)
# print(t3-t2)
# print(t4-t3)

r = {
            "start_date",
            "end_date",
            "stock_starting_cash",
            "frequency",
            "benchmark",
            "user_id",
            "user_account",
            "strategy_id",
            "strategy_name",
            "code_type",
            "task_id",
        }

s = {
            "start_date",
            "end_date",
            "stock_starting_cash",
            "frequency",
            "benchmark",
            "user_id",
            "user_account",
            "strategy_id",
            "strategy_name",
            "code_type",
            "task_id"
}

b = {
            "start_date",
            "end_date",
            "stock_starting_cash",
            "frequency",
            "benchmark",
            "user_id",
            "user_account",
            "strategy_id",
            "strategy_name",
            "code_type",
            "log_level",
            "task_id",
}
# common = r&s&b
# {'frequency', 'user_id', 'end_date', 'user_account', 'stock_starting_cash',
# 'strategy_id', 'task_id', 'code_type', 'start_date', 'strategy_name', 'benchmark'}


# print(r-common)
# print()
# print(s-common)
# print()
# print(b-common)
# print()


# if self.type == "向导式":
#     guide = self.guide
#     stock_pool = guide.pop('stock', {})
#     hedge = guide.pop('hedge', {})
#     mod_config.update({
#         "guide_buy_sell__kwarg": json.dumps(guide),
#         "guide_stockpool__kwarg": json.dumps(stock_pool)
#     })
#     configs.update({"source_code": self.source_code})
# elif self.type == "编码式":
#     # 如果为编码式 就将向导式增加的参数 pop 出去
#     mod_config.pop("guide_buy_sell__kwarg")
#     mod_config.pop("guide_stockpool__kwarg")
#     mod_config.pop("guide_buy_sell__enabled")
#     mod_config.pop("guide_stockpool__enabled")
#
#     mod_config.pop("realtime__fps")







