import platform
from smb.SMBConnection import SMBConnection
import base64
import traceback
import sys
from logger import *

class Connect:
    @classmethod
    def fileserver(self):

        log = logger(logger)
        
        s = "MzRYdjJEKzk="
        latios = str(base64.b64decode(s))
        latios = latios.replace("b'", "")
        latios = latios.replace("'", "")

        # connection open
        conn = SMBConnection(
            'administrator',
            latios,
            platform.uname().node,
            'dwfs04',
            domain='dad-way.local',
            use_ntlm_v2=True)

        try:
            conn.connect('192.168.100.8', 139)
        except:
            log.error("ファイルサーバー接続時に例外が発生しました。")
            log.error(sys.exc_info())
            traceback.print_exc()
            sys.exit(False)
        else:
            log.info("ファイルサーバーの接続に成功しました。")


        with open('.\etc\\brand.json', 'wb') as file:
            try:
                conn.retrieveFile('share', 'open\DDIV\OCSD\\ECG\\Online\\80_s5tool\\brand.json', file)
            except:
                log.error("「brand.json」のコピーで例外が発生しました。")
                log.error(sys.exc_info())
                traceback.print_exc()
                sys.exit(False)
        
        with open('.\etc\\deletecharacter.json', 'wb') as file:
            try:
                conn.retrieveFile('share', 'open\DDIV\OCSD\\ECG\\Online\\80_s5tool\\deletecharacter.json', file)
            except:
                log.error("「deletecharacter.json」のコピーで例外が発生しました。")
                log.error(sys.exc_info())
                traceback.print_exc()
                sys.exit(False)

        conn.close()