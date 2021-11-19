def sendMailSeveralAttachment(Subject, toaddr, path, file,header, body_text, path2, file2):
    fromaddr = "your_service_account@your_domain.com"
    msg = FormatNewMailWithoutDataframe(header,body_text)
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)      

    msg['Subject'] = Subject
    mail_file = MIMEBase('application', 'csv')
    mail_file.set_payload(open(path + file, 'rb').read())
    mail_file.add_header('Content-Disposition', 'attachment', filename=file)
    encoders.encode_base64(mail_file)
    msg.attach(mail_file)
    
    
    mail_file2 = MIMEBase('application', 'csv')
    mail_file2.set_payload(open(path2 + file2, 'rb').read())
    mail_file2.add_header('Content-Disposition', 'attachment', filename=file2)
    encoders.encode_base64(mail_file2)
    msg.attach(mail_file2)
    
    
    server = smtplib.SMTP(SMTPServer, <your_server_port>)
    server.login(SMTPUser, SMTPPwd)
    server.sendmail(fromaddr, toaddr, msg.as_string())