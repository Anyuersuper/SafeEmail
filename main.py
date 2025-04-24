from find import fetch_emails_by_sender_and_recipient
from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/safeemail/')
def index():
    return render_template('index.html')


@app.route('/safeemail/ymail/<emailaddr>', methods=['GET'])
def ymail(emailaddr):
    result = fetch_emails_by_sender_and_recipient("no-reply@cursor.sh", emailaddr, 50)
    if len(result) > 0:
        # 直接处理字典数据
        email_data = result[0]
        print(email_data)
        if isinstance(email_data, dict) and 'body' in email_data:
            email_data['body'] = email_data['body'].replace('\r\n', '\n')
        return jsonify(email_data)
    else:
        return "没有找到邮件"
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9838)
    