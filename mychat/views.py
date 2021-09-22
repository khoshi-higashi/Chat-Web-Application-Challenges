from django.http import response
from django.shortcuts import render

from django.shortcuts import redirect
from django.views.generic import ListView
from . import models

from django.shortcuts import redirect
import urllib.parse

from django.db.models.base import ModelBase
import datetime
import pytz
from pytz import timezone
from django.http import JsonResponse
import json
# Create your views here.

######################################
# スタート画面表示
######################################
def startView(request):
  # 展開される出力画面のテンプレートファイル
  template_file = "mychat/start.html"
  # 受け渡しデータ
  options = {}
  return render(request, template_file, options)

######################################
# メイン画面表示
######################################
def mainView(request):
  # 展開される出力画面のテンプレートファイル
  template_file = "mychat/main.html"

  roomlist = models.Chatroom.objects.all()

  # 受け渡しデータ
  options = {
    'roomlist':roomlist
  }

  # クッキー情報から取得
  value = request.COOKIES.get('USER')
  # クッキー情報から取得できたとき
  if value is not None:
    # 日本語に対応する処理
    japanese = urllib.parse.unquote(value)
    if japanese is not None:
      # ユーザ情報を取得
      target = models.User.objects.filter(name__exact=japanese).first()
      # ログイン中のユーザを削除したとき
      if target.name == "###":
        # 一時的に作った"###"というユーザ情報を削除する
        models.User.objects.filter(name__exact="###").delete()
        response = render(request, "mychat/start.html", options)
        # クッキー情報からも一時的に作った"###"を削除する
        response.delete_cookie("USER")
        return response
      # ログイン情報がTrueのとき
      elif target.islogin == True:
        return render(request, template_file, options)
      else:
        response = render(request, "mychat/start.html", options)
        response.delete_cookie("USER")
        return response


  # フォームからデータを取得
  if "name" in request.POST:
    user = request.POST.get("name")
  if "password" in request.POST:
    password = request.POST.get("password")
  if "login" in request.POST:
    login = request.POST.get("login")

  if request.POST.get("login") != "on":
    return render(request, "mychat/start.html", options)

  # エラーメッセージ
  error_message = []

  # 入力エラーチェック
  if user is None or user == '':
    error_message.append("名前が入力されていません")
  if password is None or password == '':
    error_message.append("パスワードが入力されていません")

  # エラーがあったら入力画面に差し戻す
  if len(error_message) > 0:
    errors = {'error_message':error_message}
    return render(request, "mychat/start.html", errors)

  user_target = models.User.objects.filter(name__exact=user, password__exact=password).first()

  if user_target is None:
    error_message.append("ユーザ名，パスワードが一致しません")
    errors = {'error_message':error_message}
    return render(request, "mychat/start.html", errors)
  else:
    user_target.islogin = True
    user_target.save()
    response = render(request, template_file, options)
    response.set_cookie('USER', urllib.parse.quote(user))
    # response.set_cookie('USER', user) # key, value は保存したいキー名と値
    return response

  return render(request, template_file, options)

######################################
# クリエイト・ユーザー画面表示
######################################
def createUser(request):
  # 展開される出力画面のテンプレートファイル
  template_file = "mychat/createuser.html"
  # 受け渡しデータ
  options = {}
  return render(request, template_file, options)

######################################
# アッド・ユーザー画面表示
######################################
def addUser(request):
  # 展開される出力画面のテンプレートファイル
  template_file = "mychat/adduser.html"
  # エラーがあったときは入力画面に戻す
  back_file = "mychat/createuser.html"

  # エラーメッセージ
  error_message = []
  result_message = []

  # フォームからデータを取得
  if "name" in request.POST:
    name = request.POST.get("name")
  if "password" in request.POST:
    password = request.POST.get("password")

  # 入力エラーチェック
  if name is None or name == '':
    error_message.append("名前が入力されていません")
  if password is None or password == '':
    error_message.append("パスワードが入力されていません")

  # ユーザ名がnameのデータを抽出
  if len(error_message) == 0:
    if name is not None or name != "" and password is not None or password != "":
      target = models.User.objects.filter(name__exact=name).first()
      if target is not None:
        error_message.append("ユーザ" + name + "は既に登録済みです")
      else:
        # 新規にプロフィールデータを作成する
        newdata  =  models.User.objects.create(
          name  =  name,
          password  =  password,
        )
        # データベースに保存する
        newdata.save()
        result_message.append("ユーザ" + name + "を登録しました")

  # 受け渡しデータ
  options = {
    'error_message':error_message,
    'result_message':result_message
    }

  return render(request, template_file, options)

