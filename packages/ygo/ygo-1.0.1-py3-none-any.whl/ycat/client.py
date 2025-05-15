# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2024/7/1 09:44
@author: ZhangYundi
@email: yundi.xxii@outlook.com
---------------------------------------------
"""
import os
import re
from typing import Optional
from .yck import connect, query_polars

import duckdb
import polars as pl
import ylog
from dynaconf import Dynaconf
from sqlalchemy import create_engine
from functools import partial

from .parse import extract_table_names_from_sql

# 配置文件在 “~/.catdb/setting.toml”
USERHOME = os.path.expanduser('~')  # 用户家目录
CONFIG_PATH = os.path.join(USERHOME, ".catdb", "settings.toml")
if not os.path.exists(CONFIG_PATH):
    try:
        os.makedirs(os.path.dirname(CONFIG_PATH))
    except FileExistsError as e:
        ...
    except Exception as e:
        ylog.error(f"配置文件生成失败: {e}")
    catdb_path = os.path.join(USERHOME, "catdb")
    template_content = f"""[paths]
catdb="{catdb_path}"  # 本地数据库，默认家目录

## 数据库配置：
[database]
[database.ck]
# urls=["<host1>:<port1>", "<host2>:<port2>",]
# user="xxx"
# password="xxxxxx"
[database.jy]
# url="<host>:<port>"
# user="xxxx"
# password="xxxxxx"

## 视情况自由增加其他配置
    """
    with open(CONFIG_PATH, "w") as f:
        f.write(template_content)
    ylog.info(f"生成配置文件: {CONFIG_PATH}")


def get_settings():
    try:
        return Dynaconf(settings_files=[CONFIG_PATH])
    except:
        return


HOME = USERHOME
CATDB = os.path.join(HOME, "catdb")
# 读取配置文件覆盖
SETTINGS = get_settings()
if SETTINGS is not None:
    CATDB = SETTINGS.paths.catdb


# ======================== 本地数据库 catdb ========================
def tb_path(tb_name: str) -> str:
    """
    返回指定表名 完整的本地路径
    Parameters
    ----------
    tb_name: str
       表名，路径写法: a/b/c
    Returns
    -------
        full_abs_path: str
        完整的本地绝对路径 $HOME/catdb/a/b/c
    """
    return os.path.join(CATDB, tb_name)

def put(df: pl.DataFrame, tb_name: str, partitions: Optional[list[str]] = None):
    """
    将数据写入duck_db支持的parquet格式文件
    Parameters
    ----------
    df: pandas.DataFrame | pandas.Series | polars.DataFrame
        写入的数据
    tb_name: str
        表名,支持路径写法, a/b/c
    partitions: Optional[List[str]]
        根据哪些字段进行分区，默认不分区
    """
    tbpath = tb_path(tb_name)
    if not os.path.exists(tbpath):
        try:
            os.makedirs(tbpath)
        except FileExistsError as e:
            pass
    if partitions is not None:
        for field in partitions:
            assert field in df.columns, f'dataframe must have Field `{field}`'
    df.write_parquet(tbpath, partition_by=partitions)


def sql(query: str):
    """
    从duckdb中读取数据, query语法与mysql一致，特殊语法请查duckdb官网: https://duckdb.org/docs/sql/query_syntax/select
    Parameters
    ----------
    query: str
        查询语句
    Returns
    -------
    result: duckdb.DuckDBPyRelation
        查询结果
    """
    tbs = extract_table_names_from_sql(query)
    convertor = dict()
    for tb in tbs:
        db_path = tb_path(tb)
        format_tb = f"read_parquet('{db_path}/**/*.parquet', hive_partitioning = true)"
        convertor[tb] = format_tb
    pattern = re.compile("|".join(re.escape(k) for k in convertor.keys()))
    new_query = pattern.sub(lambda m: convertor[m.group(0)], query)
    conn = duckdb.connect()
    conn.execute("PRAGMA disable_progress_bar;")
    conn.execute("PRAGMA threads=1;")
    res = conn.execute(new_query).fetch_arrow_table()
    res = pl.from_arrow(res)
    conn.close()
    return res

def create_engine_ck(urls: list[str], user: str, password: str):
    return partial(connect, urls, user, password)

def read_ck(sql, eng)->pl.DataFrame:
    with eng() as conn:
        return query_polars(sql, conn)

def create_engine_mysql(url, user, password, database):
    """
    :param url: <host>:<port>
    :param user:
    :param password:
    :param database:
    :return:
    """
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{url}/{database}")
    return engine

def read_mysql(sql, eng) -> pl.DataFrame:
    with eng.connect() as conn:
        return pl.read_database(sql, conn)