import os
import zipfile
import requests
from tqdm import tqdm
from PyQt5 import QtWidgets

from controller import MainWindow_controller

local_version = "v1.5.0"

def check_version():
    download_url = "https://github.com/DinforML/workingTools/releases/download/%s/default.zip"
    url = "https://api.github.com/repos/DinforML/workingTools/releases/latest"
    response = requests.get(url)
    online_version = response.json()['tag_name']

    if local_version >= online_version:
        print(f"当前版本为最新版本[ {local_version} ] ！")
    else:
        name = 'WorkingTools ' + online_version.replace('/','_') + '.zip'
        print(f"当前版本[{local_version}]已过期，下载新版本[{online_version}]中...")
        response = requests.get(download_url % online_version, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        block_size = 1024 #1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(name, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("下载失败，请重新尝试。")
        print("下载完毕。")
        if os.path.getsize(name) != 0:
            with zipfile.ZipFile(name,"r") as zip_ref:
                zip_ref.extractall(path=f'./workingTools {online_version}')
            #os.rename('default',f'WorkingTools-{online_version}')
            os.remove(name)
        input(f'请使用新版本 {online_version}\npress ENTER to quit...')
        os.startfile(f'workingTools {online_version}')
        exit()

if __name__ == '__main__':
    check_version()
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec_())
