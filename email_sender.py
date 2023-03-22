import smtplib as smtp

login = 'schoolchat.024@gmail.com'
password = 'pmykcpwjjplumrem'

server = smtp.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(login, password)

subject = 'main theme'
text = 'text of letter'

server.sendmail(login, 'test@email.com', f'Subject:{subject}\n{text}')
