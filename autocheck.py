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

##################################################
# Error抑制
import warnings
warnings.simplefilter('ignore', FutureWarning)

# web操作 ライブラリ
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.edge.options import Options as EdgeOptions

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
        # 先月
        args = sys.argv
        self.prev = False
        
        if len(args) == 2:
            if 'p' in args[1]:
                self.prev = True

        # メソッド
        self.start()
        
    def start(self):
        # Error抑制
        options = EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # ページ起動
        driver = webdriver.Edge(options=options)
        driver.get(URL)
        time.sleep(WEB_LOAD_TIME)
        
        # ページ内で要素を指定
        user_box = driver.find_element(By.ID,'')
        pass_box = driver.find_element(By.ID,'')
        login_button = driver.find_element(By.ID,'')
        
        # 指定した要素に入力
        user_box.send_keys(USER_ID)
        pass_box.send_keys(PASSWORD)
        
        # ログインボタンをクリック
        login_button.click()
        time.sleep(WEB_LOAD_TIME)
        
        # ページ移動
        driver.get(URL_3)
        time.sleep(WEB_LOAD_TIME)
        
        # 先月ページ移動
        if self.prev == True:
            prev_month_button = driver.find_element(By.ID,'')
            prev_month_button.click()
            time.sleep(WEB_LOAD_TIME)
            
        # 表を取得
        elem_table = driver.find_element(By.ID,'')
        html = elem_table.get_attribute('outerHTML')
        tmp = pd.read_html(html, header = 0)
        data = tmp[0]
        
        # 出勤/退勤時間を取得
        in_out_time_list = data['出／退']
        comment_list = data['コメント']
        
        # ページ移動
        driver.get(URL_2)
        time.sleep(WEB_LOAD_TIME)
        
        # 先月ページ移動
        if self.prev == True:
            prev_month_button = driver.find_element(By.ID,'')
            prev_month_button.click()
            time.sleep(WEB_LOAD_TIME)
        
        # 表を取得
        elem_table2 = driver.find_element(By.ID,'')
        html2 = elem_table2.get_attribute('outerHTML')
        tmp2 = pd.read_html(html2, header = 0)
        data2 = tmp2[0]
        
        # 出勤/退勤時間を取得
        in_time_list2 = data2['出勤']
        out_time_list2 = data2['退勤']
        off_day_list2 = data2['休暇／休日']
        comment_list2 = data2['コメント']
        day_list2 = data2['日付']
        
        # 表から情報を取り出す
        for i in range(1, len(data2)):
            print('-----Day:' + day_list2[i])
            if type(out_time_list2[i]) is str:
                plan_in_out_time = in_out_time_list[2*(i-1)]
                plan_out_time_hh = plan_in_out_time[8:10]
                plan_out_time_mm = plan_in_out_time[11:13]
        
                out_time = out_time_list2[i].split(':')
                h_out_time = out_time[0]
                m_out_time = out_time[1]
                
                # 予定内容表示
                print('[予定]')
                print(plan_out_time_hh + ':' + plan_out_time_mm)
                print(comment_list[2*(i-1)])
                
                # 実績内容表示
                print('[実績]')
                print(out_time_list2[i])
                print(comment_list2[i])
                
                # メッセージ表示
                if type(comment_list[2*(i-1)]) is str:
                    if '残業あり' not in comment_list[2*(i-1)] and '残業なし' not in comment_list[2*(i-1)]:
                        print('[NG]勤務予定未入力 残業あり/残業なし')
                else:
                    print('[NG]勤務予定コメント未入力')
                    
                if type(comment_list2[i]) is str:
                    if int(plan_out_time_hh) < int(h_out_time):
                        print('[NG]退勤予定時間 < 退勤実績時間')
                        if '残業あり' not in comment_list2[i] and '残業なし' not in comment_list2[i]:
                            print('[NG]勤務実績コメント未入力 残業あり/残業なし')
                    
                    elif int(plan_out_time_hh) == int(h_out_time) and int(plan_out_time_mm) < int(m_out_time):
                        print('[NG]退勤予定時間 < 退勤実績時間')
                        if '残業あり' not in comment_list2[i] and '残業なし' not in comment_list2[i]:
                            print('[NG]勤務実績コメント未入力 残業あり/残業なし')
                    
                    elif int(plan_out_time_hh) == int(h_out_time) and int(plan_out_time_mm) == int(m_out_time):
                        if '残業あり' not in comment_list2[i] and '残業なし' not in comment_list2[i]:
                            print('[NG]勤務実績コメント未入力 残業あり/残業なし')
                            
                    elif int(plan_out_time_hh) == int(h_out_time) and int(plan_out_time_mm) > int(m_out_time):
                        if '残業あり' not in comment_list2[i] and '残業なし' not in comment_list2[i]:
                            print('[NG]勤務実績コメント未入力 残業あり/残業なし')
                        if '差分理由' not in comment_list2[i]:
                            print('[NG]差分理由コメント未入力')

                    elif int(plan_out_time_hh) > int(h_out_time):
                        if '残業あり' not in comment_list2[i] and '残業なし' not in comment_list2[i]:
                            print('[NG]勤務実績コメント未入力 残業あり/残業なし')
                        if '差分理由' not in comment_list2[i]:
                            print('[NG]差分理由コメント未入力')

                else:
                    print('[NG]勤務実績コメント未入力')
            else:
                if off_day_list2[i] == '無給休暇' or off_day_list2[i] == '夏期休暇' or off_day_list2[i] == '法定休日' or off_day_list2[i] == '休日':
                    print('休日')
                else:
                    print('退勤未入力')
                    
        input('[Enter]キーで終了')
        driver.quit()                            
        
# 開始
web = Web()