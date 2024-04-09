from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from pathlib import Path
import openpyxl
import datetime
import math
import os
import environ
from ..models import member
from ..models import Business_Time_graph
from ..models import kosu_division
from ..models import team_member
from ..models import administrator_data
from ..forms import loginForm
from ..forms import administrator_data_Form
from ..forms import uploadForm




#--------------------------------------------------------------------------------------------------------





# ログイン画面定義
def login(request):

  # POST時の処理
  if (request.method == 'POST'):

    # POST送信された値を変数に入れる
    find = request.POST['employee_No4']

    # POST送信された値が空の場合の処理
    if find == '':
      # エラーメッセージ出力
      messages.error(request, '従業員番号を入力して下さい。ERROR001')
      # このページをリダイレクト
      return redirect(to = '/login')
    

    # 人員登録データの内、従業員番号がPOST送信された値と等しいレコードのオブジェクトを取得
    data = member.objects.filter(employee_No = find)


    # POST送信された値が人員登録の中にない場合
    if data.count() == 0:
      # エラーメッセージ出力
      messages.error(request, '入力された従業員番号は登録がありません。ERROR002')
      # このページをリダイレクト
      return redirect(to = '/login')
    
    # POST送信された値が人員登録の中にいる場合
    if data.count() >= 1:
      # 従業員番号をセッションに保存する
      request.session['login_No'] = find
      # 使用する工数区分を読み込む(最新のもの)
      def_Ver = kosu_division.objects.order_by("id").last()
      request.session['input_def'] = def_Ver.kosu_name

      # メインページに飛ぶ
      return redirect(to = '/')
   

   
  # HTMLに渡す辞書
  library_m = {
    'title' : 'ログイン',
    'form' : loginForm(),
    }
  
  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/login.html', library_m)





#--------------------------------------------------------------------------------------------------------





# メイン画面定義
def main(request):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')

  # ログイン者の情報取得
  data = member.objects.get(employee_No = request.session.get('login_No', None))



  # POST時の処理
  if (request.method == 'POST'):

    # セッションを削除
    request.session.flush()

    # ログインページに飛ぶ
    return redirect(to = '/login')



  # HTMLに渡す辞書
  library_m = {
    'title' : 'MENU',
    'data' : data,
    }
  


  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/main.html', library_m)





#--------------------------------------------------------------------------------------------------------





# 工数メイン画面定義
def kosu_main(request):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:

    return redirect(to = '/login')


  # ログイン者の情報取得
  data = member.objects.get(employee_No = request.session.get('login_No', None))



  # HTMLに渡す辞書
  library_m = {
    'title' : '工数MENU',
    'data' : data,
    }
  


  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/kosu_main.html', library_m)





#--------------------------------------------------------------------------------------------------------





# 工数区分定義メイン画面定義
def def_main(request):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:

    return redirect(to = '/login')

  # ログイン者の情報取得
  data = member.objects.get(employee_No = request.session.get('login_No', None))



  # HTMLに渡す辞書
  library_m = {
    'title' : '工数区分定義MENU',
    'data' : data,
    }
  


  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/def_main.html', library_m)





#--------------------------------------------------------------------------------------------------------





# 人員メイン画面定義
def member_main(request):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:

    return redirect(to = '/login')

  # ログイン者の情報取得
  data = member.objects.get(employee_No = request.session.get('login_No', None))

  # ログイン者に権限がなければメインページに戻る
  if data.authority == False:

    return redirect(to = '/')
  


  # HTMLに渡す辞書
  library_m = {
    'title' : '人員MENU',
    'data' : data,
    }
  


  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/member_main.html', library_m)





#--------------------------------------------------------------------------------------------------------





# 班員メイン画面定義
def team_main(request):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:

    return redirect(to = '/login')


  # ログイン者の情報取得
  data = member.objects.get(employee_No = request.session.get('login_No', None))


  # ログイン者に権限がなければメインページに戻る
  if data.authority == False:

    return redirect(to = '/')
  


  # HTMLに渡す辞書
  library_m = {
    'title' : '班員MENU',
    'data' : data,
    }



  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/team_main.html', library_m)





#--------------------------------------------------------------------------------------------------------





