from django.db import models

# Create your models here.

class User(models.Model):
    '''
    uid
    uname
    sex
    header
    pwd
    qq
    email
    '''
    u_id = models.CharField(max_length=128)
    u_name = models.CharField(max_length=256)
    u_sex = models.CharField(max_length=32)
    u_header = models.ImageField(upload_to='./static/headers')
    create_time = models.DateTimeField(auto_now_add=True) #创建时间不再改动
    change_time = models.DateTimeField(auto_now=True)  #修改时间
    u_password = models.CharField(max_length=512)
    u_qq = models.IntegerField()
    u_email = models.EmailField()

    class Meta:
        db_table = 'al_user'




class BlogText(models.Model):
    '''
    t_id
    t_title
    t_center
    is_del
    '''
    t_id = models.IntegerField(primary_key=True)
    t_title = models.CharField(max_length=64,unique=True)#标题唯一
    t_center = models.TextField()
    is_del = models.BooleanField(default=False)
    user = models.ForeignKey("User")

    class Meta:
        db_table = 'al_blog_text'




class AccountVip(models.Model):
    web_name = models.CharField(max_length=128)
    v_user = models.CharField(max_length=128)
    v_passwd = models.CharField(max_length=128)

    class Meta:
        db_table = 'account_vip'



