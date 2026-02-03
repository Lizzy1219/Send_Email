import smtplib, ssl
from getpass import getpass
from email.message import EmailMessage

# 建立SSL的上下文（因為憑證問題所以改成略過驗證）
context = ssl._create_unverified_context() 

# 輸入地址和密碼，密碼用getpass避免顯示在螢幕上外洩(所以打的時候沒有東西)
email_address = input("Email: ")
email_password = getpass("Password: ")

# 主旨和內容
subject = "Homework – Email API with Attachment"
body = "This email includes a test attachment sent via SMTP."

# 寄件人、收件人（同寄件人）、內文
msg = EmailMessage()
msg['subject'] = subject
msg['From'] = email_address
msg['To'] = email_address
msg.set_content(body)

# 指定檔案
filename = 'cat.JPG'
with open(filename, 'rb') as f:
    filedata = f.read() # 二進制開啟檔案，讀原始資料

# 把附件加進郵件（會自動轉Base64）
msg.add_attachment(filedata, maintype='image', subtype='jpeg', filename=filename)

# 連線！
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

    print('Email sent successfully with attachment!')
except smtplib.SMTPAuthenticationError:
    print("登入失敗！請確認 email 和 password 是否正確。")
except Exception as e:
    print(f"發送失敗：{e}！")
