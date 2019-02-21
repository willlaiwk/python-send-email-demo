from pathlib import Path
from smtplib import SMTP_SSL, SMTPException
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 定義變數
host = "imap.gmail.com"
port = 465
user = "will.coding.test@gmail.com"
password = ""
from_addr = "will.coding.test@gmail.com"
to_addrs = ["will.coding.test@gmail.com", "will.lai.wk@gmail.com"]

# 建立 message 實體
# 使用 MIMEMultipart("alternative"): 當收件人的軟體不支援 HTML 時，才顯示 context_plain。
# 直接打 MIMEMultipart(): context_plain 與 context_html 都會同時顯示。
message = MIMEMultipart()
# message = MIMEMultipart("alternative")

# 郵件標頭
message['From'] = Header("科技時代", "utf-8")
message['To'] = ",".join(to_addrs)
# ? 用 Header(",".join(to_addrs), "utf-8")，收件人會不見，會出現在密件副本，不知道為啥？
# message['To'] = Header(",".join(to_addrs), "utf-8")
message['Subject'] = Header("測試主旨", 'utf-8')

# 郵件內容主體
# 圖片路徑 cid:{id} 會對應到附加檔案的 add_header('Content-ID', '<{}>'.format(file.name))，若引用就不會出現在附加檔案了
context_plain = "這是「科技時代」用 Python 發的純文字內文。"
context_html = """
<h3>這是<i>「科技時代」</i>用 Python 發的 HTML 內文。</h3>
<a href="www.google.com">Google 連結</a>
<br />
<br />
<h4>底下顯示貓咪1的圖</h4>
<img src="cid:cat1.jpg" alt="cat1" />
<br />
<p>附件為貓咪2的圖與 sample.pdf</p>
"""
message.attach(MIMEText(context_plain, "plain", "utf-8"))
message.attach(MIMEText(context_html, "html", "utf-8"))

# 附加檔案
attachments = [
  "files/cat1.jpg",
  "files/cat2.jpg",
  "files/sample.pdf"
]
for attachment in attachments:
  file = Path(attachment)
  with open(file, 'rb') as fp:
    msg = MIMEBase("application", "octet-stream")
    msg.set_payload(fp.read())
  encoders.encode_base64(msg)
  msg.add_header('Content-Disposition', 'attachment', filename=file.name)
  # 加上 Content-ID 可在 HTML 中引用附檔
  msg.add_header('Content-ID', '<{}>'.format(file.name))
  message.attach(msg)

# 發送郵件
try:
  conn_smtp = SMTP_SSL(host, port)
  conn_smtp.login(user, password)
  conn_smtp.sendmail(from_addr, to_addrs, message.as_string())
  conn_smtp.quit()
  print("郵件發送成功。")
except SMTPException:
  print("Error: 郵件發送失敗...")
