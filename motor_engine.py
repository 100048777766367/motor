import json
import time
import os
from cells.muscle_cell import MuscleCell

class MotorEngine:
    def __init__(self):
        # Cặp cơ đối vận kinh điển trong sinh học: Cơ Co (Flexor) & Cơ Duỗi (Extensor)
        self.flexor = MuscleCell("m_flexor")
        self.extensor = MuscleCell("m_extensor")

    def execute_action(self, verified_command_file="verified_command.json"):
        # Mặc định xung kích hoạt thần kinh là [0.5, 0.5] nếu chưa nhận được lệnh
        pulse = [0.5, 0.5]
        timestamp = int(time.time())

        if os.path.exists(verified_command_file):
            try:
                with open(verified_command_file, "r") as f:
                    data = json.load(f)
                pulse = data.get("command_pulse", [0.5, 0.5])
                timestamp = data.get("timestamp", timestamp)
                print(f"⚡ [XUNG THẦN KINH VẬN ĐỘNG] Nhận lệnh từ Não: {pulse}")
            except Exception as e:
                print(f"⚠️ Đọc lệnh thất bại, dùng phản xạ tự nhiên: {e}")

        # Tế bào cơ co và cơ duỗi phát lực
        force_left = self.flexor.contract(pulse[0])
        force_right = self.extensor.contract(pulse[1])

        # Tổng hợp lực động học (Net Movement)
        displacement_x = round(force_right - force_left, 4)
        net_power = round(force_left + force_right, 4)

        if displacement_x > 0.1:
            decision = "DODGE_RIGHT (NÉ SANG PHẢI)"
        elif displacement_x < -0.1:
            decision = "DODGE_LEFT (NÉ SANG TRÁI)"
        else:
            decision = "HOLD_POSITION (GIỮ VỮNG VỊ TRÍ)"

        # ĐÓNG GÓI VECTOR HÀNH ĐỘNG THỰC TẾ RA THẾ GIỚI
        action_packet = {
            "contract": "bodhi.action.v1",
            "source": "motor_effector",
            "timestamp": timestamp,
            "action": {
                "decision": decision,
                "vector_displacement": [displacement_x, 0.0],
                "net_power": net_power
            }
        }

        with open("motor_action.json", "w") as f:
            json.dump(action_packet, f, indent=4)

        print("-" * 50)
        print(f"🦾 [CƠ BẮP PHÁT LỰC] Hành động: {decision}")
        print(f"   Độ lệch tọa độ: dx = {displacement_x} | Tổng lực phát ra: {net_power} N")
        print("-" * 50)
        return action_packet

if __name__ == "__main__":
    engine = MotorEngine()
    engine.execute_action()
