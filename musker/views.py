from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Tweep
from .forms import TweepForm

def home(request):
    if request.user.is_authenticated:
        form = TweepForm(request.POST or None)
        if request.method == "POST":
            tweep = form.save(commit=False)
            tweep.user =request.user
            tweep.save()
            messages.success(request, 'Your Tweep has been posted..')
            return redirect('home')

        tweeps = Tweep.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweeps":tweeps, "form":form})
    else:
        tweeps = Tweep.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweeps":tweeps})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)      #this excludes the person logged on from the list
        
        return render(request, 'profile_list.html', {'profiles': profiles}) 
    else: 
        messages.success(request, 'You must be logged in to view this page..')
        return render(request ,'home.html') 

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweeps =Tweep.objects.filter(user_id=pk).order_by("-created_at")

        #Post Form Logic
        if request.method == "POST":
            #Get current user ID
            current_user_profile = request.user.profile
            #Get form data
            action = request.POST['follow']
            #Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            #Save the profile
            current_user_profile.save()  


        return render(request, "profile.html", {"profile":profile, "tweeps":tweeps})   

    else: 
        messages.success(request, 'You must be logged in to view this page..')
        return render(request ,'home.html')       