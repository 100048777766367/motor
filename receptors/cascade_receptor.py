import os
import subprocess

OWNER = os.environ.get("REPO_OWNER", "")
PARENT = os.environ.get("REPO_PARENT", "")
UPSTREAM_SEED = "100048777766367"

TARGET_FILE = "synapse_command.json"

def try_fetch(target_owner):
    if not target_owner: return False
    url = f"https://raw.githubusercontent.com/{target_owner}/neuron/main/synapse_backward.json"
    print(f"📡 [XÚC TU CƠ BẮP] Đang dò tìm lệnh Não tại: {target_owner}/neuron...")
    res = subprocess.run(["curl", "-s", "-f", url, "-o", TARGET_FILE], capture_output=True)
    if res.returncode == 0 and os.path.exists(TARGET_FILE):
        print(f"🎯 [BẮT ĐƯỢC LỆNH] Đã nhận được xung lệnh từ Bộ Não của {target_owner}!")
        return True
    return False

def main():
    if OWNER and try_fetch(OWNER): return
    if PARENT and try_fetch(PARENT): return
    if try_fetch(UPSTREAM_SEED): return
    print("🍃 [MÔI TRƯỜNG TĨNH] Cơ bắp chưa nhận được lệnh mới, duy trì phản xạ tĩnh.")

if __name__ == "__main__":
    main()
