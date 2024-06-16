#web操作 ライブラリ
from selenium import webdriver
from selenium.webdriver.common.by import By

import os
import signal

#タイマー ライブラリ
import time

#設定値
USER_ID = ''
PASSWORD = ''
URL = ''
URL_2 = ''

# クラス生成
class Web():
    def __init__(self):
        # 最初に処理
        print("__init__")

    def launch(self):
        print("launch")
        # Edgeを指定する
        driver = webdriver.Edge()
        driver.get(URL)
        # 5秒待機する
        time.sleep(5)
        # ページ内で要素を指定する
        user_box = driver.find_element(By.ID,'')
        pass_box = driver.find_element(By.ID,'')
        login_button = driver.find_element(By.ID,'')
        
        # 指定した要素に入力する
        user_box.send_keys(USER_ID)
        time.sleep(5)
        pass_box.send_keys(PASSWORD)
        time.sleep(5)
        
        # ログインボタンをクリックする
        login_button.click()
        time.sleep(5)
        
        driver.get(URL_2)
        
        try:
            print("Wait")
        finally:
            os.kill(driver.service.process.pid,signal.SIGTERM)
        
# 起動時
# ファイル内のクラス
web = Web()
web.launch()
