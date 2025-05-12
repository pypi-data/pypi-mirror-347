import sys 
from . import version
from .dev_run_static_service import devRunService

def print_help():
    print(f"dev_run({version.__version__}) ") 
    print("Usage: dev_run <command>")  
    print("Commands:")
    print("help       Print help") 
    print("ui         start ui") 
    print("list       list all dev_run files ")  
    print("his        list recent dev_run files")   
    print("refresh    search currend dir and create cache data") 
    print("clear      clear history list data") 
    print(".          run recent dev_run task ")    
    print("1,2,3,4,5          run recent dev_run task by index ") 
    print("[part_of_file_name]      run special dev_run task by name, or list or list name ")  


def main():
    # print(sys.argv)  # ['dev_run', 'arg1', 'arg2'] 
    size = len(sys.argv)
    # print("size", size) 
    if size != 2:
        print_help()
        return
    
    cmd = sys.argv[1]
    if cmd == "help":
        print_help()
        return 

    devRunService.init()

    if cmd == "ui": 
        devRunService.start_ui()
    elif cmd == "list": 
        devRunService.list()
    elif cmd == "his": 
        devRunService.his()
    elif cmd == "clear":
        devRunService.clear()  
    elif cmd == "refresh":
        devRunService.refresh() 
    elif cmd == ".":
        print("run recent dev_run task ....") 
        devRunService.run_cmd(1) 
    elif cmd in ["1", "2", "3", "4", "5"]:
        devRunService.run_cmd(int(cmd)) 
    else:        
        devRunService.run_cmd(cmd)  


if __name__ == "__main__":
    main() 