from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth, messages
from .models import blog, User
from .helper import send_reset_link, send_verification_link
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.decorators import login_required
from html_sanitizer import Sanitizer
import six
 

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.email) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


def home(request):
    response = render(request, "index.html")
    return response


def custom_404(request, exception):
    return render(request, '404.html')


@login_required
def write_blog(request):
    if not request.user.is_authenticated:
        return redirect('/')
    return render(request, 'blog_editor.html')


def save_artical(request):
    if request.method == "POST":
        sanitizer = Sanitizer()
        sanitizer.tags.add('style')
        title = sanitizer.sanitize(request.POST['title'])
        artical=request.POST['artical'].replace('\n','<br>')
        artical = sanitizer.sanitize(artical)
        new_blog = blog(title=title, artical=artical)
        slug=new_blog.slug
        new_blog.save()
    return HttpResponse(f"<script> alert('saved {slug}') </script>")


def show(request, blog_id):
    try:
        b_log = blog.objects.get(slug=blog_id)
        response=render(request,'blogs.html',{"blog":b_log.artical})
    except Exception as identifier:
        return render(request, '404.html')
    return response


def login(request):
    print(request.method)
    if request.user.is_authenticated:
        return redirect("/")
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = auth.authenticate(username=email.split('@')[0], email=email, password=password)
        messages.error(request, 'Login Success')
        if (user is not None) and User.objects.get(email=email).is_verified:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'login.html')

def signup(request):
    if request.method != 'POST':
        return render(request, 'signup.html')
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['verify-password']

    if password != password2:
        messages.info(request, 'password didn"t match')
        return redirect('signup')
    if User.objects.filter(email=email).exists() and User.objects.get(email=email).is_verified:
        messages.info(request, 'Email Taken')
        return redirect('signup')

    elif User.objects.filter(email=email).exists() and (not User.objects.filter(email=email).first().is_verified):
        user = User.objects.get(eamil=email)
        token = TokenGenerator().make_token(user)
        s = send_verification_link(email, token)
        user.update(token=token)
        user.save()
        return redirect('login')
    else:
        user = User.objects.create_user(
            email=email, username=email.split('@')[0], password=password)
        token = TokenGenerator().make_token(user)
        user.token = token
        send_verification_link(email, token)
        user.save()
        return redirect('login')
    return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')


def reset(request,token):
    if request.method=="POST" and request.POST.get("password")!=None:
        token=request.POST.get("token")
        user=User.objects.filter(token=token).first()
        print(user.token)
        ch_token=TokenGenerator().check_token(user,token)
        if ch_token:
            password=request.POST.get("password")
            user.set_password(password)
            user.save()
            return redirect("login")
        else:
            messages.info(request, 'Invalid Link')
            return redirect("/")
    user=User.objects.filter(token=token).first()
    ch_token=TokenGenerator().check_token(user,token)
    if ch_token:
        return render(request, 'reset_password.html',{"ch_token":ch_token,'token':token})
    else:
        messages.info(request, 'Invalid Link')
        return redirect("/")
    return redirect("/")


def verify(request, token):
    user = User.objects.get(token=token)
    ch_token = TokenGenerator().check_token(user, token)
    if ch_token and (not user.is_verified):
        user.is_verified = True
        user.token = None
        user.save()
    return redirect("login")

def forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        usr_obj = User.objects.filter(email=email)
        if usr_obj.exists():
            user = User.objects.get(email=email)
            token = TokenGenerator().make_token(user)
            send_reset_link(user.email, user.username, token)
            user.token = token
            user.save()
            messages.success(request, 'Email sent on your email')
            print("Email sent")
            return HttpResponse('''<h4 align="center" style="color:green">Email sent on your email</h4>''')
        else:
            return HttpResponse('''<h4 align="center" style="color:red">User not found</h4>''')
    return HttpResponse('''<h4 align="center" style="color:red">Invalid request</h4>''')


def search(request):
    if request.method=="GET":
        search_query=request.GET['search'].lower()
        print(search_query)
        sugetions=""
        url=request.get_host()
        if search_query!="":
            links=blog.objects.all()
            for i in links:
                if search_query in i.title.lower():
                    sugetions+=f"""<a href="https://{url}/blog/{i.slug}" class='link'>{i.title} ({i.slug})</a> <br>"""
        return HttpResponse(sugetions)
    return HttpResponse("")