from colorama import init
import os
import platform
import datetime
import subprocess
import psutil

init(autoreset=True)

def system_info():
    status = 200
    info = {
        "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "computer_name": platform.node(),
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.architecture()[0],
    }
    return status, info

def check_services(services):
    active_services = {}
    for service in services:
        result = subprocess.run(f"sc query {service}", capture_output=True, text=True, shell=True)
        active_services[service] = "Running" if "RUNNING" in result.stdout else "Not Running"
    return active_services

def get_process_start_times(process_names):
    process_start_times = {}
    for process in psutil.process_iter(['name', 'create_time']):
        try:
            if process.info['name'] in process_names:
                start_time = datetime.datetime.fromtimestamp(process.info['create_time']).strftime("%Y-%m-%d %H:%M:%S")
                process_start_times[process.info['name']] = start_time
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return process_start_times

banner = """
  _________               __                   .___        _____       
 /   _____/__.__. _______/  |_  ____   _____   |   | _____/ ____\____  
 \_____  <   |  |/  ___/\   __\/ __ \ /     \  |   |/    \   __\/  _ \ 
 /        \___  |\___ \  |  | \  ___/|  Y Y  \ |   |   |  \  | (  <_> )
/_______  / ____/____  > |__|  \___  >__|_|  / |___|___|  /__|  \____/ 
        \/\/         \/            \/      \/           \/                                                
"""

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)
    
    status, info = system_info()

    if status == 200:
        print("\033[39m Status \033[92m200 \u2713") 
        print("\033[94m [\U0001F4C5] \033[39mCurrent Time:\033[94m " + info["current_time"])
        print("\033[94m [\U0001F4BB] \033[39mComputer Name:\033[94m " + info["computer_name"])
        print("\033[94m [\U0001F4C8] \033[39mOperating System:\033[94m " + info["os"] + " " + info["os_version"])
        print("\033[94m [\U0001F4C8] \033[39mArchitecture:\033[94m " + info["architecture"])
        
        services_to_check = ["pcasvc", "DPS", "Diagtrack", "sysmain", "eventlog"]
        active_services = check_services(services_to_check)

        print("\n\033[94m [\U0001F6A7] \033[39mService Status:")
        for service, status in active_services.items():
            print(f"\033[94m [\U0001F6A7] \033[39m{service}:\033[94m {status}")

        process_names = ["explorer.exe","notepad.exe"]
        process_start_times = get_process_start_times(process_names)

        print("\n\033[94m [\U0001F4C5] \033[39mProcess Start Times:")
        if process_start_times:
            for process, start_time in process_start_times.items():
                print(f"\033[94m [\U0001F4C5] \033[39m{process}:\033[94m {start_time}")
        else:
            print("\033[94m [\U0001F6AB] \033[39mNo processes found in the specified list.")

if __name__ == "__main__":
    main()