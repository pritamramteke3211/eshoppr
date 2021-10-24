from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.views import View
from shop.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import  *
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from shop.forms import SignupForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.views import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


class HomePage(View):
    template_name = 'mhome.html'
    def get(self, request):
        context = {'mhome':'active'}
        return render(request,self.template_name,context)


def prac(request):
    context = {'prac':'active'}
    return render(request,'prac.html',context)

def jsondata(request):
    if request.user.is_authenticated:
        data = list(Cart.objects.filter(user=request.user).values())
        return JsonResponse(data,safe = False)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
def signup(request):
    users = User.objects.all()

    if request.method == 'POST':
        # Get the post paramters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        for i in users:
          if  username == i.username:
              messages.error(request, "Username Already")
              return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page
        
        # Check for errorneous inputs
        # username should be under 10 character
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page
        
        # username should be lowercase
        if not username.islower():
            messages.error(request, "Username should in lowercase")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page

        # username should be alphanumeric
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page

        # password should match
        if pass1 != pass2:
            messages.error(request, "Password do not match")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page


        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,'Your MAC account has been successfully created')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page 

    else:
        return render(request,'signup.html')


def userlogin(request):
    if request.method == 'POST':
        # Get the post paramters
        uname = request.POST['username']
        pass1 = request.POST['pass1']
                   
        user = authenticate(username=uname, password=pass1)
        if user is not None:
            login(request, user)
            # messages.success(request,f'Welcome {str(request.user).capitalize()}')
            return redirect('home')

        else:
            messages.error(request, "Invalid Crendentials, Please try again")
            return redirect('home')
    else:
        return render(request,'login.html')

def userlogout(request):
    logout(request)
    messages.success(request,'User Logout successfully')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page

class MyPasswordChangeView(PasswordChangeView):
    template_name='changepass.html'
    # success_url='/password_change_done/'
    
class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name='password_change_done.html'
    
class MyPasswordResetView(PasswordResetView):
    template_name='password_reset.html'
    
class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name='password_reset_done.html'
    
class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name='password_reset_confirm.html'
    
class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name='password_reset_complete.html'
