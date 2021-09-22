from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
  name = models.CharField(max_length=20, null=False, blank=False)
  password = models.CharField(max_length=20, null=False, blank=False)
  islogin = models.BooleanField(default=False)
  def __str__(self):
    return self.name

class Chatroom(models.Model):
  name = models.TextField(null=False, blank=False)
  def __str__(self):
    return self.name

class ChatLog(models.Model):
  chatroom = models.ForeignKey('Chatroom', on_delete=models.PROTECT, null=False)
  user = models.ForeignKey('User', on_delete=models.PROTECT, null=False)
  message = models.TextField(verbose_name='メッセージ', blank=True, null=False)
  date = models.DateTimeField(verbose_name= '投稿日時', default=timezone.now)

############################################################
# チャットのアクセスログ
############################################################
# class AccessLog(models.Model):
#   # ルーム
#   chatroom = models.ForeignKey('Chatroom', on_delete=models.PROTECT, null=False)
#   # ユーザ
#   user = models.ForeignKey('User', on_delete=models.PROTECT, null=False)
#   # 最終アクセス(現在時刻で常に更新)
#   date = models.DateTimeField(verbose_name= '最終アクセス', auto_now=True)