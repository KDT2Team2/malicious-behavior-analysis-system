import requests
import json
import os
from urllib.parse import unquote
import subprocess
import time
import sys

AGENT_URL = 'http://localhost:8080'

def get_request():
    response = requests.get(f'{AGENT_URL}/')
    print("GET Response:")
    print(response.text)

def post_command(command, timeout=15):
    data = {'command': command}
    headers = {'Content-type': 'application/json'}
    response = requests.post(f'{AGENT_URL}/command', data=json.dumps(data), headers=headers)
    print("\nPOST Response:")
    print(response.json())

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f'{AGENT_URL}/status')
            status = response.json().get('status')
            if status == 'completed':
                print(f"{command} completed successfully.")
                break
            elif status == 'failed':
                print(f"{command} failed.")
                break
            time.sleep(1)
        except Exception as e:
            print(f"Error checking status: {e}")
            break
    else:
        print(f"{command} did not complete within the specified timeout. Terminating the process.")
        try:
            response = requests.post(f'{AGENT_URL}/terminate')
            print("Process terminated.")
        except Exception as e:
            print(f"Error terminating process: {e}")
    
def upload_file(file_path):
    file_name = os.path.basename(file_path)
    headers = {'X-File-Name': file_name}
    with open(file_path, 'rb') as file:
        response = requests.post(f'{AGENT_URL}/upload', headers=headers, data=file.read())
    print("\nUpload Response:")
    print(response.text)

def download_file(file_name, save_path):
    response = requests.get(f'{AGENT_URL}/download/{file_name}', stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("\nDownload Complete")
    else:
        print(f"\nDownload Failed. Status Code: {response.status_code}, Response Text: {response.text}")

def run_sysmon():
    sysmon_path = 'Sysmon.exe'
    command = f'"{sysmon_path}"'

    # 현재 스크립트를 관리자 권한으로 다시 실행
    if sys.platform == 'win32' and 'admin' in os.environ.get('USERNAME', '').lower():
        subprocess.Popen(command, shell=True)
        print("Sysmon이 실행되었습니다.")
    else:
        try:
            # 현재 스크립트를 관리자 권한으로 다시 실행
            params = f'{sys.executable} {os.path.realpath(__file__)}'
            subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
            print("Sysmon이 다시 실행되었습니다.")
        except Exception as e:
            print(f"관리자 권한으로 다시 실행하는 동안 오류 발생: {e}")

if __name__ == '__main__':
    get_request()
    file_to_execute = input("실행할 파일의 이름을 입력하세요: ")
    upload_file(file_to_execute)
    post_command(file_to_execute) 
