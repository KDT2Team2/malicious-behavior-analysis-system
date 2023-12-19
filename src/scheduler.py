import subprocess
import requests
import json
import os
import time
from urllib.parse import unquote
from vbox import *
from commander import *

VM_NAME = "WinDev2311Eval"
AGENT_URL = 'http://localhost:5000'

def start_vm():
    try:
        subprocess.run(["VBoxManage", "startvm", VM_NAME])
        print(f"{VM_NAME} 가상머신이 시작되었습니다.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"가상머신 시작 중 오류 발생: {e}")
        return False

def wait_for_vm_start():
    max_attempts = 10  # 적절한 횟수로 조정
    attempts = 0

    while attempts < max_attempts:
        try:
            subprocess.run(["VBoxManage", "guestproperty", "get", VM_NAME, "/VirtualBox/GuestInfo/Net/0/V4/IP"])
            print(f"{VM_NAME} 가상머신이 시작 및 사용 가능한 상태입니다.")
            return True
        except subprocess.CalledProcessError:
            attempts += 1
            print(f"가상머신 시작 대기 중 ({attempts}/{max_attempts})...")
            time.sleep(5)  # 5초 대기 후 다시 시도

    print("가상머신이 시작되지 않았거나 사용 가능한 상태가 아닙니다.")
    return False

def stop_vm():
    try:
        subprocess.run(["VBoxManage", "controlvm", VM_NAME, "poweroff"])
        print(f"{VM_NAME} 가상머신이 종료되었습니다.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"가상머신 종료 중 오류 발생: {e}")
        return False

# 기존 함수들과 함께 추가된 함수들

def start_analyze(vm_name, file_path, snapshot_name, argument, timeout):
    try:
        rollback_vm(snapshot_name)
        start_vm()
        wait_for_vm_start()
        remote_path = 'c:\\target.exe'
        upload_file(file_path)
        # exec_remote_path(vm_name, remote_path, argument, timeout)
        # exec_event_export(vm_name)
        download_file("..\\..\\..\\..\\..\\..\\..\\..\\..\\..\\..\\Windows\\System32\\winevt\\Logs\\Microsoft-Windows-Sysmon%4Operational.evtx", 'C:/Users/dealu/OneDrive/바탕 화면/프로젝트/project 2-2/test/sys_test.evtx')
        stop_vm()
        rollback_vm(snapshot_name)
        # db_handler = connect_db('YourDatabaseAddress')
        # upload_to_db('C:\\path\\to\\your\\local\\event\\log.csv', 'YourIndexName', db_handler)
        # close_db(db_handler)
    except Exception as e:
        print(f"분석 중 오류 발생: {e}")

def main():
    analyze_target_path = './test.exe'
    vm_name = 'WinDev2311Eval'
    argument = ''
    timeout = 30
    snapshot_name = "snapshot6"

    try:
        start_analyze(vm_name, analyze_target_path, snapshot_name, argument, timeout)
    except Exception as e:
        print(f"자동 분석 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
