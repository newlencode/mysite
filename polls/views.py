from django.shortcuts import render,redirect
from . import models,forms
import datetime
import hashlib
from django.utils import timezone

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code
def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login')
    return render(request, 'polls/index.html')


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.Users.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'polls/login.html', locals())
            if not user.has_confirmed:

                message = '该用户还未经过邮件确认！'
                return render(request, 'polls/login.html', locals())
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index')
            else:
                message = '密码不正确！'
                return render(request, 'polls/login.html', locals())
        else:
            return render(request, 'polls/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'polls/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'polls/register.html', locals())
            else:
                same_name_user = models.Users.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.Users.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'polls/register.html', locals())

                new_user = models.Users()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往邮箱进行确认！'
                return render(request, 'polls/confirm.html', locals())
        else:
            return render(request, 'polls/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'polls/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login")

from django.conf import settings

def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自jackpardon的注册确认邮件'

    text_content = '''感谢注册jackpardon的站点！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>jackpardon的网站</a>，\
                    这里是jackpardon的个人站点</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = timezone.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'polls/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'polls/confirm.html', locals())

def myblogs(request):
    if not request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/login')
    username = request.session.get('user_name')
    user = models.Users.objects.get(name=username)
    blogs = models.BlogPost.objects.filter(b_userid=user.id)

    return render(request,'polls/myblogs.html', locals())

def new_blog(request):
    if not request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/login')
    if request.method == 'POST':
        newblog = models.BlogPost()
        newblog.title = request.POST.get('title')
        newblog.content = request.POST.get('content')
        newblog.pub_time = request.POST.get('pub_time')
        username = request.session.get('user_name')
        user = models.Users.objects.get(name=username)
        newblog.b_userid = user
        newblog.save()
        return redirect('/myblogs')
    return render(request,'polls/new_blog.html', locals())


def blog_detail(request,blog_detail_id):
    if not request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/login')
    blog = models.BlogPost.objects.get(id=blog_detail_id)
    return render(request,'polls/blog_detail.html', locals())


def blog_delete(request,blog_detail_id):
    if not request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/login')
    blog = models.BlogPost.objects.filter(id=blog_detail_id)
    blog.delete()
    return redirect('/myblogs')

