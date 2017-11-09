# coding:utf-8

# 此文件说明： 取得用户输入的代码，保存到对应的文件
import codecs
import logging

import config
import os

# 需改进：代码还未存进数据库。当前方法：直接访问
# 改进方法：在django中将代码存入数据库，然后在这里使用solution获取代码
from judge.db import run_sql
from judge.protect import low_level


def get_code(solution_id, pro_language):

    select_code_sql = "SELECT code FROM app_problem_submit WHERE id = %s" % solution_id
    feh = run_sql(select_code_sql)
    code = feh[0][0]
    try:
        work_path = os.path.join(config.work_dir, str(solution_id))
        low_level()
        os.makedirs(work_path)
    except OSError as e:
        if (str(e).find('exist')) > 0: # 文件夹已存在
            pass
        else:
            logging.error(e)
            return False

    try:
        real_path = os.path.join(
            config.work_dir,
            str(solution_id),
            config.file_name[pro_language]
        )
    except KeyError as e:
        logging.error(e)
        return False
    print real_path
    try:
        low_level()
        f = codecs.open(real_path, 'w', 'utf-8')
        try:
            f.write(code)
        except Exception as e:
            print e.message
            logging.error("%s not write code to file" % solution_id)
            f.close()
            return False
    except OSError as e:
        logging.error(e)
        return False
    return True
