from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin
from aliyun_blog.models import User

class UserAuthMiddle(MiddlewareMixin):

    def process_request(self,request):
        white_path = ['/main/','/login/','/regist/','/']

        if request.path not in white_path:
            id = request.session.get('id')
            if not id:
                return redirect('/login/')
            else:
                user = User.objects.filter(u_id=id).first()
                if user:
                   return None

                else:
                    return redirect('login/')
        else:
            return None