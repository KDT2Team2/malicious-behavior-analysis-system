from vbox import *

def uploadfile_to_vm(vm_name:str, local_path:str, remote_path:str):
    # 구현
    pass

def exec_remote_path(vm_name:str, remote_path:str, argument:str, timeout:int):
    # 구현
    pass

def exec_event_export(vm_name:str):
    # 구현
    pass

def download_remote_file(vm_name:str, remote_path:str, local_path:str):
    # 구현
    pass

def connect_db(db_address:str):
    # 구현
    pass

def close_db(db_handle):
    # 구현
    pass

def upload_to_db(csv_path:str, index_name:str, db_handle):
    # 구현
    pass

def start_analyze(vm_name:str, file_path:str, argument:str, timeout:int):
    # 가상머신 시작
    start_vm(vm_name)
    # 분석대상 파일을 Real 머신에서 가상머신으로 업로드
    remote_path = 'c:\\target.exe'
    uploadfile_to_vm(vm_name, file_path, remote_path)
    
    # 업로드 분석대상 파일 실행
    exec_remote_path(vm_name, remote_path, argument, timeout)
    
    # Windows Sysmon 실행결과 이벤트 로그를 csv로 export(가상머신 내부에 결과 생성)
    exec_event_export(vm_name)
    
    # 가상머신 내부에 존재하는 이벤트 로그 csv 파일을 Real머신 환경으로 다운로드
    download_remote_file(vm_name, <REMOTE_EVENT_CSV_PATH>, <LOCAL_CSV_PATH>)
    
    # 가상머신 중지 및 원래 상태로 rollback
    stop_vm(vm_name)
    rollback_vm(vm_name, <SNAPSHOT_NAME>)

    # 다운로드 받은 이벤트 로그를 이벤트 로그 저장소에 업로드
    db_handler = connect_db(<DATABASE_ADDRESS>)
    upload_to_db(<LOCAL_CSV_PATH>, <INDEXNAME>, db_handler)
    close_db(db_handler)

if __name__ == '__main__':
    analyze_target_path = './test.exe'
    vm_name = 'windows_10_sandbox'
    argument = ''
    timeout = 30
    start_analyze(vm_name, analyze_target_path, argument, timeout)
