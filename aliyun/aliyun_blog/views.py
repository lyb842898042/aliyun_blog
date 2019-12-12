# from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from aliyun_blog.models import User, AccountVip ,BlogText
import datetime


def home(request):
    return render(request,'home.html')



def if_change(string1,string2):
    s1 = str(string1)
    s2 = str(string2)
    if s2 == s1 or s2 == '':
        return string1
    else:
        return string2



def re_main(request):
    if request.session.get('id'):
        id = request.session.get('id')
        user = User.objects.filter(u_id=id).first()
        # print(data['header'])
        return render(request,'main.html',{'user':user})
        # return render(request, 'main.html', data)
    else:
        return render(request, 'main.html')
        # return render(request, 'main.html')

#注册
def al_regrist(request):
    '''
    uid
    uname
    sex
    header
    pwd
    qq
    email
    '''
    if request.method == 'GET':
        return render(request,'regist.html')
    elif request.method == 'POST':
        ur = User()
        ur.u_id = request.POST.get('uid')
        ur.u_name = request.POST.get('uname')
        ur.u_email = request.POST.get('email')
        ur.u_password = request.POST.get('pwd')
        ur.u_qq = request.POST.get('qq')
        ur.u_sex = request.POST.get('sex')
        ur.u_header = request.FILES.get('header')
        ur.save()
        return render(request,'login.html')
    else:
        return render(request,'404.html')

#登录
def al_login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        uid = request.POST.get('uid')
        pwd = request.POST.get('pwd')

        user = User.objects.filter(u_id=uid,u_password=pwd).first()
        if user:
            request.session['id'] = user.u_id
            return redirect('/main/')
        else:
            return render(request,'404.html')


    else:
        return render(request,'404.html')



def al_logout(request):
    request.session.flush()
    return render(request,'main.html')
    # return render(request, 'main.html')


def user_msg(request):
    if request.session.get('id'):
        id = request.session.get('id')
        user = User.objects.filter(u_id=id).first()
        data = {
            'user':user
        }
        # print(data['header'])
        return render(request,'user_msg.html',data)
        # return render(request, 'main.html', data)
    return render(request,'404.html')


def cgmsg(request):
    if request.session.get('id'):
        id = request.session.get('id')
        if request.method == 'GET':
            user = User.objects.get(u_id=id)
            return render(request,'change_msg.html',{'user':user})
        else:
            user = User.objects.get(u_id=id)
            user.u_name = if_change(user.u_name,request.POST.get('uname'))
            user.u_email = if_change(user.u_email,request.POST.get('mail'))
            user.u_qq = if_change(user.u_qq,request.POST.get('qq'))
            user.save()
            return redirect('/main/')
    else:
        return render(request,'login.html')


def cgpwd(request):
    if request.session.get('id'):
        id = request.session.get('id')
        if request.method == 'GET':
            user = User.objects.get(u_id=id)
            return render(request,'cgpwd.html',{'user':user})
        elif request.method == 'POST':
            user = User.objects.get(u_id=id)
            oldpwd = user.u_password
            post_old_pwd = request.POST.get('oldpwd')
            new_pwd = request.POST.get('newpwd')
            res_pwd = request.POST.get('respwd')
            if oldpwd == post_old_pwd:
                if res_pwd == new_pwd:
                    user = User.objects.get(u_id=id)
                    user.u_password = res_pwd
                    print(res_pwd)
                    user.save()
                    return redirect('/login/')
                else:
                    print(user.id)
                    return render(request,'cgpwd.html',{'msg':'重复密码错误！','user':user})
            else:
                print(user.id)
                return render(request, 'cgpwd.html', {'msg': '密码错误！','user':user})

    else:
        return render(request,'login.html')


def cgheader(request):
    if request.session.get('id'):
        id = request.session.get('id')
        if request.method == 'GET':
            user = User.objects.get(u_id=id)
            return render(request,'cgheader.html',{'user':user})
        else:
            user = User.objects.get(u_id=id)
            user.u_header = request.FILES.get('header')
            user.save()
            return render(request,'cgheader.html',{'user':user})
    else:
        return redirect('/login/')


def btext(request):
    id = request.session.get('id')
    user = User.objects.filter(u_id=id).first()

    return render(request,'blog_text.html',{'user':user})


def vip_account(request):
    creat_page = request.GET.get('page')
    if request.method == 'GET':
        accounts = AccountVip.objects.all().order_by('id')
        u_id = request.session.get('id')
        user = User.objects.get(u_id=u_id)
        # accounts = AccountVip.objects.all().order_by('web_name')
        # for i in accounts:
        #     print('****************************')
        #     print(i.id)
        paginator = Paginator(accounts,4)
        try:
            posts = paginator.page(creat_page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        data ={
            # 'accounts': accounts,
            'creat_page': int(creat_page),
            'user': user,
            'posts':posts
        }
        # print('******************************************')
        # print(type(creat_page))
        # for num in posts.paginator.page_range:
        #     print(type(num))
        return render(request,'vip_account.html',data)
    else:
        accounts = AccountVip.objects.all().order_by('id')
        account = AccountVip()
        name = request.POST.get('name')
        v_user = request.POST.get('user')
        v_pwd = request.POST.get('pwd')
        if name != '' and v_user != '' and v_pwd != '':
            account.web_name = request.POST.get('name')
            account.v_user = request.POST.get('user')
            account.v_passwd = request.POST.get('pwd')
            account.save()
        else:
            pass
        u_id = request.session.get('id')
        user = User.objects.get(u_id=u_id)
        paginator = Paginator(accounts,4)
        try:
            posts = paginator.page(creat_page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        data ={
            # 'accounts': accounts,
            'creat_page': int(creat_page),
            'user': user,
            'posts':posts
        }
        # print('******************************************')
        # # print(type(creat_page))
        # for num in posts.paginator.page_range:
        #     print(type(num))
        return render(request, 'vip_account.html', data)