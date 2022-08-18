from email import message
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from q_a.models import Question
from .forms import UserSignupForm

# Create your views here.


def signup(request):

    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Welcome to R_Solutions {username}, please sign-in to continue")
            return redirect('users:signin')
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {'form': form})

    # if request.method == 'POST':
    #     username = request.POST['username']
    #     email = request.POST['email']
    #     password = request.POST['password']
    #     password2 = request.POST['password2']``

    #     if password == password2:
    #         if User.objects.filter(email=email).exists():
    #             messages.info(request, 'Email already exists')
    #             return redirect('signup')
    #         elif User.objects.filter(username=username).exists():
    #             messages.info(request, 'Username unavailable')
    #             return redirect('signup')
    #         else:
    #             user = User.objects.create_user(
    #                 username=username, email=email, password=password)
    #             user.save()

    #             user_login = auth.authenticate(
    #                 username=username, password=password)
    #             auth.login(request, user_login)

    #             user_model = User.objects.get(username=username)
    #             new_profile = Profile.objects.create(
    #                 user=user_model, id_user=user_model.id)
    #             new_profile.save()
    #             return redirect('/')
    #     else:
    #         messages.info(request, 'Passwords do not match')
    #         return redirect('signup')

    # else:
    #     return render(request, 'signup.html')


def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('signin')

    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def profile(request, pk):

    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Question.objects.filter(user=pk)
    user_post_length = len(user_posts)
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length
    }
    return render(request, 'profile.html', context)
