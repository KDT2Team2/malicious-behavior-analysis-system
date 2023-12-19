import requests
import json
import os
from urllib.parse import unquote

AGENT_URL = 'http://localhost:5000'

def get_request():
    response = requests.get(f'{AGENT_URL}/')
    print("GET Response:")
    print(response.text)

def post_command(command):
    data = {'command': command}
    headers = {'Content-type': 'application/json'}
    response = requests.post(f'{AGENT_URL}/command', data=json.dumps(data), headers=headers)
    print("\nPOST Response:")
    print(response.json())
    
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


if __name__ == '__main__':
    get_request()
    # 보낼 파일 이름
    # upload_file("test.exe")
    # 가상환경 파일이름, 저장할 주소

    # download_file("Microsoft-Windows-Sysmon%4Operational.evtx", 'C:/Users/dealu/OneDrive/바탕 화면/프로젝트/project 2-2/test/test.evtx')
    download_file("..\\..\\..\\..\\..\\..\\Windows\\System32\\winevt\\Logs\\Microsoft-Windows-Sysmon%4Operational.evtx", 'C:/Users/dealu/OneDrive/바탕 화면/프로젝트/project 2-2/test/te222st.evtx')
