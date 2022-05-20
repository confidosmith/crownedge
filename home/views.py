import requests
import json 
import uuid 

from multiprocessing import context
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from userprofile.forms import *
from userprofile.models import *
from booking.models import *
from . models import *
from room.models import *
from .forms import TalkToUsForm

# Create your views here.


def home(request):
    standard_suite = Room.objects.filter(standard_suite=True).order_by('-updated_at')[:1]
    luxury_suite = Room.objects.filter(luxury_suite=True).order_by('-updated_at')[:1]
    deluxe_suite = Room.objects.filter(deluxe_suite=True)[:1]
    royal_suite = Room.objects.filter(royal_suite=True)[:1]

    context = {
        'standard_suite': standard_suite,
        'luxury_suite': luxury_suite,
        'deluxe_suite': deluxe_suite,
        'royal_suite': royal_suite,
    }
    return render(request, 'index.html', context)

    #display all the available rooms



def rooms(request):
    rooms = Room.objects.all().filter(available=True)
    p = Paginator(rooms, 8)
    page = request.GET.get('page')
    paginate = p.get_page(page)

    context = {
        'paginate':paginate
    }

    return render(request, 'rooms.html', context)



def categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'categories.html', context)



def category(request,id,slug):
    category = Room.objects.filter(category_id = id)
    specific_category = Category.objects.get(pk = id)

    context = {
        'category': category,
        'specific_category': specific_category,
    }

    return render(request, 'category.html', context)



def details(request, id, slug):
    detail = Room.objects.get(pk = id)

    context = {
        'detail':detail,
    }

    return render(request, 'details.html', context)



def talktous(request):
    talkform = TalkToUsForm() #instantiate the form for a Get request

    if request.method == 'POST': # method POST is used to collect data from users so as to persist the data to the Database 
        talkform = TalkToUsForm(request.POST) #instantiate the form for a POST request
        if talkform.is_valid(): # form validations holds at this point
            talkform.save() # form is saved if it passes the validation check
            messages.success(request, 'Your messages has been sent successfully! We will contact you shortly, Thank you.') # alert pop us message will be sent automatically
            return redirect('home')

    context = {
        'talkform':talkform
    }

    return render(request, 'index.html', context)


def search(request):
    if request.method == 'POST':
        items = request.POST['search']
        searched = Q(Q(tag__icontains=items)| Q(rate__icontains=items)| Q(room_no__icontains=items))
        searched_item = Room.objects.filter(searched)
        context = {
            'items':items,
            'searched_item':searched_item
        }

        return render(request, 'search.html', context)
    else:
        return render(request, 'search.html')

# authentication 
def signout(request):
    logout(request)
    messages.success(request, 'You have successfully signed out!')
    return redirect('home')



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'login successful!')
            return redirect('home')
        else:
            messages.info(request, 'Username/Password is incorrect, please try again.')
            return redirect('signin')

    return render(request, 'signin.html')



def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        phone = request.POST['phone']
        pix = request.POST['pix']
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            newuser = Profile(user = user)
            newuser.first_name = user.first_name
            newuser.last_name = user.last_name
            newuser.phone = phone
            newuser.pix = pix 
            newuser.save()
            login(request, user)
            messages.success(request, f'Congratulations {user.username} Your Registration is Successful!')
            return redirect('home')
        else:
            messages.error(request, form.errors)
            return redirect('signup')

    return render(request, 'signup.html')
# authentication done



