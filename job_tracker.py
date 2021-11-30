import requests
import json
import smtplib, ssl

def send_email(message):
    port = 465
    smtp_server = 'smtp.gmail.com'
    sender_email = 'pythonscript@gmail.com'
    #Here you type your email and password
    receiver_email = ''
    password = ''

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        try:
            server.login(sender_email, password)
            res = server.sendmail(sender_email, receiver_email, message)
            print('email sent!')
        except:
            print('could not login or send the mail.')


URL = "https://remoteok.io/api"
keys = ['date', 'company', 'position', 'tags','location', 'url']

wanted_tags = ["python", "entry", "web"]

def get_jobs():
    response = requests.get(URL)
    job_results = response.json()

    jobs = []
    for job_res in job_results:
        job = {k: v for k, v in job_res.items() if k in keys}

        if job:
            tags = job.get('tags')
            tags = {tag.lower() for tag in tags}
            if tags.intersection(wanted_tags):
                jobs.append(job)
    return jobs

if __name__ == '__main__':
    python_jobs = get_jobs()

    if python_jobs:
        message = "Subject: Remote Python Jobs!\n\n"
        message += "Found some cool Python jobs!\n\n"

        for job in python_jobs:
            message += f"{json.dumps(job)}\n\n"
        
        send_email(message)