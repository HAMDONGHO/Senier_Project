from django.db import models

# Create your models here.

class EnoB_user(models.Model):
    
    email = models.EmailField(verbose_name='사용자이메일',primary_key=True)
    password = models.CharField(max_length=64,
                                verbose_name='비밀번호')
    username = models.CharField(max_length=32,
                                verbose_name='사용자이름')
    phone = models.CharField(max_length=32,
                                verbose_name='사용자번호')
    birth = models.CharField(max_length=32,verbose_name='사용자생일')
    sex = models.CharField(max_length=16,
                                verbose_name='성별')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                verbose_name='등록시간')
    
    class Meta:
        db_table = 'EnoB_User'
        verbose_name = 'EnoB 사용자'
        verbose_name_plural = 'EnoB 사용자'