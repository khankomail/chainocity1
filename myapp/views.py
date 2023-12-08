from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model,authenticate, login,logout
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from .models import ChainUser,Product,Payment,Receipt
from django.db import IntegrityError
from django.utils import timezone
import hashlib
from datetime import datetime, timedelta
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
# JAZZCASH_MERCHANT_ID = config('JAZZCASH_MERCHANT_ID')
# JAZZCASH_PASSWORD = config('JAZZCASH_PASSWORD')
# JAZZCASH_INTEGERITY_SALT = config('JAZZCASH_INTEGERITY_SALT')
# JAZZCASH_HTTP_POST_URL =config ('JAZZCASH_HTTP_POST_URL')

# Create your views here.
def index(request):
	return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not (username and email and dob and password and confirm_password):
            messages.error(request, 'Please fill in all fields.')
            return redirect('signup')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        # Create a new user
        User = get_user_model()
        try:
            new_user = User(
                username=username,
                email=email,
                dob=dob,
                password=make_password(password),
            )
            new_user.save()
            messages.success(request, 'Signup successful. Please login.')
            return redirect('login')
        except IntegrityError as e:
            if 'UNIQUE constraint failed: myapp_chainuser.username' in str(e):
                messages.error(request, 'Username already exists. Please choose a different username.')
            elif 'UNIQUE constraint failed: myapp_chainuser.email' in str(e):
                messages.error(request, 'Email address already exists. Please use a different email.')
            else:
                messages.error(request, f'Error creating user: {str(e)}')
            return redirect('signup')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            id_string = user.id_string  # Replace with the actual attribute name
            return redirect('home', id_string=id_string)
        else:
            messages.error(request, 'Invalid email/username or password. Please try again.')

    return render(request, 'login.html')

def home(request, id_string):
    # Query the user model using id_string
    user = get_object_or_404(get_user_model(), id_string=id_string)

    # Access user attributes
    username = user.username
    email = user.email
    dob = user.dob
    referral_code_own = user.referral_code_own
    referral_code_other = user.referral_code_other
    earning = user.earning
    package = user.package
    referral_code_users = user.referral_code_users

    # Query code_users count
    code_users = get_user_model().objects.filter(referral_code_other=user.referral_code_own).count()
    remaining_users = 10 - code_users

    # Query all products
    products = Product.objects.all()

    return render(request, 'home.html', {
        'id_string': id_string,
        'username': username,
        'email': email,
        'dob': dob,
        'referral_code_own': referral_code_own,
        'referral_code_other': referral_code_other,
        'earning': earning,
        'package': package,
        'referral_code_users': referral_code_users,
        'code_users': code_users,  # Add code_users to the context
        'products': products,
        'remaining_users': remaining_users,
    })

def profile(request, id_string):
    # Query the user model using user_id
    user = get_object_or_404(get_user_model(), id_string=id_string)

    # Access user attributes
    username = user.username
    email = user.email
    dob = user.dob
    package = user.package
    # Add other attributes as needed

    return render(request, 'profile.html', {
        'id_string': id_string,
        'username': username,
        'email': email,
        'package': package,
        'dob': dob,
        # Add other attributes as needed
    })

def affiliatecode(request, id_string):
    # Query the user model using user_id
    user = get_object_or_404(get_user_model(), id_string=id_string)

    # Access user attributes
    username = user.username
    email = user.email
    dob = user.dob
    package = user.package
    referral_code_own = user.referral_code_own

    # Query users with the same referral_code_other as the current user's referral_code_own
    users = get_user_model().objects.filter(referral_code_other=request.user.referral_code_own)

    return render(request, 'affiliatecode.html', {
        'id_string': id_string,
        'username': username,
        'email': email,
        'package': package,
        'dob': dob,
        'referral_code_own': referral_code_own,
        'users': users,  # Pass the users variable to the template context
        
    })	

def packages(request, id_string):
    # Query the user model using user_id
    user = get_object_or_404(get_user_model(), id_string=id_string)

    # Access user attributes
    username = user.username
    email = user.email
    dob = user.dob
    package = user.package
    referral_code_users = user.referral_code_users.all()  # Use .all() to get all related users
   
    # Retrieve the current value of referral_code_other
    referral_code_other = user.referral_code_other

    if request.method == 'POST':
        new_referral_code_other = request.POST.get('referral_code_other')
        try:
            # Update referral_code_other only if a new value is provided
            if new_referral_code_other is not None:
                user.referral_code_other = new_referral_code_other
                user.save()
                # Redirect to the same page after saving
                return redirect('packages', id_string=id_string)
        except get_user_model().DoesNotExist:
            # Handle the case where the user with the given id_string doesn't exist
            pass

    return render(request, 'packages.html', {
        'id_string': id_string,
        'username': username,
        'email': email,
        'package': package,
        'dob': dob,
        'referral_code_users': referral_code_users,
        'referral_code_other': referral_code_other,
        # Add other attributes as needed
    })


	