# user profile 
@login_required(login_url='signin')
def profile(request):
    profile = Profile.objects.get(user__username=request.user.username)

    context = {
        'profile':profile
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def profile_update(request):
    profile = Profile.objects.get(user__username=request.user.username)
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            user = form.save()
            new = user.first_name.title()
            messages.success(request, f'Dear {new}, your profile update is successful')
            return redirect('profile')
        else:
            messages.error(request,f'Dear {new}, your profile update generated the following errors: {form.errors}')
            return redirect('profile_update')

    context = {
        'form':form,
        'profile':profile
    }

    return render(request, 'profile_update.html', context)

@login_required(login_url='signin')
def password_update(request):
    profile = Profile.objects.get(user__username = request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            new = user.username.title()
            update_session_auth_hash(request, user)
            messages.success(request, f'Dear {new} your password update is successful')
            return redirect('profile')
        else:
            messages.error(request, f'Dear {new} your password update is unsuccessful, {form.errors}')
            return redirect('password_update')

    context = {
        'profile':profile,
        'form':form
    }

    return render(request, 'password_update.html', context)
# user profile done

# booking

@login_required(login_url='signin')
def booking(request):
    profile = Profile.objects.get(user__username = request.user.username)
    code = profile.id 
    if request.method == 'POST':
        datein = request.POST['checkin']
        dateout = request.POST['checkout']
        droom = request.POST['roomid']
        specific = Room.objects.get(pk=droom)
        booking = Booking.objects.filter(user__username = request.user.username, paid=False)
        if booking:
            reserve = Booking.objects.filter(room=specific.id, checkin=datein, checkout=dateout, user__username=request.user.username, paid=False)
            if reserve:
                reserve.checkin = datein
                reserve.checkout = dateout
                if reserve.checkin > dateout or reserve.checkout < datein:
                    reserve.save()
                    messages.success(request,'The room has been reserved for you.')
                    return redirect('booked')
                else:
                    messages.info(request,'The room requested is already booked.')
                    return redirect('rooms')
            
            else:
                newroom = Booking()
                newroom.user = request.user
                newroom.room = specific
                newroom.room_no = specific.room_no
                newroom.booking_code = code 
                newroom.checkin = datein
                newroom.checkout = dateout
                newroom.price = specific.rate 
                newroom.paid = False
                newroom.available = False
                newroom.save()
                messages.success(request,'Your booking reservation is successful!')
                return redirect('booked')

        else:
            new = Booking()
            new.user = request.user
            new.room = specific
            new.room_no = specific.room_no
            new.booking_code = code 
            new.checkin = datein
            new.checkout = dateout
            new.price = specific.rate 
            new.paid = False
            new.available = False
            new.save()
            messages.success(request,'Your booking reservation is successful!')

    return redirect('booked')

@login_required(login_url='signin')
def booked(request):
    Booking.objects.filter(del_booking__lte = timezone.now() - timezone.timedelta(minutes=30)).filter(paid=False).delete()
    booking = Booking.objects.filter(user__username = request.user.username, paid=False)

    for item in booking:
        item.no_days = (item.checkout - item.checkin).days
        item.amount = item.price * item.no_days
        item.save()

    subtotal = 0
    vat = 0
    total = 0

    for item in booking:
        subtotal += item.price * item.no_days

    vat = 0.075 * subtotal
    total = subtotal + vat 

    context = {
        'booking':booking,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
    }
    
    return render(request, 'booked.html', context)

@login_required(login_url='signin')
def delete(request):
    if request.method == 'POST':
        del_room = request.POST['room_id']
        Booking.objects.filter(pk=del_room).delete()
        messages.success(request,'one item deleted')
        return redirect('booked')

@login_required(login_url='signin')
def checkout(request):
    profile = Profile.objects.get(user__username = request.user.username)
    booking = Booking.objects.filter(user__username = request.user.username, paid=False)

    subtotal = 0
    vat = 0
    total = 0

    for item in booking:
        subtotal += item.price * item.no_days

    vat = 0.075 * subtotal
    total = subtotal + vat 

    context = {
        'booking':booking,
        'profile':profile,
        'total':total,
    }

    return render(request, 'checkout.html', context)

@login_required(login_url='signin')
def pay(request):
    if request.method == 'POST':
        api_key = 'sk_test_ad502719e58fd78a40fd31ab9415532181331240'#secret key from paystack
        curl = 'https://api.paystack.co/transaction/initialize'#paystack call url
        cburl = 'http://54.227.14.173/callback/' #crownedge callback url to send payment success message
        ref = str(uuid.uuid4()) #reference number required by paystack as an additional order number
        profile = Profile.objects.get(user__username = request.user.username)
        booking_code = profile.id #main booking order number 
        total = float(request.POST['total']) * 100 #total amount to be charged from the client's bank 
        user = User.objects.get(username = request.user.username)#query the User model for client's details
        email = user.email #store client's email detail to send to paystack
        first_name = request.POST['first_name'] #collect from the template incase there is a change
        last_name = request.POST['last_name']#collect from the template incase there is a change 
        phone = request.POST['phone']#collect from the template incase there is a change

        #collect data to send to paystack via call 
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference': ref, 'amount': int(total), 'email': user.email, 'callback_url': cburl, 'order_number': booking_code, 'currency': 'NGN'}

        #make a call to paystack
        try:
            r = requests.post(curl, headers=headers, json=data) #pip install requests
        except Exception:
            messages.error(request, 'Network busy, try again')
        else:
            transback = json.loads(r.text)
            rdurl = transback['data']['authorization_url']

            account = Payment()
            account.user = user
            account.first_name = user.first_name
            account.last_name = user.last_name
            account.amount = total/100
            account.paid = True 
            account.phone = phone
            account.pay_code = ref 
            account.booking_code = booking_code
            account.save()


            return redirect(rdurl)

    return redirect('checkout')

def callback(request):
    profile = Profile.objects.get(user__username = request.user.username)
    booking = Booking.objects.filter(user__username = request.user.username, paid=False)
    reserved = Booking.objects.filter(user__username = request.user.username, paid=True, future=True)

    for item in booking:
        item.paid = True 
        item.available = False 
        item.future = True 
        item.save()

        room = Room.objects.get(pk=item.room.id)
        room.available = False 
        room.save()

    subtotal = 0
    vat = 0
    total = 0

    for item in reserved:
        subtotal += item.price * item.no_days

    vat = 0.075 * subtotal
    total = subtotal + vat 

    context = {
        'profile':profile,
        'reserved':reserved,
        'total':total,
    }

    return render(request, 'callback.html', context)


@login_required(login_url='signin')
def history(request):
    profile = Profile.objects.get(user__username = request.user.username)
    reserved = Booking.objects.filter(user__username = request.user.username, paid=True, future= False, display=True)


    subtotal = 0
    vat = 0
    total = 0

    for item in reserved:
        subtotal += item.price * item.no_days

    vat = 0.075 * subtotal
    total = subtotal + vat 

    context = {
        'profile':profile,
        'reserved':reserved,
        'total':total,
    }

    return render(request, 'history.html', context)

def del_history(request):
    if request.method == 'POST':
        history_id = request.POST['history_id']
        del_detail = Booking.objects.filter(pk = history_id)
        for item in del_detail:
            item.display = False
            item.save()
            messages.success(request, 'Booking history deleted sucessfully')
        return redirect('history')

# booking done