# 管理者画面定義
def administrator_menu(request):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:

    return redirect(to = '/login')


  # ログイン者の情報取得
  data = member.objects.get(employee_No = request.session.get('login_No', None))


  # ログイン者が管理者でなければメインページに戻る
  if data.administrator == False:

    return redirect(to = '/')


  # 設定データ取得
  default_data = administrator_data.objects.order_by("id").last()

  # 設定データの最新のレコードのID取得
  record_id = default_data.id


  # フォーム初期値
  form_default = {'menu_row' : default_data.menu_row, 'file_location_P' : default_data.file_location_P, \
                  'file_location_R' : default_data.file_location_R, 'file_location_W1' : default_data.file_location_W1, \
                    'file_location_W2' : default_data.file_location_W2, 'file_location_T1' : default_data.file_location_T1, \
                      'file_location_T2' : default_data.file_location_T2, 'file_location_A1' : default_data.file_location_A1, \
                        'file_location_A2' : default_data.file_location_A2, 'backup_file' : default_data.backup_file}
  
  # フォームに初期値を入れて定義
  form = administrator_data_Form(form_default)



  # 設定更新時の処理
  if 'registration' in request.POST:

    # 一覧表示項目数が自然数でない場合のエラー出力
    if math.floor(float(request.POST['menu_row'])) != float(request.POST['menu_row']) or \
      float(request.POST['menu_row']) <= 0:
      # エラーメッセージ出力
      messages.error(request, '一覧表示項目数は自然数で入力して下さい。ERROR029')
      # このページをリダイレクト
      return redirect(to = '/administrator')

    # 登録したフォルダーがない場合の処理
    if os.path.isdir(request.POST['file_location_P']) == False:
      # エラーメッセージ出力
      messages.error(request, 'Pショップの登録しようとした保存場所は存在しません。ERROR030')
      # このページをリダイレクト
      return redirect(to = '/administrator')

    # 登録したフォルダーがない場合の処理
    if os.path.isdir(request.POST['file_location_R']) == False:
      # エラーメッセージ出力
      messages.error(request, 'Rショップの登録しようとした保存場所は存在しません。ERROR031')
      # このページをリダイレクト
      return redirect(to = '/administrator')

    # 登録したフォルダーがない場合の処理
    if os.path.isdir(request.POST['file_location_W1']) == False:
      # エラーメッセージ出力
      messages.error(request, 'W1ショップの登録しようとした保存場所は存在しません。ERROR032')
      # このページをリダイレクト
      return redirect(to = '/administrator')

    # 登録したフォルダーがない場合の処理
    if os.path.isdir(request.POST['file_location_W2']) == False:
      # エラーメッセージ出力
      messages.error(request, 'W2ショップの登録しようとした保存場所は存在しません。ERROR033')
      # このページをリダイレクト
      return redirect(to = '/administrator')
    
    # 登録したフォルダーがない場合の処理
    if os.path.isdir(request.POST['file_location_T1']) == False:
      # エラーメッセージ出力
      messages.error(request, 'T1ショップの登録しようとした保存場所は存在しません。ERROR034')
      # このページをリダイレクト
      return redirect(to = '/administrator')

    # 登録したフォルダーがない場合の処理
    if os.path.isdir(request.POST['file_location_T2']) == False:
      # エラーメッセージ出力
      messages.error(request, 'T2ショップの登録しようとした保存場所は存在しません。ERROR035')
      # このページをリダイレクト
      return redirect(to = '/administrator')

    # 登録したフォルダーがない場合の処理
    if os.path.isdir(request.POST['file_location_A1']) == False:
      # エラーメッセージ出力
      messages.error(request, 'A1ショップの登録しようとした保存場所は存在しません。ERROR036')
      # このページをリダイレクト
      return redirect(to = '/administrator')

    # 登録したフォルダーがない場合の処理
    if os.path.isdir(request.POST['file_location_A2']) == False:
      # エラーメッセージ出力
      messages.error(request, 'A2ショップの登録しようとした保存場所は存在しません。ERROR037')
      # このページをリダイレクト
      return redirect(to = '/administrator')
    
    # 登録したフォルダーがない場合の処理
    if os.path.isdir(request.POST['backup_file']) == False:
      # エラーメッセージ出力
      messages.error(request, 'バックアップ場所で登録しようとした保存場所は存在しません。ERROR038')
      # このページをリダイレクト
      return redirect(to = '/administrator')

    # レコードにPOST送信された値を上書きする
    administrator_data.objects.update_or_create(id = record_id, \
        defaults = {'menu_row' : request.POST['menu_row'], \
                    'file_location_P' : request.POST['file_location_P'], \
                    'file_location_R' : request.POST['file_location_R'], \
                    'file_location_W1' : request.POST['file_location_W1'], \
                    'file_location_W2' : request.POST['file_location_W2'], \
                    'file_location_T1' : request.POST['file_location_T1'], \
                    'file_location_T2' : request.POST['file_location_T2'], \
                    'file_location_A1' : request.POST['file_location_A1'], \
                    'file_location_A2' : request.POST['file_location_A2'], \
                    'backup_file' : request.POST['backup_file'], \
                    })
    
    # フォームにPOST値を入れて定義
    form = administrator_data_Form(request.POST)



  # 工数情報バックアップ処理
  if 'kosu_backup' in request.POST:

    # 日付指定空の場合の処理
    if request.POST['data_day'] == '':

      # エラーメッセージ出力
      messages.error(request, 'バックアップする日付を指定してください。ERROR022')

      # このページをリダイレクト
      return redirect(to = '/administrator')


    # 新しいExcelブック作成
    wb = openpyxl.Workbook()

    # 書き込みシート選択
    ws = wb.worksheets[0]

    # 工数データ取得
    kosu_gurahu = Business_Time_graph.objects.filter(work_day2__lte = request.POST['data_day'])


    # Excelに書き込み(項目名)
    ws.cell(row = 1, column = 1, value = '従業員番号')
    ws.cell(row = 1, column = 2, value = '氏名')
    ws.cell(row = 1, column = 3, value = '工数区分定義Ver')
    ws.cell(row = 1, column = 4, value = '就業日')
    ws.cell(row = 1, column = 5, value = '直')
    ws.cell(row = 1, column = 6, value = '作業内容')
    ws.cell(row = 1, column = 7, value = '作業詳細')
    ws.cell(row = 1, column = 8, value = '残業時間')
    ws.cell(row = 1, column = 9, value = '昼休憩時間')
    ws.cell(row = 1, column = 10, value = '残業休憩時間1')
    ws.cell(row = 1, column = 11, value = '残業休憩時間2')
    ws.cell(row = 1, column = 12, value = '残業休憩時間3')
    ws.cell(row = 1, column = 13, value = '就業形態')
    ws.cell(row = 1, column = 14, value = '工数出力済')
    ws.cell(row = 1, column = 15, value = '工数入力OK_NG')


    # Excelに書き込み(項目)
    for index, dt in enumerate(kosu_gurahu):
      ws.cell(row = index + 2, column = 1, value = dt.employee_No3)
      ws.cell(row = index + 2, column = 2, value = dt.name)
      ws.cell(row = index + 2, column = 3, value = dt.def_Ver2)
      ws.cell(row = index + 2, column = 4, value = dt.work_day2)
      ws.cell(row = index + 2, column = 5, value = dt.tyoku2)
      ws.cell(row = index + 2, column = 6, value = dt.time_work)
      ws.cell(row = index + 2, column = 7, value = dt.detail_work)
      ws.cell(row = index + 2, column = 8, value = dt.over_time)
      ws.cell(row = index + 2, column = 9, value = dt.breaktime)
      ws.cell(row = index + 2, column = 10, value = dt.breaktime_over1)
      ws.cell(row = index + 2, column = 11, value = dt.breaktime_over2)
      ws.cell(row = index + 2, column = 12, value = dt.breaktime_over3)
      ws.cell(row = index + 2, column = 13, value = dt.work_time)
      ws.cell(row = index + 2, column = 14, value = dt.completion)
      ws.cell(row = index + 2, column = 15, value = dt.judgement)

    wb.save(r'{}\{}_工数データバックアップ.xlsx'.format(default_data.backup_file, request.POST['data_day']))



  # 工数データ読み込み
  if 'kosu_load' in request.POST:

    # POSTされたファイルパスを変数に入れる
    file_path = request.POST['kosu_file']


    # 登録したファイルがない場合の処理
    if os.path.isfile(file_path) == False:

      # エラーメッセージ出力
      messages.error(request, 'ロードしようとしたファイルは存在しません。ERROR043')

      # このページをリダイレクト
      return redirect(to = 'administrator')


    # 指定Excelを開く
    wb = openpyxl.load_workbook('{}'.format(file_path), data_only = True)
    # 書き込みシート選択
    ws = wb.worksheets[0]


    # 読み込むファイルが正しいファイルでない場合の処理
    if ws.cell(1, 1).value != '従業員番号' or ws.cell(1, 2).value != '氏名' or \
      ws.cell(1, 3).value != '工数区分定義Ver' or ws.cell(1, 4).value != '就業日' or \
      ws.cell(1, 5).value != '直' or ws.cell(1, 6).value != '作業内容' or \
      ws.cell(1, 7).value != '作業詳細' or ws.cell(1, 8).value != '残業時間' or \
      ws.cell(1, 9).value != '昼休憩時間' or ws.cell(1, 10).value != '残業休憩時間1' or \
      ws.cell(1, 11).value != '残業休憩時間2' or ws.cell(1, 12).value != '残業休憩時間3' or \
      ws.cell(1, 13).value != '就業形態' or ws.cell(1, 14).value != '工数出力済' or \
      ws.cell(1, 15).value != '工数入力OK_NG':

      # エラーメッセージ出力
      messages.error(request, 'ロードしようとしたファイルは工数データバックアップではありません。ERROR048')
  
      # このページをリダイレクト
      return redirect(to = 'administrator')


    # レコード数取得
    data_num = ws.max_row


    # Excelからデータを読み込こむループ
    for i in range(1, data_num):

      # 読み込み予定データと同一の日のデータが存在するか確認
      del_data_filter = Business_Time_graph.objects.filter(employee_No3 = ws.cell(row = i + 1, column = 1).value, \
                                                           work_day2 = ws.cell(row = i + 1, column = 4).value)

      # 読み込み予定データと同一の日のデータが存在する場合の処理
      if del_data_filter.count() != 0:

        # 読み込み予定データと同一の日のデータを取得
        del_data_get = Business_Time_graph.objects.get(employee_No3 = ws.cell(row = i + 1, column = 1).value, \
                                                       work_day2 = ws.cell(row = i + 1, column = 4).value)
        
        # 読み込み予定データと同一の日のデータを削除
        del_data_get.delete()

      # Excelからデータを読み込こみ
      new_data = Business_Time_graph(employee_No3 = ws.cell(row = i + 1, column = 1).value, \
                                      name = ws.cell(row = i + 1, column = 2).value, \
                                      def_Ver2 = ws.cell(row = i + 1, column = 3).value, \
                                      work_day2 = ws.cell(row = i + 1, column = 4).value, \
                                      tyoku2 = ws.cell(row = i + 1, column = 5).value, \
                                      time_work = ws.cell(row = i + 1, column = 6).value, \
                                      detail_work = ws.cell(row = i + 1, column = 7).value, \
                                      over_time = ws.cell(row = i + 1, column = 8).value, \
                                      breaktime = ws.cell(row = i + 1, column = 9).value, \
                                      breaktime_over1 = ws.cell(row = i + 1, column = 10).value, \
                                      breaktime_over2 = ws.cell(row = i + 1, column = 11).value, \
                                      breaktime_over3 = ws.cell(row = i + 1, column = 12).value, \
                                      work_time = ws.cell(row = i + 1, column = 13).value, \
                                      completion = ws.cell(row = i + 1, column = 14).value, \
                                      judgement = ws.cell(row = i + 1, column = 15).value) 

      # レコードセーブ
      new_data.save()



  # 工数データ読み込み
  if 'kosu_delete' in request.POST:

    # 日付指定空の場合の処理
    if request.POST['data_day'] == '':

      # エラーメッセージ出力
      messages.error(request, '削除する日付を指定してください。ERROR023')

      # このページをリダイレクト
      return redirect(to = '/administrator')


    # 工数データ取得
    kosu_obj = Business_Time_graph.objects.filter(work_day2__lte = request.POST['data_day'])

    # 取得した工数データを削除
    kosu_obj.delete()



  # 人員情報バックアップ処理
  if 'member_backup' in request.POST:

    # 今日の日付取得
    today = datetime.date.today()

    # 新しいExcelブック作成
    wb = openpyxl.Workbook()
    # 書き込みシート選択
    ws = wb.worksheets[0]

    # 人員データ取得
    member_data = member.objects.all()

    # Excelに書き込み(項目名)
    ws.cell(row = 1, column = 1, value = '従業員番号')
    ws.cell(row = 1, column = 2, value = '氏名')
    ws.cell(row = 1, column = 3, value = 'ショップ')
    ws.cell(row = 1, column = 4, value = '権限')
    ws.cell(row = 1, column = 5, value = '管理者')
    ws.cell(row = 1, column = 6, value = '1直昼休憩時間')
    ws.cell(row = 1, column = 7, value = '1直残業休憩時間1')
    ws.cell(row = 1, column = 8, value = '1直残業休憩時間2')
    ws.cell(row = 1, column = 9, value = '1直残業休憩時間3')
    ws.cell(row = 1, column = 10, value = '2直昼休憩時間')
    ws.cell(row = 1, column = 11, value = '2直残業休憩時間1')
    ws.cell(row = 1, column = 12, value = '2直残業休憩時間2')
    ws.cell(row = 1, column = 13, value = '2直残業休憩時間3')
    ws.cell(row = 1, column = 14, value = '3直昼休憩時間')
    ws.cell(row = 1, column = 15, value = '3直残業休憩時間1')
    ws.cell(row = 1, column = 16, value = '3直残業休憩時間2')
    ws.cell(row = 1, column = 17, value = '3直残業休憩時間3')
    ws.cell(row = 1, column = 18, value = '常昼昼休憩時間')
    ws.cell(row = 1, column = 19, value = '常昼残業休憩時間1')
    ws.cell(row = 1, column = 20, value = '常昼残業休憩時間2')
    ws.cell(row = 1, column = 21, value = '常昼残業休憩時間3')

    # Excelに書き込み(項目)
    for index, dt in enumerate(member_data):
      ws.cell(row = index + 2, column = 1, value = dt.employee_No)
      ws.cell(row = index + 2, column = 2, value = dt.name)
      ws.cell(row = index + 2, column = 3, value = dt.shop)
      ws.cell(row = index + 2, column = 4, value = dt.authority)
      ws.cell(row = index + 2, column = 5, value = dt.administrator)
      ws.cell(row = index + 2, column = 6, value = dt.break_time1)
      ws.cell(row = index + 2, column = 7, value = dt.break_time1_over1)
      ws.cell(row = index + 2, column = 8, value = dt.break_time1_over2)
      ws.cell(row = index + 2, column = 9, value = dt.break_time1_over3)
      ws.cell(row = index + 2, column = 10, value = dt.break_time2)
      ws.cell(row = index + 2, column = 11, value = dt.break_time2_over1)
      ws.cell(row = index + 2, column = 12, value = dt.break_time2_over2)
      ws.cell(row = index + 2, column = 13, value = dt.break_time2_over3)
      ws.cell(row = index + 2, column = 14, value = dt.break_time3)
      ws.cell(row = index + 2, column = 15, value = dt.break_time3_over1)
      ws.cell(row = index + 2, column = 16, value = dt.break_time3_over2)
      ws.cell(row = index + 2, column = 17, value = dt.break_time3_over3)
      ws.cell(row = index + 2, column = 18, value = dt.break_time4)
      ws.cell(row = index + 2, column = 19, value = dt.break_time4_over1)
      ws.cell(row = index + 2, column = 20, value = dt.break_time4_over2)
      ws.cell(row = index + 2, column = 21, value = dt.break_time4_over3)

    wb.save(r'{}\{}_人員データバックアップ.xlsx'.format(default_data.backup_file, today))



  # 人員情報読み込み
  if 'member_load' in request.POST:

    # POSTされたファイルパスを変数に入れる
    file_path = request.POST['member_file']

    # 登録したファイルがない場合の処理
    if os.path.isfile(file_path) == False:
      # エラーメッセージ出力
      messages.error(request, 'ロードしようとしたファイルは存在しません。ERROR044')
      # このページをリダイレクト
      return redirect(to = 'administrator')

    # 指定Excelを開く
    wb = openpyxl.load_workbook('{}'.format(file_path), data_only = True)
    # 書き込みシート選択
    ws = wb.worksheets[0]

    if ws.cell(1, 1).value != '従業員番号' or ws.cell(1, 2).value != '氏名' or \
      ws.cell(1, 3).value != 'ショップ' or ws.cell(1, 4).value != '権限' or \
      ws.cell(1, 5).value != '管理者' or ws.cell(1, 6).value != '1直昼休憩時間' or \
      ws.cell(1, 7).value != '1直残業休憩時間1' or ws.cell(1, 8).value != '1直残業休憩時間2' or \
      ws.cell(1, 9).value != '1直残業休憩時間3' or ws.cell(1, 10).value != '2直昼休憩時間' or \
      ws.cell(1, 11).value != '2直残業休憩時間1' or ws.cell(1, 12).value != '2直残業休憩時間2' or \
      ws.cell(1, 13).value != '2直残業休憩時間3' or ws.cell(1, 14).value != '3直昼休憩時間' or \
      ws.cell(1, 15).value != '3直残業休憩時間1' or ws.cell(1, 16).value != '3直残業休憩時間2' or \
      ws.cell(1, 17).value != '3直残業休憩時間3' or ws.cell(1, 18).value != '常昼昼休憩時間' or \
      ws.cell(1, 19).value != '常昼残業休憩時間1' or ws.cell(1, 20).value != '常昼残業休憩時間2' or \
      ws.cell(1, 21).value != '常昼残業休憩時間3':

      # エラーメッセージ出力
      messages.error(request, 'ロードしようとしたファイルは人員情報バックアップではありません。ERROR049')
      # このページをリダイレクト
      return redirect(to = 'administrator')

    # レコード数取得
    data_num = ws.max_row

    # 人員情報を全て削除
    member_del = member.objects.all()
    member_del.delete()
    # Excelからデータを読み込み
    for i in range(1, data_num):
      new_data = member(employee_No = ws.cell(row = i + 1, column = 1).value, \
                        name = ws.cell(row = i + 1, column = 2).value, \
                        shop = ws.cell(row = i + 1, column = 3).value, \
                        authority = ws.cell(row = i + 1, column = 4).value, \
                        administrator = ws.cell(row = i + 1, column = 5).value, \
                        break_time1 = ws.cell(row = i + 1, column = 6).value, \
                        break_time1_over1 = ws.cell(row = i + 1, column = 7).value, \
                        break_time1_over2 = ws.cell(row = i + 1, column = 8).value, \
                        break_time1_over3 = ws.cell(row = i + 1, column = 9).value, \
                        break_time2 = ws.cell(row = i + 1, column = 10).value, \
                        break_time2_over1 = ws.cell(row = i + 1, column = 11).value, \
                        break_time2_over2 = ws.cell(row = i + 1, column = 12).value, \
                        break_time2_over3 = ws.cell(row = i + 1, column = 13).value, \
                        break_time3 = ws.cell(row = i + 1, column = 14).value, \
                        break_time3_over1 = ws.cell(row = i + 1, column = 15).value, \
                        break_time3_over2 = ws.cell(row = i + 1, column = 16).value, \
                        break_time3_over3 = ws.cell(row = i + 1, column = 17).value, \
                        break_time4 = ws.cell(row = i + 1, column = 18).value, \
                        break_time4_over1 = ws.cell(row = i + 1, column = 19).value, \
                        break_time4_over2 = ws.cell(row = i + 1, column = 20).value, \
                        break_time4_over3 = ws.cell(row = i + 1, column = 21).value)

      new_data.save()


  # 班員情報バックアップ処理
  if 'team_backup' in request.POST:

    # 今日の日付取得
    today = datetime.date.today()

    # 新しいExcelブック作成
    wb = openpyxl.Workbook()
    # 書き込みシート選択
    ws = wb.worksheets[0]

    # 班員データ取得
    team_data = team_member.objects.all()

    # Excelに書き込み(項目名)
    ws.cell(row = 1, column = 1, value = '従業員番号')
    ws.cell(row = 1, column = 2, value = '班員1')
    ws.cell(row = 1, column = 3, value = '班員2')
    ws.cell(row = 1, column = 4, value = '班員3')
    ws.cell(row = 1, column = 5, value = '班員4')
    ws.cell(row = 1, column = 6, value = '班員6')
    ws.cell(row = 1, column = 7, value = '班員7')
    ws.cell(row = 1, column = 8, value = '班員8')
    ws.cell(row = 1, column = 9, value = '班員9')
    ws.cell(row = 1, column = 10, value = '班員10')

    # Excelに書き込み(項目)
    for index, dt in enumerate(team_data):
      ws.cell(row = index + 2, column = 1, value = dt.employee_No5)
      ws.cell(row = index + 2, column = 2, value = dt.member1)
      ws.cell(row = index + 2, column = 3, value = dt.member2)
      ws.cell(row = index + 2, column = 4, value = dt.member3)
      ws.cell(row = index + 2, column = 5, value = dt.member4)
      ws.cell(row = index + 2, column = 6, value = dt.member5)
      ws.cell(row = index + 2, column = 7, value = dt.member6)
      ws.cell(row = index + 2, column = 8, value = dt.member7)
      ws.cell(row = index + 2, column = 9, value = dt.member8)
      ws.cell(row = index + 2, column = 10, value = dt.member9)
      ws.cell(row = index + 2, column = 11, value = dt.member10)

    wb.save(r'{}\{}_班員データバックアップ.xlsx'.format(default_data.backup_file, today))


  # 班員情報読み込み
  if 'team_load' in request.POST:

    # POSTされたファイルパスを変数に入れる
    file_path = request.POST['team_file']

    # 登録したファイルがない場合の処理
    if os.path.isfile(file_path) == False:
      # エラーメッセージ出力
      messages.error(request, 'ロードしようとしたファイルは存在しません。ERROR045')
      # このページをリダイレクト
      return redirect(to = 'administrator')

    # 指定Excelを開く
    wb = openpyxl.load_workbook('{}'.format(file_path), data_only = True)
    # 書き込みシート選択
    ws = wb.worksheets[0]

    # 読み込むファイルが正しいファイルでない場合エラー出力
    if ws.cell(1, 1).value != '従業員番号' or ws.cell(1, 2).value != '班員1' or \
      ws.cell(1, 3).value != '班員2' or ws.cell(1, 4).value != '班員3' or \
      ws.cell(1, 5).value != '班員4' or ws.cell(1, 6).value != '班員5' or \
      ws.cell(1, 7).value != '班員6' or ws.cell(1, 8).value != '班員7' or \
      ws.cell(1, 9).value != '班員8' or ws.cell(1, 10).value != '班員9' or \
      ws.cell(1, 11).value != '班員10':
      # エラーメッセージ出力
      messages.error(request, 'ロードしようとしたファイルは班員情報バックアップではありません。ERROR050')
      # このページをリダイレクト
      return redirect(to = 'administrator')

    # レコード数取得
    data_num = ws.max_row

    # 人員情報を全て削除
    member_del = team_member.objects.all()
    member_del.delete()
    # Excelからデータを読み込み
    for i in range(1, data_num):
      new_data = team_member(employee_No5 = ws.cell(row = i + 1, column = 1).value, \
                             member1 = ws.cell(row = i + 1, column = 2).value, \
                             member2 = ws.cell(row = i + 1, column = 3).value, \
                             member3 = ws.cell(row = i + 1, column = 4).value, \
                             member4 = ws.cell(row = i + 1, column = 5).value, \
                             member5 = ws.cell(row = i + 1, column = 6).value, \
                             member6 = ws.cell(row = i + 1, column = 7).value, \
                             member7 = ws.cell(row = i + 1, column = 8).value, \
                             member8 = ws.cell(row = i + 1, column = 9).value, \
                             member9 = ws.cell(row = i + 1, column = 10).value, \
                             member10 = ws.cell(row = i + 1, column = 11).value) 

      new_data.save()
 

  # 工数区分定義バックアップ処理
  if 'def_backup' in request.POST:

    # 今日の日付取得
    today = datetime.date.today()

    # 新しいExcelブック作成
    wb = openpyxl.Workbook()
    # 書き込みシート選択
    ws = wb.worksheets[0]

    # メンバーデータ取得
    def_data = kosu_division.objects.all()

    # Excelに書き込み(項目名)
    ws.cell(row = 1, column = 1, value = '工数区分定義Ver名')
    ws.cell(row = 1, column = 2, value = '工数区分名1')
    ws.cell(row = 1, column = 3, value = '定義1')
    ws.cell(row = 1, column = 4, value = '作業内容1')
    ws.cell(row = 1, column = 5, value = '工数区分名2')
    ws.cell(row = 1, column = 6, value = '定義2')
    ws.cell(row = 1, column = 7, value = '作業内容2')
    ws.cell(row = 1, column = 8, value = '工数区分名3')
    ws.cell(row = 1, column = 9, value = '定義3')
    ws.cell(row = 1, column = 10, value = '作業内容3')
    ws.cell(row = 1, column = 11, value = '工数区分名4')
    ws.cell(row = 1, column = 12, value = '定義4')
    ws.cell(row = 1, column = 13, value = '作業内容4')
    ws.cell(row = 1, column = 14, value = '工数区分名5')
    ws.cell(row = 1, column = 15, value = '定義5')
    ws.cell(row = 1, column = 16, value = '作業内容5')
    ws.cell(row = 1, column = 17, value = '工数区分名6')
    ws.cell(row = 1, column = 18, value = '定義6')
    ws.cell(row = 1, column = 19, value = '作業内容6')
    ws.cell(row = 1, column = 20, value = '工数区分名7')
    ws.cell(row = 1, column = 21, value = '定義7')
    ws.cell(row = 1, column = 22, value = '作業内容7')
    ws.cell(row = 1, column = 23, value = '工数区分名8')
    ws.cell(row = 1, column = 24, value = '定義8')
    ws.cell(row = 1, column = 25, value = '作業内容8')
    ws.cell(row = 1, column = 26, value = '工数区分名9')
    ws.cell(row = 1, column = 27, value = '定義9')
    ws.cell(row = 1, column = 28, value = '作業内容9')
    ws.cell(row = 1, column = 29, value = '工数区分名10')
    ws.cell(row = 1, column = 30, value = '定義10')
    ws.cell(row = 1, column = 31, value = '作業内容10')
    ws.cell(row = 1, column = 32, value = '工数区分名11')
    ws.cell(row = 1, column = 33, value = '定義11')
    ws.cell(row = 1, column = 34, value = '作業内容11')
    ws.cell(row = 1, column = 35, value = '工数区分名12')
    ws.cell(row = 1, column = 36, value = '定義12')
    ws.cell(row = 1, column = 37, value = '作業内容12')
    ws.cell(row = 1, column = 38, value = '工数区分名13')
    ws.cell(row = 1, column = 39, value = '定義13')
    ws.cell(row = 1, column = 40, value = '作業内容13')
    ws.cell(row = 1, column = 41, value = '工数区分名14')
    ws.cell(row = 1, column = 42, value = '定義14')
    ws.cell(row = 1, column = 43, value = '作業内容14')
    ws.cell(row = 1, column = 44, value = '工数区分名15')
    ws.cell(row = 1, column = 45, value = '定義15')
    ws.cell(row = 1, column = 46, value = '作業内容15')
    ws.cell(row = 1, column = 47, value = '工数区分名16')
    ws.cell(row = 1, column = 48, value = '定義16')
    ws.cell(row = 1, column = 49, value = '作業内容16')
    ws.cell(row = 1, column = 50, value = '工数区分名17')
    ws.cell(row = 1, column = 51, value = '定義17')
    ws.cell(row = 1, column = 52, value = '作業内容17')
    ws.cell(row = 1, column = 53, value = '工数区分名18')
    ws.cell(row = 1, column = 54, value = '定義18')
    ws.cell(row = 1, column = 55, value = '作業内容18')
    ws.cell(row = 1, column = 56, value = '工数区分名19')
    ws.cell(row = 1, column = 57, value = '定義19')
    ws.cell(row = 1, column = 58, value = '作業内容19')
    ws.cell(row = 1, column = 59, value = '工数区分名20')
    ws.cell(row = 1, column = 60, value = '定義20')
    ws.cell(row = 1, column = 61, value = '作業内容20')
    ws.cell(row = 1, column = 62, value = '工数区分名21')
    ws.cell(row = 1, column = 63, value = '定義21')
    ws.cell(row = 1, column = 64, value = '作業内容21')
    ws.cell(row = 1, column = 65, value = '工数区分名22')
    ws.cell(row = 1, column = 66, value = '定義22')
    ws.cell(row = 1, column = 67, value = '作業内容22')
    ws.cell(row = 1, column = 68, value = '工数区分名23')
    ws.cell(row = 1, column = 69, value = '定義23')
    ws.cell(row = 1, column = 70, value = '作業内容23')
    ws.cell(row = 1, column = 71, value = '工数区分名24')
    ws.cell(row = 1, column = 72, value = '定義24')
    ws.cell(row = 1, column = 73, value = '作業内容24')
    ws.cell(row = 1, column = 74, value = '工数区分名25')
    ws.cell(row = 1, column = 75, value = '定義25')
    ws.cell(row = 1, column = 76, value = '作業内容25')
    ws.cell(row = 1, column = 77, value = '工数区分名26')
    ws.cell(row = 1, column = 78, value = '定義26')
    ws.cell(row = 1, column = 79, value = '作業内容26')
    ws.cell(row = 1, column = 80, value = '工数区分名27')
    ws.cell(row = 1, column = 81, value = '定義27')
    ws.cell(row = 1, column = 82, value = '作業内容27')
    ws.cell(row = 1, column = 83, value = '工数区分名28')
    ws.cell(row = 1, column = 84, value = '定義28')
    ws.cell(row = 1, column = 85, value = '作業内容28')
    ws.cell(row = 1, column = 86, value = '工数区分名29')
    ws.cell(row = 1, column = 87, value = '定義29')
    ws.cell(row = 1, column = 88, value = '作業内容29')
    ws.cell(row = 1, column = 89, value = '工数区分名30')
    ws.cell(row = 1, column = 90, value = '定義30')
    ws.cell(row = 1, column = 91, value = '作業内容30')
    ws.cell(row = 1, column = 92, value = '工数区分名31')
    ws.cell(row = 1, column = 93, value = '定義31')
    ws.cell(row = 1, column = 94, value = '作業内容31')
    ws.cell(row = 1, column = 95, value = '工数区分名32')
    ws.cell(row = 1, column = 96, value = '定義32')
    ws.cell(row = 1, column = 97, value = '作業内容32')
    ws.cell(row = 1, column = 98, value = '工数区分名33')
    ws.cell(row = 1, column = 99, value = '定義33')
    ws.cell(row = 1, column = 100, value = '作業内容33')
    ws.cell(row = 1, column = 101, value = '工数区分名34')
    ws.cell(row = 1, column = 102, value = '定義34')
    ws.cell(row = 1, column = 103, value = '作業内容34')
    ws.cell(row = 1, column = 104, value = '工数区分名35')
    ws.cell(row = 1, column = 105, value = '定義35')
    ws.cell(row = 1, column = 106, value = '作業内容35')
    ws.cell(row = 1, column = 107, value = '工数区分名36')
    ws.cell(row = 1, column = 108, value = '定義36')
    ws.cell(row = 1, column = 109, value = '作業内容36')
    ws.cell(row = 1, column = 110, value = '工数区分名37')
    ws.cell(row = 1, column = 111, value = '定義37')
    ws.cell(row = 1, column = 112, value = '作業内容37')
    ws.cell(row = 1, column = 113, value = '工数区分名38')
    ws.cell(row = 1, column = 114, value = '定義38')
    ws.cell(row = 1, column = 115, value = '作業内容38')
    ws.cell(row = 1, column = 116, value = '工数区分名39')
    ws.cell(row = 1, column = 117, value = '定義39')
    ws.cell(row = 1, column = 118, value = '作業内容39')
    ws.cell(row = 1, column = 119, value = '工数区分名40')
    ws.cell(row = 1, column = 120, value = '定義40')
    ws.cell(row = 1, column = 121, value = '作業内容40')
    ws.cell(row = 1, column = 122, value = '工数区分名41')
    ws.cell(row = 1, column = 123, value = '定義41')
    ws.cell(row = 1, column = 124, value = '作業内容41')
    ws.cell(row = 1, column = 125, value = '工数区分名42')
    ws.cell(row = 1, column = 126, value = '定義42')
    ws.cell(row = 1, column = 127, value = '作業内容42')
    ws.cell(row = 1, column = 128, value = '工数区分名43')
    ws.cell(row = 1, column = 129, value = '定義43')
    ws.cell(row = 1, column = 130, value = '作業内容43')
    ws.cell(row = 1, column = 131, value = '工数区分名44')
    ws.cell(row = 1, column = 132, value = '定義44')
    ws.cell(row = 1, column = 133, value = '作業内容44')
    ws.cell(row = 1, column = 134, value = '工数区分名45')
    ws.cell(row = 1, column = 135, value = '定義45')
    ws.cell(row = 1, column = 136, value = '作業内容45')
    ws.cell(row = 1, column = 137, value = '工数区分名46')
    ws.cell(row = 1, column = 138, value = '定義46')
    ws.cell(row = 1, column = 139, value = '作業内容46')
    ws.cell(row = 1, column = 140, value = '工数区分名47')
    ws.cell(row = 1, column = 141, value = '定義47')
    ws.cell(row = 1, column = 142, value = '作業内容47')
    ws.cell(row = 1, column = 143, value = '工数区分名48')
    ws.cell(row = 1, column = 144, value = '定義48')
    ws.cell(row = 1, column = 145, value = '作業内容48')
    ws.cell(row = 1, column = 146, value = '工数区分名49')
    ws.cell(row = 1, column = 147, value = '定義49')
    ws.cell(row = 1, column = 148, value = '作業内容49')
    ws.cell(row = 1, column = 149, value = '工数区分名50')
    ws.cell(row = 1, column = 150, value = '定義50')
    ws.cell(row = 1, column = 151, value = '作業内容50')

    # Excelに書き込み(項目)
    for index, dt in enumerate(def_data):
      ws.cell(row = index + 2, column = 1, value = dt.kosu_name)
      ws.cell(row = index + 2, column = 2, value = dt.kosu_title_1)
      ws.cell(row = index + 2, column = 3, value = dt.kosu_division_1_1)
      ws.cell(row = index + 2, column = 4, value = dt.kosu_division_2_1)
      ws.cell(row = index + 2, column = 5, value = dt.kosu_title_2)
      ws.cell(row = index + 2, column = 6, value = dt.kosu_division_1_2)
      ws.cell(row = index + 2, column = 7, value = dt.kosu_division_2_2)
      ws.cell(row = index + 2, column = 8, value = dt.kosu_title_3)
      ws.cell(row = index + 2, column = 9, value = dt.kosu_division_1_3)
      ws.cell(row = index + 2, column = 10, value = dt.kosu_division_2_3)
      ws.cell(row = index + 2, column = 11, value = dt.kosu_title_4)
      ws.cell(row = index + 2, column = 12, value = dt.kosu_division_1_4)
      ws.cell(row = index + 2, column = 13, value = dt.kosu_division_2_4)
      ws.cell(row = index + 2, column = 14, value = dt.kosu_title_5)
      ws.cell(row = index + 2, column = 15, value = dt.kosu_division_1_5)
      ws.cell(row = index + 2, column = 16, value = dt.kosu_division_2_5)
      ws.cell(row = index + 2, column = 17, value = dt.kosu_title_6)
      ws.cell(row = index + 2, column = 18, value = dt.kosu_division_1_6)
      ws.cell(row = index + 2, column = 19, value = dt.kosu_division_2_6)
      ws.cell(row = index + 2, column = 20, value = dt.kosu_title_7)
      ws.cell(row = index + 2, column = 21, value = dt.kosu_division_1_7)
      ws.cell(row = index + 2, column = 22, value = dt.kosu_division_2_7)
      ws.cell(row = index + 2, column = 23, value = dt.kosu_title_8)
      ws.cell(row = index + 2, column = 24, value = dt.kosu_division_1_8)
      ws.cell(row = index + 2, column = 25, value = dt.kosu_division_2_8)
      ws.cell(row = index + 2, column = 26, value = dt.kosu_title_9)
      ws.cell(row = index + 2, column = 27, value = dt.kosu_division_1_9)
      ws.cell(row = index + 2, column = 28, value = dt.kosu_division_2_9)
      ws.cell(row = index + 2, column = 29, value = dt.kosu_title_10)
      ws.cell(row = index + 2, column = 30, value = dt.kosu_division_1_10)
      ws.cell(row = index + 2, column = 31, value = dt.kosu_division_2_10)
      ws.cell(row = index + 2, column = 32, value = dt.kosu_title_11)
      ws.cell(row = index + 2, column = 33, value = dt.kosu_division_1_11)
      ws.cell(row = index + 2, column = 34, value = dt.kosu_division_2_11)
      ws.cell(row = index + 2, column = 35, value = dt.kosu_title_12)
      ws.cell(row = index + 2, column = 36, value = dt.kosu_division_1_12)
      ws.cell(row = index + 2, column = 37, value = dt.kosu_division_2_12)
      ws.cell(row = index + 2, column = 38, value = dt.kosu_title_13)
      ws.cell(row = index + 2, column = 39, value = dt.kosu_division_1_13)
      ws.cell(row = index + 2, column = 40, value = dt.kosu_division_2_13)
      ws.cell(row = index + 2, column = 41, value = dt.kosu_title_14)
      ws.cell(row = index + 2, column = 42, value = dt.kosu_division_1_14)
      ws.cell(row = index + 2, column = 43, value = dt.kosu_division_2_14)
      ws.cell(row = index + 2, column = 44, value = dt.kosu_title_15)
      ws.cell(row = index + 2, column = 45, value = dt.kosu_division_1_15)
      ws.cell(row = index + 2, column = 46, value = dt.kosu_division_2_15)
      ws.cell(row = index + 2, column = 47, value = dt.kosu_title_16)
      ws.cell(row = index + 2, column = 48, value = dt.kosu_division_1_16)
      ws.cell(row = index + 2, column = 49, value = dt.kosu_division_2_16)
      ws.cell(row = index + 2, column = 50, value = dt.kosu_title_17)
      ws.cell(row = index + 2, column = 51, value = dt.kosu_division_1_17)
      ws.cell(row = index + 2, column = 52, value = dt.kosu_division_2_17)
      ws.cell(row = index + 2, column = 53, value = dt.kosu_title_18)
      ws.cell(row = index + 2, column = 54, value = dt.kosu_division_1_18)
      ws.cell(row = index + 2, column = 55, value = dt.kosu_division_2_18)
      ws.cell(row = index + 2, column = 56, value = dt.kosu_title_19)
      ws.cell(row = index + 2, column = 57, value = dt.kosu_division_1_19)
      ws.cell(row = index + 2, column = 58, value = dt.kosu_division_2_19)
      ws.cell(row = index + 2, column = 59, value = dt.kosu_title_20)
      ws.cell(row = index + 2, column = 60, value = dt.kosu_division_1_20)
      ws.cell(row = index + 2, column = 61, value = dt.kosu_division_2_20)
      ws.cell(row = index + 2, column = 62, value = dt.kosu_title_21)
      ws.cell(row = index + 2, column = 63, value = dt.kosu_division_1_21)
      ws.cell(row = index + 2, column = 64, value = dt.kosu_division_2_21)
      ws.cell(row = index + 2, column = 65, value = dt.kosu_title_22)
      ws.cell(row = index + 2, column = 66, value = dt.kosu_division_1_22)
      ws.cell(row = index + 2, column = 67, value = dt.kosu_division_2_22)
      ws.cell(row = index + 2, column = 68, value = dt.kosu_title_23)
      ws.cell(row = index + 2, column = 69, value = dt.kosu_division_1_23)
      ws.cell(row = index + 2, column = 70, value = dt.kosu_division_2_23)
      ws.cell(row = index + 2, column = 71, value = dt.kosu_title_24)
      ws.cell(row = index + 2, column = 72, value = dt.kosu_division_1_24)
      ws.cell(row = index + 2, column = 73, value = dt.kosu_division_2_24)
      ws.cell(row = index + 2, column = 74, value = dt.kosu_title_25)
      ws.cell(row = index + 2, column = 75, value = dt.kosu_division_1_25)
      ws.cell(row = index + 2, column = 76, value = dt.kosu_division_2_25)
      ws.cell(row = index + 2, column = 77, value = dt.kosu_title_26)
      ws.cell(row = index + 2, column = 78, value = dt.kosu_division_1_26)
      ws.cell(row = index + 2, column = 79, value = dt.kosu_division_2_26)
      ws.cell(row = index + 2, column = 80, value = dt.kosu_title_27)
      ws.cell(row = index + 2, column = 81, value = dt.kosu_division_1_27)
      ws.cell(row = index + 2, column = 82, value = dt.kosu_division_2_27)
      ws.cell(row = index + 2, column = 83, value = dt.kosu_title_28)
      ws.cell(row = index + 2, column = 84, value = dt.kosu_division_1_28)
      ws.cell(row = index + 2, column = 85, value = dt.kosu_division_2_28)
      ws.cell(row = index + 2, column = 86, value = dt.kosu_title_29)
      ws.cell(row = index + 2, column = 87, value = dt.kosu_division_1_29)
      ws.cell(row = index + 2, column = 88, value = dt.kosu_division_2_29)
      ws.cell(row = index + 2, column = 89, value = dt.kosu_title_30)
      ws.cell(row = index + 2, column = 90, value = dt.kosu_division_1_30)
      ws.cell(row = index + 2, column = 91, value = dt.kosu_division_2_30)
      ws.cell(row = index + 2, column = 92, value = dt.kosu_title_31)
      ws.cell(row = index + 2, column = 93, value = dt.kosu_division_1_31)
      ws.cell(row = index + 2, column = 94, value = dt.kosu_division_2_31)
      ws.cell(row = index + 2, column = 95, value = dt.kosu_title_32)
      ws.cell(row = index + 2, column = 96, value = dt.kosu_division_1_32)
      ws.cell(row = index + 2, column = 97, value = dt.kosu_division_2_32)
      ws.cell(row = index + 2, column = 98, value = dt.kosu_title_33)
      ws.cell(row = index + 2, column = 99, value = dt.kosu_division_1_33)
      ws.cell(row = index + 2, column = 100, value = dt.kosu_division_2_33)
      ws.cell(row = index + 2, column = 101, value = dt.kosu_title_34)
      ws.cell(row = index + 2, column = 102, value = dt.kosu_division_1_34)
      ws.cell(row = index + 2, column = 103, value = dt.kosu_division_2_34)
      ws.cell(row = index + 2, column = 104, value = dt.kosu_title_35)
      ws.cell(row = index + 2, column = 105, value = dt.kosu_division_1_35)
      ws.cell(row = index + 2, column = 106, value = dt.kosu_division_2_35)
      ws.cell(row = index + 2, column = 107, value = dt.kosu_title_36)
      ws.cell(row = index + 2, column = 108, value = dt.kosu_division_1_36)
      ws.cell(row = index + 2, column = 109, value = dt.kosu_division_2_36)
      ws.cell(row = index + 2, column = 110, value = dt.kosu_title_37)
      ws.cell(row = index + 2, column = 111, value = dt.kosu_division_1_37)
      ws.cell(row = index + 2, column = 112, value = dt.kosu_division_2_37)
      ws.cell(row = index + 2, column = 113, value = dt.kosu_title_38)
      ws.cell(row = index + 2, column = 114, value = dt.kosu_division_1_38)
      ws.cell(row = index + 2, column = 115, value = dt.kosu_division_2_38)
      ws.cell(row = index + 2, column = 116, value = dt.kosu_title_39)
      ws.cell(row = index + 2, column = 117, value = dt.kosu_division_1_39)
      ws.cell(row = index + 2, column = 118, value = dt.kosu_division_2_39)
      ws.cell(row = index + 2, column = 119, value = dt.kosu_title_40)
      ws.cell(row = index + 2, column = 120, value = dt.kosu_division_1_40)
      ws.cell(row = index + 2, column = 121, value = dt.kosu_division_2_40)
      ws.cell(row = index + 2, column = 122, value = dt.kosu_title_41)
      ws.cell(row = index + 2, column = 123, value = dt.kosu_division_1_41)
      ws.cell(row = index + 2, column = 124, value = dt.kosu_division_2_41)
      ws.cell(row = index + 2, column = 125, value = dt.kosu_title_42)
      ws.cell(row = index + 2, column = 126, value = dt.kosu_division_1_42)
      ws.cell(row = index + 2, column = 127, value = dt.kosu_division_2_42)
      ws.cell(row = index + 2, column = 128, value = dt.kosu_title_43)
      ws.cell(row = index + 2, column = 129, value = dt.kosu_division_1_43)
      ws.cell(row = index + 2, column = 130, value = dt.kosu_division_2_43)
      ws.cell(row = index + 2, column = 131, value = dt.kosu_title_44)
      ws.cell(row = index + 2, column = 132, value = dt.kosu_division_1_44)
      ws.cell(row = index + 2, column = 133, value = dt.kosu_division_2_44)
      ws.cell(row = index + 2, column = 134, value = dt.kosu_title_45)
      ws.cell(row = index + 2, column = 135, value = dt.kosu_division_1_45)
      ws.cell(row = index + 2, column = 136, value = dt.kosu_division_2_45)
      ws.cell(row = index + 2, column = 137, value = dt.kosu_title_46)
      ws.cell(row = index + 2, column = 138, value = dt.kosu_division_1_46)
      ws.cell(row = index + 2, column = 139, value = dt.kosu_division_2_46)
      ws.cell(row = index + 2, column = 140, value = dt.kosu_title_47)
      ws.cell(row = index + 2, column = 141, value = dt.kosu_division_1_47)
      ws.cell(row = index + 2, column = 142, value = dt.kosu_division_2_47)
      ws.cell(row = index + 2, column = 143, value = dt.kosu_title_48)
      ws.cell(row = index + 2, column = 144, value = dt.kosu_division_1_48)
      ws.cell(row = index + 2, column = 145, value = dt.kosu_division_2_48)
      ws.cell(row = index + 2, column = 146, value = dt.kosu_title_49)
      ws.cell(row = index + 2, column = 147, value = dt.kosu_division_1_49)
      ws.cell(row = index + 2, column = 148, value = dt.kosu_division_2_49)
      ws.cell(row = index + 2, column = 149, value = dt.kosu_title_50)
      ws.cell(row = index + 2, column = 150, value = dt.kosu_division_1_50)
      ws.cell(row = index + 2, column = 151, value = dt.kosu_division_2_50)

    wb.save(r'{}\{}_工数区分定義データバックアップ.xlsx'.format(default_data.backup_file, today))

  # 工数区分定義読み込み
  if 'def_load' in request.POST:

    # POSTされたファイルパスを変数に入れる
    file_path = request.POST['def_file']

    # 登録したファイルがない場合の処理
    if os.path.isfile(file_path) == False:
      # エラーメッセージ出力
      messages.error(request, 'ロードしようとしたファイルは存在しません。ERROR046')
      # このページをリダイレクト
      return redirect(to = 'administrator')

    # 指定Excelを開く
    wb = openpyxl.load_workbook('{}'.format(file_path), data_only = True)
    # 書き込みシート選択
    ws = wb.worksheets[0]

    # 読み込むファイルが正しいファイルでない場合エラー出力
    if ws.cell(1, 1).value != '工数区分定義Ver名' or ws.cell(1, 2).value != '工数区分名1' or \
      ws.cell(1, 3).value != '定義1' or ws.cell(1, 4).value != '作業内容1' or \
      ws.cell(1, 5).value != '工数区分名2' or ws.cell(1, 6).value != '定義2' or \
      ws.cell(1, 7).value != '作業内容2' or ws.cell(1, 8).value != '工数区分名3' or \
      ws.cell(1, 9).value != '定義3' or ws.cell(1, 10).value != '作業内容3' or \
      ws.cell(1, 11).value != '工数区分名4' or ws.cell(1, 12).value != '定義4' or \
      ws.cell(1, 13).value != '作業内容4' or ws.cell(1, 14).value != '工数区分名5' or \
      ws.cell(1, 15).value != '定義5' or ws.cell(1, 16).value != '作業内容5' or \
      ws.cell(1, 17).value != '工数区分名6' or ws.cell(1, 18).value != '定義6' or \
      ws.cell(1, 19).value != '作業内容6' or ws.cell(1, 20).value != '工数区分名7' or \
      ws.cell(1, 21).value != '定義7' or ws.cell(1, 22).value != '作業内容7' or \
      ws.cell(1, 23).value != '工数区分名8' or ws.cell(1, 24).value != '定義8' or \
      ws.cell(1, 25).value != '作業内容8' or ws.cell(1, 26).value != '工数区分名9' or \
      ws.cell(1, 27).value != '定義9' or ws.cell(1, 28).value != '作業内容9' or \
      ws.cell(1, 29).value != '工数区分名10' or ws.cell(1, 30).value != '定義10' or \
      ws.cell(1, 31).value != '作業内容10' or ws.cell(1, 32).value != '工数区分名11' or \
      ws.cell(1, 33).value != '定義11' or ws.cell(1, 34).value != '作業内容11' or \
      ws.cell(1, 35).value != '工数区分名12' or ws.cell(1, 36).value != '定義12' or \
      ws.cell(1, 37).value != '作業内容12' or ws.cell(1, 38).value != '工数区分名13' or \
      ws.cell(1, 39).value != '定義13' or ws.cell(1, 40).value != '作業内容13' or \
      ws.cell(1, 41).value != '工数区分名14' or ws.cell(1, 42).value != '定義14' or \
      ws.cell(1, 43).value != '作業内容14' or ws.cell(1, 44).value != '工数区分名15' or \
      ws.cell(1, 45).value != '定義15' or ws.cell(1, 46).value != '作業内容15' or \
      ws.cell(1, 47).value != '工数区分名16' or ws.cell(1, 48).value != '定義16' or \
      ws.cell(1, 49).value != '作業内容16' or ws.cell(1, 50).value != '工数区分名17' or \
      ws.cell(1, 51).value != '定義17' or ws.cell(1, 52).value != '作業内容17' or \
      ws.cell(1, 53).value != '工数区分名18' or ws.cell(1, 54).value != '定義18' or \
      ws.cell(1, 55).value != '作業内容18' or ws.cell(1, 56).value != '工数区分名19' or \
      ws.cell(1, 57).value != '定義19' or ws.cell(1, 58).value != '作業内容19' or \
      ws.cell(1, 59).value != '工数区分名20' or ws.cell(1, 60).value != '定義20' or \
      ws.cell(1, 61).value != '作業内容20' or ws.cell(1, 62).value != '工数区分名21' or \
      ws.cell(1, 63).value != '定義21' or ws.cell(1, 64).value != '作業内容21' or \
      ws.cell(1, 65).value != '工数区分名22' or ws.cell(1, 66).value != '定義22' or \
      ws.cell(1, 67).value != '作業内容22' or ws.cell(1, 68).value != '工数区分名23' or \
      ws.cell(1, 69).value != '定義23' or ws.cell(1, 70).value != '作業内容23' or \
      ws.cell(1, 71).value != '工数区分名24' or ws.cell(1, 72).value != '定義24' or \
      ws.cell(1, 73).value != '作業内容24' or ws.cell(1, 74).value != '工数区分名25' or \
      ws.cell(1, 75).value != '定義25' or ws.cell(1, 76).value != '作業内容25' or \
      ws.cell(1, 77).value != '工数区分名26' or ws.cell(1, 78).value != '定義26' or \
      ws.cell(1, 79).value != '作業内容26' or ws.cell(1, 80).value != '工数区分名27' or \
      ws.cell(1, 81).value != '定義27' or ws.cell(1, 82).value != '作業内容27' or \
      ws.cell(1, 83).value != '工数区分名28' or ws.cell(1, 84).value != '定義28' or \
      ws.cell(1, 85).value != '作業内容28' or ws.cell(1, 86).value != '工数区分名29' or \
      ws.cell(1, 87).value != '定義29' or ws.cell(1, 88).value != '作業内容29' or \
      ws.cell(1, 89).value != '工数区分名30' or ws.cell(1, 90).value != '定義30' or \
      ws.cell(1, 91).value != '作業内容30' or ws.cell(1, 92).value != '工数区分名31' or \
      ws.cell(1, 93).value != '定義31' or ws.cell(1, 94).value != '作業内容31' or \
      ws.cell(1, 95).value != '工数区分名32' or ws.cell(1, 96).value != '定義32' or \
      ws.cell(1, 97).value != '作業内容32' or ws.cell(1, 98).value != '工数区分名33' or \
      ws.cell(1, 99).value != '定義33' or ws.cell(1, 100).value != '作業内容33' or \
      ws.cell(1, 101).value != '工数区分名34' or ws.cell(1, 102).value != '定義34' or \
      ws.cell(1, 103).value != '作業内容34' or ws.cell(1, 104).value != '工数区分名35' or \
      ws.cell(1, 105).value != '定義35' or ws.cell(1, 106).value != '作業内容35' or \
      ws.cell(1, 107).value != '工数区分名36' or ws.cell(1, 108).value != '定義36' or \
      ws.cell(1, 109).value != '作業内容36' or ws.cell(1, 110).value != '工数区分名37' or \
      ws.cell(1, 111).value != '定義37' or ws.cell(1, 112).value != '作業内容37' or \
      ws.cell(1, 113).value != '工数区分名38' or ws.cell(1, 114).value != '定義38' or \
      ws.cell(1, 115).value != '作業内容38' or ws.cell(1, 116).value != '工数区分名39' or \
      ws.cell(1, 117).value != '定義39' or ws.cell(1, 118).value != '作業内容39' or \
      ws.cell(1, 119).value != '工数区分名40' or ws.cell(1, 120).value != '定義40' or \
      ws.cell(1, 121).value != '作業内容40' or ws.cell(1, 122).value != '工数区分名41' or \
      ws.cell(1, 123).value != '定義41' or ws.cell(1, 124).value != '作業内容41' or \
      ws.cell(1, 125).value != '工数区分名42' or ws.cell(1, 126).value != '定義42' or \
      ws.cell(1, 127).value != '作業内容42' or ws.cell(1, 128).value != '工数区分名43' or \
      ws.cell(1, 129).value != '定義43' or ws.cell(1, 130).value != '作業内容43' or \
      ws.cell(1, 131).value != '工数区分名44' or ws.cell(1, 132).value != '定義44' or \
      ws.cell(1, 133).value != '作業内容44' or ws.cell(1, 134).value != '工数区分名45' or \
      ws.cell(1, 135).value != '定義45' or ws.cell(1, 136).value != '作業内容45' or \
      ws.cell(1, 137).value != '工数区分名46' or ws.cell(1, 138).value != '定義46' or \
      ws.cell(1, 139).value != '作業内容46' or ws.cell(1, 140).value != '工数区分名47' or \
      ws.cell(1, 141).value != '定義47' or ws.cell(1, 142).value != '作業内容47' or \
      ws.cell(1, 143).value != '工数区分名48' or ws.cell(1, 144).value != '定義48' or \
      ws.cell(1, 145).value != '作業内容48' or ws.cell(1, 146).value != '工数区分名49' or \
      ws.cell(1, 147).value != '定義49' or ws.cell(1, 148).value != '作業内容49' or \
      ws.cell(1, 149).value != '工数区分名50' or ws.cell(1, 150).value != '定義50' or \
      ws.cell(1, 151).value != '作業内容50':
      
      # エラーメッセージ出力
      messages.error(request, 'ロードしようとしたファイルは工数区分定義情報バックアップではありません。ERROR051')
      # このページをリダイレクト
      return redirect(to = 'administrator')

    # レコード数取得
    data_num = ws.max_row

    # 工数区分定義を全て削除
    def_del = kosu_division.objects.all()
    def_del.delete()
    # Excelからデータを読み込み
    for i in range(1, data_num):
      new_data = kosu_division(kosu_name = ws.cell(row = i + 1, column = 1).value, \
                               kosu_title_1 = ws.cell(row = i + 1, column = 2).value, \
                               kosu_division_1_1 = ws.cell(row = i + 1, column = 3).value, \
                               kosu_division_2_1 = ws.cell(row = i + 1, column = 4).value, \
                               kosu_title_2 = ws.cell(row = i + 1, column = 5).value, \
                               kosu_division_1_2 = ws.cell(row = i + 1, column = 6).value, \
                               kosu_division_2_2 = ws.cell(row = i + 1, column = 7).value, \
                               kosu_title_3 = ws.cell(row = i + 1, column = 8).value, \
                               kosu_division_1_3 = ws.cell(row = i + 1, column = 9).value, \
                               kosu_division_2_3 = ws.cell(row = i + 1, column = 10).value, \
                               kosu_title_4 = ws.cell(row = i + 1, column = 11).value, \
                               kosu_division_1_4 = ws.cell(row = i + 1, column = 12).value, \
                               kosu_division_2_4 = ws.cell(row = i + 1, column = 13).value, \
                               kosu_title_5 = ws.cell(row = i + 1, column = 14).value, \
                               kosu_division_1_5 = ws.cell(row = i + 1, column = 15).value, \
                               kosu_division_2_5 = ws.cell(row = i + 1, column = 16).value, \
                               kosu_title_6 = ws.cell(row = i + 1, column = 17).value, \
                               kosu_division_1_6 = ws.cell(row = i + 1, column = 18).value, \
                               kosu_division_2_6 = ws.cell(row = i + 1, column = 19).value, \
                               kosu_title_7 = ws.cell(row = i + 1, column = 20).value, \
                               kosu_division_1_7 = ws.cell(row = i + 1, column = 21).value, \
                               kosu_division_2_7 = ws.cell(row = i + 1, column = 22).value, \
                               kosu_title_8 = ws.cell(row = i + 1, column = 23).value, \
                               kosu_division_1_8 = ws.cell(row = i + 1, column = 24).value, \
                               kosu_division_2_8 = ws.cell(row = i + 1, column = 25).value, \
                               kosu_title_9 = ws.cell(row = i + 1, column = 26).value, \
                               kosu_division_1_9 = ws.cell(row = i + 1, column = 27).value, \
                               kosu_division_2_9 = ws.cell(row = i + 1, column = 28).value, \
                               kosu_title_10 = ws.cell(row = i + 1, column = 29).value, \
                               kosu_division_1_10 = ws.cell(row = i + 1, column = 30).value, \
                               kosu_division_2_10 = ws.cell(row = i + 1, column = 31).value, \
                               kosu_title_11 = ws.cell(row = i + 1, column = 32).value, \
                               kosu_division_1_11 = ws.cell(row = i + 1, column = 33).value, \
                               kosu_division_2_11 = ws.cell(row = i + 1, column = 34).value, \
                               kosu_title_12 = ws.cell(row = i + 1, column = 35).value, \
                               kosu_division_1_12 = ws.cell(row = i + 1, column = 36).value, \
                               kosu_division_2_12 = ws.cell(row = i + 1, column = 37).value, \
                               kosu_title_13 = ws.cell(row = i + 1, column = 38).value, \
                               kosu_division_1_13 = ws.cell(row = i + 1, column = 39).value, \
                               kosu_division_2_13 = ws.cell(row = i + 1, column = 40).value, \
                               kosu_title_14 = ws.cell(row = i + 1, column = 41).value, \
                               kosu_division_1_14 = ws.cell(row = i + 1, column = 42).value, \
                               kosu_division_2_14 = ws.cell(row = i + 1, column = 43).value, \
                               kosu_title_15 = ws.cell(row = i + 1, column = 44).value, \
                               kosu_division_1_15 = ws.cell(row = i + 1, column = 45).value, \
                               kosu_division_2_15 = ws.cell(row = i + 1, column = 46).value, \
                               kosu_title_16 = ws.cell(row = i + 1, column = 47).value, \
                               kosu_division_1_16 = ws.cell(row = i + 1, column = 48).value, \
                               kosu_division_2_16 = ws.cell(row = i + 1, column = 49).value, \
                               kosu_title_17 = ws.cell(row = i + 1, column = 50).value, \
                               kosu_division_1_17 = ws.cell(row = i + 1, column = 51).value, \
                               kosu_division_2_17 = ws.cell(row = i + 1, column = 52).value, \
                               kosu_title_18 = ws.cell(row = i + 1, column = 53).value, \
                               kosu_division_1_18 = ws.cell(row = i + 1, column = 54).value, \
                               kosu_division_2_18 = ws.cell(row = i + 1, column = 55).value, \
                               kosu_title_19 = ws.cell(row = i + 1, column = 56).value, \
                               kosu_division_1_19 = ws.cell(row = i + 1, column = 57).value, \
                               kosu_division_2_19 = ws.cell(row = i + 1, column = 58).value, \
                               kosu_title_20 = ws.cell(row = i + 1, column = 59).value, \
                               kosu_division_1_20 = ws.cell(row = i + 1, column = 60).value, \
                               kosu_division_2_20 = ws.cell(row = i + 1, column = 61).value, \
                               kosu_title_21 = ws.cell(row = i + 1, column = 62).value, \
                               kosu_division_1_21 = ws.cell(row = i + 1, column = 63).value, \
                               kosu_division_2_21 = ws.cell(row = i + 1, column = 64).value, \
                               kosu_title_22 = ws.cell(row = i + 1, column = 65).value, \
                               kosu_division_1_22 = ws.cell(row = i + 1, column = 66).value, \
                               kosu_division_2_22 = ws.cell(row = i + 1, column = 67).value, \
                               kosu_title_23 = ws.cell(row = i + 1, column = 68).value, \
                               kosu_division_1_23 = ws.cell(row = i + 1, column = 69).value, \
                               kosu_division_2_23 = ws.cell(row = i + 1, column = 70).value, \
                               kosu_title_24 = ws.cell(row = i + 1, column = 71).value, \
                               kosu_division_1_24 = ws.cell(row = i + 1, column = 72).value, \
                               kosu_division_2_24 = ws.cell(row = i + 1, column = 73).value, \
                               kosu_title_25 = ws.cell(row = i + 1, column = 74).value, \
                               kosu_division_1_25 = ws.cell(row = i + 1, column = 75).value, \
                               kosu_division_2_25 = ws.cell(row = i + 1, column = 76).value, \
                               kosu_title_26 = ws.cell(row = i + 1, column = 77).value, \
                               kosu_division_1_26 = ws.cell(row = i + 1, column = 78).value, \
                               kosu_division_2_26 = ws.cell(row = i + 1, column = 79).value, \
                               kosu_title_27 = ws.cell(row = i + 1, column = 80).value, \
                               kosu_division_1_27 = ws.cell(row = i + 1, column = 81).value, \
                               kosu_division_2_27 = ws.cell(row = i + 1, column = 82).value, \
                               kosu_title_28 = ws.cell(row = i + 1, column = 83).value, \
                               kosu_division_1_28 = ws.cell(row = i + 1, column = 84).value, \
                               kosu_division_2_28 = ws.cell(row = i + 1, column = 85).value, \
                               kosu_title_29 = ws.cell(row = i + 1, column = 86).value, \
                               kosu_division_1_29 = ws.cell(row = i + 1, column = 87).value, \
                               kosu_division_2_29 = ws.cell(row = i + 1, column = 88).value, \
                               kosu_title_30 = ws.cell(row = i + 1, column = 89).value, \
                               kosu_division_1_30 = ws.cell(row = i + 1, column = 90).value, \
                               kosu_division_2_30 = ws.cell(row = i + 1, column = 91).value, \
                               kosu_title_31 = ws.cell(row = i + 1, column = 92).value, \
                               kosu_division_1_31 = ws.cell(row = i + 1, column = 93).value, \
                               kosu_division_2_31 = ws.cell(row = i + 1, column = 94).value, \
                               kosu_title_32 = ws.cell(row = i + 1, column = 95).value, \
                               kosu_division_1_32 = ws.cell(row = i + 1, column = 96).value, \
                               kosu_division_2_32 = ws.cell(row = i + 1, column = 97).value, \
                               kosu_title_33 = ws.cell(row = i + 1, column = 98).value, \
                               kosu_division_1_33 = ws.cell(row = i + 1, column = 99).value, \
                               kosu_division_2_33 = ws.cell(row = i + 1, column = 100).value, \
                               kosu_title_34 = ws.cell(row = i + 1, column = 101).value, \
                               kosu_division_1_34 = ws.cell(row = i + 1, column = 102).value, \
                               kosu_division_2_34 = ws.cell(row = i + 1, column = 103).value, \
                               kosu_title_35 = ws.cell(row = i + 1, column = 104).value, \
                               kosu_division_1_35 = ws.cell(row = i + 1, column = 105).value, \
                               kosu_division_2_35 = ws.cell(row = i + 1, column = 106).value, \
                               kosu_title_36 = ws.cell(row = i + 1, column = 107).value, \
                               kosu_division_1_36 = ws.cell(row = i + 1, column = 108).value, \
                               kosu_division_2_36 = ws.cell(row = i + 1, column = 109).value, \
                               kosu_title_37 = ws.cell(row = i + 1, column = 110).value, \
                               kosu_division_1_37 = ws.cell(row = i + 1, column = 111).value, \
                               kosu_division_2_37 = ws.cell(row = i + 1, column = 112).value, \
                               kosu_title_38 = ws.cell(row = i + 1, column = 113).value, \
                               kosu_division_1_38 = ws.cell(row = i + 1, column = 114).value, \
                               kosu_division_2_38 = ws.cell(row = i + 1, column = 115).value, \
                               kosu_title_39 = ws.cell(row = i + 1, column = 116).value, \
                               kosu_division_1_39 = ws.cell(row = i + 1, column = 117).value, \
                               kosu_division_2_39 = ws.cell(row = i + 1, column = 118).value, \
                               kosu_title_40 = ws.cell(row = i + 1, column = 119).value, \
                               kosu_division_1_40 = ws.cell(row = i + 1, column = 120).value, \
                               kosu_division_2_40 = ws.cell(row = i + 1, column = 121).value, \
                               kosu_title_41 = ws.cell(row = i + 1, column = 122).value, \
                               kosu_division_1_41 = ws.cell(row = i + 1, column = 123).value, \
                               kosu_division_2_41 = ws.cell(row = i + 1, column = 124).value, \
                               kosu_title_42 = ws.cell(row = i + 1, column = 125).value, \
                               kosu_division_1_42 = ws.cell(row = i + 1, column = 126).value, \
                               kosu_division_2_42 = ws.cell(row = i + 1, column = 127).value, \
                               kosu_title_43 = ws.cell(row = i + 1, column = 128).value, \
                               kosu_division_1_43 = ws.cell(row = i + 1, column = 129).value, \
                               kosu_division_2_43 = ws.cell(row = i + 1, column = 130).value, \
                               kosu_title_44 = ws.cell(row = i + 1, column = 131).value, \
                               kosu_division_1_44 = ws.cell(row = i + 1, column = 132).value, \
                               kosu_division_2_44 = ws.cell(row = i + 1, column = 133).value, \
                               kosu_title_45 = ws.cell(row = i + 1, column = 134).value, \
                               kosu_division_1_45 = ws.cell(row = i + 1, column = 135).value, \
                               kosu_division_2_45 = ws.cell(row = i + 1, column = 136).value, \
                               kosu_title_46 = ws.cell(row = i + 1, column = 137).value, \
                               kosu_division_1_46 = ws.cell(row = i + 1, column = 138).value, \
                               kosu_division_2_46 = ws.cell(row = i + 1, column = 139).value, \
                               kosu_title_47 = ws.cell(row = i + 1, column = 140).value, \
                               kosu_division_1_47 = ws.cell(row = i + 1, column = 141).value, \
                               kosu_division_2_47 = ws.cell(row = i + 1, column = 142).value, \
                               kosu_title_48 = ws.cell(row = i + 1, column = 143).value, \
                               kosu_division_1_48 = ws.cell(row = i + 1, column = 144).value, \
                               kosu_division_2_48 = ws.cell(row = i + 1, column = 145).value, \
                               kosu_title_49 = ws.cell(row = i + 1, column = 146).value, \
                               kosu_division_1_49 = ws.cell(row = i + 1, column = 147).value, \
                               kosu_division_2_49 = ws.cell(row = i + 1, column = 148).value, \
                               kosu_title_50 = ws.cell(row = i + 1, column = 149).value, \
                               kosu_division_1_50 = ws.cell(row = i + 1, column = 150).value, \
                               kosu_division_2_50 = ws.cell(row = i + 1, column = 151).value)

      new_data.save()


  # 設定情報バックアップ処理
  if 'setting_backup' in request.POST:

    # 今日の日付取得
    today = datetime.date.today()

    # 新しいExcelブック作成
    wb = openpyxl.Workbook()
    # 書き込みシート選択
    ws = wb.worksheets[0]

    # 設定データ取得
    setting_data = administrator_data.objects.all()

    # Excelに書き込み(項目名)
    ws.cell(row = 1, column = 1, value = '一覧表示項目数')
    ws.cell(row = 1, column = 2, value = 'ファイル場所_P')
    ws.cell(row = 1, column = 3, value = 'ファイル場所_R')
    ws.cell(row = 1, column = 4, value = 'ファイル場所_W1')
    ws.cell(row = 1, column = 5, value = 'ファイル場所_W2')
    ws.cell(row = 1, column = 6, value = 'ファイル場所_T1')
    ws.cell(row = 1, column = 7, value = 'ファイル場所_T2')
    ws.cell(row = 1, column = 8, value = 'ファイル場所_A1')
    ws.cell(row = 1, column = 9, value = 'ファイル場所_A2')
    ws.cell(row = 1, column = 10, value = 'バックアップ場所')

    # Excelに書き込み(項目)
    for index, dt in enumerate(setting_data):
      ws.cell(row = index + 2, column = 1, value = dt.menu_row)
      ws.cell(row = index + 2, column = 2, value = dt.file_location_P)
      ws.cell(row = index + 2, column = 3, value = dt.file_location_R)
      ws.cell(row = index + 2, column = 4, value = dt.file_location_W1)
      ws.cell(row = index + 2, column = 5, value = dt.file_location_W2)
      ws.cell(row = index + 2, column = 6, value = dt.file_location_T1)
      ws.cell(row = index + 2, column = 7, value = dt.file_location_T2)
      ws.cell(row = index + 2, column = 8, value = dt.file_location_A1)
      ws.cell(row = index + 2, column = 9, value = dt.file_location_A2)
      ws.cell(row = index + 2, column = 10, value = dt.backup_file)

    wb.save(r'{}\{}_設定データバックアップ.xlsx'.format(default_data.backup_file, today))


  # 設定情報読み込み
  if 'setting_load' in request.POST:

    # POSTされたファイルパスを変数に入れる
    file_path = request.POST['setting_file']

    # 登録したファイルがない場合の処理
    if os.path.isfile(file_path) == False:
      # エラーメッセージ出力
      messages.error(request, 'ロードしようとしたファイルは存在しません。ERROR047')
      # このページをリダイレクト
      return redirect(to = 'administrator')

    # 指定Excelを開く
    wb = openpyxl.load_workbook('{}'.format(file_path), data_only = True)
    # 書き込みシート選択
    ws = wb.worksheets[0]

    # 読み込むファイルが正しいファイルでない場合エラー出力
    if ws.cell(1, 1).value != '一覧表示項目数' or ws.cell(1, 2).value != 'ファイル場所_P' or \
      ws.cell(1, 3).value != 'ファイル場所_R' or ws.cell(1, 4).value != 'ファイル場所_W1' or \
      ws.cell(1, 5).value != 'ファイル場所_W2' or ws.cell(1, 6).value != 'ファイル場所_T1' or \
      ws.cell(1, 7).value != 'ファイル場所_T2' or ws.cell(1, 8).value != 'ファイル場所_A1' or \
      ws.cell(1, 9).value != 'ファイル場所_A2' or ws.cell(1, 10).value != 'バックアップ場所':
      # エラーメッセージ出力
      messages.error(request, 'ロードしようとしたファイルは設定情報バックアップではありません。ERROR052')
      # このページをリダイレクト
      return redirect(to = 'administrator')

    # レコード数取得
    data_num = ws.max_row

    # 設定情報を全て削除
    setting_del = administrator_data.objects.all()
    setting_del.delete()
    # Excelからデータを読み込み
    for i in range(1, data_num):
      new_data = administrator_data(menu_row = ws.cell(row = i + 1, column = 1).value, \
                                    file_location_P = ws.cell(row = i + 1, column = 2).value, \
                                    file_location_R = ws.cell(row = i + 1, column = 3).value, \
                                    file_location_W1 = ws.cell(row = i + 1, column = 4).value, \
                                    file_location_W2 = ws.cell(row = i + 1, column = 5).value, \
                                    file_location_T1 = ws.cell(row = i + 1, column = 6).value, \
                                    file_location_T2 = ws.cell(row = i + 1, column = 7).value, \
                                    file_location_A1 = ws.cell(row = i + 1, column = 8).value, \
                                    file_location_A2 = ws.cell(row = i + 1, column = 9).value, \
                                    backup_file = ws.cell(row = i + 1, column = 10).value)

      new_data.save()

    # このページを読み直す
    return redirect(to = '/administrator')



  # HTMLに渡す辞書
  library_m = {
    'title' : '管理者MENU',
    'form' : form,
    }
  


  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/administrator_menu.html', library_m)





