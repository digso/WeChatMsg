from app.decrypt.get_bias_addr import BiasAddr
from app.decrypt.get_wx_info import read_info

from PyQt5.QtCore import pyqtSignal, QThread
class DecryptThread(QThread):
    signal = pyqtSignal(str)
    maxNumSignal = pyqtSignal(int)
    okSignal = pyqtSignal(str)
    errorSignal = pyqtSignal(bool)

    def __init__(self, db_path, key):
        super(DecryptThread, self).__init__()
        self.db_path = db_path
        self.key = key
        self.textBrowser = None

    def __del__(self):
        pass

    def run(self):
        from app.DataBase import close_db
        close_db()
        # from app.config import DB_DIR
        DB_DIR = './data/database'
        output_dir = DB_DIR
        import os
        os.makedirs(output_dir, exist_ok=True)
        tasks = []
        if os.path.exists(self.db_path):
            for root, dirs, files in os.walk(self.db_path):
                for file in files:
                    if '.db' == file[-3:]:
                        if 'xInfo.db' == file:
                            continue
                        inpath = os.path.join(root, file)
                        # print(inpath)
                        output_path = os.path.join(output_dir, file)
                        tasks.append([self.key, inpath, output_path])
                    else:
                        try:
                            name, suffix = file.split('.')
                            if suffix.startswith('db_SQLITE'):
                                inpath = os.path.join(root, file)
                                # print(inpath)
                                output_path = os.path.join(output_dir, name + '.db')
                                tasks.append([self.key, inpath, output_path])
                        except:
                            continue
        self.maxNumSignal.emit(len(tasks))
        for i, task in enumerate(tasks):
            from app.decrypt.decrypt import decrypt
            if decrypt(*task) == -1:
                self.errorSignal.emit(True)
            self.signal.emit(str(i))
        # print(self.db_path)
        # 目标数据库文件
        target_database = os.path.join(DB_DIR, 'MSG.db')
        # 源数据库文件列表
        source_databases = [os.path.join(DB_DIR, f"MSG{i}.db") for i in range(1, 50)]
        import shutil
        if os.path.exists(target_database):
            os.remove(target_database)
        shutil.copy2(os.path.join(DB_DIR, 'MSG0.db'), target_database)  # 使用一个数据库文件作为模板
        # 合并数据库
        from app.DataBase.merge import merge_databases, merge_MediaMSG_databases
        merge_databases(source_databases, target_database)

        # 音频数据库文件
        target_database = os.path.join(DB_DIR, 'MediaMSG.db')
        # 源数据库文件列表
        if os.path.exists(target_database):
            os.remove(target_database)
        source_databases = [os.path.join(DB_DIR, f"MediaMSG{i}.db") for i in range(1, 50)]
        shutil.copy2(os.path.join(DB_DIR, 'MediaMSG0.db'), target_database)  # 使用一个数据库文件作为模板

        # 合并数据库
        merge_MediaMSG_databases(source_databases, target_database)
        self.okSignal.emit('ok')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--account", type=str, help="微信号", required=False)
    parser.add_argument("--mobile", type=str, help="手机号", required=False)
    parser.add_argument("--name", type=str, help="微信昵称", required=False)

    args = parser.parse_args()

    import sys
    sys.path.append('.')

    from app.decrypt.get_bias_addr import BiasAddr
    bias_addr = BiasAddr(args.account, args.mobile, args.name, '', '')
    data = bias_addr.run(logging_path=True)
    print(data)

    from app.decrypt.get_wx_info import read_info
    result = read_info(data)
    print(result)

    path = result[0]['filePath']
    key = result[0]['key']
    worker = DecryptThread(path, key)
    worker.run()