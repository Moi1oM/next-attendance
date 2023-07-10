from uuid import uuid4
import boto3
from django.shortcuts import render
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt

from attend_check.models import User
import os
import smtplib
from email.message import EmailMessage

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")

# Create your views here.
def index(request):
    return render(request, 'index.html')

def sendEmail(email, time):
    # STMP 서버의 url과 port 번호
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 465

    # 1. SMTP 서버 연결
    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

    EMAIL_ADDR = os.environ.get("MAIL_USER")
    EMAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    print(EMAIL_ADDR, EMAIL_PASSWORD)

    # 2. SMTP 서버에 로그인
    smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)

    # 3. MIME 형태의 이메일 메세지 작성
    message = EmailMessage()
    message.set_content(f'{time}에 알고리즘 스터디 인증 제출이 완료되었습니다. 앞으로도 열심히 해봅시다!')
    message["Subject"] = "알고리즘 스터디 인증 제출 완료"
    message["From"] = EMAIL_ADDR  # 보내는 사람의 이메일 계정
    message["To"] = email

    # 4. 서버로 메일 보내기
    smtp.send_message(message)

    # 5. 메일을 보내면 서버와의 연결 끊기
    smtp.quit()


@csrf_exempt
def spreadsheet(request):
    name = request.POST.get('username', None)
    tmi = request.POST.get('tmi', None)
    email = request.POST.get('email', None)
    get_file = request.FILES.get("get_file")
    current_time = str(datetime.now())

    data = [name,current_time, tmi, email, get_file]

    print(data, request)

    sendEmail(email, current_time)

    if get_file:
        uuid_name = uuid4()
        image_datetime = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        fileobj_key = name + "_" + image_datetime + "_" + str(uuid_name)

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        s3_client.upload_fileobj(
            get_file,
            AWS_STORAGE_BUCKET_NAME,
            fileobj_key,
            ExtraArgs={
                "ContentType": get_file.content_type,
            },
        )

        image_url = fileobj_key
        image_src = os.environ.get("AWS_BUCKET_URL") + image_url

        User.objects.create(
            email = email,
            name = name,
            tmi = tmi,
            time = current_time,
            url = image_src
        )
    
    return render(request, 'spreadsheet.html', {"name": name})