from store.models import Customer, ShippingAddress
from django.shortcuts import render, redirect
from firebase import Firebase
import requests

config = {
    "apiKey": "AIzaSyAWYDFRNDsOHJvX0CGuv1DTr9jj6O2HwzA",
    "authDomain": "ecom-589b9.firebaseapp.com",
    "databaseURL": "https://ecom-589b9-default-rtdb.firebaseio.com",
    "projectId": "ecom-589b9",
    "storageBucket": "ecom-589b9.appspot.com",
    "messagingSenderId": "463191758445",
    "appId": "1:463191758445:web:cb184e7e3a114adf749164",
    "measurementId": "G-07FZZDWMN8"

}

firebase = Firebase(config) 
firebase_auth = firebase.auth()
database = firebase.database()


def home(request):
    if request.session.get('uid', None):
        return render(request, 'store/home.html', {'user': True})
    return redirect('accounts:login')


def login(request):
    if request.session.get('uid', None):
        return redirect('store:home')

    if request.method == 'POST':
        email = request.POST.get('email')
        passwd = request.POST.get("pass")
        try:
            user = firebase_auth.sign_in_with_email_and_password(email, passwd)
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
            
            
            return redirect('store:home')
        except requests.exceptions.HTTPError:
            error = "Invalid Credentials"
            return render(request, 'accounts/login.html', {'message': error})
    return render(request, 'accounts/login.html')


def register(request):
    if request.session.get('uid', None):
        return redirect('store:home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone_no')
        email = request.POST.get('new_email')
        adress = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pin_code = request.POST.get('pin_code')
        passwd = request.POST.get('passwd')
        confirmed_passwd = request.POST.get('confirmed_passwd')

        if passwd == confirmed_passwd:
            try:
                user = firebase_auth.create_user_with_email_and_password(email, confirmed_passwd)
            except requests.exceptions.HTTPError:
                return render(request, 'accounts/registration.html', {'message': 'some error occurred'})
            user_id = user['localId']
            customer_details = Customer(user_id = user_id, first_name = first_name, last_name = last_name, 
                                    phone = phone,email = email)
            customer_details.save_customer_details()
            customer_id = Customer.objects.get(user_id = user_id)
            customerId = customer_id.id
            shipping_address = ShippingAddress(customer = Customer(id=customerId), adress = adress, city = city,
                                state = state, counrty = country, pin_code = pin_code)
            shipping_address.save_address_details()
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/registration.html', {'message': 'passwords don\'t match'})
    return render(request, 'accounts/registration.html')


def logout(request):
    if request.session.get('uid', None):
        del request.session['uid']
    return redirect('accounts:login')