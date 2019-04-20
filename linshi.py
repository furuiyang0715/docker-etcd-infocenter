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
import time
"""第一种方法："""
t1 = time.time()
r1 = dict(list(zip(config_atr, ["" for i in range(len(config_atr))])))
t2 = time.time()

"""第二种方法：遍历赋默认值"""
r2 = dict()
for atr in config_atr:
    r2.update({atr: ''})
t3 = time.time()

"""第三种：使用具有默认值的字典"""
r3 = dict()
for k, v in dict():
    r3.setdefault(k, "").add(v)
t4 = time.time()


print(t2-t1)
print()
print()
print(t3-t2)
print()
print()
print(t4-t3)

# stu = [('wang', 1), ('zhang', 4), ('fu', 2), ('li', 3), ('fu', 7), ('wang', 2), ('wang', 8)]
# stu_set = {}
# for k, v in stu:
#     stu_set.setdefault(k, set()).add(v)


