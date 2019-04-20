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

print(r1)
print(r1 == r2)
print(r2 == r3)


print(t2-t1)
print()
print()
print(t3-t2)
print()
print()
print(t4-t3)


