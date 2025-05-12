

import os 
import importlib.util

# def list_dev_run_files():
#     # 初始化文件列表
#     dev_run_files = []
    
#     # 遍历当前目录下的所有文件和文件夹
#     for root, dirs, files in os.walk('.', topdown=True):
#         # 过滤掉所有不包含__init__.py的目录
#         if not any(os.path.join(root, d) == '__init__.py' for d in dirs):
#             # 遍历当前目录下的所有文件
#             for file in files:
#                 # 判断文件是否以_dev_run.py结尾
#                 if file.endswith('_dev_run.py'):
#                     # 拼接完整文件路径并添加到列表中
#                     dev_run_files.append(os.path.join(root, file))
    
#     return dev_run_files 

def list_dev_run_files(directory='.'):
    dev_run_files = []

    def _list_files(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path) and '__init__.py' in os.listdir(item_path):
                _list_files(item_path)
            elif item.endswith('_dev_run.py'):
                dev_run_files.append(item_path)

    _list_files(directory)
    return dev_run_files




def run_dev_run_function(file_path):
    """
    运行给定路径下的Python文件中的dev_run函数。

    参数：
    file_path: str，Python文件的路径。

    返回：
    如果dev_run函数存在并成功执行，则返回其返回值，否则返回None。
    """
    # 检查文件路径是否存在
    if not os.path.exists(file_path):
        print(f"文件 '{file_path}' 不存在。")
        return None
    
    # 获取文件名和扩展名
    file_name, file_extension = os.path.splitext(file_path)
    
    # 检查文件是否为Python文件
    if file_extension != '.py':
        print(f"文件 '{file_path}' 不是Python文件。")
        return None
    
    # 尝试动态导入模块
    try:
        module_name = os.path.basename(file_name)

        # print(f"module_name: {module_name}")
        # print(f"file_path: {file_path}")
        # file_path: .\fly_dev_run\dev_run_util_dev_run.py 
        #

        def convert_path_to_string(input_str):
            # 移除字符串开头的 "."
            input_str = input_str.lstrip(".")
            # 将 "\\" 替换为 "."
            input_str = input_str.replace("\\", ".")
            input_str = input_str.replace("/", ".")
            # 移除字符串末尾的 ".py"
            input_str = input_str.rstrip(".py")
            return input_str[1:]
        
        run_module = convert_path_to_string(file_path)
        print("run_module", run_module) 

        with open("_dev_run.py", "w") as file:
            file.write(f"from {run_module} import dev_run \r\ndev_run() ")         

        # spec = importlib.util.find_spec(name) 
        # spec = importlib.util.spec_from_file_location("_dev_run.py", "./_dev_run.py") 

        # module = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(module)
    except Exception as e:
        print(f"导入模块 '{module_name}' 时出现错误：{e}")
        return None
    
    os.system("python _dev_run.py") 
    
    # # 检查模块是否包含 dev_run 函数
    # if not hasattr(module, 'dev_run'):
    #     print(f"模块 '{module_name}' 中不存在 dev_run 函数。")
    #     return None
    
    # # 运行 dev_run 函数
    # try:
    #     result = module.dev_run()
    #     print(f"文件 '{file_path}' 中的 dev_run 函数成功执行。")
    #     return result
    # except Exception as e:
    #     print(f"执行文件 '{file_path}' 中的 dev_run 函数时出现错误：{e}") 
    #     return None


def save_to_cache_file(data_list,filename):
    # 文件名
    # filename = '.fly_dev_run.cache.txt'
    
    # 确保目录存在
    if not os.path.exists('.'):
        os.makedirs('.')
    
    # 打开文件并写入数据
    with open(filename, 'w') as f:
        for data in data_list:
            f.write(data + '\n')
    
    # print(f'数据已保存到 {filename}')

def read_from_cache_file(filename):
    # 文件名
    # filename = '.fly_dev_run.cache.txt'
    
    # 打开文件并读取数据
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    # 去掉空行
    data_list = [line.strip() for line in lines if line.strip()]

    return data_list 
    
    # print(f'从 {filename} 读取的数据：')
    # print(data_list)

def filter_by_string(data_list, target_string):
    """
    过滤出包含指定字符串的数据列表

    :param data_list: 原始数据列表
    :param target_string: 指定的字符串
    :return: 包含指定字符串的数据列表
    """
    if data_list is None:
        return [] 

    # 使用列表推导式过滤出包含指定字符串的元素    

    filtered_list = [item for item in data_list if target_string in item]

    if len(filtered_list) > 1:
        # 完全匹配直接返回  
        # print("len(filtered_list) > 1")
        for item in filtered_list:
            
            filename = os.path.basename(item)
            # print("aaa",item, filename, target_string)  
            if filename == target_string or filename == target_string + ".py":
                return [item]
               

    return filtered_list


def check_cache_file_exists(file_name):
    # ".fly_dev_run.cache.txt" 
    # 当前文件夹路径
    current_directory = os.getcwd()
        
    # 文件完整路径
    file_path = os.path.join(current_directory, file_name)
    
    # 检查文件是否存在
    if os.path.isfile(file_path):
        return True
    else:
        return False




# 使用函数并打印结果
# print(list_dev_run_files())
