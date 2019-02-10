import urllib
import hashlib
import smtplib
import os

page = urllib.urlopen('<url>')
hasher = hashlib.md5()
buf = page.read()
hasher.update(buf)
obj = open('gradeHash.txt', 'r')
if obj.read() != hasher.hexdigest():
 msg = "\r\n".join([
 "From: <email>",
 "To: <email>",
 "Subject: Math Grades updated!",
 "",
 ])
 smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
 smtpObj.ehlo()
 smtpObj.starttls()
 smtpObj.login("<email>", "<password>")
 smtpObj.sendmail('<email>','<email>',msg)
 smtpObj.quit()
 print('mismatch!')
obj = open('gradeHash.txt', 'w+')
obj.write(hasher.hexdigest())
obj.close
print(hasher.hexdigest())
