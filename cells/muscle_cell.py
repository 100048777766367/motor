import random
import json
import os

class MuscleCell:
    def __init__(self, muscle_id, storage_dir="synapses"):
        self.id = muscle_id
        self.storage_path = os.path.join(storage_dir, f"{self.id}.json")
        self.os_dir = storage_dir
        
        self.tone = 1.0       # Trương lực cơ (Độ căng)
        self.elasticity = 0.5 # Độ đàn hồi
        
        self.load_self()

    def load_self(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                self.tone = data.get("tone", 1.0)
                self.elasticity = data.get("elasticity", 0.5)
                return
            except Exception:
                pass

        # TỰ KHỞI SINH: Tạo độ trương lực cơ ngẫu nhiên
        self.tone = random.uniform(0.8, 1.5)
        self.elasticity = random.uniform(0.3, 0.7)
        self.save_self()

    # CO CƠ SINH LỰC: Lực = Xung thần kinh * Trương lực cơ * Độ đàn hồi
    def contract(self, neural_pulse):
        force = neural_pulse * self.tone * self.elasticity
        return round(max(0.0, force), 4)

    # ĐIỀU CHỈNH CƠ HỌC (Tự tăng cơ bắp khi hoạt động nhiều)
    def adapt(self, performance_feedback, lr=0.05):
        self.tone += lr * performance_feedback
        self.tone = max(0.2, min(3.0, self.tone)) # Giới hạn an toàn sinh học
        self.save_self()

    def save_self(self):
        os.makedirs(self.os_dir, exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump({"tone": round(self.tone, 4), "elasticity": round(self.elasticity, 4)}, f, indent=4)