def earnings(request, id_string):
    # Query the user model using user_id
    user = get_object_or_404(get_user_model(), id_string=id_string)
    username = user.username
    email = user.email
    dob = user.dob
    package = user.package
    referral_code_own = user.referral_code_own
    earning=user.earning

    users = get_user_model().objects.filter(referral_code_other=request.user.referral_code_own)

    # # Access user attributes
    # username = user.username
    # email = user.email
    # dob = user.dob
    # package = user.package
    # referral_code_own = user.referral_code_own
    # earning=user.earning
    # # Add other attributes as needed

    return render(request, 'earnings.html', {
        'id_string': id_string,
        'username': username,
        'email': email,
        'package': package,
        'dob': dob,
        'referral_code_own': referral_code_own,
        'earning' : earning,
        'users': users,
        # Add other attributes as needed
    })

# views.py



def withdraw(request, id_string):
    # Assuming your User model is the default User model provided by Django
    User = get_user_model()

    # Get the user based on the id_string parameter
    user = get_object_or_404(User, id_string=id_string)

    # Accessing user attributes
    user_id = user.id_string
    user_email = user.email
    user_package = user.package
    earning = user.earning

    # Check if the form is submitted
    if request.method == 'POST':
        # Access form data
        amount = request.POST.get('amount')
        acc_no = request.POST.get('acc_no')

        # Validate the form data (you may add more validation as needed)
        if not amount or not acc_no:
            messages.error(request, 'Please fill out all fields.')
        else:
            # Redirect to the receipt view with necessary parameters
            return redirect('receipt', user_id=user_id, amount=amount, acc_no=acc_no)

    # Render the 'withdraw.html' template with the user details
    return render(request, 'withdraw.html', {'user_id': user_id, 'user_email': user_email, 'user_package': user_package, 'earning': earning})



def receipt(request, user_id, amount, acc_no):
    # Assuming your User model is the default User model provided by Django
    User = get_user_model()

    # Get the user based on the user_id parameter
    user = get_object_or_404(User, id_string=user_id)

    # Accessing user attributes
    user_id = user.id_string
    user_email = user.email
    user_package = user.package
    earning = user.earning

    # Calculate remaining balance
    withdrawal_amount = float(amount)
    remaining_balance = earning - withdrawal_amount

    # Create a Receipt instance
    receipt = Receipt.objects.create(
        recipient=user.username,
        w_amount=withdrawal_amount,
        ave_balc=remaining_balance,
        acc_no=acc_no
    )

    return render(request, 'receipt.html', {'user_id': user_id, 'user_email': user_email, 'user_package': user_package, 'earning': earning, 'receipt': receipt})



@csrf_exempt
def success(request):
    if request.method == 'POST':
        # Check if required parameters are present in the POST request
        if all(param in request.POST for param in ['pp_Amount', 'pp_AuthCode', 'pp_ResponseCode', 'pp_MerchantID',
                                                    'pp_SecureHash', 'pp_TxnRefNo', 'pp_RetreivalReferenceNo']):
            try:
                # Get transaction information from POST data
                transaction_id = request.POST['pp_TxnRefNo']
                amount = request.POST['pp_Amount']
                auth_code = request.POST['pp_AuthCode']
                response_code = request.POST['pp_ResponseCode']
                response_message = request.POST['pp_ResponseMessage']
                merchant_id = request.POST['pp_MerchantID']
                secure_hash = request.POST['pp_SecureHash']
                retreival_reference_no = request.POST['pp_RetreivalReferenceNo']

                # Add period before the last two digits of amount
                amount = f"{amount[:-2]}.00"

                # Insert transaction data into the database
                if response_code == '000':
                    payment_status = 1
                else:
                    payment_status = 0

                message = response_message

                payment = Payment.objects.create(
                    transaction_id=transaction_id,
                    product_price=amount,
                    total=amount,
                    created_date=timezone.now(),
                    status=payment_status
                )

                payment_id = payment.id
                # Handle the rest of your logic here
                # ...

                return render(request, 'success.html', {'payment_id': payment_id, 'success': True, 'message':message})
            except Exception as e:
                return render(request, 'success.html', {'error_message': str(e), 'success': False})
        else:
            return render(request, 'success.html', {'error_message': 'Incomplete transaction data', 'success': False})
    else:
        return render(request, 'success.html', {'error_message': 'Invalid request method', 'success': False})

 
