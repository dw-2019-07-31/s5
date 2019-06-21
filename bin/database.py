import cx_Oracle
import json
import os
import sys
import re
import traceback
from logger import *

class Database:
    
    #しんぐるとん
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    #DB接続
    def __init__(self):
        # Database設定の読み込み
        self.log = logger(logger)
        try:
            database_settings = json.load(
                open(".\\etc\\database_settings.json", 'r')
            )
            lis = database_settings["oracle"]["lis"]
        except:
            self.log.error("database設定の読み込み時に例外が発生しました。")
            self.log.error(sys.exc_info())
            traceback.print_exc()
            sys.exit(False)
        
        os.environ["NLS_LANG"] = lis["lang"]
        tns = cx_Oracle.makedsn(
            lis["server_address"], lis["port"], lis["instance_name"]
        )
        try:
            self.conn = cx_Oracle.connect(lis["username"], lis["password"], tns)
            self.cur = self.conn.cursor()
        except:
            self.log.error("Oracleの接続で例外が発生しました。")
            self.log.error(sys.exc_info())
            traceback.print_exc()
            sys.exit(False)
        finally:
            self.log.info("Oracleの接続に成功しました。")

    #selectの結果を返すメソッド
    def sql_execute(self, table, column, code):
        columns = []
        try:
            self.cur.execute(
                "SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME = '%s' ORDER BY COLUMN_ID" % table
            )
        except:
            self.log.error("%sのカラム名取得時に例外が発生しました。" % table)
            self.log.error(sys.exc_info())
            traceback.print_exc()
            sys.exit(False)
        
        tmp1 = self.cur.fetchall()
        for a in tmp1:
            for b in a:
                columns.append(b)

        rows = []
        try:
            self.cur.execute(
                "SELECT * FROM %s WHERE %s = '%s'" % (table, column, code)
            )
        except:
            self.log.error("%sの商品情報取得時に例外が発生しました。" % table)
            self.log.error(sys.exc_info())
            traceback.print_exc()
            sys.exit(False)

        tmp2 = self.cur.fetchall()
        for a in tmp2:
            for b in a:
                if b != None:
                    rows.append(b)
                else:
                    rows.append("")
        
        mydict = {}
        i = 0
        for column in columns:           
            mydict.setdefault(column, rows[i])
            i += 1
        
        if table == "MST_ITEM_INCIDENTAL1":

            if mydict["ITEM_SIZE"] != "":
                mydict["ITEM_SIZE"] = mydict["ITEM_SIZE"] + "cm"
       
            if mydict["WEIGHT"] != "":
                mydict["WEIGHT"] = str(int(mydict["WEIGHT"])) + "g"

        return mydict
