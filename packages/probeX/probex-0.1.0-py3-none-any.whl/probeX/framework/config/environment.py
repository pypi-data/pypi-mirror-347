#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   environment.py
@Time    :   2025/04/27 16:55:33
@Author  :   yanggy 
@Version :   1.0
@Contact :   yangguangyu_cn@163.com
@License :   (C)Copyright 2021-2022, Liugroup-NLPR-CASIA
@Desc    :   None
'''

from dataclasses import dataclass
from probeX.framework.config.Config import config


@dataclass
class Env():
    name: str
    host: str
    kubf_config_file: str
    db_config: str


def get_env_config():
    from probeX.framework.config.Config import config
    envs_config = config.get("env")
    e = Env(name=envs_config["name"], host=envs_config["host"], 
                db_config=envs_config["db_config"], kubf_config_file=envs_config["kube_config_file"])
    return e

env_config = get_env_config()