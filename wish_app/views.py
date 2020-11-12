from django.shortcuts import render, HttpResponse,redirect
from .models import User, Wish
from django.contrib import messages
from datetime import datetime
import bcrypt
from django.contrib.sessions.models import Session
#from wall_app import views as wall_app_views


# Create your views here.
def index(request):
    return render(request, 'register_login.html')

def dashboard(request):
    if 'id' in request.session:
        all_wishes = Wish.objects.all()
        user = User.objects.get(id=request.session['id'])
        user_wishes = user.wishes.all().order_by('-created_at').order_by('-updated_at')
        context = {
            'user' : user,
            'all_wishes' : all_wishes,
            'user_wishes' : user_wishes
        }
        return render(request, 'dashboard.html', context)
    return redirect(index)

def register(request):
    if request.method == 'POST':
        response_from_models = User.objects.validateRegister(request.POST)

        if len(response_from_models) < 1:
            pw_hash = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
            new_user = User(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            new_user.save()
            id = new_user.id
            request.session['id'] = id
            request.session['user_name'] = request.POST['first_name']
            #request.session['type'] = 'registerd!'
            return redirect(dashboard)
        
        else:
            # send E msgs to C
            for err in response_from_models:
                messages.error(request, err)

    return redirect(index)

def login(request):
    if request.method == 'POST':
        response_from_models = User.objects.validateLogin(request.POST)

        if len(response_from_models) < 1:
            user = User.objects.filter(email=request.POST['email'])
            user_id = user[0].id
            user_name = user[0].first_name
            request.session['id'] = user_id
            request.session['user_name'] = user_name
            #request.session['type'] = 'logged in!'
            return redirect(dashboard)
        
        else:
            # send E msgs to C
            for err in response_from_models:
                messages.error(request, err)
                
    return redirect(index)

def add_wish(request):
    if 'id' in request.session:
        return render(request, 'new_wish.html')
    return redirect(index)
def make_wish(request):
    if 'id' in request.session:
        if request.method == 'POST':
            response_from_models = Wish.objects.validateWish(request.POST)

            if len(response_from_models) < 1:
                user = User.objects.get(id=request.session['id'])
                wish = Wish.objects.create(name=request.POST['name'], desc=request.POST['desc'], granted_date=datetime.now(), wisher=user)
                user.wishes.add(wish)
                user.save()
                return redirect(dashboard)

            else:
                # send E msgs to C
                for err in response_from_models:
                    messages.error(request, err)

    return redirect(add_wish)

def remove_wish(request, wish_id):
    if 'id' in request.session:
        wish = Wish.objects.get(id=wish_id)
        wish.delete()
        return redirect(dashboard)
    return redirect(index)

def edit_wish(request, wish_id):
    if 'id' in request.session:
        context = {
            'wish' : Wish.objects.get(id=wish_id)
        }
        return render(request, 'edit_wish.html', context)
    return redirect(index)

def make_edit(request, wish_id):
    if 'id' in request.session:
        if request.method == 'POST':
            response_from_models = Wish.objects.validateWish(request.POST)

            if len(response_from_models) < 1:
                wish = Wish.objects.filter(id=wish_id)
                wish.update(
                    name=request.POST['name'], 
                    desc=request.POST['desc'],
                )
                wish[0].save()
                return redirect(dashboard)

            else:
                # send E msgs to C
                for err in response_from_models:
                    messages.error(request, err)

    return redirect(edit_wish, wish_id)

def grant_wish(request, wish_id):
    if 'id' in request.session:
        wish = Wish.objects.get(id=wish_id)
        wish.granted_date = datetime.now()
        wish.status = 'granted'
        wish.save()
        return redirect(dashboard)
    return redirect(index)
def like_wish(request, wish_id):
    if 'id' in request.session:
        user = User.objects.get(id=request.session['id'])
        wish = Wish.objects.get(id=wish_id)
        wish.liked_by.add(user)
        wish.save()
        return redirect(dashboard)
    return redirect(index)

def view_stats(request):
    if 'id' in request.session:
        all_wishes = Wish.objects.all()
        user = User.objects.get(id=request.session['id'])
        all_granted = 0
        user_granted = 0 
        user_pending = 0

        for wish in all_wishes:
                if wish.status == 'granted':
                    all_granted +=1

        for wish in user.wishes.all():
            if wish.status == 'granted':
                user_granted +=1
            else:
                user_pending +=1

        context = {
            'all_granted_count' : all_granted,
            'user_granted_count' : user_granted,
            'user_pending_count' : user_pending
        }
        return render(request, 'stats.html', context)

    return redirect(index)


def logout(request):

    request.session.clear()		# clears all keys
    if 'id' in request.session:
        del request.session['id']
    if 'user_name' in request.session:
        del request.session['user_name']

    return redirect(index)
    