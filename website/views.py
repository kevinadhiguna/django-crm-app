from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()

    # Check if user is logged in
    if request.method == 'POST':
        # -- Following causes MultiValueDictKeyError -- #
        # username = request.POST['username'] # <- Get the value of username in the form (<input ... name="username" ...>)
        # password = request.POST['password']
        # --------------------------------------------- #
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in successfully!")
            return redirect('website:home')
        else:
            messages.success(request, "There was an error logging in, please try again...")
            return redirect('website:home')
    else:
        return render(request, 'home.html', {'records': records})

# def login_user(request):
#     pass

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('website:home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            # Authenticate and login immediately
            username = form.cleaned_data['username'] # Pulls out the submitted username
            password = form.cleaned_data['password1'] # 'password1' is how the password is declared in forms.py (not in the form)
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('website:home')
        else:
            messages.success(request, "Something went wrong while registering (invalid form), please try again...")
            return render(request, 'register.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})

# @login_required
def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up records
        customer_record = Record.objects.get(id=pk) # <- 'id' is an automatically created primary key
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        # The message below is not displayed if @login_required is present. Instead it shows 'Page not found' error.
        messages.success(request, "You must be logged in to view the page")
        return redirect('website:home')

# @login_required
def delete_record(request, pk):
    if request.user.is_authenticated:
        to_be_deleted = Record.objects.get(id=pk)
        to_be_deleted.delete()
        messages.success(request, 'Successfully deleted the record')
        return redirect('website:home')
    else:
        message.success(request, 'You must be logged in to delete a record')
        return redirect('website:home')

# @login_required
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record added successfully!")
                return redirect('website:home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to add a record")
        return redirect('website:home')

# @login_required
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated successfully!")
            return redirect('website:home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, 'You must be logged in to update a record!')
        return redirect('website:home')
