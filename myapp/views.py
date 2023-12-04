from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'index.html')

def signup(request):
    

    return render(request, 'signup.html')

def login(request):
	return render(request, 'login.html')

def home(request):
	return render(request, 'home.html')

def profile(request):
	return render(request, 'profile.html')

def affiliatecode(request):
	return render(request, 'affiliatecode.html')

def packages(request):
	return render(request, 'packages.html')

def earnings(request):
	return render(request, 'earnings.html')

def withdraw(request):
	return render(request, 'withdraw.html')

def withdraw(request):
	return render(request, 'withdraw.html')

def success(request):
	return render(request, 'success.html')

def confirmdetail(request):
	return render(request, 'confirmdetail.html')

def newpassword(request):
	return render(request, 'newpassword.html')