## 初期設定
# 待機時間
WEB_LOAD_TIME = 5

# Webページ1
URL = ''
# Webページ2
URL_2 = ''
# Webページ3
URL_3 = ''

# ログインID
USER_ID = ''

# ログインパスワード
PASSWORD = ''

# コメント
S_COMMENT = ''

# Web2ページ1
URL2_1 = ''

# ログインID
COMPANY_ID = ''
USER_ID2 = ''

# パスワード
PASSWORD2 = ''

##################################################
# Error抑制
import warnings
warnings.simplefilter('ignore', FutureWarning)

# web操作 ライブラリ
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.edge.options import EdgeOptions

# 表取得 ライブラリ
import pandas as pd

# タイマー ライブラリ
import time

# Other
import os
import signal
import sys

class Web():
    def __init__(self):
        self.start()

    def start(self):
        input('[Enter]キーで終了')
        driver.quit()
        
# 開始
web = Web()
