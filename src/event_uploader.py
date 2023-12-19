import yaml
import subprocess
def start_winlogbeat():
    # winlogbeat의 초기 설정 완료하고  가정
    subprocess.Popen(["powershell.exe","Restart-Service winlogbeat"])

def set_winlogbeat(file_name:str,yml_file_path):
    with open(yml_file_path,'r') as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
        config['output.elasticsearch']['index'] = r'winlogbeat-%{[agent.version]}-%{+yyyy.MM.dd}-' + file_name
        with open(yml_file_path,'w') as a:
            yaml.dump(config,a)

if __name__ == "__main__":
    winlogbeat_yml = r'C:\Program Files\Winlogbeat\winlogbeat.yml'
    target_program_name = 'testfilename'
    set_winlogbeat(target_program_name, winlogbeat_yml)
    start_winlogbeat()