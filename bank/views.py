from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from .models import Account
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Account

from rest_framework.authtoken.models import Token


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account
from django.contrib.auth.hashers import check_password

from decimal import Decimal  # Add this import statement
from django.contrib.auth import logout


from django.contrib.auth.models import User


# views.py
from django.shortcuts import render
from .models import User

from django.urls import get_resolver

def show_links(request):
    # Define the links to display
    links = [
        {'name': 'Register', 'url': 'register'},
        {'name': 'Login', 'url': 'login'},
    ]
    
    # Pass the links to the template context
    context = {'links': links}
    
    # Render the template with the links
    return render(request, 'links.html', context)


def users(request):
    # Retrieve only active users from the database
    users = User.objects.filter(is_active=True)
    
    # Extract user IDs and usernames from the active user objects
    user_data = [{'id': user.id, 'username': user.username} for user in users]
    
    # Pass user data to the template context
    context = {'user_data': user_data}
    
    # Render the template with the user data
    return render(request, 'users.html', context)


class AddBalanceView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        account_id = request.data.get('account_id')
        amount = request.data.get('amount')

        if account_id and amount:
            try:
                account = Account.objects.get(id=account_id)
                account.balance += float(amount)
                account.save()
                return Response({'message': 'Balance added successfully.'}, status=status.HTTP_200_OK)
            except (Account.DoesNotExist, ValueError):
                return Response({'error': 'Invalid account ID or amount.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Account ID or amount not provided.'}, status=status.HTTP_400_BAD_REQUEST)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create an Account object for the newly registered user
            Account.objects.create(user=user)
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('account_detail')  # Redirect to account detail page after successful login
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return render(request, 'links.html')



def account_detail(request):
    user = request.user
    account = Account.objects.get(user=user)
    context = {
        'account': account,
        'user_id': user.id,  # Add user ID to the context
    }
    return render(request, 'account_detail.html', context)

def send_money(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        amount = Decimal(request.POST.get('amount'))  # Convert to Decimal
        password = request.POST.get('password')

        try:
            receiver_account = Account.objects.get(user__id=receiver_id)
            sender_account = Account.objects.get(user=request.user)

            if check_password(password, request.user.password):
                if sender_account.balance >= amount:  # Use Decimal comparison
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()
                    return render(request,"paymentdone.html")
                else:
                    return HttpResponse("Insufficient balance.")
            else:
                return HttpResponse("Invalid password.")
        except (Account.DoesNotExist, ValueError):
            return HttpResponse("Invalid user ID or amount.")
    else:
        return HttpResponse("Method not allowed.")