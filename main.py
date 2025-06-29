from flask import Flask, render_template, request, jsonify
from find import fetch_emails_by_sender_and_recipient

app = Flask(__name__)

def load_safe_senders():
    try:
        with open('config.info', 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            return [line.strip() for line in lines if line.strip()]
    except Exception as e:
        print('读取配置文件失败:', e)
        return []

SAFE_SENDERS = load_safe_senders()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_safe_senders')
def get_safe_senders():
    return jsonify(SAFE_SENDERS)

@app.route('/ymail', methods=['POST'])
def ymail():
    data = request.get_json()
    sender = data.get("sender")
    recipient = data.get("recipient")

    if not sender or not recipient:
        return "参数不完整", 400

    if sender not in SAFE_SENDERS:
        return "非法发件人", 403
    
    result = fetch_emails_by_sender_and_recipient(sender, recipient, 50)
    if result:
        email_data = result[0]
        if isinstance(email_data, dict) and 'body' in email_data:
            email_data['body'] = email_data['body'].replace('\r\n', '\n')
        return jsonify(email_data)
    else:
        return "没有找到邮件"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9838)
