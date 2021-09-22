from django.urls import path
from . import views, chat

app_name = 'mychat'
urlpatterns = [
  # ログイン認証処理（ログイン画面＆メイン画面）
  path('', views.mainView, name='main'),
  path('createuser', views.createUser, name='createuser'),
  path('adduser', views.addUser, name='adduser'),
  path('createroom', views.createRoom, name='createroom'),
  path('addroom', views.addRoom, name='addroom'),
  path('logout', views.logout, name='logout'),
  path('chat/<int:id>', views.chatView, name='chat'),
  # チャット処理１：全メッセージの取得
  path('getChatMessage/<int:id>', chat.getChatMessage, name='getChatMessage'),
  # チャット処理２：新規メッセージの投稿
  path('submitChatMessage/<int:id>', chat.submitChatMessage, name='submitChatMessage'),
  # チャット処理３：指定メッセージの削除
  path('deleteChatMessage/<int:id>', chat.deleteChatMessage, name='deleteChatMessage'),

  path('deleteroom', views.deleteRoom, name='deleteroom'),
  path('delete', views.delete, name='delete'),

  path('deleteuser', views.deleteUser, name='deleteuser'),
  path('deleteuserresult', views.deleteUserResult, name='deleteuserresult'),
]