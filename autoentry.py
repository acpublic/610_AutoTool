### 初期設定 ##################################################
# 待機時間
WEB_LOAD_TIME = 5
WAIT_TIME = 3

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
COMPANY_ID2 = ''
USER_ID2 = ''

# パスワード
PASSWORD2 = ''

# デフォルト値
DEFAULT_START_HH = 
DEFAULT_START_MM = 

DEFAULT_END_HH = 
DEFAULT_END_MM = 

DEFAULT_RST_HH = 
DEFAULT_RST_MM = 

# コメント
REMARK = ''

REMARK_ADD = ''

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

##################################################
class Web():
    def __init__(self):
        
        args = sys.argv
        self.prev = False
        
        if len(args) == 2:
            if 'p' in args[1]:
                self.prev = True
        
        # メソッド
        self.start()

    def start(self):
        # エラー抑制
        options = EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # ページ起動
        driver2 = webdriver.Edge(options=options)
        driver2.get(URL2_1)
        time.sleep(WEB_LOAD_TIME)

        # ページ内で要素を指定
        companyid_box = driver2.find_element(By.ID,'')
        userid_box = driver2.find_element(By.ID,'')
        password_box = driver2.find_element(By.ID,'')
        ja_login_button = driver2.find_element(By.ID,'')

        # 指定した要素に入力
        companyid_box.send_keys(COMPANY_ID2)
        userid_box.send_keys(USER_ID2)
        password_box.send_keys(PASSWORD2)

        # ログインボタンをクリック
        ja_login_button.click()
        time.sleep(WEB_LOAD_TIME)

        try:
            closebtn = driver2.find_element(By.CLASS_NAME,'')
            closebtn.click()
            print('通知画面表示')
        except:
            print('通知画面非表示')
        time.sleep(WAIT_TIME)
        
        # リストページに移動
        list_button = driver2.find_element(By.XPATH,'')
        list_button.click()
        time.sleep(WAIT_TIME)
        
        # 先月ページに移動
        if self.prev == True:
            print("先月に移動") 
            prev_month_btn = driver2.find_element(By.XPATH,(''))
            prev_month_btn.click()
            time.sleep(WAIT_TIME)
        
        # ページ内で要素を指定
        date_1day = driver2.find_element(By.ID,'')
        date_1day.click()
        time.sleep(WAIT_TIME)

        # ページを起動
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
        
        # ページを移動
        driver.get(URL_2)
        time.sleep(WEB_LOAD_TIME)
        
        #先月ページに移動
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
        in_time_list = data['出勤']
        out_time_list = data['退勤']
        off_day_list = data['休暇／休日']
        comment_list = data['コメント']
        day_list = data['日付']

        # 表から情報を取り出す
        for i in range(1, len(data)):
            print('-----Day:' + day_list[i])
            if type(in_time_list[i]) is str:
                in_time = in_time_list[i].split(':')
                h_in_time = in_time[0]
                m_in_time = in_time[1]
                out_time = out_time_list[i].split(':')
                h_out_time = out_time[0]
                m_out_time = out_time[1]
                
                # ページ内で要素を指定
                dropdown = driver2.find_element(By.ID,'')
                rh_box = driver2.find_element(By.ID,'')
                rm_box = driver2.find_element(By.ID,'')
                linktext = driver2.find_element(By.XPATH,'')
        
                # 区分入力
                select = Select(dropdown)
                select.select_by_index(1)
                
                # 休憩時間設定
                input_remark = REMARK
                rst_time_hh = DEFAULT_RST_HH
                rst_time_mm = DEFAULT_RST_MM
                comment_tmp = comment_list[i]
                print(comment_tmp)
                
                self.mywork = False                
                if '[' in comment_tmp and ']' in comment_tmp:
                    self.mywork = True
                
                if self.mywork == True:
                    internal_work = comment_tmp[comment_tmp.find('[') + 1:comment_tmp.find(']')]
                    internal_work_tmp = internal_work.split(':')
                    internal_work_h = internal_work_tmp[0]
                    internal_work_m = internal_work_tmp[1]
                    rst_time_hh = rst_time_hh + int(internal_work_h)
                    rst_time_mm = rst_time_mm + int(internal_work_m)
                    
                    input_remark = REMARK + REMARK_ADD + internal_work
                
                # 休憩時間入力
                rh_box.send_keys(rst_time_hh)
                rm_box.send_keys(rst_time_mm)
                              
                # 備考にコメント入力
                linktext.click()
                time.sleep(WAIT_TIME)
                remark_text = driver2.find_element(By.ID,'')
                remark_text.clear()
                remark_text.send_keys(input_remark)
                time.sleep(WAIT_TIME)
                remark_btn = driver2.find_element(By.ID,'')
                remark_btn.click()
                time.sleep(WAIT_TIME)
                
                # ページ内で要素を指定
                sh_box = driver2.find_element(By.ID,'')
                sm_box = driver2.find_element(By.ID,'')
                eh_box = driver2.find_element(By.ID,'')
                em_box = driver2.find_element(By.ID,'')
                
                # 出勤/退勤時間を入力
                sh_box.send_keys(h_in_time)
                sm_box.send_keys(m_in_time)
                eh_box.send_keys(h_out_time)
                em_box.send_keys(m_out_time)

                # 入力内容表示
                print(h_in_time + ':' + m_in_time)
                print(h_out_time + ':' + m_out_time)
                print(str(rst_time_hh) + 'h' + str(rst_time_mm) + 'm')
                print(input_remark)

                # 一時保存
                saved_btn = driver2.find_element(By.CLASS_NAME,'')
                saved_btn.click()
                time.sleep(WAIT_TIME)
            
            else:
                if off_day_list[i] == '無給休暇' or off_day_list[i] == '有休' or off_day_list[i] == '夏期休暇':
                    print('休暇')
                    # ページ内で要素を指定
                    dropdown = driver2.find_element(By.ID,'')
                    # 指定した要素に入力
                    select = Select(dropdown)
                    select.select_by_index(2)
                    # 一時保存
                    try:
                        saved_btn = driver2.find_element(By.CLASS_NAME,'')
                        saved_btn.click()
                        #print('一時保存')
                    except:
                        print('一時保存無し')
                        
                    time.sleep(WAIT_TIME)
            
            # 次の日にする
            next_day_btn = driver2.find_element(By.XPATH,(''))
            next_day_btn.click()
            time.sleep(WAIT_TIME)
        

        input("[Enter]キーで終了")
        driver.quit()
        driver2.quit()
        
# 開始
web = Web()
