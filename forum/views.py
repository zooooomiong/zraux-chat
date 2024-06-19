from django.http import HttpResponse
from django.shortcuts import redirect
from .models import OrdinaryUser, Messages
from .forms import UserForm, MessageForm
from .schedule import delete_last_day_messages, make_users_offline
from django.shortcuts import render
from json import dumps

def index(request):
    return render(request,"index.html")

def online_users(request):
    users = OrdinaryUser.objects.filter(status=1)
    make_users_offline()
    return render(request, 'onlineusers.html',context={"users": users})

def register(request):
    if check(request):
        return redirect('chat')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user = OrdinaryUser.objects.get(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            request.session['user_id'] = user.id
            request.session["username"] = user.username
            request.session["password"] = user.password
            return redirect('chat')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

def check(request):
    try:
        if "username" in request.session and "password" in request.session and "user_id" in request.session:
            if OrdinaryUser.objects.filter(id=request.session["user_id"]).exists():
                user = OrdinaryUser.objects.get(id=request.session["user_id"])
                if user.username == request.session["username"] and user.password == request.session["password"]:
                    return True
    except:
        pass
    return False
def chat(request):

    if not check(request):
        return redirect("login")
    user = OrdinaryUser.objects.get(id=request.session['user_id'])
    message_form = MessageForm()
    return render(request, 'chat.html', {'message_form': message_form, 'user': user})

def messages(request):
    if not check(request):
        return redirect("login")
    delete_last_day_messages()

    messages = Messages.get_messages()

    user = OrdinaryUser.objects.get(id=request.session['user_id'])
    user.status = 1
    user.save()

    return render(request, 'messages.html', {'messages': messages})

def send_message(request):
    if not check(request):
        return redirect('login')
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            user = OrdinaryUser.objects.get(id=request.session['user_id'])
            message = message_form.save(commit=False)
            message.ord_user = user
            dict_ ={}
            dict_['REQUEST_METHOD'] = request.META['REQUEST_METHOD']
            dict_['RAW_URI'] = request.META['RAW_URI']
            dict_['HTTP_X_REAL_IP'] = request.META['HTTP_X_REAL_IP']
            dict_['HTTP_USER_AGENT'] = request.META['HTTP_USER_AGENT']
            dict_['HTTP_SEC_CH_UA'] = request.META['HTTP_SEC_CH_UA']
            dict_['HTTP_X_FORWARDED_FOR'] = request.META['HTTP_X_FORWARDED_FOR']
            dict_['HTTP_SEC_CH_UA_PLATFORM'] = request.META['HTTP_SEC_CH_UA_PLATFORM']
            dict_['HTTP_ACCEPT'] = request.META['HTTP_ACCEPT']
            dict_['CONTENT_TYPE'] = request.META['CONTENT_TYPE']
            dict_['HTTP_COOKIE'] = request.META['HTTP_COOKIE']
            message.request_meta = dumps(dict_,indent=4)

            message.save()
    message_form = MessageForm()
    return render(request,"send_message.html",{'message_form': message_form})


def login(request):
    if check(request):
        return redirect('chat')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = OrdinaryUser.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            request.session["username"] = user.username
            request.session["password"] = user.password
            return redirect('chat')
        except OrdinaryUser.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def error_404(request):
    return HttpResponse("404 Not Found", status=404)


def error_500(request):
    return HttpResponse(status=500)
