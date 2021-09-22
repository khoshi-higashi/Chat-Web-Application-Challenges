
from django.core.checks import messages
from django.db.models.base import ModelBase
from . import models
import datetime
import pytz
from pytz import timezone
from django.http import JsonResponse
import json
import urllib.parse

######################################
# チャットの発言リストを取得する
######################################
def getChatMessage(request, id=None):
    #========================================================
    # 以下のuser_name, user, targetをNoneではなくそれぞれのコメントにしたがって値を取得する

    # [10-1-1] クッキーからユーザ名を取得
    user_name = request.COOKIES.get('USER')
    japanese = urllib.parse.unquote(user_name)

    # [10-1-2] データベースからユーザ名が一致するユーザ情報を取得
    # user = models.User.objects.filter(name__exact=user_name).first()
    user = models.User.objects.filter(name__exact=japanese).first()

    # [10-1-3] idが一致するルーム情報を取得
    target = models.Chatroom.objects.get(id=id)

    #========================================================

    # 日付を取得
    today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))     # タイムゾーンの生成
    display_date = today.strftime("%Y/%m/%d %H:%M")

    # ルーム情報が取得できない場合エラーを返す
    if target is None:
        return JsonResponse({"log":[{"user":"System","date":display_date,"message":"ルーム情報が取得できませんでした．"}]})

    # チャットの全てのログを返す
    json_message = getChatMessageByJson(id)
    return JsonResponse(json_message)


######################################
# 投稿メッセージを保存する
######################################
def submitChatMessage(request, id=None):
    #========================================================
    # 以下のuser_name, user, targetをNoneではなくそれぞれのコメントにしたがって値を取得する

    # [9-4-1] クッキー情報からユーザ名を取得
    user_name = request.COOKIES.get('USER')
    japanese = urllib.parse.unquote(user_name)

    # [9-4-2] データベースからユーザ名が一致するユーザ情報を取得
    user = models.User.objects.filter(name__exact=japanese).first()

    # [9-4-3] idが一致するルーム情報を取得
    target = models.Chatroom.objects.get(id=id)

    #========================================================

    # 日付を取得
    today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))     # タイムゾーンの生成
    # display_date = today.strftime("%Y/%m/%d %H:%M")
    display_date = today.strftime("%Y-%m-%d %H:%M")

    # メッセージを取得
    if "message" in request.GET:
        message = request.GET.get("message")
    else:
        message = None
    # 投稿メッセージが無い(Noneまたは空)なら何もせずにログを返して終了
    if message is None or len(message) == 0:
        json_message = getChatMessageByJson(id)
        return JsonResponse(json_message)

    # メッセージの保存
    if target is not None and user is not None:
        #========================================================
        # [9-4-4] 新たなログデータを作成しメッセージをChatLogに保存する
        newData = models.ChatLog.objects.create(
            chatroom  =  target,
            user  =  user,
            message  =  message,
            date  =  display_date
        ) # Noneは消して、正しく書き直す

        # データベースに保存する
        newData.save()
        #========================================================
    else:
        return JsonResponse({"log":[{"user":"System","date":display_date,"message":"指定されたルームまたはユーザが存在しません．"}]})

    # チャットの全てのログを返す
    json_message = getChatMessageByJson(id)
    return JsonResponse(json_message)



######################################
# チャットの発言を削除する
######################################
def deleteChatMessage(request, id=None):
    # 削除対象のメッセージIDを取得
    if "mes_id" in request.GET:
        mes_id = request.GET.get("mes_id")

    #========================================================
    # 以下のuser_name, user, target_messageをNoneではなくそれぞれのコメントにしたがって値を取得する

    # [13-3-1] クッキー情報からユーザ名を取得
    user_name = request.COOKIES.get('USER')
    japanese = urllib.parse.unquote(user_name)

    # [13-3-2] データベースからユーザ名が一致するユーザ情報を取得
    user = models.User.objects.filter(name__exact=japanese).first()

    # [13-3-3] 削除対象のメッセージIDと一致するメッセージをChatLogから取得
    target_message = models.ChatLog.objects.get(id=mes_id)

    #========================================================

    # 日付を取得
    today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))     # タイムゾーンの生成
    display_date = today.strftime("%Y/%m/%d %H:%M")

    # メッセージがないか、ユーザが異なるならば何もしない
    if target_message is None:
        return JsonResponse({"log":[{"user":"System","date":display_date,"message":"削除対象が見つかりませんでした．"}]})
    if target_message.user != user :
        return JsonResponse({"log":[{"user":"System","date":display_date,"message":"削除権限がありません．"}]})

    #========================================================
    # [13-3-4] 対象メッセージを削除
    models.ChatLog.objects.filter(id__exact=target_message.id).delete()

    #========================================================

    # 削除後のチャットメッセージを返す
    json_message = getChatMessageByJson(id)
    return JsonResponse(json_message)


######################################
# チャットの発言すべてをJSON形式のデータとして返す
######################################
def getChatMessageByJson(id=None):
    # 空の出力で初期化
    json_output = "{}"

    if id is not None:
        # ルーム情報を取得 (Roomをmodels.pyで定義した名前に揃える)
        target = models.Chatroom.objects.get(id=id)

        # JSON形式のテキスト
        json_output = "{"

        # メッセージを取得 (ChatLogをmodels.pyで定義した名前に揃える)
        messages = models.ChatLog.objects.filter(chatroom__exact=target).all()

        # ルームID
        json_output += "\"id\":\"" + str(id) +"\","

        if messages is not None:
            # リストの先頭を挿入
            json_output += "\"log\":["

            ####繰り返し文####
            for mes in messages:
                # 初期化
                user_data = None
                username = None

                # 投稿日時のフォーマットを変更
                submited_date = mes.date
                jst_date = submited_date.astimezone(timezone('Asia/Tokyo'))
                display_date = jst_date.strftime("%Y/%m/%d %H:%M")

                # 週のコラムの先頭
                json_output += "{"

                #========================================================
                # [10-2] ログデータmesに基づいて、logのデータを生成
                json_output += "\"id\":\"" + str(mes.id) + "\"," + "\"user\":\"" + str(mes.user) + "\"," + "\"date\":\"" + str(display_date) + "\"," + "\"message\":\"" + str(mes.message) + "\","



                #========================================================

                # 末尾のコンマを取り除く
                json_output = json_output.rstrip(",")

                # 週のコラムの末尾
                json_output += "},"

            # 末尾のコンマを取り除く
            json_output = json_output.rstrip(",")
            # リストの末尾を挿入
            json_output += "]}"
            # 改行の除去
            json_output.replace('\n','')
        else:
            # 末尾のコンマを取り除く
            json_output = json_output.rstrip(",")
            # リストの末尾を挿入
            json_output += "}"
            # 改行の除去
            json_output.replace('\n','')

    # 生成したJsonデータを返す
    return json.loads(json_output)


######################################
# アクセスログを更新する(チャレンジ課題のサンプル)
######################################

def updateAccessLog(room, user):
    # ユーザのアクセスログを取得する
    accessLog = accessLog = models.AccessLog.objects.filter(chatroom__exact=room,user__exact=user).last()

    # アクセスログが無い場合は新規に作成
    if accessLog is None:
        accessLog = models.AccessLog.objects.create(
            # レポート
            chatroom = room,
            # ユーザ名
            user = user,
        )

    # 保存する(既存データも再保存→最終アクセス時刻が更新)
    accessLog.save()

    # 成功を返す
    return True
