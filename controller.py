import os
import time
import asyncio
from datetime import datetime
import pandas as pd
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog , QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from LoginUI import Ui_LoginPage
from MainUI import Ui_MainPage

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from Webauto import *

url_link = {
    "BB":{
        "urlPre":"http://fundmng.aballbet.com/",
        "domain":"http://fundmng.aballbet.com/login",
        "homePage":"http://fundmng.aballbet.com/system/navigation",
        "member-list":"http://fundmng.aballbet.com/system/user-management/member-list"
    },
    "ML":{
        "urlPre":"http://fundmng.m6admin.com/",
        "domain":"http://fundmng.m6admin.com/login",
        "homePage":"http://fundmng.m6admin.com/system/navigation",
        "member-list":"http://fundmng.m6admin.com/system/user-management/member-list"
    }
}
def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    timeStyle = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return timeStyle

class ThreadTask(QThread):
    qthread_signal = pyqtSignal(int)

    def __init__(self):
        super(ThreadTask, self).__init__()

    def __del__(self):
        self.wait()

    def start_progress_flow(self,driver,QtW,filePath,temp_list):
        df = pd.read_excel(filePath)
        before_username = ""
        flow = ""
        count = 0
        user_count = df.last_valid_index() + 1
        for i in range(user_count):
            count += 100 / user_count
            username = str(df.iat[i,0])
            username_input = WebDriverWait(driver, 20, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="create-form_username"]')))
            username_input.clear()
            username_input.send_keys(username)
            username_input.send_keys(Keys.ENTER)
            before = flow
            while True:
                time.sleep(1)
                try:
                    winlose = WebDriverWait(driver, 3, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div/div[3]/div/div/div/div/div/div/div/table/tbody/tr/td[10]/p'))).text
                    valid_flow = WebDriverWait(driver, 3, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div/div[3]/div/div/div/div/div/div/div/table/tbody/tr/td[9]/p'))).text
                    flow = valid_flow.split('\n')[1].replace(",","")
                    winlose = winlose.split('\n')[0].replace(",","")
                    lose = float(winlose) * -1
                except:
                    flow = None
                    lose = None
                if before_username != username:
                    before_username == username
                    break
            temp = {
                '会员账号':username,
                '体育流水': float(flow) if flow else "",
                '体育输赢': lose if lose else ""
                }
            temp_list.append(temp)
            if i + 1 == user_count:
                count = 100
            self.qthread_signal.emit(int(count))
        while True:
            try:
                end = pd.DataFrame(temp_list)
                end.to_csv("数据.csv",encoding="utf_8_sig")
                break
            except:
                QMessageBox.about(QtW,'Error','请先关闭 数据.csv 窗口，然后点击 确认 以继续进行')
        print("体育流水完成。")
        return temp_list

    def start_progress_nflow(self,driver,QtW,filePath,temp_list,Checker):
        df = pd.read_excel(filePath)
        a = df.last_valid_index()
        before_username = ""
        flow = ""
        user_count = df.last_valid_index() + 1
        count = 0
        for i in range(user_count):
            count += 100 / user_count
            username = str(df.iat[i,0])
            username_input = WebDriverWait(driver, 20, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="create-form_username"]')))
            username_input.clear()
            username_input.send_keys(username)
            username_input.send_keys(Keys.ENTER)
            before = flow
            while True:
                time.sleep(1)
                try:
                    winlose = WebDriverWait(driver, 2, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div/div[3]/div/div/div/div/div/div/div/table/tbody/tr/td[10]/p'))).text
                    valid_flow = WebDriverWait(driver, 2, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div/div[3]/div/div/div/div/div/div/div/table/tbody/tr/td[9]/p'))).text
                    flow = valid_flow.split('\n')[1].replace(",","")
                    winlose = winlose.split('\n')[0].replace(",","")
                    lose = float(winlose) * -1
                except:
                    flow = None
                    lose = None
                if before_username != username:
                    before_username == username
                    break
            if temp_list != []:
                if Checker['体育流水']:
                    userList = []
                    for UserDict in temp_list:
                        if UserDict['会员账号'] == username:
                            UserDict['娱乐流水'] = float(flow) if flow else ""
                            UserDict['娱乐输赢'] = lose if lose else ""
                else:
                    temp = {
                        '会员账号':username,
                        '娱乐流水': float(flow) if flow else "",
                        '娱乐输赢': lose if lose else ""
                        }
                    temp_list.append(temp)
            else:
                temp = {
                    '会员账号':username,
                    '娱乐流水': float(flow) if flow else "",
                    '娱乐输赢': lose if lose else ""
                    }
                temp_list.append(temp)
            if i + 1 == user_count:
                count = 100
            self.qthread_signal.emit(int(count))
        while True:
            try:
                end = pd.DataFrame(temp_list)
                end.to_csv("数据.csv",encoding="utf_8_sig")
                break
            except:
                QMessageBox.about(QtW,'Error','请先关闭 数据.csv 窗口，然后点击 确认 以继续进行')
        print("娱乐流水完成。")
        return temp_list

    def start_progress_user(self,driver,QtW,platform,filePath,temp_list,Checker):
        def get_responce_Info(driver,platform):
            logs_raw = driver.get_log("performance")
            logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
            def log_filter(log_):
                    return (log_["method"] == "Network.responseReceived" and "json" in log_["params"]["response"]["mimeType"])
            for log in filter(log_filter, logs):
                request_id = log["params"]["requestId"]
                resp_url = log["params"]["response"]["url"]
                if resp_url == f"{url_link[platform]['urlPre']}api/manage/data/user/detail/by/username":
                    data = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body']
                    data = json.loads(data)
                    if data['message'].lower() == 'success':
                        lastBetTime = str(timeStamp(data['data']['lastBettingTime'])) if data['data']['lastBettingTime'] else "无投注"
                        parent = data['data']['parentName']
                        userVIP = data['data']['vipLevel']

                    else:
                        return '账号错误' , '账号错误' , '账号错误' , '账号错误', '账号错误'
                elif resp_url == f"{url_link[platform]['urlPre']}api/manage/data/trend/userFund":
                    data = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body']
                    data = json.loads(data)
                    if data['message'].lower() == 'success':
                        rechargeTimes = str(data['data']['rechargeNum'])
                        upAmountTimes = str(data['data']['upAmountTimes'])
                    else:
                        rechargeTimes = upAmountTimes = '-'
            return lastBetTime, rechargeTimes , upAmountTimes , parent , userVIP

        df = pd.read_excel(filePath)
        a = df.last_valid_index()
        before_username = ""
        flow = ""
        user_count = df.last_valid_index() + 1
        counting = 0
        error_acc = []
        count = 0
        for i in range(user_count):
            count += 100 / user_count
            while True:
                try:
                    username = str(df.iat[i,0])
                    input_username = WebDriverWait(driver, 20, 0.5).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div/section/section/header[2]/div/div[2]/span/span/span[1]/input')))
                    input_username.clear()
                    input_username.send_keys(username)
                    input_username.send_keys(Keys.ENTER)
                    time.sleep(0.5)
                    lastBet , rechargeTimes , upAmountTimes , UParent , userVIP = get_responce_Info(driver,platform)
                    break
                except:
                    driver.refresh()
            error_acc.append(username) if lastBet == '账号错误' else error_acc
            if temp_list != []:
                if Checker['体育流水'] or Checker['娱乐流水']:
                    userList = []
                    for UserDict in temp_list:
                        if UserDict['会员账号'] == username:
                            if Checker['最后投注时间']:
                                UserDict['最后投注时间'] = str(lastBet) if lastBet else '账号错误'
                            if Checker['(代)充值次数']:
                                UserDict['存款次数'] = str(rechargeTimes) if rechargeTimes else ''
                                UserDict['代充次数'] = str(upAmountTimes) if upAmountTimes else ''
                            if Checker['上级代理']:
                                UserDict['上级代理'] = str(UParent) if UParent else ''
                            if Checker['VIP等级']:
                                UserDict['VIP等级'] = str(userVIP) if userVIP else ''
                else:
                    temp = {
                        '会员账号': username
                        }
                    if Checker['最后投注时间']:
                        temp['最后投注时间'] = str(lastBet) if lastBet else ""
                    if Checker['(代)充值次数']:
                        temp['存款次数'] = str(rechargeTimes) if rechargeTimes else ''
                        temp['代充次数'] = str(upAmountTimes) if upAmountTimes else ''
                    if Checker['上级代理']:
                        temp['上级代理'] = str(UParent) if UParent else ''
                    if Checker['VIP等级']:
                        temp['VIP等级'] = str(userVIP) if userVIP else ''
                    temp_list.append(temp)
            else:
                temp = {
                    '会员账号': username
                    }
                if Checker['最后投注时间']:
                    temp['最后投注时间'] = str(lastBet) if lastBet else ""
                if Checker['(代)充值次数']:
                    temp['存款次数'] = str(rechargeTimes) if rechargeTimes else ''
                    temp['代充次数'] = str(upAmountTimes) if upAmountTimes else ''
                if Checker['上级代理']:
                    temp['上级代理'] = str(UParent) if UParent else ''
                if Checker['VIP等级']:
                    temp['VIP等级'] = str(userVIP) if userVIP else ''
                temp_list.append(temp)
            if i - 1 == user_count:
                count = 100
            self.qthread_signal.emit(int(count))

        while True:
            try:
                end = pd.DataFrame(temp_list)
                end.to_csv("数据.csv",encoding="utf_8_sig")
                break
            except:
                QMessageBox.about(QtW,'Error','请先关闭 数据.csv 窗口，然后点击 确认 以继续进行')
        if error_acc:
            print('以下为 错误账号\n')
            for i in error_acc:
                print(i)
            print('-'*30)
        print("会员数据完成。")
        return temp_list

    def start_progress_daoge(self,driver,QtW,platform,filePath,temp_list,Checker):
        def get_deposit_Info(driver,platform):
            logs_raw = driver.get_log("performance")
            logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
            def log_filter(log_):
                    return (log_["method"] == "Network.responseReceived" and "json" in log_["params"]["response"]["mimeType"])
            for log in filter(log_filter, logs):
                request_id = log["params"]["requestId"]
                resp_url = log["params"]["response"]["url"]
                if resp_url == f"{url_link[platform]['urlPre']}api/manage/fund/recharge/record/list/sum":
                    data = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body']
                    data = json.loads(data)
                    if data['message'].lower() == 'success':
                        deposit_amount = str(data['data']['arrivalAmountCollect']) if data['data']['arrivalAmountCollect'] > 0 else ""
                        return deposit_amount
        def get_withdraw_Info(driver,platform):
            logs_raw = driver.get_log("performance")
            logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
            def log_filter(log_):
                    return (log_["method"] == "Network.responseReceived" and "json" in log_["params"]["response"]["mimeType"])
            for log in filter(log_filter, logs):
                request_id = log["params"]["requestId"]
                resp_url = log["params"]["response"]["url"]
                if resp_url == f"{url_link[platform]['urlPre']}api/manage/fund/withdraw/record/list/history":
                    data = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body']
                    data = json.loads(data)
                    if data['message'].lower() == 'success':
                        for withdraw_row in data['data']['list']:
                            if withdraw_row['actualAmount'] > 0:
                                withdraw_info = f"{str(timeStamp(withdraw_row['receiveDate']))} {str(withdraw_row['actualAmount'])} USDT提现"
                                return withdraw_info
                        no_withdraw = ''
                        return no_withdraw
        n = 1
        while n <= 2:
            driver.get(url_link[platform]['homePage'])
            game_list = WebDriverWait(driver, 20, 0.5).until(EC.visibility_of_element_located((By.XPATH, f'//a[text()="{"充值记录" if n == 1 else "提现订单记录"}"]')))
            game_list.click()
            while True:
                QMessageBox.about(QtW,'NextStep',f"{'请先调整时间和支付方式，然后点击 确认 以继续进行' if n == 1 else '请先调整时间，然后点击 确认 以继续进行'}")
                res = QMessageBox.information(QtW,'查询确认', '是否调整完毕?', QMessageBox.Yes | QMessageBox.No)
                if res == 16384:
                    break
            data_name = '充值总金额' if n == 1 else '最近一次提款记录'
            df = pd.read_excel(filePath)
            a = df.last_valid_index()
            user_count = df.last_valid_index() + 1
            count = 0
            check_u = ''
            us1 = 0
            for i in range(user_count):
                count += 100 / user_count
                while True:
                    try:
                        username = str(df.iat[i,0])
                        input_username = WebDriverWait(driver, 20, 0.5).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="create-form_userName"]')))
                        input_username.clear()
                        input_username.send_keys(username)
                        input_username.send_keys(Keys.ENTER)
                        time.sleep(0.3)
                        result = get_deposit_Info(driver,platform) if n == 1 else get_withdraw_Info(driver,platform)
                        if us1 != 0:
                            break
                        us1 = 1
                    except:
                        pass
                if temp_list != []:
                    if n == 2:
                        userList = []
                        for UserDict in temp_list:
                            if UserDict['会员账号'] == username:
                                UserDict[data_name] = str(result) if result else ""
                    else:
                        temp = {
                            '会员账号': username
                            }
                        temp[data_name] = str(result) if result else ""
                        temp_list.append(temp)
                else:
                    temp = {
                        '会员账号': username
                        }
                    temp[data_name] = str(result) if result else ""
                    temp_list.append(temp)
                if i - 1 == user_count:
                    count = 100
                self.qthread_signal.emit(int(count))
    
            while True:
                try:
                    end = pd.DataFrame(temp_list)
                    end.to_csv("数据.csv",encoding="utf_8_sig")
                    break
                except:
                    QMessageBox.about(QtW,'Error','请先关闭 数据.csv 窗口，然后点击 确认 以继续进行')
            n += 1
        print("道哥奇耙数据完成。")
        return temp_list

    def start_progress_rescue(self,driver,QtW,platform,filePath,temp_list,Checker):
        def click_locxy(driver,x,y,left_click=True):
            if left_click:
                ActionChains(driver).move_by_offset(x,y).click().perform()
            else:
                ActionChains(driver).move_by_offset(x,y).context_click().perform()
            ActionChains(driver).move_by_offset(-x,-y).perform()
        def get_responce_Info(driver,platform):
            logs_raw = driver.get_log("performance")
            logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
            def log_filter(log_):
                    return (log_["method"] == "Network.responseReceived" and "json" in log_["params"]["response"]["mimeType"])
            for log in filter(log_filter, logs):
                request_id = log["params"]["requestId"]
                resp_url = log["params"]["response"]["url"]
                if resp_url == f"{url_link[platform]['urlPre']}api/manage/data/trend/userFund":
                    data = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body']
                    data = json.loads(data)
                    if data['message'].lower() == 'success':
                        winlose = data['data']['winSum'] * -1
                        bonus = data['data']['bonusSum']
            return winlose, bonus
            
        df = pd.read_excel(filePath)
        before_username = ""
        flow = ""
        count = 0
        user_count = df.last_valid_index() + 1
        #driver.maximize_window()
        for i in range(user_count):
            count += 100 / user_count
            username = str(df.iat[i,0])
            input_username = WebDriverWait(driver, 20, 0.5).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div/section/section/header[2]/div/div[2]/span/span/span[1]/input')))
            input_username.clear()
            input_username.send_keys(username)
            input_username.send_keys(Keys.ENTER)
            while True:
                time.sleep(0.3)
                try:
                    click_locxy(driver,1700,530)
                    click_locxy(driver,1500,830)
                    time.sleep(0.3)
                    winlose , bonus = get_responce_Info(driver,platform)
                except:
                    print(f'{username} Error!')
                if before_username != username:
                    before_username == username
                    break
            temp = {
                '会员账号':username,
                '玩家输赢': float(winlose) if winlose else "",
                '红利': float(bonus) if bonus else ""
                }
            temp_list.append(temp)
            driver.refresh()
            if i + 1 == user_count:
                count = 100
            self.qthread_signal.emit(int(count))
        while True:
            try:
                end = pd.DataFrame(temp_list)
                end.to_csv("数据.csv",encoding="utf_8_sig")
                break
            except:
                QMessageBox.about(QtW,'Error','请先关闭 数据.csv 窗口，然后点击 确认 以继续进行')
        print("救援金完成。")
        return temp_list

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginPage()
        self.ui.setupUi(self)
        self.Login_setup_control()

### Login Page
    def Login_setup_control(self):
        self.ui.confirmButton.clicked.connect(self.confirmClicked)
        self.ui.exitButton.clicked.connect(self.exited)

    def confirmClicked(self):
        print('Confirm Button clicked!')
        if self.ui.platformBox.currentText() == '请选择':
            QMessageBox.about(self,'Error','请选择平台')
            return
        if self.ui.accountText.text() and self.ui.passwordText.text() and self.ui.codeText.text():
            print('pass')
        else:
            QMessageBox.about(self,'Error','请输入 账号&密码&验证码')
            return
        try:
            self.platform = self.ui.platformBox.currentText()
            self.driver = start_driver(self.ui.platformBox.currentText())
        except:
            QMessageBox.about(self,'Error','请更新Chrome浏览器后再尝试')
            return
           
        result = login(self.driver,
                       self.ui.accountText.text(),
                       self.ui.passwordText.text(),
                       self.ui.codeText.text())
        if result:
            QMessageBox.about(self,'Error',result)
            self.driver.quit()
            return
        self.ui = Ui_MainPage()
        self.ui.setupUi(self)
        self.Main_setup_control()
        username = WebDriverWait(self.driver, 3, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/header[2]/div/div[2]/div/span[1]'))).text
        if username != '账号: din':
            self.ui.rescue.setEnabled(False)
        position = WebDriverWait(self.driver, 3, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/header[2]/div/div[2]/div/span[2]'))).text
        if position == '岗位: 代理客服':
            self.ui.daogeData.setEnabled(False)

    def exited(self):
        import sys
        sys.exit()

### Main Page
    def Main_setup_control(self):
        # TODO
        #pass
        self.ui.progressBar.setMaximum(100)
        self.ui.fileButton.clicked.connect(self.open_file)
        self.ui.startButton.clicked.connect(self.start)
        self.ui.daogeData.clicked.connect(self.uncheck)

    def uncheck(self):
        if self.ui.daogeData.isChecked():
            self.ui.sportFlow.setChecked(False)
            self.ui.nsportFlow.setChecked(False)
            self.ui.lastBetTime.setChecked(False)
            self.ui.upamountTime.setChecked(False)
            self.ui.parent.setChecked(False)
            self.ui.userVIP.setChecked(False)
            self.ui.rescue.setChecked(False)

    def open_file(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./",
                  "Excel files (*.xlsx)")
        self.ui.filePath.setText(filename if filename else '待导入.....')

    def readExcel(self):
        df = pd.read_excel(self.ui.filePath.text())
        a = df.last_valid_index()
        user_count = df.last_valid_index() + 1
        for i in range(user_count):
            username = str(df.iat[i,0])
            print(username)

    def start(self):
        if self.ui.filePath.text() == '待导入.....':
            QMessageBox.about(self,'Error','请导入查询表格')
            return
        if self.ui.sportFlow.isChecked() or self.ui.nsportFlow.isChecked() or self.ui.lastBetTime.isChecked() or self.ui.upamountTime.isChecked() or self.ui.parent.isChecked() or self.ui.daogeData.isChecked() or self.ui.userVIP.isChecked() or self.ui.rescue.isChecked():
            pass
        else:
            QMessageBox.about(self,'Error','请选择查询选项')
            return
        self.uncheck()
        Checker = {
            "体育流水": self.ui.sportFlow.isChecked(),
            "娱乐流水": self.ui.nsportFlow.isChecked(),
            "最后投注时间": self.ui.lastBetTime.isChecked(),
            "(代)充值次数": self.ui.upamountTime.isChecked(),
            "上级代理": self.ui.parent.isChecked(),
            "道哥奇耙数据": self.ui.daogeData.isChecked(),
            "VIP等级": self.ui.userVIP.isChecked(),
            "救援金": self.ui.rescue.isChecked()
        }
        res = QMessageBox.information(self,'查询确认', (''.join("%s : %s\n" % (name,'✓' if isCheck else '✗') for name,isCheck in Checker.items())), QMessageBox.Yes | QMessageBox.No)
        if res == 16384:
            temp_list = []
            get_user = 0
            for a , b in Checker.items():
                if b:
                    if a in ['体育流水','娱乐流水']:
                        self.qthread = ThreadTask()
                        self.qthread.start()
                        self.qthread.qthread_signal.connect(self.progress_changed)
                        if a == '体育流水':
                            game_list = WebDriverWait(self.driver, 20, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//a[text()="游戏注单查询"]')))
                            game_list.click()
                            QMessageBox.about(self,'下一步','請先篩選時間&体育場館，然后点击确认')
                            QMessageBox.about(self,'下一步','确认筛选完成？')
                            self.ui.Logger.append(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} -> 体育流水查询...\n')
                            temp_list = self.qthread.start_progress_flow(self.driver,self,self.ui.filePath.text(),temp_list)
                            self.qthread.terminate()
                            self.ui.progressBar.setProperty("value", 0)
                            self.ui.Logger.append(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} -> 体育流水查询完成。\n')
                        elif a == '娱乐流水':
                            game_list = WebDriverWait(self.driver, 20, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//a[text()="游戏注单查询"]')))
                            game_list.click()
                            QMessageBox.about(self,'下一步','請先篩選時間&娱乐場館，然后点击确认')
                            QMessageBox.about(self,'下一步','确认筛选完成？')
                            self.ui.Logger.append(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} -> 娱乐流水查询...\n')
                            temp_list = self.qthread.start_progress_nflow(self.driver,self,self.ui.filePath.text(),temp_list,Checker)
                            self.qthread.terminate()
                            self.ui.progressBar.setProperty("value", 0)
                            self.ui.Logger.append(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} -> 娱乐流水查询完成。\n')
                    elif a in ['最后投注时间','(代)充值次数','上级代理','VIP等级'] and get_user == 0:
                        self.qthread = ThreadTask()
                        self.qthread.start()
                        self.qthread.qthread_signal.connect(self.progress_changed) 
                        self.ui.Logger.append(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} -> 会员数据查询...\n')
                        temp_list = self.qthread.start_progress_user(self.driver,self,self.platform,self.ui.filePath.text(),temp_list,Checker)
                        self.qthread.terminate()
                        self.ui.progressBar.setProperty("value", 0)
                        self.ui.Logger.append(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} -> 会员数据查询完成。\n')
                        get_user = 1
                    elif a == "道哥奇耙数据":
                        self.qthread = ThreadTask()
                        self.qthread.start()
                        self.qthread.qthread_signal.connect(self.progress_changed) 
                        self.ui.Logger.append(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} -> 道哥数据查询...\n')
                        temp_list = self.qthread.start_progress_daoge(self.driver,self,self.platform,self.ui.filePath.text(),temp_list,Checker)
                        self.qthread.terminate()
                        self.ui.progressBar.setProperty("value", 0)
                        self.ui.Logger.append(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} -> 道哥数据查询完成。\n')
                    elif a == "救援金":
                        self.driver.maximize_window()
                        self.qthread = ThreadTask()
                        self.qthread.start()
                        self.qthread.qthread_signal.connect(self.progress_changed) 
                        self.ui.Logger.append(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} -> 救援金数据查询...\n')
                        temp_list = self.qthread.start_progress_rescue(self.driver,self,self.platform,self.ui.filePath.text(),temp_list,Checker)
                        self.qthread.terminate()
                        self.ui.progressBar.setProperty("value", 0)
                        self.ui.Logger.append(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} -> 救援金数据查询完成。\n')
                    self.driver.get(url_link[self.platform]['homePage'])
            QMessageBox.about(self,'Finished!','数据已完成，点击 OK 开启')
            os.startfile('数据.csv')

    def progress_changed(self, value):        
        self.ui.progressBar.setValue(value)
