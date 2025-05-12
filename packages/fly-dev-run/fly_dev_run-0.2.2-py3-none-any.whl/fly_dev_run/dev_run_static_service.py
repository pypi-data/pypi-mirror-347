
import os 
from . import dev_run_util

def getFileCreateAge(filepath):
    """
    得到文件的创建时间,到现在位置的天数。（浮点数） 
    """
    import time
    ctime = os.path.getctime(filepath)
    t = time.time() - ctime
    return t / 3600 / 24   

class DevRunStaticService:
    def __init__(self):
        # self.static_service = static_service
        self.file_list_cache_file_name = '.fly_dev_run.cache.txt'
        self.command_history_list_cache_file_name = '.fly_dev_run.his_list.txt'
        self.dev_run_file_list = None
        self.command_history_list = None

    def run(self,command):
        # self.static_service.run()
        print("DevRunStaticService run ....", command)  

    def init(self):
        # print("init ....") 
        if dev_run_util.check_cache_file_exists(self.file_list_cache_file_name):
            fileAge = getFileCreateAge(self.file_list_cache_file_name) 
            print("dev_run cache file age:", fileAge)
            if fileAge > 1:
                # 重新生成缓存dev_run list 文件
                self.dev_run_file_list = dev_run_util.list_dev_run_files() 
                dev_run_util.save_to_cache_file(self.dev_run_file_list, self.file_list_cache_file_name) 
            else:
                self.dev_run_file_list = dev_run_util.read_from_cache_file(self.file_list_cache_file_name) 
        else:
            # 重新生成缓存dev_run list 文件 
            self.dev_run_file_list = dev_run_util.list_dev_run_files() 
            dev_run_util.save_to_cache_file(self.dev_run_file_list, self.file_list_cache_file_name) 

        # print(self.dev_run_file_list ) 

        if dev_run_util.check_cache_file_exists(self.command_history_list_cache_file_name):
            self.command_history_list = dev_run_util.read_from_cache_file(self.command_history_list_cache_file_name)
        else:
            self.command_history_list = [] 
            

    def list(self):
        print("list all dev_run files ....") 
        # self.command_history_list.insert(0, "list")
        if self.dev_run_file_list is None:
            print("not dev_run_file_list data. ")
            return 
        for index, item in enumerate(self.dev_run_file_list):
            print(f"{index+1} {item}") 

    def his(self):
        print("history list ....") 
        # self.command_history_list.insert(0, "list")
        if self.command_history_list is None:
            print("not command_history_list data. ")
            return 
        for index, item in enumerate(self.command_history_list):
            print(f"{index+1}. {item}") 

    def refresh(self):
        self.dev_run_file_list = dev_run_util.list_dev_run_files() 
        dev_run_util.save_to_cache_file(self.dev_run_file_list, self.file_list_cache_file_name)  

    def clear(self):
        self.command_history_list = [] 
        dev_run_util.save_to_cache_file(self.command_history_list, self.command_history_list_cache_file_name)    
    
    def start_ui(self):
        print("start_ui .... not implement.")  

    def run_cmd(self,cmd):
        if type(cmd) == int:
            index = cmd - 1
            if index < len(self.dev_run_file_list):
                file_path = self.dev_run_file_list[index]

                
                dev_run_util.run_dev_run_function(file_path)

                if file_path in self.command_history_list:
                    self.command_history_list.remove(file_path) 
                self.command_history_list.insert(0, file_path)
                dev_run_util.save_to_cache_file(self.command_history_list, self.command_history_list_cache_file_name)
            else:
                print("index out of range.") 
        else:            
            # print(self.dev_run_file_list) 
            tmp_dev_file_list = dev_run_util.filter_by_string(self.dev_run_file_list, cmd)
            if len(tmp_dev_file_list) == 1:
                

                print("run_cmd ....", tmp_dev_file_list)  
                current_path = os.getcwd()
                print(current_path)


                dev_run_util.run_dev_run_function(tmp_dev_file_list[0]) 

                if tmp_dev_file_list[0] in self.command_history_list:
                    self.command_history_list.remove(tmp_dev_file_list[0]) 
                self.command_history_list.insert(0, tmp_dev_file_list[0])
                dev_run_util.save_to_cache_file(self.command_history_list, self.command_history_list_cache_file_name) 
            else:
                print("not found or more than one.")
                for index, item in enumerate(tmp_dev_file_list):
                    print(f"{item}")  


devRunService = DevRunStaticService()  