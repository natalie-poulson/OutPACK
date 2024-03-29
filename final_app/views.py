from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import forms
from django.conf import settings
from .models import User, UserProfileInfo, Trip, Post, Gear, Food
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import date, timedelta
from icalendar import Calendar, Event
from django.contrib.sites.models import Site


def landing(request):
    login_form = AuthenticationForm()
    signup_form = UserCreationForm()

    context = {
        'login_form': login_form,
        'signup_form' : signup_form,
    }

    return render(request, 'final_app/landing.html', context)


@login_required(login_url='/accounts/signup/')
def profile_create(request):
    if request.method == "POST":        
        form = forms.CreateProfile(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('final_app:profile')
    else:
        form = forms.CreateProfile()

    return render(request, 'final_app/profile_create.html', {'form': form})


@login_required(login_url='/accounts/login/')
def profile_view(request):
    user = request.user
    trips = Trip.objects.filter(user=request.user).order_by('-start_date')

    context = {
        'user': user,
        'trips' : trips
    }

    return render(request, 'final_app/profile.html', context)


@login_required(login_url='/accounts/login/')
def profile_edit(request):
    if request.method == "POST":
        profile_form = forms.CreateProfile(data=request.POST, instance=request.user.profile, files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            if 'profile_picture' in request.FILES:
                profile_form.profile_picture = request.FILES['profile_picture']
            profile_form.save()
            return redirect('final_app:profile')
        else:
            return render(request, 'final_app/profile_edit.html', {'profile_form': profile_form})
    else:
        profile_form = forms.CreateProfile(instance=request.user.profile)

    return render(request, 'final_app/profile_edit.html', {'profile_form': profile_form})


@login_required(login_url='/accounts/login/')
def trip_detail(request, slug):
    trip = Trip.objects.get(slug=slug)
    post_form = forms.CreatePost()
    gear_form = forms.CreateGear()
    food_form = forms.CreateFood()

    context = {
        'trip': trip,
        'post_form' : post_form,
        'gear_form': gear_form,
        'food_form': food_form
    }

    return render(request, 'final_app/trip_detail.html', context)


@login_required(login_url='/accounts/login/')    
def post_detail(request, slug):
    post = Post.objects.get(slug=slug)

    return render(request, 'final_app/post_detail.html', {'post': post})


@login_required(login_url='/accounts/login/')
def post_create(request):
    if request.method == 'POST':
        post_form = forms.CreatePost(request.POST, request.FILES)
        trip_id = request.POST.get('trip_id')
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.user = request.user
            instance.trip = Trip.objects.get(pk=trip_id)
            instance.save()
            trip = Trip.objects.get(pk=trip_id)

            return redirect('final_app:post_detail', slug=instance.slug)       


@login_required(login_url='/accounts/login/')
def trip_create(request):
    if request.method == 'POST':
        trip_form = forms.CreateTrip(request.POST)
        if trip_form.is_valid():
            instance = trip_form.save(commit=False)
            instance.user = request.user
            if (instance.end_date) < date.today():
                instance.completed = True
            instance.save()
            trip = Trip.objects.get(id = instance.id)
        return redirect('final_app:trip_detail', slug =trip.slug)
    else:
        trip_form = forms.CreateTrip()
    return render(request, 'final_app/trip_create.html', {'trip_form': trip_form})


@login_required(login_url='/accounts/login/')
def trip_delete(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        trip = Trip.objects.get(pk=trip_id)
        trip.delete()
        return redirect('final_app:profile')


@login_required(login_url='/accounts/login/')
def post_delete(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        trip = Trip.objects.get(pk=post.trip.id)
        post.delete()
        return redirect('final_app:trip_detail', slug=trip.slug)


@login_required(login_url='/accounts/login/')
def trips(request):
    trips_completed = Trip.objects.filter(user=request.user).filter(completed=True).order_by('-start_date')
    trips_future = Trip.objects.filter(user=request.user).filter(completed=False).order_by('-start_date')

    context = {
        'trips_completed':trips_completed,
        'trips_future': trips_future
    }

    return render (request, 'final_app/trips.html', context)


@login_required(login_url='/accounts/login/')
def post_edit(request,slug ):
    post = Post.objects.get(slug=slug)
    if request.method == "POST":
        post_edit_form = forms.CreatePost(data=request.POST, instance=post, files=request.FILES)
        if post_edit_form.is_valid():
            post_edit_form.save()
            if 'image' in request.FILES:
                post_edit_form.media = request.FILES['image']
            if 'video' in request.FILES:
                post_edit_form.media = request.FILES['video']
            post_edit_form.save()
            return redirect('final_app:post_detail', slug =post.slug)
    else:
        post_edit_form = forms.CreatePost(instance=post)

    return render(request, 'final_app/post_edit.html', {'post_edit_form': post_edit_form})


@login_required(login_url='/accounts/login/')
def trip_edit(request,slug ):
    trip = Trip.objects.get(slug=slug)
    if request.method == "POST":
        form = forms.CreateTrip(data=request.POST, instance=trip)
        if form.is_valid():
            form.save()   
        return redirect('final_app:trip_detail', slug =trip.slug)
    else:
        form = forms.CreateTrip(instance=trip)

    return render(request, 'final_app/trip_edit.html', {'form': form})


@login_required(login_url='/accounts/login/')
def gear_create(request):
    if request.method == 'POST':
        gear_form = forms.CreateGear(request.POST)
        trip_id = request.POST.get('trip_id')
        if gear_form.is_valid():
            instance = gear_form.save(commit=False)
            instance.trip = Trip.objects.get(pk=trip_id)
            instance.save()
            trip = Trip.objects.get(pk=trip_id)
            return redirect('final_app:trip_detail', slug =trip.slug)

    return redirect('final_app:trip_detail')


@login_required(login_url='/accounts/login/')
def gear_edit(request,pk ):
    gear = Gear.objects.get(pk=pk)
    trip = Trip.objects.get(trip_gears=gear)
    if request.method == "POST":
        form = forms.CreateGear(data=request.POST, instance=gear)
        if form.is_valid():
            form.save()   
        return redirect('final_app:trip_detail', slug =trip.slug)
    else:
        form = forms.CreateGear(instance=gear)

    return render(request, 'final_app/gear_edit.html', {'form': form})


@login_required(login_url='/accounts/login/')
def gear_delete(request,pk ):
    gear = Gear.objects.get(pk=pk)
    trip = Trip.objects.get(trip_gears=gear)
    gear.delete()

    return redirect('final_app:trip_detail', slug =trip.slug)


@login_required(login_url='/accounts/login/')
def food_create(request):
    if request.method == 'POST':
        food_form = forms.CreateFood(request.POST)
        trip_id = request.POST.get('trip_id')
        trip_day = request.POST.get('trip_day')

        print ("PRINT:", request.POST.get('trip_day'))

        if food_form.is_valid():
            instance = food_form.save(commit=False)
            instance.trip = Trip.objects.get(pk=trip_id)
            instance.day = trip_day
            instance.save()
            trip = Trip.objects.get(pk=trip_id)
            return redirect('final_app:trip_detail', slug =trip.slug)


@login_required(login_url='/accounts/login/')
def food_edit(request,pk ):
    food = Food.objects.get(pk=pk)
    trip = Trip.objects.get(trip_foods=food)
    if request.method == "POST":
        form = forms.CreateFood(data=request.POST, instance=food)
        if form.is_valid():
            form.save()   
        return redirect('final_app:trip_detail', slug =trip.slug)
    else:
        form = forms.CreateFood(instance=food)

    return render(request, 'final_app/food_edit.html', {'form': form})


@login_required(login_url='/accounts/login/')
def food_delete(request,pk ):
    food = Food.objects.get(pk=pk)
    trip = Trip.objects.get(trip_foods=food)
    food.delete()
    return redirect('final_app:trip_detail', slug =trip.slug)


@login_required(login_url='/accounts/login/')
def other_profile(request, username):
    user = User.objects.get(username=username)
    trips = Trip.objects.filter(user=user).order_by('-start_date')
    
    context = {
        'user': user,
        'trips': trips
    }

    return render(request, 'final_app/profile.html', context)


@login_required(login_url='/accounts/login/')
def other_trip_detail(request,username, slug):
    trip = Trip.objects.get(slug=slug)   

    return render(request, 'final_app/trip_detail.html', {'trip': trip})


@login_required(login_url='/accounts/login/')    
def other_post_detail(request, username, slug):
    post = Post.objects.get(slug=slug)

    return render(request, 'final_app/other_post_detail.html', {'post': post})


@login_required(login_url='/accounts/login/')
def explore(request):        
    db_results = Trip.objects.exclude(user=request.user).exclude(user__profile__privacy_choice='PRIVATE')

    return render(request,'final_app/explore.html',{'results':db_results})
    
@login_required(login_url='/accounts/login/')
def export(request, slug):
    event = Trip.objects.get(slug = slug)

    cal = Calendar()
    site = Site.objects.get_current()

    cal.add('prodid', '-//%s Events Calendar//%s//' % (site.name, site.domain))
    cal.add('version', '2.0')

    site_token = site.domain.split('.')
    site_token.reverse()
    site_token = '.'.join(site_token)

    ical_event = Event()
    ical_event.add('summary', event.trail)
    ical_event.add('dtstart', event.start_date)
    ical_event.add('dtend', event.end_date + timedelta(days=1))
    ical_event['uid'] = '%d.event.events.%s' % (event.id, site_token)
    cal.add_component(ical_event)

    response = HttpResponse(cal.to_ical(), content_type="text/calendar")
    response['Content-Disposition'] = 'attachment; filename=%s.ics' % event.slug

    return response