######################################
# クリエイト・ルーム画面表示
######################################
def createRoom(request):
  # 展開される出力画面のテンプレートファイル
  template_file = "mychat/createroom.html"
  # 受け渡しデータ
  options = {}
  return render(request, template_file, options)

######################################
# アッド・ルーム画面表示
######################################
def addRoom(request):
  # 展開される出力画面のテンプレートファイル
  template_file = "mychat/addroom.html"

  if "name" in request.POST:
    name = request.POST.get("name")

  error_message = []
  result_message = []

  if name is None or name == "":
    error_message.append("ルーム名が未記入です")
  else:
    target = models.Chatroom.objects.filter(name__exact=name).first()
    if target is not None:
      error_message.append("ルーム" + name + "は既に存在します")
    else:
      newdata = models.Chatroom.objects.create(name  =  name)
      newdata.save()
      result_message.append("ルーム" + name + "を作成しました")

  # 受け渡しデータ
  options = {
    'error_message':error_message,
    'result_message':result_message
  }
  return render(request, template_file, options)

######################################
# ログアウト画面表示
######################################
def logout(request):
  # 展開される出力画面のテンプレートファイル
  template_file = "mychat/start.html"

  value = request.COOKIES.get('USER')
  if value is not None:
    cookie_value = urllib.parse.unquote(value)
    target = models.User.objects.filter(name__exact=cookie_value).first()
    target.islogin = False
    target.save()
    return redirect('/mychat')

  # 受け渡しデータ
  options = {}
  return render(request, template_file, options)

######################################
# チャット画面表示
######################################
def chatView(request, id=None):
  # 展開される出力画面のテンプレートファイル
  template_file = "mychat/chat.html"

  # idが指定されている場合はデータを取得
  if id is not None:
    data = models.Chatroom.objects.get(id=id)
  else:
    data = None

  #-------------------------------
  # 連想配列の生成
  #-------------------------------
  if data is not None:
    options = {
      'data':data
    }
  else:
    options = {
    }

  return render(request, template_file, options)

######################################
# 削除ルーム画面表示
######################################
def deleteRoom(request):
  # 展開される出力画面のテンプレートファイル
  template_file = "mychat/deleteroom.html"

  roomlist = models.Chatroom.objects.all()

  # 受け渡しデータ
  options = {
    'roomlist':roomlist
  }
  return render(request, template_file, options)

######################################
# 削除ルーム画面表示
######################################
def delete(request):
  # 展開される出力画面のテンプレートファイル
  template_file = "mychat/delete.html"

  # フォームからデータを取得
  if "roomid" in request.POST:
    id = request.POST.get("roomid")

  target = models.Chatroom.objects.filter(id__exact=id).first()
  # target = models.Chatroom.objects.filter(id__in=id).first()

  value = target.name

  # 受け渡しデータ
  options = {
    'target':value
  }
  # 対象のチャットルーム（ひとつ）のチャットログをすべて削除
  models.ChatLog.objects.filter(chatroom__exact=target).delete()
  # チャットルーム（ひとつ）削除
  models.Chatroom.objects.filter(id__exact=id).delete()
  # models.Chatroom.objects.filter(id__in=id).delete()
  return render(request, template_file, options)

######################################
# 削除ユーザ画面表示
######################################
def deleteUser(request):
  # 展開される出力画面のテンプレートファイル
  template_file = "mychat/deleteuser.html"

  userlist = models.User.objects.all()

  # 受け渡しデータ
  options = {
    'userlist':userlist
  }
  return render(request, template_file, options)

######################################
# 削除ユーザ画面表示
######################################
def deleteUserResult(request):
  # 展開される出力画面のテンプレートファイル
  template_file = "mychat/deleteuserresult.html"

  # フォームからデータを取得
  if "userid" in request.POST:
    id = request.POST.get("userid")

  # 選択したユーザを取得
  target = models.User.objects.filter(id__exact=id).first()

  value = target.name

  # 受け渡しデータ
  options = {
    'target':value
  }

  # 選択したユーザのチャットログを削除
  models.ChatLog.objects.filter(user__exact=target).delete()
  # models.ChatLog.objects.filter(user__in=target).delete()
  # 選択したユーザのユーザ情報を削除
  models.User.objects.filter(id__exact=id).delete()
  # models.User.objects.filter(id__in=id).delete()
  # ログイン中のユーザを削除したとき
  if target.name == request.COOKIES.get('USER'):
    response = render(request, template_file, options)
    # クッキー情報を"###"にする
    response.set_cookie("USER", "###")
    # "###"というユーザ情報を作る
    newdata = models.User.objects.create(
      name = "###",
      password = "###",
    )
    newdata.save
    return response
  response = render(request, template_file, options)
  return response