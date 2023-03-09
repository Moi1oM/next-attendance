from django.shortcuts import render
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os

# Create your views here.
def index(request):
    return render(request, 'index.html')

def spreadsheet(request):
    name = request.GET.get('username', None)
    tmi = request.GET.get('tmi', None)
    code = request.GET.get('code', None)
    current_time = str(datetime.now())
    data = [name,current_time, tmi, code]
    json_file_name = 'friend-alarm-dc2c393048ea.json'
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    print(os.getcwd())
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)
    gc1 = gc.open('NEXT 출석부')
    worksheet=gc1.worksheet('시트1')
    worksheet.append_row(data)
    
    return render(request, 'spreadsheet.html', {'name': name, 'tmi': tmi})