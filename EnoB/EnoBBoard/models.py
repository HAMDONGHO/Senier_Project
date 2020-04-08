from django.db import models

# Create your models here.
class EnoB_Board(models.Model):
    board_id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=128,
                                verbose_name='제목')

    contents = models.TextField(verbose_name='내용')

    writer = models.ForeignKey('EnoBUser.EnoB_user', on_delete=models.CASCADE,
                                verbose_name='글쓴이')
    
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                            verbose_name='등록시간')
    

    class Meta:
        db_table = 'EonB_Board'
        verbose_name = 'EnoB 게시글'
        verbose_name_plural = 'EnoB 게시글'

