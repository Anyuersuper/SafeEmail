import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr

# QQ邮箱配置
EMAIL = "15@qq.com"
PASSWORD = "jjjj"
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
            if content_type in ["text/plain", "text/html"] and "attachment" not in content_dispo:
                payload = part.get_payload(decode=True)
                if payload:
                    try:
                        return payload.decode(part.get_content_charset() or "utf-8", errors="ignore")
                    except:
                        return payload.decode("utf-8", errors="ignore")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode("utf-8", errors="ignore")
    return "(无正文内容)"

def fetch_emails_by_sender_and_recipient(sender_email, recipient_email, latest_count=50):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)

        status, count_data = mail.select("inbox")
        mail.noop()  # 刷新邮件列表，确保是最新状态


        status, count_data = mail.select("inbox")
        message_count = int(count_data[0])
        start_index = max(1, message_count - latest_count + 1)

        for seq_num in range(message_count, start_index - 1, -1):  # 从最新往前
            result, msg_data = mail.fetch(str(seq_num), "(RFC822)")
            if result != 'OK' or not msg_data or not msg_data[0]:
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            actual_from = parseaddr(msg["From"])[1]
            actual_to = parseaddr(msg["To"])[1]

            if sender_email.lower() == actual_from.lower() and recipient_email.lower() == actual_to.lower():
                return [{
                    "id": str(seq_num),
                    "subject": clean_subject(msg["Subject"]),
                    "from": msg["From"],
                    "to": msg["To"],
                    "date": msg["Date"],
                    "body": get_body(msg)
                }]

        return []  # 没有找到匹配邮件

    except Exception as e:
        print(f"发生错误：{str(e)}")
        return None
    finally:
        try:
            mail.logout()
        except:
            pass

if __name__ == "__main__":
    result = fetch_emails_by_sender_and_recipient("no-reply@cursor.sh", "adasdas@anyuer.club", 4)
    if result and len(result) > 0:
        print(len(result))
    else:
        print("没有找到邮件")
