import yaml
import subprocess
WINLOGBEAT_YML_FILE_PATH = r'C:\Program Files\Winlogbeat\winlogbeat.yml'
def start_winlogbeat():
    # winlogbeat의 초기 설정 완료하고  가정
    subprocess.Popen(["powershell.exe","Restart-Service winlogbeat"])

def set_winlogbeat(file_name:str,evtx_file_path):
    with open(WINLOGBEAT_YML_FILE_PATH,'r') as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
        config['output.elasticsearch']['index'] = r'winlogbeat-%{[agent.version]}-%{+yyyy.MM.dd}-' + file_name
        config['winlogbeat.event_logs'][0]['name'] = evtx_file_path
        with open(WINLOGBEAT_YML_FILE_PATH,'w') as a:
            yaml.dump(config,a)
