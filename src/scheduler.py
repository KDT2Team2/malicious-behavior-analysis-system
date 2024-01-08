import subprocess
import time
from urllib.parse import unquote
from vbox import *
from commander import *
from event_uploader import *

VM_NAME = "WinDev2311Eval"   # 가상머신 이름

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
        rollback_vm(vm_name,snapshot_name) 
        start_vm() 
        wait_for_vm_start() 
        upload_file(file_path) 

        # run_sysmon() # Sysmon.exe 실행
        post_command(file_path)

        download_file(v_file, r_file) # sysmon 결과 파일 다운로드
        stop_vm() 
        rollback_vm(vm_name,snapshot_name) 
    except Exception as e:
        print(f"분석 중 오류 발생: {e}")

def main():
    analyze_target_path = './test.exe' # 가상환경에서 테스트할 파일의 경로
    vm_name = 'WinDev2311Eval' # 가상머신 이름 (맨 위의 전역변수도 변경 필요)
    targe_file_name = 'test.exe'
    argument = ''
    timeout = 15 
    snapshot_name = "initsnapshot" # 가상환경에 생성되어있는 스냅샷 이름
    # 가상환경 sysmon 결과 파일 경로
    v_file = "..\\..\\..\\Windows\\System32\\winevt\\Logs\\Microsoft-Windows-Sysmon%4Operational.evtx"
    r_file = 'C:\\Users\\ADMIN\\'+'sys_'+targe_file_name+'.evtx' # 출력된 파일 저장 경로

    try:
        start_analyze(vm_name, targe_file_name, snapshot_name, argument, timeout, v_file, r_file)
        set_winlogbeat(targe_file_name,r_file)
    except Exception as e:
        print(f"자동 분석 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