#--------------------------------------------------------------------------------------------------------





# ヘルプ画面定義
def help(request):

  # ルートディレクトリを取得
  BASE_DIR = Path(__file__).resolve().parent.parent
  # 環境変数ファイルを読み込む
  env = environ.Env()
  env.read_env(os.path.join(BASE_DIR, '.env'))


  # フォームを定義
  form = uploadForm(request.POST)



  # GET時の処理
  if (request.method == 'GET'):
    # ファイルロード欄非表示
    display = False



  # 復帰パスワード入力時処理
  if 'help_button' in request.POST:
    # パスワード判定
    if request.POST['help_path'] ==  env('HELP_PATH'):
      display = True
    else:
      display = False
      messages.error(request, 'パスワードが違います。ERROR042')
   


  # データ読み込み
  if 'data_load' in request.POST:
    
    # データ読み込み欄表示
    display = True


    # 人員ファイル定義
    uploaded_file = request.FILES['member_file']

    # 一時的なファイルをサーバー上に作成
    with open('member_file_path.xlsx', 'wb+') as destination:

      # アップロードしたファイルを一時ファイルに書き込み
      for chunk in uploaded_file.chunks():
        destination.write(chunk)

    # 一時ファイルを開く
    wb = openpyxl.load_workbook('member_file_path.xlsx')

    # 一番最初のシートを指定
    ws = wb.worksheets[0]

    # レコード数取得
    data_num = ws.max_row

    # 人員情報取得
    member_del = member.objects.all()


    # Excelからデータを読み込み
    for i in range(1, data_num):
      new_data = member(employee_No = ws.cell(row = i + 1, column = 1).value, \
                        name = ws.cell(row = i + 1, column = 2).value, \
                        shop = ws.cell(row = i + 1, column = 3).value, \
                        authority = ws.cell(row = i + 1, column = 4).value, \
                        administrator = ws.cell(row = i + 1, column = 5).value, \
                        break_time1 = ws.cell(row = i + 1, column = 6).value, \
                        break_time1_over1 = ws.cell(row = i + 1, column = 7).value, \
                        break_time1_over2 = ws.cell(row = i + 1, column = 8).value, \
                        break_time1_over3 = ws.cell(row = i + 1, column = 9).value, \
                        break_time2 = ws.cell(row = i + 1, column = 10).value, \
                        break_time2_over1 = ws.cell(row = i + 1, column = 11).value, \
                        break_time2_over2 = ws.cell(row = i + 1, column = 12).value, \
                        break_time2_over3 = ws.cell(row = i + 1, column = 13).value, \
                        break_time3 = ws.cell(row = i + 1, column = 14).value, \
                        break_time3_over1 = ws.cell(row = i + 1, column = 15).value, \
                        break_time3_over2 = ws.cell(row = i + 1, column = 16).value, \
                        break_time3_over3 = ws.cell(row = i + 1, column = 17).value, \
                        break_time4 = ws.cell(row = i + 1, column = 18).value, \
                        break_time4_over1 = ws.cell(row = i + 1, column = 19).value, \
                        break_time4_over2 = ws.cell(row = i + 1, column = 20).value, \
                        break_time4_over3 = ws.cell(row = i + 1, column = 21).value)                           

      new_data.save()


    # 一時ファイル削除
    os.remove('member_file_path.xlsx')



    # 工数定義区分ファイル定義
    uploaded_file = request.FILES['def_file']

    # 一時的なファイルをサーバー上に作成
    with open('def_file_path.xlsx', 'wb+') as destination:

      # アップロードしたファイルを一時ファイルに書き込み
      for chunk in uploaded_file.chunks():
        destination.write(chunk)

    # 一時ファイルを開く
    wb1 = openpyxl.load_workbook('def_file_path.xlsx')

    # 一番最初のシートを指定
    ws1 = wb1.worksheets[0]

    # レコード数取得
    data_num = ws1.max_row

    # 工数区分定義取得
    def_del = kosu_division.objects.all()


    # Excelからデータを読み込み
    for i in range(1, data_num):
      new_data1 = kosu_division(kosu_name = ws1.cell(row = i + 1, column = 1).value, \
                                kosu_title_1 = ws1.cell(row = i + 1, column = 2).value, \
                                kosu_division_1_1 = ws1.cell(row = i + 1, column = 3).value, \
                                kosu_division_2_1 = ws1.cell(row = i + 1, column = 4).value, \
                                kosu_title_2 = ws1.cell(row = i + 1, column = 5).value, \
                                kosu_division_1_2 = ws1.cell(row = i + 1, column = 6).value, \
                                kosu_division_2_2 = ws1.cell(row = i + 1, column = 7).value, \
                                kosu_title_3 = ws1.cell(row = i + 1, column = 8).value, \
                                kosu_division_1_3 = ws1.cell(row = i + 1, column = 9).value, \
                                kosu_division_2_3 = ws1.cell(row = i + 1, column = 10).value, \
                                kosu_title_4 = ws1.cell(row = i + 1, column = 11).value, \
                                kosu_division_1_4 = ws1.cell(row = i + 1, column = 12).value, \
                                kosu_division_2_4 = ws1.cell(row = i + 1, column = 13).value, \
                                kosu_title_5 = ws1.cell(row = i + 1, column = 14).value, \
                                kosu_division_1_5 = ws1.cell(row = i + 1, column = 15).value, \
                                kosu_division_2_5 = ws1.cell(row = i + 1, column = 16).value, \
                                kosu_title_6 = ws1.cell(row = i + 1, column = 17).value, \
                                kosu_division_1_6 = ws1.cell(row = i + 1, column = 18).value, \
                                kosu_division_2_6 = ws1.cell(row = i + 1, column = 19).value, \
                                kosu_title_7 = ws1.cell(row = i + 1, column = 20).value, \
                                kosu_division_1_7 = ws1.cell(row = i + 1, column = 21).value, \
                                kosu_division_2_7 = ws1.cell(row = i + 1, column = 22).value, \
                                kosu_title_8 = ws1.cell(row = i + 1, column = 23).value, \
                                kosu_division_1_8 = ws1.cell(row = i + 1, column = 24).value, \
                                kosu_division_2_8 = ws1.cell(row = i + 1, column = 25).value, \
                                kosu_title_9 = ws1.cell(row = i + 1, column = 26).value, \
                                kosu_division_1_9 = ws1.cell(row = i + 1, column = 27).value, \
                                kosu_division_2_9 = ws1.cell(row = i + 1, column = 28).value, \
                                kosu_title_10 = ws1.cell(row = i + 1, column = 29).value, \
                                kosu_division_1_10 = ws1.cell(row = i + 1, column = 30).value, \
                                kosu_division_2_10 = ws1.cell(row = i + 1, column = 31).value, \
                                kosu_title_11 = ws1.cell(row = i + 1, column = 32).value, \
                                kosu_division_1_11 = ws1.cell(row = i + 1, column = 33).value, \
                                kosu_division_2_11 = ws1.cell(row = i + 1, column = 34).value, \
                                kosu_title_12 = ws1.cell(row = i + 1, column = 35).value, \
                                kosu_division_1_12 = ws1.cell(row = i + 1, column = 36).value, \
                                kosu_division_2_12 = ws1.cell(row = i + 1, column = 37).value, \
                                kosu_title_13 = ws1.cell(row = i + 1, column = 38).value, \
                                kosu_division_1_13 = ws1.cell(row = i + 1, column = 39).value, \
                                kosu_division_2_13 = ws1.cell(row = i + 1, column = 40).value, \
                                kosu_title_14 = ws1.cell(row = i + 1, column = 41).value, \
                                kosu_division_1_14 = ws1.cell(row = i + 1, column = 42).value, \
                                kosu_division_2_14 = ws1.cell(row = i + 1, column = 43).value, \
                                kosu_title_15 = ws1.cell(row = i + 1, column = 44).value, \
                                kosu_division_1_15 = ws1.cell(row = i + 1, column = 45).value, \
                                kosu_division_2_15 = ws1.cell(row = i + 1, column = 46).value, \
                                kosu_title_16 = ws1.cell(row = i + 1, column = 47).value, \
                                kosu_division_1_16 = ws1.cell(row = i + 1, column = 48).value, \
                                kosu_division_2_16 = ws1.cell(row = i + 1, column = 49).value, \
                                kosu_title_17 = ws1.cell(row = i + 1, column = 50).value, \
                                kosu_division_1_17 = ws1.cell(row = i + 1, column = 51).value, \
                                kosu_division_2_17 = ws1.cell(row = i + 1, column = 52).value, \
                                kosu_title_18 = ws1.cell(row = i + 1, column = 53).value, \
                                kosu_division_1_18 = ws1.cell(row = i + 1, column = 54).value, \
                                kosu_division_2_18 = ws1.cell(row = i + 1, column = 55).value, \
                                kosu_title_19 = ws1.cell(row = i + 1, column = 56).value, \
                                kosu_division_1_19 = ws1.cell(row = i + 1, column = 57).value, \
                                kosu_division_2_19 = ws1.cell(row = i + 1, column = 58).value, \
                                kosu_title_20 = ws1.cell(row = i + 1, column = 59).value, \
                                kosu_division_1_20 = ws1.cell(row = i + 1, column = 60).value, \
                                kosu_division_2_20 = ws1.cell(row = i + 1, column = 61).value, \
                                kosu_title_21 = ws1.cell(row = i + 1, column = 62).value, \
                                kosu_division_1_21 = ws1.cell(row = i + 1, column = 63).value, \
                                kosu_division_2_21 = ws1.cell(row = i + 1, column = 64).value, \
                                kosu_title_22 = ws1.cell(row = i + 1, column = 65).value, \
                                kosu_division_1_22 = ws1.cell(row = i + 1, column = 66).value, \
                                kosu_division_2_22 = ws1.cell(row = i + 1, column = 67).value, \
                                kosu_title_23 = ws1.cell(row = i + 1, column = 68).value, \
                                kosu_division_1_23 = ws1.cell(row = i + 1, column = 69).value, \
                                kosu_division_2_23 = ws1.cell(row = i + 1, column = 70).value, \
                                kosu_title_24 = ws1.cell(row = i + 1, column = 71).value, \
                                kosu_division_1_24 = ws1.cell(row = i + 1, column = 72).value, \
                                kosu_division_2_24 = ws1.cell(row = i + 1, column = 73).value, \
                                kosu_title_25 = ws1.cell(row = i + 1, column = 74).value, \
                                kosu_division_1_25 = ws1.cell(row = i + 1, column = 75).value, \
                                kosu_division_2_25 = ws1.cell(row = i + 1, column = 76).value, \
                                kosu_title_26 = ws1.cell(row = i + 1, column = 77).value, \
                                kosu_division_1_26 = ws1.cell(row = i + 1, column = 78).value, \
                                kosu_division_2_26 = ws1.cell(row = i + 1, column = 79).value, \
                                kosu_title_27 = ws1.cell(row = i + 1, column = 80).value, \
                                kosu_division_1_27 = ws1.cell(row = i + 1, column = 81).value, \
                                kosu_division_2_27 = ws1.cell(row = i + 1, column = 82).value, \
                                kosu_title_28 = ws1.cell(row = i + 1, column = 83).value, \
                                kosu_division_1_28 = ws1.cell(row = i + 1, column = 84).value, \
                                kosu_division_2_28 = ws1.cell(row = i + 1, column = 85).value, \
                                kosu_title_29 = ws1.cell(row = i + 1, column = 86).value, \
                                kosu_division_1_29 = ws1.cell(row = i + 1, column = 87).value, \
                                kosu_division_2_29 = ws1.cell(row = i + 1, column = 88).value, \
                                kosu_title_30 = ws1.cell(row = i + 1, column = 89).value, \
                                kosu_division_1_30 = ws1.cell(row = i + 1, column = 90).value, \
                                kosu_division_2_30 = ws1.cell(row = i + 1, column = 91).value, \
                                kosu_title_31 = ws1.cell(row = i + 1, column = 92).value, \
                                kosu_division_1_31 = ws1.cell(row = i + 1, column = 93).value, \
                                kosu_division_2_31 = ws1.cell(row = i + 1, column = 94).value, \
                                kosu_title_32 = ws1.cell(row = i + 1, column = 95).value, \
                                kosu_division_1_32 = ws1.cell(row = i + 1, column = 96).value, \
                                kosu_division_2_32 = ws1.cell(row = i + 1, column = 97).value, \
                                kosu_title_33 = ws1.cell(row = i + 1, column = 98).value, \
                                kosu_division_1_33 = ws1.cell(row = i + 1, column = 99).value, \
                                kosu_division_2_33 = ws1.cell(row = i + 1, column = 100).value, \
                                kosu_title_34 = ws1.cell(row = i + 1, column = 101).value, \
                                kosu_division_1_34 = ws1.cell(row = i + 1, column = 102).value, \
                                kosu_division_2_34 = ws1.cell(row = i + 1, column = 103).value, \
                                kosu_title_35 = ws1.cell(row = i + 1, column = 104).value, \
                                kosu_division_1_35 = ws1.cell(row = i + 1, column = 105).value, \
                                kosu_division_2_35 = ws1.cell(row = i + 1, column = 106).value, \
                                kosu_title_36 = ws1.cell(row = i + 1, column = 107).value, \
                                kosu_division_1_36 = ws1.cell(row = i + 1, column = 108).value, \
                                kosu_division_2_36 = ws1.cell(row = i + 1, column = 109).value, \
                                kosu_title_37 = ws1.cell(row = i + 1, column = 110).value, \
                                kosu_division_1_37 = ws1.cell(row = i + 1, column = 111).value, \
                                kosu_division_2_37 = ws1.cell(row = i + 1, column = 112).value, \
                                kosu_title_38 = ws1.cell(row = i + 1, column = 113).value, \
                                kosu_division_1_38 = ws1.cell(row = i + 1, column = 114).value, \
                                kosu_division_2_38 = ws1.cell(row = i + 1, column = 115).value, \
                                kosu_title_39 = ws1.cell(row = i + 1, column = 116).value, \
                                kosu_division_1_39 = ws1.cell(row = i + 1, column = 117).value, \
                                kosu_division_2_39 = ws1.cell(row = i + 1, column = 118).value, \
                                kosu_title_40 = ws1.cell(row = i + 1, column = 119).value, \
                                kosu_division_1_40 = ws1.cell(row = i + 1, column = 120).value, \
                                kosu_division_2_40 = ws1.cell(row = i + 1, column = 121).value, \
                                kosu_title_41 = ws1.cell(row = i + 1, column = 122).value, \
                                kosu_division_1_41 = ws1.cell(row = i + 1, column = 123).value, \
                                kosu_division_2_41 = ws1.cell(row = i + 1, column = 124).value, \
                                kosu_title_42 = ws1.cell(row = i + 1, column = 125).value, \
                                kosu_division_1_42 = ws1.cell(row = i + 1, column = 126).value, \
                                kosu_division_2_42 = ws1.cell(row = i + 1, column = 127).value, \
                                kosu_title_43 = ws1.cell(row = i + 1, column = 128).value, \
                                kosu_division_1_43 = ws1.cell(row = i + 1, column = 129).value, \
                                kosu_division_2_43 = ws1.cell(row = i + 1, column = 130).value, \
                                kosu_title_44 = ws1.cell(row = i + 1, column = 131).value, \
                                kosu_division_1_44 = ws1.cell(row = i + 1, column = 132).value, \
                                kosu_division_2_44 = ws1.cell(row = i + 1, column = 133).value, \
                                kosu_title_45 = ws1.cell(row = i + 1, column = 134).value, \
                                kosu_division_1_45 = ws1.cell(row = i + 1, column = 135).value, \
                                kosu_division_2_45 = ws1.cell(row = i + 1, column = 136).value, \
                                kosu_title_46 = ws1.cell(row = i + 1, column = 137).value, \
                                kosu_division_1_46 = ws1.cell(row = i + 1, column = 138).value, \
                                kosu_division_2_46 = ws1.cell(row = i + 1, column = 139).value, \
                                kosu_title_47 = ws1.cell(row = i + 1, column = 140).value, \
                                kosu_division_1_47 = ws1.cell(row = i + 1, column = 141).value, \
                                kosu_division_2_47 = ws1.cell(row = i + 1, column = 142).value, \
                                kosu_title_48 = ws1.cell(row = i + 1, column = 143).value, \
                                kosu_division_1_48 = ws1.cell(row = i + 1, column = 144).value, \
                                kosu_division_2_48 = ws1.cell(row = i + 1, column = 145).value, \
                                kosu_title_49 = ws1.cell(row = i + 1, column = 146).value, \
                                kosu_division_1_49 = ws1.cell(row = i + 1, column = 147).value, \
                                kosu_division_2_49 = ws1.cell(row = i + 1, column = 148).value, \
                                kosu_title_50 = ws1.cell(row = i + 1, column = 149).value, \
                                kosu_division_1_50 = ws1.cell(row = i + 1, column = 150).value, \
                                kosu_division_2_50 = ws1.cell(row = i + 1, column = 151).value)

      new_data1.save()


    # 一時ファイル削除
    os.remove('def_file_path.xlsx')



    # 工数定義区分ファイル定義
    uploaded_file = request.FILES['setting_file']

    # 一時的なファイルをサーバー上に作成
    with open('setting_file_path.xlsx', 'wb+') as destination:

      # アップロードしたファイルを一時ファイルに書き込み
      for chunk in uploaded_file.chunks():
        destination.write(chunk)

    # 一時ファイルを開く
    wb2 = openpyxl.load_workbook('setting_file_path.xlsx')

    # 一番最初のシートを指定
    ws2 = wb2.worksheets[0]

    # レコード数取得
    data_num = ws2.max_row

    # 設定情報取得
    setting_del = administrator_data.objects.all()
    

    # Excelからデータを読み込み
    for i in range(1, data_num):
      new_data2 = administrator_data(menu_row = ws2.cell(row = i + 1, column = 1).value, \
                                     file_location_P = ws2.cell(row = i + 1, column = 2).value, \
                                     file_location_R = ws2.cell(row = i + 1, column = 3).value, \
                                     file_location_W1 = ws2.cell(row = i + 1, column = 4).value, \
                                     file_location_W2 = ws2.cell(row = i + 1, column = 5).value, \
                                     file_location_T1 = ws2.cell(row = i + 1, column = 6).value, \
                                     file_location_T2 = ws2.cell(row = i + 1, column = 7).value, \
                                     file_location_A1 = ws2.cell(row = i + 1, column = 8).value, \
                                     file_location_A2 = ws2.cell(row = i + 1, column = 9).value, \
                                     backup_file = ws2.cell(row = i + 1, column = 10).value)

      new_data2.save()



  # HTMLに渡す辞書
  library_m = {
    'title' : 'ヘルプ',
    'form' : form,
    'display' : display,
    }
  


  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/help.html', library_m)





#--------------------------------------------------------------------------------------------------------