def checkout(request, plan):
    # Simulate the database query with package details
    if plan == 'gold':
        # Check user package (replace 'request.user.package' with actual code)
        if request.user.package == 'basic':
            package = {
                'name': 'gold',  # Replace with actual package name
                'price': 700.00  # Replace with actual package price
            }
        else:
            package = {
                'name': 'gold',  # Replace with actual package name
                'price': 1000.00  # Replace with actual package price
            }
    else:
        package = {
            'name': 'basic',  # Replace with actual package name
            'price': 300.00  # Replace with actual package price
        }

    # 1. Get formatted price (remove period from the price)
    temp_amount = int(package['price'] * 100)
    pp_Amount = str(temp_amount)

    # 2. Get the current date and time
    pp_TxnDateTime = datetime.now().strftime('%Y%m%d%H%M%S')

    # 3. Make expiry date and time (add one hour to the current date and time)
    pp_TxnExpiryDateTime = (datetime.now() + timedelta(hours=1)).strftime('%Y%m%d%H%M%S')

    # 4. Make a unique transaction id using the current date
    pp_TxnRefNo = 'T' + pp_TxnDateTime

    # Create the post_data dictionary
    post_data = {
        "pp_Version": "1.1",
        "pp_TxnType": "MWALLET",
        "pp_Language": "EN",
        "pp_MerchantID": 'MC62624',
        "pp_Password": '9b9e2w8zg7',
        "pp_BankID": "TBANK",
        "pp_ProductID": "RETL",
        "pp_TxnRefNo": pp_TxnRefNo,
        "pp_Amount": pp_Amount,
        "pp_TxnCurrency": "PKR",
        "pp_TxnDateTime": pp_TxnDateTime,
        "pp_BillReference": "billRef",
        "pp_Description": "Description of transaction",
        "pp_TxnExpiryDateTime": pp_TxnExpiryDateTime,
        "pp_ReturnURL": "http://127.0.0.1:8000/success",
        "pp_SecureHash": "pp_SecureHash",
        "ppmpf_1": "1",
        "ppmpf_2": "2",
        "ppmpf_3": "3",
        "ppmpf_4": "4",
        "ppmpf_5": "5",
    }

    # 5. Create an alphabetically ordered string and skip blank fields
    sorted_string = '39y8s6y9w1' + '&'.join(f"{k}={v}" for k, v in post_data.items() if v)

    # Sha256 hash encoding
    pp_SecureHash = hashlib.sha256(sorted_string.encode()).hexdigest()

    # Add the secure hash to the post_data dictionary
    post_data['pp_SecureHash'] = pp_SecureHash

    # Insert post_data into the database for validating secure hash if needed

    # Render the checkout.html template with the post_data
    return render(request, 'checkout.html', {'post_data': post_data, 'package': package, 'JAZZCASH_HTTP_POST_URL':'https://sandbox.jazzcash.com.pk/CustomerPortal/transactionmanagement/merchantform/'})


def confirmdetail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        dob = request.POST.get('dob')

        try:
            user = get_user_model().objects.get(email=email, dob=dob )
            id_string = user.id_string

            return redirect('newpassword', id_string=id_string)
        except get_user_model().DoesNotExist:
            messages.error(request, 'Invalid Email or date of birth. Please try again.')

    return render(request, 'confirmdetail.html')
	

def newpassword(request, id_string):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            try:
                user = get_user_model().objects.get(id_string=id_string)
                user.set_password(new_password)
                user.save()

                messages.success(request, 'Password updated successfully. You can now log in with your new password.')
                return redirect('login')
            except get_user_model().DoesNotExist:
                messages.error(request, 'User not found.')
        else:
            messages.error(request, 'Passwords do not match. Please try again.')

    return render(request, 'newpassword.html', {'id_string': id_string})


def logout_view(request):
    logout(request)
    return redirect('login')




