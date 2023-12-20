import subprocess
import requests
import json
import os
import time
from urllib.parse import unquote
from vbox import *
from commander import *

VM_NAME = "WinDev2311Eval"   # 가상머신 이름
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

def exec_remote_path(vm_name, remote_path, argument, timeout):
    try:
        subprocess.run(remote_path, timeout=timeout, check=True)
        print(f"{remote_path} 파일이 실행되었습니다.")
    except subprocess.CalledProcessError as e:
        print(f"파일 실행 중 오류 발생: {e}")
    except subprocess.TimeoutExpired:
        print(f"파일 실행 시간이 초과되었습니다.")




def start_analyze(vm_name, file_path, snapshot_name, argument, timeout, v_file, r_file):
    try:
        rollback_vm(snapshot_name) # 가상환경을 스냅샷으로 초기화
        start_vm() # 가상환경 실행
        wait_for_vm_start() # 가상환경이 스냅샷 버젼으로 실행될 때 까지 대기
        upload_file(file_path) # 테스트 대상 파일 업로드

        run_sysmon() # Sysmon.exe 실행

        time.sleep(timeout)

        exec_remote_path(vm_name, file_path, argument, timeout) # 테스트 대상 파일 실행

        time.sleep(timeout)

        download_file(v_file, r_file) # sysmon 결과 파일 다운로드
        stop_vm() # 가상환경 중지
        rollback_vm(snapshot_name) # 가상환경을 스냅샷으로 초기화

        # db_handler = connect_db('YourDatabaseAddress')
        # upload_to_db('C:\\path\\to\\your\\local\\event\\log.csv', 'YourIndexName', db_handler)
        # close_db(db_handler)
    except Exception as e:
        print(f"분석 중 오류 발생: {e}")

def main():
    analyze_target_path = './test.exe' # 가상환경에서 테스트할 파일의 경로
    vm_name = 'WinDev2311Eval' # 가상머신 이름 (맨 위의 전역변수도 변경 필요)
    argument = ''
    timeout = 30
    snapshot_name = "snapshot9" # 가상환경에 생성되어있는 스냅샷 이름
    # 가상환경 sysmon 결과 파일 경로
    v_file = "..\\..\\..\\..\\..\\..\\..\\..\\..\\..\\..\\Windows\\System32\\winevt\\Logs\\Microsoft-Windows-Sysmon%4Operational.evtx"
    r_file = 'C:/Users/dealu/OneDrive/바탕 화면/프로젝트/project 2-2/test/sys_test3.evtx' # 출력된 파일 저장 경로


    try:
        start_analyze(vm_name, analyze_target_path, snapshot_name, argument, timeout, v_file, r_file)
    except Exception as e:
        print(f"자동 분석 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
