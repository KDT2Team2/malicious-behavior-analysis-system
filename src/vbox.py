import subprocess

# 가상머신 상태 확인
def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# 가상머신 시작
def start_vm(vm_name: str) -> bool:
    return run_command(["VBoxManage", "startvm", vm_name, "--type", "headless"])

# 가상머신 중지
def stop_vm(vm_name: str) -> bool:
    return run_command(["VBoxManage", "controlvm", vm_name, "poweroff"])

# 가상머신 목록
def list_vm() -> list:
    result = subprocess.run(["VBoxManage", "list", "vms"], capture_output=True, text=True)
    if result.returncode == 0:
        return [line.split('"')[1] for line in result.stdout.splitlines()]
    else:
        return []

# 가상머신 스냅샷 생성
def snapshot_vm(vm_name: str, snapshot_name: str) -> bool:
    return run_command(["VBoxManage", "snapshot", vm_name, "take", snapshot_name])

# 가상머신 스냅샷 롤백
def rollback_vm(vm_name: str, snapshot_name: str) -> bool:
    return run_command(["VBoxManage", "snapshot", vm_name, "restore", snapshot_name])

def main():
    action = input("Command (start, stop, list, snapshot, rollback, exit): ").strip().lower()

    if action == "exit":
        return
    elif action in ["start", "stop", "snapshot", "rollback"]:
        vm_name = input("VM Name: ").strip()
        if action in ["snapshot", "rollback"]:
            snapshot_name = input("Enter the name of the snapshot: ").strip()
            success = snapshot_vm(vm_name, snapshot_name) if action == "snapshot" else rollback_vm(vm_name, snapshot_name)
        else:
            success = start_vm(vm_name) if action == "start" else stop_vm(vm_name)
        print("Success" if success else "Failed")
    elif action == "list":
        vms = list_vm()
        print("\n".join(vms) if vms else "No virtual machine")
    else:
        print("Unknown action.")

if __name__ == "__main__":
    main()
