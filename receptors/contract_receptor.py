import json
import os

RAW_SIGNAL = "synapse_command.json"
VERIFIED_SIGNAL = "verified_command.json"

def verify_and_purify():
    if not os.path.exists(RAW_SIGNAL): return False
    try:
        with open(RAW_SIGNAL, "r") as f:
            data = json.load(f)

        # Lấy xung kích hoạt (từ trường gradients hoặc features)
        pulse = data.get("gradients_for_eye", data.get("features", [0.5, 0.5]))
        clean_pulse = [max(0.0, min(1.0, abs(float(p)))) for p in pulse[:2]]

        purified_packet = {
            "contract": "bodhi.motor.command.v1",
            "timestamp": data.get("timestamp", data.get("reply_to_timestamp", 0)),
            "command_pulse": clean_pulse
        }

        with open(VERIFIED_SIGNAL, "w") as f:
            json.dump(purified_packet, f, indent=4)

        print(f"🛡️ [KIỂM DỊCH LỆNH AN TOÀN] Xung kích thích cơ bắp: {clean_pulse}")
        return True
    except Exception as e:
        print(f"⚠️ [LỆNH HỎNG]: {e}")
        return False

if __name__ == "__main__":
    verify_and_purify()
