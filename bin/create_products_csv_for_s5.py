import os
import sys
import json
import csv
import datetime
import traceback
#クラスファイルがスクリプトと同一ディレクトリにないと動かないんだけどなぜ？
from database import Database
from spec_info import *
from content import *
from creation_date import *
from constant import *
from fileserver_connect import *
from logger import *
# CSV入力/出力設定の読み込み

log = logger(logger)

log.info("処理を開始します。")

Connect.fileserver()

#csv_settings.jsonの読み込み
try:
    s5_csv_settings = json.load(open(".\\etc\\csv_settings.json", "r"))
    s5_index = s5_csv_settings["s5"]["input"]
except:
    log.error("「csv_settings.json」の読み込み時に例外が発生しました。")
    log.error(sys.exc_info())
    traceback.print_exc()
    sys.exit(False)
else:
    log.info("「csv_settings.json」を読み込みました。")

#brand.jsonの読み込み
try:
    brand_csv_settings = json.load(open(".\\etc\\brand.json", "r" ))
    brand_kana = brand_csv_settings["brand"]["kana"]
except:
    log.error("「brand.json」の読み込み時に例外が発生しました。")
    log.error(sys.exc_info())
    traceback.print_exc()
    sys.exit(False)
else:
    log.info("「brand.json」を読み込みました。")

# 対象商品一覧CSVを読み込み
try:
    csv_file = open(
        ".\\s5.csv", "r", encoding="shift_jis", errors="", newline=""
    )
    csv_list = csv.reader(
        csv_file, delimiter=",", doublequote=True,
        lineterminator="\r\n", quotechar='"', skipinitialspace=True
    )
except:
    log.error("「s5.csv」の読み込み時に例外が発生しました。")
    log.error(sys.exc_info())
    traceback.print_exc()
    sys.exit(False)
else:
    log.info("「s5.csv」を読み込みました。")

#インスタンス化
db = Database()
pd = Productdetail()

log.info("「s5.csv」へのデータ出力を開始します。")

with open(".\\test.csv", "w", newline="") as test:  

    i = 1
    # データ抽出/加工
    for line in csv_list:

        output_array = []
        #MST_ITEMをselect
        item = db.sql_execute("MST_ITEM", "ITEM_CODE", line[s5_index["lis_item_code"]])

        #MST_BRANDをselect
        brand = db.sql_execute("MST_BRAND", "BRAND_CODE", item["BRAND_CODE"])

        #MST_ITEM_INCIDENTAL1をselect
        incidental = db.sql_execute("MST_ITEM_INCIDENTAL1", "ITEM_CODE", line[s5_index["lis_item_code"]])

        #
        text = pd.create_tagging(item, incidental)
        image_value = Content.image_name_change(int(line[s5_index["image_number"]]), line[s5_index["lis_item_code"]])
        serial_date = Date.date_change(i)
        standard = Date.create_standard(item["ITEM_NAME"], item["STANDARD"])

        output_array.extend([
                line[s5_index["s5_item_code"]],
                delivery_code,
                icon_image_code,
                expiration_date,
                classification_code,
                standard,
                brand["BRAND_NAME"],
                serial_date,
                "", 
                line[s5_index["lis_item_code"]],
                active_gateway,
                text, #LISのデータにHTMLタグ適当につけた
                image_value, #品番の後ろの連番どうする？
                "",
                "",
                "",
                "",
                "%s,%s,%s" % (brand["BRAND_NAME"], brand_kana[brand["BRAND_NAME"]], line[s5_index["lis_item_code"]]), #ブランドカナ名設定ファイルで取得してる。
                "",
                round(item["RETAIL"] * tax),
                "",
                "false"
        ])

        try:
            writer = csv.writer(test, lineterminator="\r\n") #quoting=csv.QUOTE_NONE, escapechar=' ', quotechar=' '
            writer.writerow(output_array)
        except:
            log.error("「s5.csv」へのデータ出力時に%d行目で例外が発生しました。" % i)
            log.error(sys.exc_info())
            traceback.print_exc()
            sys.exit(False)
        else:
            log.info("%d行目のデータが出力されました。" % i)
        finally:
            i += 1

log.info("処理が終了しました。")