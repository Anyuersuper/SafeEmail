import imaplib
import email
from email.header import decode_header

# QQ邮箱配置
EMAIL = "1505637260@qq.com"
PASSWORD = "rkymkfuasfzibabj"
IMAP_SERVER = "imap.qq.com"

def clean_subject(subject):
    decoded, charset = decode_header(subject)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(charset or "utf-8")
    return decoded

def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_dispo = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_dispo:
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()

def fetch_emails_by_recipient(recipient_email):
    try:
        # 连接服务器
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        # 搜索发送给指定收件人的邮件
        search_criteria = f'(TO "{recipient_email}")'
        result, data = mail.search(None, search_criteria)
        email_ids = data[0].split()

        if not email_ids:
            print(f"\n❌ 没有找到发送给 {recipient_email} 的邮件")
            return

        print(f"\n📧 找到 {len(email_ids)} 封发送给 {recipient_email} 的邮件：")
        print("=" * 80)

        for eid in email_ids:
            result, msg_data = mail.fetch(eid, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = clean_subject(msg["Subject"])
            from_ = msg["From"]
            to_ = msg["To"]
            date = msg["Date"]
            body = get_body(msg)

            print(f"\n📨 邮件标题：{subject}")
            print(f"👤 发件人：{from_}")
            print(f"📬 收件人：{to_}")
            print(f"📅 发送时间：{date}")
            print(f"📄 内容：\n{body}")
            print("-" * 80)

    except Exception as e:
        print(f"\n❌ 发生错误：{str(e)}")
    finally:
        mail.logout()

def main():
    print("\n📧 QQ邮箱邮件获取工具")
    print("=" * 30)
    
    while True:
        recipient_email = input("\n请输入要查询的收件人邮箱地址（输入 'q' 退出）：")
        
        if recipient_email.lower() == 'q':
            print("\n👋 感谢使用，再见！")
            break
            
        if '@' not in recipient_email:
            print("\n❌ 请输入有效的邮箱地址！")
            continue
            
        fetch_emails_by_recipient(recipient_email)

if __name__ == "__main__":
    main()
