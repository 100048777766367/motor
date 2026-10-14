import os
import json
import urllib.request

TARGET_FILE = "synapse_command.json"
TOPIC_KEYWORD = "bodhi-synapse"

def search_global_brain():
    if os.path.exists(TARGET_FILE): return
    print(f"📡 [ANTEN CƠ BẮP] Quét sóng tìm Bộ Não điều khiển toàn cầu (#{TOPIC_KEYWORD})...")
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"User-Agent": "Bodhi-Motor-Effector"}
    if token: headers["Authorization"] = f"Bearer {token}"

    api_url = f"https://api.github.com/search/repositories?q=topic:{TOPIC_KEYWORD}&sort=updated&order=desc"
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            items = json.loads(response.read().decode()).get("items", [])

        for repo in items:
            raw_url = f"https://raw.githubusercontent.com/{repo['full_name']}/main/synapse_backward.json"
            try:
                raw_req = urllib.request.Request(raw_url, headers=headers)
                with urllib.request.urlopen(raw_req, timeout=5) as raw_resp:
                    content = raw_resp.read().decode()
                    with open(TARGET_FILE, "w") as f: f.write(content)
                    print(f"🎉 [KẾT NỐI TOÀN CẦU] Cơ bắp đã bắt được lệnh từ: {repo['full_name']}!")
                    return
            except Exception: continue
    except Exception as e:
        print(f"🍃 [ANTEN TĨNH] Không tìm thấy lệnh toàn cầu: {e}")

if __name__ == "__main__":
    search_global_brain()
