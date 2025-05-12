from . import dev_run_util  

def test1():
    print('test1 122')
    data = dev_run_util.list_dev_run_files()
    print(data) 

def test2():
    filepath = ".\\fly_dev_run\\sample_dev_run.py"
    filepath = "sample2_dev_run.py" 
    dev_run_util.run_dev_run_function(filepath) 

def test3():
    # 使用示例
    data_list = ['dev_run', 'arg1', 'arg2']
    dev_run_util.save_to_cache_file(data_list, '.fly_dev_run.cache.txt') 
    dev_run_util.read_from_cache_file()

def dev_run():
    test1()  
    # test2() 
    # test3()