def basic(request, id_string):
    # Find the user using the id_string
    user = get_object_or_404(ChainUser, id_string=id_string)

    # Set the user's package to 'basic'
    user.package = 'basic'

    # Fixed amount for the basic package
    amount = 300

    # Initialize earnings variables
    user_earning = 0
    referrer_earning = 0
    referrer_of_referrer_earning = 0

    # Calculate earnings for the current user
    if user.referral_code_other:
        # Find the user with the referral_code_other
        referrer = ChainUser.objects.filter(referral_code_own=user.referral_code_other).first()
        if referrer:
            # Referrer found, calculate earnings
            user_earning = amount * 0
            referrer_earning = amount * 0.50

            # Update the user's earning attribute
            user.earning += user_earning
            referrer.earning += referrer_earning
            referrer.save()

            # Continue the loop for the referrer of referrer
            referrer_of_referrer = None
            if referrer.referral_code_other:
                # Find the user with the referral_code_other of referrer
                referrer_of_referrer = ChainUser.objects.filter(referral_code_own=referrer.referral_code_other).first()
                if referrer_of_referrer:
                    # Referrer of referrer found, calculate earnings
                    referrer_of_referrer_earning = amount * 0.15
                    referrer_of_referrer.earning += referrer_of_referrer_earning
                    referrer_of_referrer.save()

                    # One more iteration for referrer of referrer's referrer
                    referrer_of_referrer_of_referrer = None
                    if referrer_of_referrer.referral_code_other:
                        # Find the user with the referral_code_other of referrer of referrer
                        referrer_of_referrer_of_referrer = ChainUser.objects.filter(
                            referral_code_own=referrer_of_referrer.referral_code_other
                        ).first()
                        if referrer_of_referrer_of_referrer:
                            # Referrer of referrer of referrer found, calculate earnings
                            referrer_of_referrer_of_referrer_earning = amount * 0.10
                            referrer_of_referrer_of_referrer.earning += referrer_of_referrer_of_referrer_earning
                            referrer_of_referrer_of_referrer.save()

    user.save()

    return render(request, 'basic.html', {
        'user': user,
        'amount': amount,
        'user_earning': user_earning,
        'referrer_earning': referrer_earning,
        'referrer_of_referrer_earning': referrer_of_referrer_earning if referrer_of_referrer else 0,
        'referrer_of_referrer_of_referrer_earning': referrer_of_referrer_of_referrer_earning
        if referrer_of_referrer_of_referrer
        else 0,
        'package': 'basic',
    })


def gold(request, id_string):
    # Find the user using the id_string
    user = get_object_or_404(ChainUser, id_string=id_string)

    # Check if the user's package is 'basic' and update the amount
    if user.package == 'basic':
        amount = 700
    else:
        amount = 1000

    # Set the user's package to 'gold'
    user.package = 'gold'

    # Initialize earnings variables
    user_earning = 0
    referrer_earning = 0
    referrer_of_referrer_earning = 0
    referrer_of_referrer_of_referrer_earning = 0

    # Calculate earnings for the current user
    if user.referral_code_other:
        # Find the user with the referral_code_other
        referrer = ChainUser.objects.filter(referral_code_own=user.referral_code_other).first()
        if referrer:
            # Referrer found, calculate earnings
            user_earning = amount * 0
            referrer_earning = amount * 0.50

            # Update the user's earning attribute
            user.earning += user_earning
            referrer.earning += referrer_earning
            referrer.save()

            # Continue the loop for the referrer of referrer
            referrer_of_referrer = None
            if referrer.referral_code_other:
                # Find the user with the referral_code_other of referrer
                referrer_of_referrer = ChainUser.objects.filter(referral_code_own=referrer.referral_code_other).first()
                if referrer_of_referrer:
                    # Referrer of referrer found, calculate earnings
                    referrer_of_referrer_earning = amount * 0.15
                    referrer_of_referrer.earning += referrer_of_referrer_earning
                    referrer_of_referrer.save()

                    # One more iteration for referrer of referrer's referrer
                    referrer_of_referrer_of_referrer = None
                    if referrer_of_referrer.referral_code_other:
                        # Find the user with the referral_code_other of referrer of referrer
                        referrer_of_referrer_of_referrer = ChainUser.objects.filter(
                            referral_code_own=referrer_of_referrer.referral_code_other
                        ).first()
                        if referrer_of_referrer_of_referrer:
                            # Referrer of referrer of referrer found, calculate earnings
                            referrer_of_referrer_of_referrer_earning = amount * 0.10
                            referrer_of_referrer_of_referrer.earning += referrer_of_referrer_of_referrer_earning
                            referrer_of_referrer_of_referrer.save()

    user.save()

    return render(request, 'basic.html', {
        'user': user,
        'amount': amount,
        'user_earning': user_earning,
        'referrer_earning': referrer_earning,
        'referrer_of_referrer_earning': referrer_of_referrer_earning if referrer_of_referrer else 0,
        'referrer_of_referrer_of_referrer_earning': referrer_of_referrer_of_referrer_earning
        if referrer_of_referrer_of_referrer
        else 0,
        'package': 'gold',
    })











