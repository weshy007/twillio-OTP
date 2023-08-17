from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from twilio.rest import Client

from core import settings

account_sid = settings.ACCOUNT_SID
auth_token = settings.AUTH_TOKEN
verify_sid = settings.VERIFY_SID

client = Client(account_sid,auth_token)

# Create your views here.
def index(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        request.session['username'] = username
        request.session['password'] = password

        user = authenticate(request, username=username, password=password)

        if user is not None:
            return redirect('verify-number')
        else:
            return redirect('login')
        
    return render(request, 'login.html')


def verify_number(request):
    if request.method == 'POST':
        phone_no = request.POST.get('phone_no')
        return redirect('verify', phone_no=phone_no)
    
    return render(request, 'verify_number.html')


def verify(request, phone_no):
    if request.method == 'POST':
        code = request.POST.get('code')
        verification_check = client.verify.services(verify_sid).verification_checks.create(to=f"+254{phone_no}", code=code)

        if verification_check.status == 'approved':
            user = authenticate(request, username=request.session.get('username'), password=request.session.get('password'))

            login(request, user)

            return redirect('index')
        
        else:
            return redirect('login')
    
    verification = client.verify.services(verify_sid).verifications.create(to=f"+254{phone_no}",channel='call')
    
    return render(request, 'verify.html')