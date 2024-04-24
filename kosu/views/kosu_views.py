from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
import itertools
from .. import forms
from ..models import member
from ..models import Business_Time_graph
from ..models import kosu_division
from ..models import administrator_data
from ..forms import input_kosuForm
from ..forms import timeForm
from ..forms import kosu_dayForm
from ..forms import team_kosuForm
from ..forms import schedule_timeForm
from ..forms import scheduleForm





#--------------------------------------------------------------------------------------------------------





# 工数履歴画面定義
def kosu_list(request, num):


  # 今日の日時取得
  kosu_today = datetime.date.today()



  # セッションに検索履歴がある場合の処理
  if request.session.get('find_day', '') != '':

    # フォームの初期値に検索履歴を入れる
    start_list = {'kosu_day' : request.session.get('find_day', '')}

  
  # セッションに検索履歴がない場合の処理
  else:

    # フォームの初期値に今日の日付を入れる
    start_list = {'kosu_day' : str(kosu_today)}



  # ログイン者の情報取得
  member_data = member.objects.get(employee_no = request.session.get('login_No', None))

  # セッションにログインした従業員番号がない場合の処理
  if request.session.get('login_No', None) == None:

    # 未ログインならログインページに飛ぶ
    return redirect(to = '/login')



  # 設定データ取得
  page_num = administrator_data.objects.order_by("id").last()



  # POST時の処理
  if (request.method == 'POST'):

    # POST送信時のフォームの状態(POSTした値は入ったまま)
    form = kosu_dayForm(request.POST)

    # POSTした値をセッションに登録
    find = request.POST['kosu_day']
    request.session['find_day'] = find

    # 就業日とログイン者の従業員番号でフィルターをかけて一致した工数データを取得
    obj_filter = Business_Time_graph.objects.filter(work_day2__contains = find, \
                                                    employee_no3 = request.session.get('login_No', '')).\
                                                    order_by('work_day2').reverse()

    # 取得した工数データを1ページあたりの件数分取得
    data = Paginator(obj_filter, page_num.menu_row)


  # POSTしていない時の処理
  else:

    # POST送信していない時のフォームの状態(今日の日付が入ったフォーム)
    form = kosu_dayForm(start_list)

    # ログイン者の従業員番号でフィルターをかけて一致した工数データを取得
    obj_filter = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', ''), \
                                                    work_day2__contains = request.session.get('find_day', '')).\
                                                    order_by('work_day2').reverse()
    
    # 取得した工数データを1ページあたりの件数分取得
    data = Paginator(obj_filter, page_num.menu_row)



  # HTMLに渡す辞書
  library_m = {
    'title' : '工数履歴',
    'member_data' : member_data,
    'data' : data.get_page(num),
    'form' : form,
    'num' : num,
    }
  


  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/kosu_list.html', library_m)





#--------------------------------------------------------------------------------------------------------





# 工数入力画面定義
def input(request):


  # セッションにログインした従業員番号がない場合の処理
  if request.session.get('login_No', None) == None:

    # 未ログインならログインページに飛ぶ
    return redirect(to = '/login')



  # 今日の日時を変数に格納
  kosu_today = datetime.date.today()



  # ログイン者の情報取得
  member_obj = member.objects.get(employee_no = request.session.get('login_No', None))



  # セッションに就業日の履歴がない場合の処理
  if request.session.get('day', None) == None:

    # フォームの初期値に今日の日付を入れる
    new_work_day = kosu_today

  
  # セッションに就業日の履歴がある場合の処理
  else:

    # フォームの初期値に就業日の履歴を入れる
    new_work_day = request.session.get('day', None)



  # GET時の処理
  if (request.method == 'GET'):

    # グラフデータ確認用データ取得
    data_count = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None),\
                                                    work_day2 = new_work_day)


    # グラフラベルデータリセット
    graph_item = []

    # 0:00から23:55までの5分毎のリスト作成(グラフラベル用)
    for i in range(24):
        for n in range(0, 60, 5):
            t = n
            if n == 0:
              t = '00'
            if n == 5:
              t = '05'
            graph_item.append('{}:{}'.format(i, t))



    # 選択されている就業日のグラフデータがない場合の処理
    if data_count.count() == 0:

      # 0を288個入れたリスト作成
      graph_list = list(itertools.repeat(0, 288))


    # 選択されている就業日のグラフデータがある場合の処理
    else:

      # グラフデータを取得
      graph_obj = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', None),\
                                                  work_day2 = new_work_day)

      # 取得したグラフデータを文字型からリストに解凍
      graph_list = list(graph_obj.time_work)

      # グラフデータリスト内の各文字を定義
      str_list = ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', \
                    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', \
                      'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                          'q', 'r', 's', 't', 'u', 'v', 'w', 'x',]
      

      # グラフデータリスト内の各文字を数字に変更
      for i in range(288):

        for n, m in enumerate(str_list):

          if graph_list[i]  == m:

            graph_list[i] = n
            break


      # 作業内容が空でない場合の処理
      if graph_list != list(itertools.repeat(0, 288)):

        # 入力直が3直でない場合の処理
        if graph_obj.tyoku2 != '3':

          # 工数が入力され始めのインデント取得ループ
          for i in range(288):
            
            # 工数入力データが空でない時の処理
            if graph_list[i] != 0:

              # 最初のループである場合の処理
              if i == 0:
                
                # 工数が入力され始めのインデントで0を取得
                graph_start_index = i


              # 最初のループ以外の処理
              else:
                
                # 工数が入力され始めのインデントで最後の空データのインデント取得
                graph_start_index = i - 1
                # ループから抜ける
                break
          

          # 工数が入力され終わりのインデント取得ループ
          for i in range(1, 289):

            # 工数入力データが空でない場合の処理(後ろから順に)
            if graph_list[-i] != 0:

              # 最初のループの場合の処理
              if i == 1:

                # 工数が入力され終わりのインデント取得
                graph_end_index = 289 - i


              # 最初のループ以外の場合の処理
              else:

                # 工数が入力され終わりのインデント取得
                graph_end_index = 290 - i
                # ループから抜ける
                break


          # 入力直が1直の場合の処理
          if graph_obj.tyoku2 == '1':

            # 工数が入力され終わりのインデントが184以下である場合の処理(工数入力が15:20以前の場合)
            if graph_end_index <= 184:

              # 工数が入力され終わりのインデントを184にする(15:20の定時まで表示)
              graph_end_index = 184


          # 入力直が2直の場合の処理でログイン者のショップがボデーか組立の場合の処理
          if graph_obj.tyoku2 == '2' and (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
                                          member_obj.shop == 'A1' or member_obj.shop == 'A2'):
            
            # 工数が入力され終わりのインデントが240以下である場合の処理(工数入力が20:00以前の場合)
            if graph_end_index <= 240:

              # 工数が入力され終わりのインデントを240にする(20:00の定時まで表示)
              graph_end_index = 240


          # 入力直が2直の場合の処理でログイン者のショップがプレス、成形、塗装、その他、組長以上の場合の処理
          if graph_obj.tyoku2 == '2' and (member_obj.shop == 'P' or member_obj.shop == 'R' or \
                                          member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
                                          member_obj.shop == 'その他' or member_obj.shop == '組長以上'):
            
            # 工数が入力され終わりのインデントが270以下である場合の処理(工数入力が22:30以前の場合)
            if graph_end_index <= 270:

              # 工数が入力され終わりのインデントを270にする(22:30の定時まで表示)
              graph_end_index = 270


          # 入力直が常昼の場合の処理
          if graph_obj.tyoku2 == '4':

            # 工数が入力され終わりのインデントが204以下である場合の処理(工数入力が17:00以前の場合)
            if graph_end_index <= 204:

              # 工数が入力され終わりのインデントを204にする(17:00の定時まで表示)
              graph_end_index = 204


          # グラフ表示のリストを工数データが空の部分を削除する
          del graph_list[graph_end_index:]
          del graph_list[:graph_start_index]
          del graph_item[graph_end_index:]
          del graph_item[:graph_start_index]


        # 入力直が3直の場合の処理
        else:

          # グラフ表示のリストを2回繰り返す
          graph_list = graph_list*2
          graph_item = graph_item*2

          # 17時～のグラフ表示に変更
          del graph_list[:204]
          del graph_list[288:]
          del graph_item[:204]
          del graph_item[288:]


          # 工数が入力され始めのインデント取得ループ
          for i in range(288):

            # 工数入力データが空でない時の処理
            if graph_list[i] != 0:

              # 最初のループの場合の処理
              if i == 0:

                # 工数が入力され始めのインデントで0を取得
                graph_start_index = i


              # 最初のループ以外の場合の処理
              else:

                # 工数が入力され始めのインデントで最後の空データのインデント取得
                graph_start_index = i - 1
                # ループから抜ける
                break


          # 工数が入力され終わりのインデント取得ループ
          for i in range(1, 289):

            # 工数入力データが空でない場合の処理(後ろから順に)
            if graph_list[-i] != 0:

              # 最初のループの場合の処理
              if i == 1:

                # 工数が入力され終わりのインデント取得
                graph_end_index = 289 - i


              # 最初のループ以外の処理
              else:

                # 工数が入力され終わりのインデント取得
                graph_end_index = 290 - i
                break


          # ログイン者のショップがボデーか組立の場合の処理
          if member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
            member_obj.shop == 'A1' or member_obj.shop == 'A2':

            # 工数が入力され終わりのインデントが140以下である場合の処理(工数入力が4:40以前の場合)
            if graph_end_index <= 140:

              # 工数が入力され終わりのインデントを140にする(4:40の定時まで表示)
              graph_end_index = 140


          # ログイン者のショップがボデーか組立以外の場合の処理
          else:

            # 工数が入力され終わりのインデントが169以下である場合の処理(工数入力が7:05以前の場合)
            if graph_end_index <= 169:

              # 工数が入力され終わりのインデントを169にする(7:05の定時まで表示)
              graph_end_index = 169


          # グラフ表示のリストを工数データが空の部分を削除する
          del graph_list[graph_end_index:]
          del graph_list[:graph_start_index]
          del graph_item[graph_end_index:]
          del graph_item[:graph_start_index]



  # グラフ更新時の処理
  if "update" in request.POST:

    # POSTされた直をセッションに保存
    request.session['tyoku'] = request.POST['tyoku2']


    # 1直がPOSTされた場合の処理
    if request.POST['tyoku2'] == '1':

      # 作業終了時のセッションに06を定数として入れ直す
      request.session['end_hour'] = '06'
      # 作業終了分のセッションに30を定数として入れ直す
      request.session['end_min'] = '30'
  

    # 2直がPOSTされてログイン者のショップがボデーか組立の場合の処理
    if request.POST['tyoku2'] == '2' and (member_obj.shop == 'W1' or \
       member_obj.shop == 'W2' or member_obj.shop == 'A1' or member_obj.shop == 'A2'):
      
      # 作業終了時のセッションに11を定数として入れ直す
      request.session['end_hour'] = '11'
      # 作業終了分のセッションに10を定数として入れ直す
      request.session['end_min'] = '10'


    # 2直がPOSTされてログイン者のショップがプレス、成形、塗装、その他、組長以上の場合の処理
    if request.POST['tyoku2'] == '2' and (member_obj.shop == 'P' or \
       member_obj.shop == 'R' or member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
       member_obj.shop == 'その他' or member_obj.shop == '組長以上'):
      
      # 作業終了時のセッションに13を定数として入れ直す
      request.session['end_hour'] = '13'
      # 作業終了分のセッションに40を定数として入れ直す
      request.session['end_min'] = '40'


    # 3直がPOSTされてログイン者のショップがボデーか組立の場合の処理
    if request.POST['tyoku2'] == '3' and (member_obj.shop == 'W1' or \
       member_obj.shop == 'W2' or member_obj.shop == 'A1' or member_obj.shop == 'A2'):
      
      # 作業終了時のセッションに19を定数として入れ直す
      request.session['end_hour'] = '19'
      # 作業終了分のセッションに50を定数として入れ直す
      request.session['end_min'] = '50'


    # 3直がPOSTされてログイン者のショップがプレス、成形、塗装、その他、組長以上の場合の処理
    if request.POST['tyoku2'] == '3' and (member_obj.shop == 'P' or \
       member_obj.shop == 'R' or member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
       member_obj.shop == 'その他' or member_obj.shop == '組長以上'):
      
      # 作業終了時のセッションに22を定数として入れ直す
      request.session['end_hour'] = '22'
      # 作業終了分のセッションに10を定数として入れ直す
      request.session['end_min'] = '10'


    # 常昼がPOSTされた場合の処理
    if request.POST['tyoku2'] == '4':

      # 作業終了時のセッションに08を定数として入れ直す
      request.session['end_hour'] = '08'
      # 作業終了分のセッションに00を定数として入れ直す
      request.session['end_min'] = '00'


    # 更新された就業日をセッションに登録
    request.session['day'] = request.POST['work_day']

    # 更新された就業日を変数に入れる
    new_work_day = request.session.get('day', None)

    # グラフデータ確認用データ取得
    data_count = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None),\
                                                    work_day2 = new_work_day)


    # グラフラベルデータリセット
    graph_item = []


    # グラフラベルデータ作成ループ(時)
    for i in range(24):
        
        # グラフラベルデータ作成ループ(分)
        for n in range(0, 60, 5):
            
            # ループデータ取得
            t = n

            # ループデータ0の場合の処理
            if n == 0:

              # 2桁表示のstr型で定義
              t = '00'


            # ループデータ5の場合の処理
            if n == 5:

              # 2桁表示のstr型で定義
              t = '05'

            
            # グラフラベルデータリストに時間を順番に追加
            graph_item.append('{}:{}'.format(i, t))


    # 選択されている就業日のグラフデータがない場合の処理
    if data_count.count() == 0:

      # 0を288個入れたリスト作成
      graph_list = list(itertools.repeat(0, 288))


    # 選択されている就業日のグラフデータがある場合の処理
    else:

      # グラフデータを取得
      graph_obj = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', None),\
                                                  work_day2 = new_work_day)

      # 取得したグラフデータをリストに解凍
      graph_list = list(graph_obj.time_work)

      # グラフデータリスト内の各文字を数値に変更
      str_list = ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', \
                    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', \
                      'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                          'q', 'r', 's', 't', 'u', 'v', 'w', 'x',]


      # グラフデータリスト内の各文字を数字に変更
      for i in range(288):

        for n, m in enumerate(str_list):

          if graph_list[i]  == m:

            graph_list[i] = n
            break


      # 作業内容が空でない場合の処理
      if graph_obj.time_work != '#'*288:

        # 入力直が3直でない場合の処理
        if graph_obj.tyoku2 != '3':

          # 工数が入力され始めのインデント取得ループ
          for i in range(288):

            # 工数入力データが空でない時の処理
            if graph_list[i] != 0:

              # 最初のループである場合の処理
              if i == 0:

                # 工数が入力され始めのインデントで0を取得
                graph_start_index = i

              
              # 最初のループ以外の処理
              else:

                # 工数が入力され始めのインデントで最後の空データのインデント取得
                graph_start_index = i - 1

                # ループから抜ける
                break
          

          # 工数が入力され終わりのインデント取得ループ
          for i in range(1, 289):

            # 工数入力データが空でない場合の処理(後ろから順に)
            if graph_list[-i] != 0:

              # 最初のループである場合の処理
              if i == 1:

                # 工数が入力され終わりのインデント取得
                graph_end_index = 289 - i


              # 最初のループ以外の処理
              else:

                # 工数が入力され終わりのインデント取得
                graph_end_index = 290 - i

                # ループから抜ける
                break


          # 入力直が1直の場合の処理
          if graph_obj.tyoku2 == '1':

            # 工数が入力され終わりのインデントが184以下である場合の処理(工数入力が15:20以前の場合)
            if graph_end_index <= 184:

              # 工数が入力され終わりのインデントを184にする(15:20の定時まで表示)
              graph_end_index = 184


          # 入力直が2直でログイン者のショップがボデーか組立の場合の処理
          if graph_obj.tyoku2 == '2' and (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
                                          member_obj.shop == 'A1' or member_obj.shop == 'A2'):
            
            # 工数が入力され終わりのインデントが240以下である場合の処理(工数入力が20:00以前の場合)
            if graph_end_index <= 240:

              # 工数が入力され終わりのインデントを240にする(20:00の定時まで表示)
              graph_end_index = 240


          # 入力直が2直でログイン者のショップがプレス、成形、塗装、その他、組長以上の場合の処理
          if graph_obj.tyoku2 == '2' and (member_obj.shop == 'P' or member_obj.shop == 'R' or \
                                          member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
                                          member_obj.shop == 'その他' or member_obj.shop == '組長以上'):
            
            # 工数が入力され終わりのインデントが270以下である場合の処理(工数入力が22:30以前の場合)
            if graph_end_index <= 270:

              # 工数が入力され終わりのインデントを270にする(22:30の定時まで表示)
              graph_end_index = 270


          # 入力直が常昼の場合の処理
          if graph_obj.tyoku2 == '4':

            # 工数が入力され終わりのインデントが204以下である場合の処理(工数入力が17:00以前の場合)
            if graph_end_index <= 204:

              # 工数が入力され終わりのインデントを204にする(17:00の定時まで表示)
              graph_end_index = 204


          # グラフ表示のリストを工数データが空の部分を削除する
          del graph_list[graph_end_index:]
          del graph_list[:graph_start_index]
          del graph_item[graph_end_index:]
          del graph_item[:graph_start_index]


        # 入力直が3直の場合の処理
        else:

          # グラフ表示のリストを2回繰り返す
          graph_list = graph_list*2
          graph_item = graph_item*2

          # 17時～のグラフ表示に変更
          del graph_list[:204]
          del graph_list[288:]
          del graph_item[:204]
          del graph_item[288:]


          # 工数が入力され始めのインデント取得ループ
          for i in range(288):

            # 工数入力データが空でない時の処理
            if graph_list[i] != 0:

              # 最初のループである場合の処理
              if i == 0:

                # 工数が入力され始めのインデントで0を取得
                graph_start_index = i


              # 最初のループ以外の処理
              else:

                # 工数が入力され始めのインデントで最後の空データのインデント取得
                graph_start_index = i - 1

                # ループを抜ける
                break


          # 工数が入力され終わりのインデント取得ループ
          for i in range(1, 289):

            # 工数入力データが空でない場合の処理(後ろから順に)
            if graph_list[-i] != 0:

              # 最初のループである場合の処理
              if i == 1:

                # 工数が入力され終わりのインデント取得
                graph_end_index = 289 - i


              # 最初のループでない場合の処理
              else:

                # 工数が入力され終わりのインデント取得
                graph_end_index = 290 - i

                # ループから抜ける
                break


          # ログイン者のショップがボデーか組立の場合の処理
          if member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
            member_obj.shop == 'A1' or member_obj.shop == 'A2':


            # 工数が入力され終わりのインデントが140以下である場合の処理(工数入力が4:40以前の場合)
            if graph_end_index <= 140:

              # 工数が入力され終わりのインデントを140にする(4:40の定時まで表示)
              graph_end_index = 140


          # ログイン者のショップがボデーか組立以外の場合の処理
          else:

            # 工数が入力され終わりのインデントが169以下である場合の処理(工数入力が7:05以前の場合)
            if graph_end_index <= 169:

              # 工数が入力され終わりのインデントを169にする(7:05の定時まで表示)
              graph_end_index = 169

          # グラフ表示のリストを工数データが空の部分を削除する
          del graph_list[graph_end_index:]
          del graph_list[:graph_start_index]
          del graph_item[graph_end_index:]
          del graph_item[:graph_start_index]



  # 工数登録時の処理
  if "Registration" in request.POST:
    
    # それぞれPOSTされた値を変数に入れる(従業員番号のみセッション値)
    work_day = request.POST['work_day']
    tyoku = request.POST['tyoku2']
    start_hour = request.POST['start_hour']
    start_min = request.POST['start_min']
    end_hour = request.POST['end_hour']
    end_min = request.POST['end_min']
    def_work = request.POST['kosu_def_list']
    detail_work = request.POST['work_detail']
    work = request.POST['work']


    # 翌日チェック状態リセット
    check = 0

    # 翌日チェックが入っている場合の処理
    if ('tomorrow_check' in request.POST):

      # 翌日チェック状態に1を入れる
      check = 1

    
    # 翌日チェックが入っていない場合の処理
    else:

      # 翌日チェック状態に0を入れる
      check = 0


    # 直、工数区分、勤務、残業のいずれかが空欄の場合の処理
    if def_work == '' or work == '' or tyoku == '' or request.POST['over_work'] == '':

      # エラーメッセージ出力
      messages.error(request, '直、工数区分、勤務、残業のいずれかが未入力です。工数登録できませんでした。ERROR060')

      # このページをリダイレクト
      return redirect(to = '/input')


    # 作業詳細に'$'が含まれている場合の処理
    if '$' in detail_work:

      # エラーメッセージ出力
      messages.error(request, '作業詳細に『$』は使用できません。工数登録できませんでした。ERROR026')

      # このページをリダイレクト
      return redirect(to = '/input')


    # 作業詳細に文字数が100文字以上の場合の処理
    if len(detail_work) >= 100:
  
      # エラーメッセージ出力
      messages.error(request, '作業詳細は100文字以内で入力して下さい。工数登録できませんでした。ERROR059')
  
      # このページをリダイレクト
      return redirect(to = '/input')


    # 残業時間が15の倍数でない場合の処理
    if int(request.POST['over_work'])%15 != 0:
  
      # エラーメッセージ出力
      messages.error(request, '残業時間が15分の倍数になっていません。工数登録できませんでした。ERROR058')
  
      # このページをリダイレクト
      return redirect(to = '/input')


    # 作業開始時間と作業終了時間が同じ場合の処理
    if start_hour == end_hour and start_min == end_min:

      # エラーメッセージ出力
      messages.error(request, '作業時間が誤っています。確認して下さい。ERROR003')

      # このページをリダイレクト
      return redirect(to = '/input')


    # 作業開始時間が作業終了時間より遅い場合の処理
    if start_hour == end_hour and start_min > end_min and check == 0 or\
        start_hour > end_hour and check == 0:

      # エラーメッセージ出力
      messages.error(request, '作業開始時間が終了時間を越えています。翌日チェックを忘れていませんか？ERROR004')

      # このページをリダイレクト
      return redirect(to = '/input')


    # 作業時間が長い場合の処理
    if (int(start_hour) - int(end_hour)) <= 2 and check == 1:

      # エラーメッセージ出力
      messages.error(request, '作業時間が長すぎます。作業時間が誤ってませんか？ERROR005')

      # このページをリダイレクト
      return redirect(to = '/input')


    # 指定日に工数データが既にあるか確認
    obj_filter = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None), \
                                                    work_day2 = work_day)

    # 作業開始時間のインデント取得
    start_time = int(start_hour)*12 + int(start_min)/5
    # 作業終了時間のインデント取得
    end_time = int(end_hour)*12 + int(end_min)/5


    # 入力日が作業内容データに登録がある場合の処理
    if obj_filter.count() != 0:

      # 作業内容データからログイン者の従業員番号と就業日が一致したオブジェクトを変数に入れる
      obj_get = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', None), \
                                                work_day2 = work_day)

      # 作業内容データを文字列からリストに解凍
      kosu_def = list(obj_get.time_work)

      # 作業詳細データを文字列からリストに解凍
      detail_list = obj_get.detail_work.split('$')


      # 以前同日に打ち込んだ工数区分定義と違う場合の処理
      if obj_get.def_ver2 != request.session.get('input_def', None) and obj_get.def_ver2 != '':

        # エラーメッセージ出力
        messages.error(request, '前に入力された工数と工数区分定義のVerが違います。入力できません。ERROR007')

        # このページをリダイレクト
        return redirect(to = '/input')


      # 工数データに休憩時間データ無いか直が変更されている場合の処理
      if obj_get.breaktime == None or obj_get.breaktime_over1 == None or \
        obj_get.breaktime_over2 == None or obj_get.breaktime_over3 == None or \
          obj_get.tyoku2 != tyoku:

        # 休憩時間取得
        break_time_obj = member.objects.get(employee_no = request.session.get('login_No', None))

        # 1直の場合の休憩時間取得
        if request.POST['tyoku2'] == '1':
          breaktime = break_time_obj.break_time1
          breaktime_over1 = break_time_obj.break_time1_over1
          breaktime_over2 = break_time_obj.break_time1_over2
          breaktime_over3 = break_time_obj.break_time1_over3

        # 2直の場合の休憩時間取得
        if request.POST['tyoku2'] == '2':
          breaktime = break_time_obj.break_time2
          breaktime_over1 = break_time_obj.break_time2_over1
          breaktime_over2 = break_time_obj.break_time2_over2
          breaktime_over3 = break_time_obj.break_time2_over3

        # 3直の場合の休憩時間取得
        if request.POST['tyoku2'] == '3':
          breaktime = break_time_obj.break_time3
          breaktime_over1 = break_time_obj.break_time3_over1
          breaktime_over2 = break_time_obj.break_time3_over2
          breaktime_over3 = break_time_obj.break_time3_over3

        # 常昼の場合の休憩時間取得
        if request.POST['tyoku2'] == '4':
          breaktime = break_time_obj.break_time4
          breaktime_over1 = break_time_obj.break_time4_over1
          breaktime_over2 = break_time_obj.break_time4_over2
          breaktime_over3 = break_time_obj.break_time4_over3


      # 工数データに休憩時間データある場合の処理
      else:

        # 休憩時間取得
        breaktime = obj_get.breaktime
        breaktime_over1 = obj_get.breaktime_over1
        breaktime_over2 = obj_get.breaktime_over2
        breaktime_over3 = obj_get.breaktime_over3


      # 休憩1開始時間のインデント取得
      break_start1 = int(breaktime[0 : 2])*12 + int(breaktime[2 : 4])/5

      # 休憩1終了時間のインデント取得
      break_end1 = int(breaktime[4 : 6])*12 + int(breaktime[6 :])/5


      # 休憩1の日またぎ変数リセット
      break_next_day1 = 0

      # 休憩開始時間より終了時間の方が早い場合の処理
      if break_start1 > break_end1:

        # 休憩1の日またぎ変数に1を入れる
        break_next_day1 = 1


      # 休憩開始時間より終了時間の方が遅い場合の処理
      else:

        # 休憩1の日またぎ変数に0を入れる
        break_next_day1 = 0


      # 休憩2開始時間のインデント取得
      break_start2 = int(breaktime_over1[0 : 2])*12 + int(breaktime_over1[2 : 4])/5

      # 休憩2終了時間のインデント取得
      break_end2 = int(breaktime_over1[4 : 6])*12 + int(breaktime_over1[6 :])/5


      # 休憩2の日またぎ変数リセット
      break_next_day2 = 0

      # 休憩開始時間より終了時間の方が早い場合の処理
      if break_start2 > break_end2:

        # 休憩2の日またぎ変数に1を入れる
        break_next_day2 = 1


      # 休憩開始時間より終了時間の方が遅い場合の処理
      else:

        # 休憩2の日またぎ変数に0を入れる
        break_next_day2 = 0


      # 休憩3開始時間のインデント取得
      break_start3 = int(breaktime_over2[0 : 2])*12 + int(breaktime_over2[2 : 4])/5
  
      # 休憩3終了時間のインデント取得
      break_end3 = int(breaktime_over2[4 : 6])*12 + int(breaktime_over2[6 :])/5


      # 休憩3の日またぎ変数リセット
      break_next_day3 = 0

      # 休憩開始時間より終了時間の方が早い場合の処理
      if break_start3 > break_end3:

        # 休憩3の日またぎ変数に1を入れる
        break_next_day3 = 1


      # 休憩開始時間より終了時間の方が遅い場合の処理
      else:

        # 休憩3の日またぎ変数に0を入れる
        break_next_day3 = 0


      # 休憩4開始時間のインデント取得
      break_start4 = int(breaktime_over3[0 : 2])*12 + int(breaktime_over3[2 : 4])/5

      # 休憩4終了時間のインデント取得
      break_end4 = int(breaktime_over3[4 : 6])*12 + int(breaktime_over3[6 :])/5


      # 休憩4の日またぎ変数リセット
      break_next_day4 = 0

      # 休憩開始時間より終了時間の方が早い場合の処理
      if break_start4 > break_end4:

        # 休憩4の日またぎ変数に1を入れる
        break_next_day4 = 1


      # 休憩開始時間より終了時間の方が遅い場合の処理
      else:

        # 休憩4の日またぎ変数に0を入れる
        break_next_day4 = 0


      # 入力時間が日をまたいでいない場合の処理
      if check == 0:

        # 工数に被りがないかチェックするループ
        for kosu in range(int(start_time), int(end_time)):

          # 工数データの要素が空でない場合の処理
          if kosu_def[kosu] != '#':

            # エラーメッセージ出力
            messages.error(request, '入力された作業時間には既に工数が入力されているので入力できません。ERROR008')

            # このページをリダイレクト
            return redirect(to = '/input')


        # 作業内容と作業詳細を書き込むループ
        for kosu in range(int(start_time), int(end_time)):

          # 作業内容リストに入力された工数定義区分の対応する記号を入れる
          kosu_def[kosu] = def_work

          # 作業詳細リストに入力した作業詳細を入れる
          detail_list[kosu] = detail_work


        # 休憩1が日を超えている場合の処理
        if break_next_day1 == 1:

          # 休憩時間内の工数データと作業詳細を消すループ(休憩時間開始～24時まで)
          for bt1 in range(int(break_start1), 288):

            # 作業内容リストの要素を空にする
            kosu_def[bt1] = '#'

            # 作業詳細リストの要素を空にする
            detail_list[bt1] = ''


          # 休憩時間内の工数データと作業詳細を消すループ(0時～休憩時間終了まで)
          for bt1 in range(0, int(break_end1)):

            # 作業内容リストの要素を空にする
            kosu_def[bt1] = '#'

            # 作業詳細リストの要素を空にする
            detail_list[bt1] = ''


        # 休憩1が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消すループ
          for bt1 in range(int(break_start1), int(break_end1)):

            # 作業内容リストの要素を空にする
            kosu_def[bt1] = '#'

            # 作業詳細リストの要素を空にする
            detail_list[bt1] = ''


        # 休憩2が日を超えている場合の処理
        if break_next_day2 == 1:

          # 休憩時間内の工数データと作業詳細を消すループ(休憩時間開始～24時まで)
          for bt2 in range(int(break_start2), 288):

            # 作業内容リストの要素を空にする
            kosu_def[bt2] = '#'

            # 作業詳細リストの要素を空にする
            detail_list[bt2] = ''


          # 休憩時間内の工数データと作業詳細を消すループ(0時～休憩時間終了まで)
          for bt2 in range(0, int(break_end2)):

            # 作業内容リストの要素を空にする
            kosu_def[bt2] = '#'

            # 作業詳細リストの要素を空にする
            detail_list[bt2] = ''


        # 休憩2が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消すループ
          for bt2 in range(int(break_start2), int(break_end2)):

            # 作業内容リストの要素を空にする
            kosu_def[bt2] = '#'

            # 作業詳細リストの要素を空にする
            detail_list[bt2] = ''


        # 休憩3が日を超えている場合の処理
        if break_next_day3 == 1:

          # 休憩時間内の工数データと作業詳細を消すループ(休憩時間開始～24時まで)
          for bt3 in range(int(break_start3), 288):

            # 作業内容リストの要素を空にする
            kosu_def[bt3] = '#'

            # 作業詳細リストの要素を空にする
            detail_list[bt3] = ''

          # 休憩時間内の工数データと作業詳細を消すループ(0時～休憩時間終了まで)
          for bt2 in range(0, int(break_end3)):

            # 作業内容リストの要素を空にする
            kosu_def[bt3] = '#'

            # 作業詳細リストの要素を空にする
            detail_list[bt3] = ''


        # 休憩3が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消す
          for bt3 in range(int(break_start3), int(break_end3)):

            # 作業内容リストの要素を空にする
            kosu_def[bt3] = '#'

            # 作業詳細リストの要素を空にする
            detail_list[bt3] = ''


        # 休憩4が日を超えている場合の処理
        if break_next_day4 == 1:

          # 休憩時間内の工数データと作業詳細を消すループ(休憩時間開始～24時まで)
          for bt4 in range(int(break_start4), 288):

            # 作業内容リストの要素を空にする
            kosu_def[bt4] = '#'

            # 作業詳細リストの要素を空にする
            detail_list[bt4] = ''


          # 休憩時間内の工数データと作業詳細を消すループ(0時～休憩時間終了まで)
          for bt4 in range(0, int(break_end4)):

            # 作業内容リストの要素を空にする
            kosu_def[bt4] = '#'

            # 作業詳細リストの要素を空にする
            detail_list[bt4] = ''


        # 休憩4が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消すループ
          for bt4 in range(int(break_start4), int(break_end4)):

            # 作業内容リストの要素を空にする
            kosu_def[bt4] = '#'

            # 作業詳細リストの要素を空にする
            detail_list[bt4] = ''


      # 入力時間が日をまたいでいる場合の処理
      if check == 1:

        # 工数に被りがないかチェックするループ
        for kosu in range(int(start_time), 288):

          # 作業内容の要素が空でない場合の処理
          if kosu_def[kosu] != '#':

            # エラーメッセージ出力
            messages.error(request, '入力された作業時間には既に工数が入力されているので入力できません。ERROR009')

            # このページをリダイレクト
            return redirect(to = '/input')


        # 工数に被りがないかチェックするループ
        for kosu in range(0, int(end_time)):

          # 作業内容の要素が空でない場合の処理
          if kosu_def[kosu] != '#':

            # エラーメッセージ出力
            messages.error(request, '入力された作業時間には既に工数が入力されているので入力できません。ERROR010')

            # このページをリダイレクト
            return redirect(to = '/input')


        # 作業内容と作業詳細を書き込むループ(作業開始時間から24時まで)
        for kosu in range(int(start_time), 288):

          # 作業内容リストに入力した工数区分定義の対応する記号を入れる
          kosu_def[kosu] = def_work

          # 作業詳細リストに入力した作業詳細を入れる
          detail_list[kosu] = detail_work


        # 作業内容と作業詳細を書き込むループ(0時から作業終了時間まで)
        for kosu in range(0, int(end_time)):

          # 作業内容リストに入力した工数区分定義の対応する記号を入れる
          kosu_def[kosu] = def_work

          # 作業詳細リストに入力した作業詳細を入れる
          detail_list[kosu] = detail_work


        # 休憩1が日を超えている場合の処理
        if break_next_day1 == 1:

          # 休憩時間内の工数データと作業詳細を消すループ(休憩時間開始～24時まで)
          for bt1 in range(int(break_start1), 288):

            # 作業内容リストに入力した工数区分定義の対応する記号を入れる
            kosu_def[bt1] = '#'

            # 作業詳細リストに入力した作業詳細を入れる
            detail_list[bt1] = ''


          # 休憩時間内の工数データと作業詳細を消すループ(0時から作業終了時間まで)
          for bt1 in range(0, int(break_end1)):

            # 作業内容リストに入力した工数区分定義の対応する記号を入れる
            kosu_def[bt1] = '#'

            # 作業詳細リストに入力した作業詳細を入れる
            detail_list[bt1] = ''


        # 休憩1が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消すループ
          for bt1 in range(int(break_start1), int(break_end1)):

            # 作業内容リストに入力した工数区分定義の対応する記号を入れる
            kosu_def[bt1] = '#'

            # 作業詳細リストに入力した作業詳細を入れる
            detail_list[bt1] = ''


        # 休憩2が日を超えている場合の処理
        if break_next_day2 == 1:

          # 休憩時間内の工数データと作業詳細を消すループ(休憩時間開始～24時まで)
          for bt2 in range(int(break_start2), 288):

            # 作業内容リストに入力した工数区分定義の対応する記号を入れる
            kosu_def[bt2] = '#'

            # 作業詳細リストに入力した作業詳細を入れる
            detail_list[bt2] = ''

          # 休憩時間内の工数データと作業詳細を消すループ(0時から作業終了時間まで)
          for bt2 in range(0, int(break_end2)):

            # 作業内容リストに入力した工数区分定義の対応する記号を入れる
            kosu_def[bt2] = '#'

            # 作業詳細リストに入力した作業詳細を入れる
            detail_list[bt2] = ''


        # 休憩2が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消すループ
          for bt2 in range(int(break_start2), int(break_end2)):

            # 作業内容リストに入力した工数区分定義の対応する記号を入れる
            kosu_def[bt2] = '#'

            # 作業詳細リストに入力した作業詳細を入れる
            detail_list[bt2] = ''


        # 休憩3が日を超えている場合の処理
        if break_next_day3 == 1:

          # 休憩時間内の工数データと作業詳細を消すループ(休憩時間開始～24時まで)
          for bt3 in range(int(break_start3), 288):

            # 作業内容リストに入力した工数区分定義の対応する記号を入れる
            kosu_def[bt3] = '#'

            # 作業詳細リストに入力した作業詳細を入れる
            detail_list[bt3] = ''

          # 休憩時間内の工数データと作業詳細を消すループ(0時から作業終了時間まで)
          for bt2 in range(0, int(break_end3)):

            # 作業内容リストに入力した工数区分定義の対応する記号を入れる
            kosu_def[bt3] = '#'

            # 作業詳細リストに入力した作業詳細を入れる
            detail_list[bt3] = ''


        # 休憩3が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消すループ
          for bt3 in range(int(break_start3), int(break_end3)):

            # 作業内容リストに入力した工数区分定義の対応する記号を入れる
            kosu_def[bt3] = '#'

            # 作業詳細リストに入力した作業詳細を入れる
            detail_list[bt3] = ''


        # 休憩4が日を超えている場合の処理
        if break_next_day4 == 1:

          # 休憩時間内の工数データと作業詳細を消すループ(休憩時間開始～24時まで)
          for bt4 in range(int(break_start4), 288):

            # 作業内容リストに入力した工数区分定義の対応する記号を入れる
            kosu_def[bt4] = '#'

            # 作業詳細リストに入力した作業詳細を入れる
            detail_list[bt4] = ''


          # 休憩時間内の工数データと作業詳細を消すループ(0時から作業終了時間まで)
          for bt4 in range(0, int(break_end4)):

            # 作業内容リストに入力した工数区分定義の対応する記号を入れる
            kosu_def[bt4] = '#'

            # 作業詳細リストに入力した作業詳細を入れる
            detail_list[bt4] = ''


        # 休憩4が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消すループ
          for bt4 in range(int(break_start4), int(break_end4)):

            # 作業内容リストに入力した工数区分定義の対応する記号を入れる
            kosu_def[bt4] = '#'

            # 作業詳細リストに入力した作業詳細を入れる
            detail_list[bt4] = ''


      # 作業詳細変数リセット
      detail_list_str = ''

      # 作業詳細リストをstr型に変更するループ
      for i, e in enumerate(detail_list):

        # 最終ループの処理
        if i == len(detail_list) - 1:

          # 作業詳細変数に作業詳細リストの要素をstr型で追加する
          detail_list_str = detail_list_str + detail_list[i]


        # 最終ループ以外の処理
        else:

          # 作業詳細変数に作業詳細リストの要素をstr型で追加し、区切り文字の'$'も追加
          detail_list_str = detail_list_str + detail_list[i] + '$'


      # 工数合計変数リセット
      kosu_total = 0


      # 工数の合計を計算するループ
      for k in kosu_def:

        # 作業内容が入っている場合の処理
        if k != '#':

          # 工数の合計に5分加算
          kosu_total += 5


      # 工数入力OK_NGリセット
      judgement = False


      # 出勤、休出時、工数合計と残業に整合性がある場合の処理
      if (work == '出勤' or work == 'シフト出') and \
        kosu_total - int(request.POST['over_work']) == 470:

        # 工数入力OK_NGをOKに切り替え
        judgement = True


      # 休出時、工数合計と残業に整合性がある場合の処理
      if work == '休出' and kosu_total == int(request.POST['over_work']):

        # 工数入力OK_NGをOKに切り替え
        judgement = True


      # 早退・遅刻時、工数合計と残業に整合性がある場合の処理
      if work == '早退・遅刻' and kosu_total != 0:

        # 工数入力OK_NGをOKに切り替え
        judgement = True


      # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Cで1直の場合の処理
      if (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
        member_obj.shop == 'A1' or member_obj.shop == 'A2') and \
          tyoku == '1':

        # 半前年休時、工数合計と残業に整合性がある場合の処理
        if work == '半前年休' and kosu_total - int(request.POST['over_work']) == 230:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


        # 半後年休時、工数合計と残業に整合性がある場合の処理
        if work == '半後年休' and kosu_total - int(request.POST['over_work']) == 240:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


      # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Cで2直の場合の処理
      if (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
        member_obj.shop == 'A1' or member_obj.shop == 'A2') and \
          tyoku == '2':

        # 半前年休時、工数合計と残業に整合性がある場合の処理
        if work == '半前年休' and kosu_total - int(request.POST['over_work']) == 290:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


        # 半後年休時、工数合計と残業に整合性がある場合の処理
        if work == '半後年休' and kosu_total - int(request.POST['over_work']) == 180:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


      # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Cで3直の場合の処理
      if (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
        member_obj.shop == 'A1' or member_obj.shop == 'A2') and \
          tyoku == '3':

        # 半前年休時、工数合計と残業に整合性がある場合の処理
        if work == '半前年休' and kosu_total - int(request.POST['over_work']) == 230:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


        # 半後年休時、工数合計と残業に整合性がある場合の処理
        if work == '半後年休' and kosu_total - int(request.POST['over_work']) == 240:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


      # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Bで1直の場合の処理
      if (member_obj.shop == 'P' or member_obj.shop == 'R' or \
        member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
          member_obj.shop == 'その他' or member_obj.shop == '組長以上') and \
          tyoku == '1':

        # 半前年休時、工数合計と残業に整合性がある場合の処理
        if work == '半前年休' and kosu_total - int(request.POST['over_work']) == 220:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


        # 半後年休時、工数合計と残業に整合性がある場合の処理
        if work == '半後年休' and kosu_total - int(request.POST['over_work']) == 250:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


      # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Bで2直の場合の処理
      if (member_obj.shop == 'P' or member_obj.shop == 'R' or \
        member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
          member_obj.shop == 'その他' or member_obj.shop == '組長以上') and \
          tyoku == '2':

        # 半前年休時、工数合計と残業に整合性がある場合の処理
        if work == '半前年休' and kosu_total - int(request.POST['over_work']) == 230:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


        # 半後年休時、工数合計と残業に整合性がある場合の処理
        if work == '半後年休' and kosu_total - int(request.POST['over_work']) == 240:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


      # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Bで3直の場合の処理
      if (member_obj.shop == 'P' or member_obj.shop == 'R' or \
        member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
          member_obj.shop == 'その他' or member_obj.shop == '組長以上') and \
          tyoku == '3':

        # 半前年休時、工数合計と残業に整合性がある場合の処理
        if work == '半前年休' and kosu_total - int(request.POST['over_work']) == 275:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


        # 半後年休時、工数合計と残業に整合性がある場合の処理
        if work == '半後年休' and kosu_total - int(request.POST['over_work']) == 195:

          # 工数入力OK_NGをOKに切り替え
          judgement = True



      # 作業内容データの内容を上書きして更新
      Business_Time_graph.objects.update_or_create(employee_no3 = request.session.get('login_No', None), \
        work_day2 = work_day, defaults = {'def_ver2' : request.session.get('input_def', None), \
                                          'work_time' : work, \
                                          'tyoku2' : tyoku, \
                                          'time_work' : ''.join(kosu_def), \
                                          'over_time' : request.POST['over_work'], \
                                          'detail_work' : detail_list_str,\
                                          'breaktime' : breaktime, \
                                          'breaktime_over1' : breaktime_over1, \
                                          'breaktime_over2' : breaktime_over2, \
                                          'breaktime_over3' : breaktime_over3, \
                                          'judgement' : judgement})



    # 入力日が作業内容データに登録がない場合の処理
    if obj_filter.count() == 0:

      # '#'が288個並んだ作業内容リスト作成
      kosu_def = list(itertools.repeat('#', 288))

      # ''が288個並んだ作業詳細リスト作成
      detail_list = list(itertools.repeat('', 288))

      # 休憩時間取得
      break_time_obj = member.objects.get(employee_no = request.session.get('login_No', None))

      # 1直の場合の休憩時間取得
      if request.POST['tyoku2'] == '1':
        breaktime = break_time_obj.break_time1
        breaktime_over1 = break_time_obj.break_time1_over1
        breaktime_over2 = break_time_obj.break_time1_over2
        breaktime_over3 = break_time_obj.break_time1_over3

      # 2直の場合の休憩時間取得
      if request.POST['tyoku2'] == '2':
        breaktime = break_time_obj.break_time2
        breaktime_over1 = break_time_obj.break_time2_over1
        breaktime_over2 = break_time_obj.break_time2_over2
        breaktime_over3 = break_time_obj.break_time2_over3

      # 3直の場合の休憩時間取得
      if request.POST['tyoku2'] == '3':
        breaktime = break_time_obj.break_time3
        breaktime_over1 = break_time_obj.break_time3_over1
        breaktime_over2 = break_time_obj.break_time3_over2
        breaktime_over3 = break_time_obj.break_time3_over3

      # 常昼の場合の休憩時間取得
      if request.POST['tyoku2'] == '4':
        breaktime = break_time_obj.break_time4
        breaktime_over1 = break_time_obj.break_time4_over1
        breaktime_over2 = break_time_obj.break_time4_over2
        breaktime_over3 = break_time_obj.break_time4_over3

      # 休憩1開始時間のインデント取得
      break_start1 = int(breaktime[0 : 2])*12 + int(breaktime[2 : 4])/5

      # 休憩1終了時間のインデント取得
      break_end1 = int(breaktime[4 : 6])*12 + int(breaktime[6 :])/5

      # 休憩1が日をまたいでいないか確認
      break_next_day1 = 0
      if break_start1 > break_end1:
        break_next_day1 = 1
      else:
        break_next_day1 = 0

      # 休憩2開始時間のインデント取得
      break_start2 = int(breaktime_over1[0 : 2])*12 + int(breaktime_over1[2 : 4])/5
      # 休憩2終了時間のインデント取得
      break_end2 = int(breaktime_over1[4 : 6])*12 + int(breaktime_over1[6 :])/5

      # 休憩2が日をまたいでいないか確認
      break_next_day2 = 0
      if break_start2 > break_end2:
        break_next_day2 = 1
      else:
        break_next_day2 = 0

      # 休憩3開始時間のインデント取得
      break_start3 = int(breaktime_over2[0 : 2])*12 + int(breaktime_over2[2 : 4])/5
      # 休憩3終了時間のインデント取得
      break_end3 = int(breaktime_over2[4 : 6])*12 + int(breaktime_over2[6 :])/5

      # 休憩3が日をまたいでいないか確認
      break_next_day3 = 0
      if break_start3 > break_end3:
        break_next_day3 = 1
      else:
        break_next_day3 = 0

      # 休憩4開始時間のインデント取得
      break_start4 = int(breaktime_over3[0 : 2])*12 + int(breaktime_over3[2 : 4])/5
      # 休憩4終了時間のインデント取得
      break_end4 = int(breaktime_over3[4 : 6])*12 + int(breaktime_over3[6 :])/5

      # 休憩4が日をまたいでいないか確認
      break_next_day4 = 0
      if break_start4 > break_end4:
        break_next_day4 = 1
      else:
        break_next_day4 = 0

      # 入力時間が日をまたいでいない場合の処理
      if check == 0:

        # リストの作業時間に合った場所に工数区分と作業詳細を入れる
        for kosu in range(int(start_time), int(end_time)):
          kosu_def[kosu] = def_work
          detail_list[kosu] = detail_work


        # 休憩1が日を超えている場合の処理
        if break_next_day1 == 1:

          # 休憩時間内の工数データと作業詳細を消す
          for bt1 in range(int(break_start1), 288):
            kosu_def[bt1] = '#'
            detail_list[bt1] = ''

          # 休憩時間内の工数データと作業詳細を消す
          for bt1 in range(0, int(break_end1)):
            kosu_def[bt1] = '#'
            detail_list[bt1] = ''

        # 休憩1が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消す
          for bt1 in range(int(break_start1), int(break_end1)):
            kosu_def[bt1] = '#'
            detail_list[bt1] = ''


        # 休憩2が日を超えている場合の処理
        if break_next_day2 == 1:

          # 休憩時間内の工数データと作業詳細を消す
          for bt2 in range(int(break_start2), 288):
            kosu_def[bt2] = '#'
            detail_list[bt2] = ''

          # 休憩時間内の工数データと作業詳細を消す
          for bt2 in range(0, int(break_end2)):
            kosu_def[bt2] = '#'
            detail_list[bt2] = ''

        # 休憩2が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消す
          for bt2 in range(int(break_start2), int(break_end2)):
            kosu_def[bt2] = '#'
            detail_list[bt2] = ''


        # 休憩3が日を超えている場合の処理
        if break_next_day3 == 1:

          # 休憩時間内の工数データと作業詳細を消す
          for bt3 in range(int(break_start3), 288):
            kosu_def[bt3] = '#'
            detail_list[bt3] = ''

          # 休憩時間内の工数データと作業詳細を消す
          for bt2 in range(0, int(break_end3)):
            kosu_def[bt3] = '#'
            detail_list[bt3] = ''

        # 休憩3が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消す
          for bt3 in range(int(break_start3), int(break_end3)):
            kosu_def[bt3] = '#'
            detail_list[bt3] = ''


        # 休憩4が日を超えている場合の処理
        if break_next_day4 == 1:

          # 休憩時間内の工数データと作業詳細を消す
          for bt4 in range(int(break_start4), 288):
            kosu_def[bt4] = '#'
            detail_list[bt4] = ''

          # 休憩時間内の工数データと作業詳細を消す
          for bt4 in range(0, int(break_end4)):
            kosu_def[bt4] = '#'
            detail_list[bt4] = ''

        # 休憩4が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消す
          for bt4 in range(int(break_start4), int(break_end4)):
            kosu_def[bt4] = '#'
            detail_list[bt4] = ''


      # 入力時間が日をまたいでいる場合の処理
      if check == 1:
        # リストの作業時間に合った場所に工数区分と作業詳細を入れる
        for kosu in range(int(start_time), 288):
          kosu_def[kosu] = def_work
          detail_list[kosu] = detail_work

        for kosu in range(0,int(end_time)):
          kosu_def[kosu] = def_work
          detail_list[kosu] = detail_work


        # 休憩1が日を超えている場合の処理
        if break_next_day1 == 1:

          # 休憩時間内の工数データと作業詳細を消す
          for bt1 in range(int(break_start1), 288):
            kosu_def[bt1] = '#'
            detail_list[bt1] = ''

          # 休憩時間内の工数データと作業詳細を消す
          for bt1 in range(0, int(break_end1)):
            kosu_def[bt1] = '#'
            detail_list[bt1] = ''

        # 休憩1が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消す
          for bt1 in range(int(break_start1), int(break_end1)):
            kosu_def[bt1] = '#'
            detail_list[bt1] = ''


        # 休憩2が日を超えている場合の処理
        if break_next_day2 == 1:

          # 休憩時間内の工数データと作業詳細を消す
          for bt2 in range(int(break_start2), 288):
            kosu_def[bt2] = '#'
            detail_list[bt2] = ''

          # 休憩時間内の工数データと作業詳細を消す
          for bt2 in range(0, int(break_end2)):
            kosu_def[bt2] = '#'
            detail_list[bt2] = ''

        # 休憩2が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消す
          for bt2 in range(int(break_start2), int(break_end2)):
            kosu_def[bt2] = '#'
            detail_list[bt2] = ''


        # 休憩3が日を超えている場合の処理
        if break_next_day3 == 1:

          # 休憩時間内の工数データと作業詳細を消す
          for bt3 in range(int(break_start3), 288):
            kosu_def[bt3] = '#'
            detail_list[bt3] = ''

          # 休憩時間内の工数データと作業詳細を消す
          for bt2 in range(0, int(break_end3)):
            kosu_def[bt3] = '#'
            detail_list[bt3] = ''

        # 休憩3が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消す
          for bt3 in range(int(break_start3), int(break_end3)):
            kosu_def[bt3] = '#'
            detail_list[bt3] = ''


        # 休憩4が日を超えている場合の処理
        if break_next_day4 == 1:

          # 休憩時間内の工数データと作業詳細を消す
          for bt4 in range(int(break_start4), 288):
            kosu_def[bt4] = '#'
            detail_list[bt4] = ''

          # 休憩時間内の工数データと作業詳細を消す
          for bt4 in range(0, int(break_end4)):
            kosu_def[bt4] = '#'
            detail_list[bt4] = ''

        # 休憩4が日を超えていない場合の処理
        else:

          # 休憩時間内の工数データと作業詳細を消す
          for bt4 in range(int(break_start4), int(break_end4)):
            kosu_def[bt4] = '#'
            detail_list[bt4] = ''


      # 作業詳細リストを文字列に変更
      detail_list_str = ''
      for i, e in enumerate(detail_list):
        if i == len(detail_list) - 1:
          detail_list_str = detail_list_str + detail_list[i]
        else:
          detail_list_str = detail_list_str + detail_list[i] + '$'


      # 変数リセット
      kosu_total = 0
      # 工数の合計を計算
      for k in kosu_def:

        # 作業内容が入っている場合の処理
        if k != '#':

          # 工数の合計に5分加算
          kosu_total += 5


      # 工数入力OK_NGリセット
      judgement = False
      # 出勤、休出時、工数合計と残業に整合性がある場合の処理
      if (work == '出勤' or work == 'シフト出') and \
        kosu_total - int(request.POST['over_work']) == 470:

        # 工数入力OK_NGをOKに切り替え
        judgement = True


      # 休出時、工数合計と残業に整合性がある場合の処理
      if work == '休出' and kosu_total == int(request.POST['over_work']):

        # 工数入力OK_NGをOKに切り替え
        judgement = True


      # 早退・遅刻時、工数合計と残業に整合性がある場合の処理
      if work == '早退・遅刻' and kosu_total != 0:

        # 工数入力OK_NGをOKに切り替え
        judgement = True


      # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Cで1直の場合の処理
      if (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
        member_obj.shop == 'A1' or member_obj.shop == 'A2') and \
          tyoku == '1':

        # 半前年休時、工数合計と残業に整合性がある場合の処理
        if work == '半前年休' and kosu_total - int(request.POST['over_work']) == 230:

          # 工数入力OK_NGをOKに切り替え
          judgement = True

        # 半後年休時、工数合計と残業に整合性がある場合の処理
        if work == '半後年休' and kosu_total - int(request.POST['over_work']) == 240:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


      # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Cで2直の場合の処理
      if (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
        member_obj.shop == 'A1' or member_obj.shop == 'A2') and \
          tyoku == '2':

        # 半前年休時、工数合計と残業に整合性がある場合の処理
        if work == '半前年休' and kosu_total - int(request.POST['over_work']) == 290:

          # 工数入力OK_NGをOKに切り替え
          judgement = True

        # 半後年休時、工数合計と残業に整合性がある場合の処理
        if work == '半後年休' and kosu_total - int(request.POST['over_work']) == 180:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


      # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Cで3直の場合の処理
      if (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
        member_obj.shop == 'A1' or member_obj.shop == 'A2') and \
          tyoku == '3':

        # 半前年休時、工数合計と残業に整合性がある場合の処理
        if work == '半前年休' and kosu_total - int(request.POST['over_work']) == 230:

          # 工数入力OK_NGをOKに切り替え
          judgement = True

        # 半後年休時、工数合計と残業に整合性がある場合の処理
        if work == '半後年休' and kosu_total - int(request.POST['over_work']) == 240:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


      # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Bで1直の場合の処理
      if (member_obj.shop == 'P' or member_obj.shop == 'R' or \
        member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
          member_obj.shop == 'その他' or member_obj.shop == '組長以上') and \
          tyoku == '1':

        # 半前年休時、工数合計と残業に整合性がある場合の処理
        if work == '半前年休' and kosu_total - int(request.POST['over_work']) == 220:

          # 工数入力OK_NGをOKに切り替え
          judgement = True

        # 半後年休時、工数合計と残業に整合性がある場合の処理
        if work == '半後年休' and kosu_total - int(request.POST['over_work']) == 250:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


      # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Bで2直の場合の処理
      if (member_obj.shop == 'P' or member_obj.shop == 'R' or \
        member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
          member_obj.shop == 'その他' or member_obj.shop == '組長以上') and \
          tyoku == '2':

        # 半前年休時、工数合計と残業に整合性がある場合の処理
        if work == '半前年休' and kosu_total - int(request.POST['over_work']) == 230:

          # 工数入力OK_NGをOKに切り替え
          judgement = True

        # 半後年休時、工数合計と残業に整合性がある場合の処理
        if work == '半後年休' and kosu_total - int(request.POST['over_work']) == 240:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


      # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Bで3直の場合の処理
      if (member_obj.shop == 'P' or member_obj.shop == 'R' or \
        member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
          member_obj.shop == 'その他' or member_obj.shop == '組長以上') and \
          tyoku == '3':

        # 半前年休時、工数合計と残業に整合性がある場合の処理
        if work == '半前年休' and kosu_total - int(request.POST['over_work']) == 275:

          # 工数入力OK_NGをOKに切り替え
          judgement = True

        # 半後年休時、工数合計と残業に整合性がある場合の処理
        if work == '半後年休' and kosu_total - int(request.POST['over_work']) == 195:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


      # 常昼の場合の処理
      if tyoku == '4':

        # 半前年休時、工数合計と残業に整合性がある場合の処理
        if work == '半前年休' and kosu_total - int(request.POST['over_work']) == 230:

          # 工数入力OK_NGをOKに切り替え
          judgement = True

        # 半後年休時、工数合計と残業に整合性がある場合の処理
        if work == '半後年休' and kosu_total - int(request.POST['over_work']) == 240:

          # 工数入力OK_NGをOKに切り替え
          judgement = True


      # 従業員番号に該当するmemberインスタンスを取得
      member_instance = member.objects.get(employee_no = request.session.get('login_No', None))

      # 指定のレコードにPOST送信された値を上書きする 
      new = Business_Time_graph(employee_no3 = request.session.get('login_No', None), \
                                name = member_instance, \
                                def_ver2 = request.session.get('input_def', None), \
                                work_day2 = work_day, \
                                work_time = work,\
                                tyoku2 = tyoku, \
                                time_work = ''.join(kosu_def), \
                                detail_work = detail_list_str, \
                                over_time = request.POST['over_work'], \
                                breaktime = breaktime, \
                                breaktime_over1 = breaktime_over1, \
                                breaktime_over2 = breaktime_over2, \
                                breaktime_over3 = breaktime_over3, \
                                judgement = judgement)

      # 工数内容リストをセーブする
      new.save()

    # 入力値をセッションに保存する
    request.session['day'] = work_day
    request.session['end_hour'] = end_hour
    request.session['end_min'] = end_min

    # このページをリダイレクトする
    return redirect(to = '/input')



  # 残業登録時の処理
  if "over_time_correction" in request.POST:

    # 未入力がないことを確認
    if request.POST['over_work'] == '':
      # エラーメッセージ出力
      messages.error(request, '残業が未入力です。工数登録できませんでした。ERROR017')
      # このページをリダイレクト
      return redirect(to = '/input')

    # 残業時間が15の倍数でない場合の処理
    if int(request.POST['over_work'])%15 != 0:
      # エラーメッセージ出力
      messages.error(request, '残業時間が15分の倍数になっていません。工数登録できませんでした。ERROR018')


    # 工数データがあるか確認
    obj_filter = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None), \
                                                    work_day2 = request.POST['work_day'])

    # 工数データがある場合の処理
    if obj_filter.count() != 0:

      # 残業を上書きして更新
      Business_Time_graph.objects.update_or_create(employee_no3 = request.session.get('login_No', None), \
                                                   work_day2 = request.POST['work_day'], \
                                                   defaults = {'over_time' : request.POST['over_work']})

    # 工数データがない場合の処理
    else:

      # 従業員番号に該当するmemberインスタンスを取得
      member_instance = member.objects.get(employee_no = request.session.get('login_No', None))

      # 工数データ作成し残業書き込み
      Business_Time_graph.objects.update_or_create(employee_no3 = request.session.get('login_No', ''), \
                                                   work_day2 = request.POST['work_day'], \
                                                   defaults = {'name' : member_instance, \
                                                               'time_work' : '#'*288, \
                                                               'detail_work' : '$'*288, \
                                                               'over_time' : request.POST['over_work']})


    # このページをリダイレクトする
    return redirect(to = '/input')



  # 現在時刻取得処理
  if "now_time" in request.POST:
    
    # 現在時刻取得
    now_time = datetime.datetime.now().time()
    # 現在時刻を5分単位で丸め
    about_time = now_time.replace(minute = now_time.minute - now_time.minute % 5, \
                                  second = 0, microsecond = 0)
    
    # 現在時刻を初期値に設定
    hour_default = str(about_time.hour).zfill(2)
    min_default = str(about_time.minute).zfill(2)

    # 更新された就業日を変数に入れる
    new_work_day = request.session.get('day', kosu_today)

    # 作業開始時間保持
    request.session['end_hour'] = request.POST['start_hour']
    request.session['end_min'] = request.POST['start_min']

    # 翌日チェックBOX、工数区分保持
    if request.POST['start_hour'] != '' and request.POST['start_min'] !='':
      start_index = (int(request.POST['start_hour'])*12) + (int(request.POST['start_min'])/5)
      end_index = (int(hour_default)*12) + (int(min_default)/5)
      if start_index > end_index :
        POST_check = True
      else:
        POST_check =False

    else:
      POST_check =False

    def_default = {'kosu_def_list' : request.POST['kosu_def_list'], \
                   'tomorrow_check' : POST_check}

    # グラフデータ確認用データ取得
    data_count = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None),\
                                                    work_day2 = new_work_day)

    # グラフラベルデータ
    graph_item = []
    for i in range(24):
        for n in range(0, 60, 5):
            t = n
            if n == 0:
              t = '00'
            if n == 5:
              t = '05'
            graph_item.append('{}:{}'.format(i, t))

    # 選択されている就業日のグラフデータがない場合の処理
    if data_count.count() == 0:
      # 0を288個入れたリスト作成
      graph_list = list(itertools.repeat(0, 288))

    # 選択されている就業日のグラフデータがある場合の処理
    else:
      # グラフデータを取得
      graph_obj = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', None),\
                                                  work_day2 = new_work_day)
      # 取得したグラフデータを文字型からリストに解凍
      graph_list = list(graph_obj.time_work)

      # グラフデータリスト内の各文字を数値に変更
      str_list = ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', \
                    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', \
                      'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                          'q', 'r', 's', 't', 'u', 'v', 'w', 'x',]
      
      for i in range(288):
        for n, m in enumerate(str_list):
          if graph_list[i]  == m:
            graph_list[i] = n
            break

      # 工数が入力されていない部分を切り捨てデータを見やすく
      if graph_obj.tyoku2 != '3':
        for i in range(288):
          if graph_list[i] != 0:
            if i == 0:
              graph_start_index = i
            else:
              graph_start_index = i - 1
              break
        
        for i in range(1, 289):
          if graph_list[-i] != 0:
            if i == 1:
              graph_end_index = 289 - i
            else:
              graph_end_index = 290 - i
              break

        if graph_obj.tyoku2 == '1':
          if graph_end_index <= 184:
            graph_end_index = 184

        if graph_obj.tyoku2 == '2' and (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
                                        member_obj.shop == 'A1' or member_obj.shop == 'A2'):
          if graph_end_index <= 240:
            graph_end_index = 240

        if graph_obj.tyoku2 == '2' and (member_obj.shop == 'P' or member_obj.shop == 'R' or \
                                        member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
                                         member_obj.shop == 'その他' or member_obj.shop == '組長以上'):
          if graph_end_index <= 270:
            graph_end_index = 270

        if graph_obj.tyoku2 == '4':
          if graph_end_index <= 204:
            graph_end_index = 204

        del graph_list[graph_end_index:]
        del graph_list[:graph_start_index]
        del graph_item[graph_end_index:]
        del graph_item[:graph_start_index]


      else:
        graph_list = graph_list*2
        graph_item = graph_item*2

        del graph_list[:204]
        del graph_list[288:]
        del graph_item[:204]
        del graph_item[288:]

        for i in range(288):
          if graph_list[i] != 0:
            if i == 0:
              graph_start_index = i
            else:
              graph_start_index = i - 1
              break

        for i in range(1, 289):
          if graph_list[-i] != 0:
            if i == 1:
              graph_end_index = 289 - i
            else:
              graph_end_index = 290 - i
              break

        if member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
          member_obj.shop == 'A1' or member_obj.shop == 'A2':

          if graph_end_index <= 140:
            graph_end_index = 140

        else:
          if graph_end_index <= 169:
            graph_end_index = 169

        del graph_list[graph_end_index:]
        del graph_list[:graph_start_index]
        del graph_item[graph_end_index:]
        del graph_item[:graph_start_index]



  # 休憩変更時の処理
  if "change_display" in request.POST:

    # 休憩変更したい日を記憶
    request.session['break_today'] = request.POST['work_day']

    # 休憩変更したい日に休憩データがあるか確認
    obj_filter = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None),\
                                                    work_day2 = request.session.get('day', kosu_today))

    # 工数データがない場合の処理
    if obj_filter.count() == 0:
      # エラーメッセージ出力
      messages.error(request, 'この日は、まだ工数データがありません。工数を1件以上入力してから休憩を変更して下さい。ERROR006')
      # このページをリダイレクト
      return redirect(to = '/input')
    
    #工数データがある場合の処理
    else:
      
      # 工数データ取得
      obj_get = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', None),\
                                                work_day2 = request.session.get('day', kosu_today))

      # 休憩データが空の場合の処理
      if obj_get.breaktime == None or obj_get.breaktime_over1 == None or \
        obj_get.breaktime_over2 == None or obj_get.breaktime_over3 == None:

        # エラーメッセージ出力
        messages.error(request, 'この日は、まだ休憩データがありません。工数を1件以上入力してから休憩を変更して下さい。ERROR016')
        # このページをリダイレクト
        return redirect(to = '/input')
      
      # 休憩データがある場合の処理 
      else:

        # 休憩変更画面へジャンプ
        return redirect(to = '/today_break_time')



  # 作業終了時の変数がある場合の処理
  if 'hour_default' in locals():

    # 処理なし
    hour_default = hour_default

  
  # 作業終了時の変数がない場合の処理
  else:

    # セッションに登録されている作業終了時を変数に入れる
    hour_default = request.session.get('end_hour', '')


  # 作業終了分の変数がある場合の処理
  if 'min_default' in locals():

    # 処理なし
    min_default = min_default


  # 作業終了分の変数がない場合の処理
  else:

    # セッションに登録されている作業終了分を変数に入れる
    min_default = request.session.get('end_min', '')
  

  # 残業データあるか確認
  over_work_filter = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None),\
                                                        work_day2 = request.session.get('day', kosu_today))


  # 残業データある場合の処理
  if over_work_filter.count() != 0:
    # 残業データ取得
    over_work_get = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', None),\
                                                    work_day2 = request.session.get('day', kosu_today))
    over_work_default = over_work_get.over_time

    # 直情報取得
    tyoku_default = over_work_get.tyoku2

    # 勤務情報取得
    work_default = over_work_get.work_time

    # 工数入力状況取得
    ok_ng = over_work_get.judgement


  # 残業データない場合の処理
  else:

    # 残業に0を入れる
    over_work_default = 0

    # 直表示に空を入れる
    tyoku_default = ''

    # 勤務表示に空を入れる
    work_default = ''

    # 工数入力状況に空を入れる
    ok_ng = False


  # 初期値を設定するリスト作成
  kosu_list = {'work' : work_default,
               'tyoku2' : tyoku_default, 
               'start_hour' : request.session.get('end_hour', ''), 
               'start_min' : request.session.get('end_min', ''), 
               'end_hour' : hour_default, 
               'end_min' : min_default,
               'over_work' : over_work_default,
               }


  # 翌日チェック、工数区分の初期値の定義
  if 'def_default' in locals():
    kosu_list.update(def_default)
  else:
    def_default = {'kosu_def_list' : '', \
                   'tomorrow_check' : ''}
    kosu_list.update(def_default)

  # 現在使用している工数区分のオブジェクトを取得
  kosu_obj = kosu_division.objects.get(kosu_name = request.session.get('input_def', None))

  # 工数区分登録カウンターリセット
  n = 0
  # 工数区分登録数カウント
  for kosu_num in range(1, 50):
    if eval('kosu_obj.kosu_title_{}'.format(kosu_num)) != None:
      n = kosu_num

  # 工数区分処理用記号リスト用意
  str_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', \
              'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', \
                'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                    'q', 'r', 's', 't', 'u', 'v', 'w', 'x',]
  # リストの長さを工数区分の登録数に応じて調整
  del str_list[n:]

  # 工数区分の選択リスト作成
  choices_list = [('','')]
  graph_kosu_list = []
  for i, m in enumerate(str_list):
    choices_list.append((m,eval('kosu_obj.kosu_title_{}'.format(i + 1))))
    graph_kosu_list.append(eval('kosu_obj.kosu_title_{}'.format(i + 1)))

  # ログイン者情報取得
  data = member.objects.get(employee_no = request.session.get('login_No', None))

  # フォームの初期状態定義
  form = input_kosuForm(kosu_list)
  
  # フォームの選択肢定義
  form.fields['kosu_def_list'].choices = choices_list



  # HTMLに渡す辞書
  library_m = {
    'title' : '工数登録',
    'form' : form,
    'new_day' : str(new_work_day),
    'graph_list' : graph_list,
    'graph_item' : graph_item,
    'graph_kosu_list' : graph_kosu_list,
    'n' : n,
    'OK_NG' : ok_ng,
    }



  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/input.html', library_m)





#--------------------------------------------------------------------------------------------------------





# 休憩時間定義画面定義
def break_time(request): 

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')


  # POST時の処理
  if (request.method == 'POST'):
    # POSTされた値を変数に入れる
    break_time1_start_hour = request.POST['break_time1_start_hour']
    break_time1_start_min = request.POST['break_time1_start_min']
    break_time1_end_hour = request.POST['break_time1_end_hour']
    break_time1_end_min = request.POST['break_time1_end_min']
    break_time1_over1_start_hour = request.POST['break_time1_over1_start_hour']
    break_time1_over1_start_min = request.POST['break_time1_over1_start_min']
    break_time1_over1_end_hour = request.POST['break_time1_over1_end_hour']
    break_time1_over1_end_min = request.POST['break_time1_over1_end_min']
    break_time1_over2_start_hour = request.POST['break_time1_over2_start_hour']
    break_time1_over2_start_min = request.POST['break_time1_over2_start_min']
    break_time1_over2_end_hour = request.POST['break_time1_over2_end_hour']
    break_time1_over2_end_min = request.POST['break_time1_over2_end_min']
    break_time1_over3_start_hour = request.POST['break_time1_over3_start_hour']
    break_time1_over3_start_min = request.POST['break_time1_over3_start_min']
    break_time1_over3_end_hour = request.POST['break_time1_over3_end_hour']
    break_time1_over3_end_min = request.POST['break_time1_over3_end_min']
    break_time2_start_hour = request.POST['break_time2_start_hour']
    break_time2_start_min = request.POST['break_time2_start_min']
    break_time2_end_hour = request.POST['break_time2_end_hour']
    break_time2_end_min = request.POST['break_time2_end_min']
    break_time2_over1_start_hour = request.POST['break_time2_over1_start_hour']
    break_time2_over1_start_min = request.POST['break_time2_over1_start_min']
    break_time2_over1_end_hour = request.POST['break_time2_over1_end_hour']
    break_time2_over1_end_min = request.POST['break_time2_over1_end_min']
    break_time2_over2_start_hour = request.POST['break_time2_over2_start_hour']
    break_time2_over2_start_min = request.POST['break_time2_over2_start_min']
    break_time2_over2_end_hour = request.POST['break_time2_over2_end_hour']
    break_time2_over2_end_min = request.POST['break_time2_over2_end_min']
    break_time2_over3_start_hour = request.POST['break_time2_over3_start_hour']
    break_time2_over3_start_min = request.POST['break_time2_over3_start_min']
    break_time2_over3_end_hour = request.POST['break_time2_over3_end_hour']
    break_time2_over3_end_min = request.POST['break_time2_over3_end_min']
    break_time3_start_hour = request.POST['break_time3_start_hour']
    break_time3_start_min = request.POST['break_time3_start_min']
    break_time3_end_hour = request.POST['break_time3_end_hour']
    break_time3_end_min = request.POST['break_time3_end_min']
    break_time3_over1_start_hour = request.POST['break_time3_over1_start_hour']
    break_time3_over1_start_min = request.POST['break_time3_over1_start_min']
    break_time3_over1_end_hour = request.POST['break_time3_over1_end_hour']
    break_time3_over1_end_min = request.POST['break_time3_over1_end_min']
    break_time3_over2_start_hour = request.POST['break_time3_over2_start_hour']
    break_time3_over2_start_min = request.POST['break_time3_over2_start_min']
    break_time3_over2_end_hour = request.POST['break_time3_over2_end_hour']
    break_time3_over2_end_min = request.POST['break_time3_over2_end_min']
    break_time3_over3_start_hour = request.POST['break_time3_over3_start_hour']
    break_time3_over3_start_min = request.POST['break_time3_over3_start_min']
    break_time3_over3_end_hour = request.POST['break_time3_over3_end_hour']
    break_time3_over3_end_min = request.POST['break_time3_over3_end_min']
    break_time4_start_hour = request.POST['break_time4_start_hour']
    break_time4_start_min = request.POST['break_time4_start_min']
    break_time4_end_hour = request.POST['break_time4_end_hour']
    break_time4_end_min = request.POST['break_time4_end_min']
    break_time4_over1_start_hour = request.POST['break_time4_over1_start_hour']
    break_time4_over1_start_min = request.POST['break_time4_over1_start_min']
    break_time4_over1_end_hour = request.POST['break_time4_over1_end_hour']
    break_time4_over1_end_min = request.POST['break_time4_over1_end_min']
    break_time4_over2_start_hour = request.POST['break_time4_over2_start_hour']
    break_time4_over2_start_min = request.POST['break_time4_over2_start_min']
    break_time4_over2_end_hour = request.POST['break_time4_over2_end_hour']
    break_time4_over2_end_min = request.POST['break_time4_over2_end_min']
    break_time4_over3_start_hour = request.POST['break_time4_over3_start_hour']
    break_time4_over3_start_min = request.POST['break_time4_over3_start_min']
    break_time4_over3_end_hour = request.POST['break_time4_over3_end_hour']
    break_time4_over3_end_min = request.POST['break_time4_over3_end_min']

    # POSTされた値をまとめる
    break_time1 = break_time1_start_hour + break_time1_start_min + \
                  break_time1_end_hour + break_time1_end_min
    break_time1_over1 = break_time1_over1_start_hour + break_time1_over1_start_min + \
                        break_time1_over1_end_hour + break_time1_over1_end_min
    break_time1_over2 = break_time1_over2_start_hour + break_time1_over2_start_min + \
                        break_time1_over2_end_hour + break_time1_over2_end_min
    break_time1_over3 = break_time1_over3_start_hour + break_time1_over3_start_min + \
                        break_time1_over3_end_hour + break_time1_over3_end_min
    break_time2 = break_time2_start_hour + break_time2_start_min + \
                  break_time2_end_hour + break_time2_end_min
    break_time2_over1 = break_time2_over1_start_hour + break_time2_over1_start_min + \
                        break_time2_over1_end_hour + break_time2_over1_end_min
    break_time2_over2 = break_time2_over2_start_hour + break_time2_over2_start_min + \
                        break_time2_over2_end_hour + break_time2_over2_end_min
    break_time2_over3 = break_time2_over3_start_hour + break_time2_over3_start_min + \
                        break_time2_over3_end_hour + break_time2_over3_end_min
    break_time3 = break_time3_start_hour + break_time3_start_min + \
                  break_time3_end_hour + break_time3_end_min
    break_time3_over1 = break_time3_over1_start_hour + break_time3_over1_start_min + \
                        break_time3_over1_end_hour + break_time3_over1_end_min
    break_time3_over2 = break_time3_over2_start_hour + break_time3_over2_start_min + \
                        break_time3_over2_end_hour + break_time3_over2_end_min
    break_time3_over3 = break_time3_over3_start_hour + break_time3_over3_start_min + \
                        break_time3_over3_end_hour + break_time3_over3_end_min
    break_time4 = break_time4_start_hour + break_time4_start_min + \
                  break_time4_end_hour + break_time4_end_min
    break_time4_over1 = break_time4_over1_start_hour + break_time4_over1_start_min + \
                        break_time4_over1_end_hour + break_time4_over1_end_min
    break_time4_over2 = break_time4_over2_start_hour + break_time4_over2_start_min + \
                        break_time4_over2_end_hour + break_time4_over2_end_min
    break_time4_over3 = break_time4_over3_start_hour + break_time4_over3_start_min + \
                        break_time4_over3_end_hour + break_time4_over3_end_min


    # 1直昼休憩時間に長すぎる時間を登録しようとした時の処理
    if (int(break_time1_end_hour)*60 + int(break_time1_end_min)) - \
      (int(break_time1_start_hour)*60 + int(break_time1_start_min)) > 60 or \
      (((int(break_time1_end_hour)*60 + int(break_time1_end_min)) < \
      (int(break_time1_start_hour)*60 + int(break_time1_start_min))) and \
      (int(break_time1_end_hour)*60 + int(break_time1_end_min) + 1440) - \
      (int(break_time1_start_hour)*60 + int(break_time1_start_min)) > 60):

      # エラーメッセージ出力
      messages.error(request, '1直の昼休憩時間が60分を超えています。正しい休憩時間を登録して下さい。ERROR061')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 2直昼休憩時間に長すぎる時間を登録しようとした時の処理
    if (int(break_time2_end_hour)*60 + int(break_time2_end_min)) - \
      (int(break_time2_start_hour)*60 + int(break_time2_start_min)) > 60 or \
      (((int(break_time2_end_hour)*60 + int(break_time2_end_min)) < \
      (int(break_time2_start_hour)*60 + int(break_time2_start_min))) and \
      (int(break_time2_end_hour)*60 + int(break_time2_end_min) + 1440) - \
      (int(break_time2_start_hour)*60 + int(break_time2_start_min)) > 60):

      # エラーメッセージ出力
      messages.error(request, '2直の昼休憩時間が60分を超えています。正しい休憩時間を登録して下さい。ERROR062')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 3直昼休憩時間に長すぎる時間を登録しようとした時の処理
    if (int(break_time3_end_hour)*60 + int(break_time3_end_min)) - \
      (int(break_time3_start_hour)*60 + int(break_time3_start_min)) > 60 or \
      (((int(break_time3_end_hour)*60 + int(break_time3_end_min)) < \
      (int(break_time3_start_hour)*60 + int(break_time3_start_min))) and \
      (int(break_time3_end_hour)*60 + int(break_time3_end_min) + 1440) - \
      (int(break_time3_start_hour)*60 + int(break_time3_start_min)) > 60):

      # エラーメッセージ出力
      messages.error(request, '3直の昼休憩時間が60分を超えています。正しい休憩時間を登録して下さい。ERROR063')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 常昼昼休憩時間に長すぎる時間を登録しようとした時の処理
    if (int(break_time4_end_hour)*60 + int(break_time4_end_min)) - \
      (int(break_time4_start_hour)*60 + int(break_time4_start_min)) > 60 or \
      (((int(break_time4_end_hour)*60 + int(break_time4_end_min)) < \
      (int(break_time4_start_hour)*60 + int(break_time4_start_min))) and \
      (int(break_time4_end_hour)*60 + int(break_time4_end_min) + 1440) - \
      (int(break_time4_start_hour)*60 + int(break_time4_start_min)) > 60):

      # エラーメッセージ出力
      messages.error(request, '常昼の昼休憩時間が60分を超えています。正しい休憩時間を登録して下さい。ERROR064')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 1直残業休憩時間1に長すぎる時間を登録しようとした時の処理
    if (int(break_time1_over1_end_hour)*60 + int(break_time1_over1_end_min)) - \
      (int(break_time1_over1_start_hour)*60 + int(break_time1_over1_start_min)) > 15 or \
      (((int(break_time1_over1_end_hour)*60 + int(break_time1_over1_end_min)) < \
      (int(break_time1_over1_start_hour)*60 + int(break_time1_over1_start_min))) and \
      (int(break_time1_over1_end_hour)*60 + int(break_time1_over1_end_min) + 1440) - \
      (int(break_time1_over1_start_hour)*60 + int(break_time1_over1_start_min)) > 15):

      # エラーメッセージ出力
      messages.error(request, '1直残業時間中の休憩時間1が15分を超えています。正しい休憩時間を登録して下さい。ERROR065')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 1直残業休憩時間2に長すぎる時間を登録しようとした時の処理
    if (int(break_time1_over2_end_hour)*60 + int(break_time1_over2_end_min)) - \
      (int(break_time1_over2_start_hour)*60 + int(break_time1_over2_start_min)) > 60 or \
      (((int(break_time1_over2_end_hour)*60 + int(break_time1_over2_end_min)) < \
      (int(break_time1_over2_start_hour)*60 + int(break_time1_over2_start_min))) and \
      (int(break_time1_over2_end_hour)*60 + int(break_time1_over2_end_min) + 1440) - \
      (int(break_time1_over2_start_hour)*60 + int(break_time1_over2_start_min)) > 60):

      # エラーメッセージ出力
      messages.error(request, '1直残業時間中の休憩時間2が60分を超えています。正しい休憩時間を登録して下さい。ERROR066')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 1直残業休憩時間3に長すぎる時間を登録しようとした時の処理
    if (int(break_time1_over3_end_hour)*60 + int(break_time1_over3_end_min)) - \
      (int(break_time1_over3_start_hour)*60 + int(break_time1_over3_start_min)) > 15 or \
      (((int(break_time1_over3_end_hour)*60 + int(break_time1_over3_end_min)) < \
      (int(break_time1_over3_start_hour)*60 + int(break_time1_over3_start_min))) and \
      (int(break_time1_over3_end_hour)*60 + int(break_time1_over3_end_min) + 1440) - \
      (int(break_time1_over3_start_hour)*60 + int(break_time1_over3_start_min)) > 15):

      # エラーメッセージ出力
      messages.error(request, '1直残業時間中の休憩時間3が15分を超えています。正しい休憩時間を登録して下さい。ERROR067')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 2直残業休憩時間1に長すぎる時間を登録しようとした時の処理
    if (int(break_time2_over1_end_hour)*60 + int(break_time2_over1_end_min)) - \
      (int(break_time2_over1_start_hour)*60 + int(break_time2_over1_start_min)) > 15 or \
      (((int(break_time2_over1_end_hour)*60 + int(break_time2_over1_end_min)) < \
      (int(break_time2_over1_start_hour)*60 + int(break_time2_over1_start_min))) and \
      (int(break_time2_over1_end_hour)*60 + int(break_time2_over1_end_min) + 1440) - \
      (int(break_time2_over1_start_hour)*60 + int(break_time2_over1_start_min)) > 15):

      # エラーメッセージ出力
      messages.error(request, '2直残業時間中の休憩時間1が15分を超えています。正しい休憩時間を登録して下さい。ERROR068')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 2直残業休憩時間2に長すぎる時間を登録しようとした時の処理
    if (int(break_time2_over2_end_hour)*60 + int(break_time2_over2_end_min)) - \
      (int(break_time2_over2_start_hour)*60 + int(break_time2_over2_start_min)) > 60 or \
      (((int(break_time2_over2_end_hour)*60 + int(break_time2_over2_end_min)) < \
      (int(break_time2_over2_start_hour)*60 + int(break_time2_over2_start_min))) and \
      (int(break_time2_over2_end_hour)*60 + int(break_time2_over2_end_min) + 1440) - \
      (int(break_time2_over2_start_hour)*60 + int(break_time2_over2_start_min)) > 60):

      # エラーメッセージ出力
      messages.error(request, '2直残業時間中の休憩時間2が60分を超えています。正しい休憩時間を登録して下さい。ERROR069')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 2直残業休憩時間3に長すぎる時間を登録しようとした時の処理
    if (int(break_time2_over3_end_hour)*60 + int(break_time2_over3_end_min)) - \
      (int(break_time2_over3_start_hour)*60 + int(break_time2_over3_start_min)) > 15 or \
      (((int(break_time2_over3_end_hour)*60 + int(break_time2_over3_end_min)) < \
      (int(break_time2_over3_start_hour)*60 + int(break_time2_over3_start_min))) and \
      (int(break_time2_over3_end_hour)*60 + int(break_time2_over3_end_min) + 1440) - \
      (int(break_time2_over3_start_hour)*60 + int(break_time2_over3_start_min)) > 15):

      # エラーメッセージ出力
      messages.error(request, '2直残業時間中の休憩時間3が15分を超えています。正しい休憩時間を登録して下さい。ERROR070')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 3直残業休憩時間1に長すぎる時間を登録しようとした時の処理
    if (int(break_time3_over1_end_hour)*60 + int(break_time3_over1_end_min)) - \
      (int(break_time3_over1_start_hour)*60 + int(break_time3_over1_start_min)) > 15 or \
      (((int(break_time3_over1_end_hour)*60 + int(break_time3_over1_end_min)) < \
      (int(break_time3_over1_start_hour)*60 + int(break_time3_over1_start_min))) and \
      (int(break_time3_over1_end_hour)*60 + int(break_time3_over1_end_min) + 1440) - \
      (int(break_time3_over1_start_hour)*60 + int(break_time3_over1_start_min)) > 15):

      # エラーメッセージ出力
      messages.error(request, '3直残業時間中の休憩時間1が15分を超えています。正しい休憩時間を登録して下さい。ERROR071')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 3直残業休憩時間2に長すぎる時間を登録しようとした時の処理
    if (int(break_time3_over2_end_hour)*60 + int(break_time3_over2_end_min)) - \
      (int(break_time3_over2_start_hour)*60 + int(break_time3_over2_start_min)) > 60 or \
      (((int(break_time3_over2_end_hour)*60 + int(break_time3_over2_end_min)) < \
      (int(break_time3_over2_start_hour)*60 + int(break_time3_over2_start_min))) and \
      (int(break_time3_over2_end_hour)*60 + int(break_time3_over2_end_min) + 1440) - \
      (int(break_time3_over2_start_hour)*60 + int(break_time3_over2_start_min)) > 60):

      # エラーメッセージ出力
      messages.error(request, '3直残業時間中の休憩時間2が60分を超えています。正しい休憩時間を登録して下さい。ERROR072')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 3直残業休憩時間3に長すぎる時間を登録しようとした時の処理
    if (int(break_time3_over3_end_hour)*60 + int(break_time3_over3_end_min)) - \
      (int(break_time3_over3_start_hour)*60 + int(break_time3_over3_start_min)) > 15 or \
      (((int(break_time3_over3_end_hour)*60 + int(break_time3_over3_end_min)) < \
      (int(break_time3_over3_start_hour)*60 + int(break_time3_over3_start_min))) and \
      (int(break_time3_over3_end_hour)*60 + int(break_time3_over3_end_min) + 1440) - \
      (int(break_time3_over3_start_hour)*60 + int(break_time3_over3_start_min)) > 15):

      # エラーメッセージ出力
      messages.error(request, '3直残業時間中の休憩時間3が15分を超えています。正しい休憩時間を登録して下さい。ERROR073')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 常昼残業休憩時間1に長すぎる時間を登録しようとした時の処理
    if (int(break_time4_over1_end_hour)*60 + int(break_time4_over1_end_min)) - \
      (int(break_time4_over1_start_hour)*60 + int(break_time4_over1_start_min)) > 15 or \
      (((int(break_time4_over1_end_hour)*60 + int(break_time4_over1_end_min)) < \
      (int(break_time4_over1_start_hour)*60 + int(break_time4_over1_start_min))) and \
      (int(break_time4_over1_end_hour)*60 + int(break_time4_over1_end_min) + 1440) - \
      (int(break_time4_over1_start_hour)*60 + int(break_time4_over1_start_min)) > 15):

      # エラーメッセージ出力
      messages.error(request, '常昼残業時間中の休憩時間1が15分を超えています。正しい休憩時間を登録して下さい。ERROR074')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 常昼残業休憩時間2に長すぎる時間を登録しようとした時の処理
    if (int(break_time4_over2_end_hour)*60 + int(break_time4_over2_end_min)) - \
      (int(break_time4_over2_start_hour)*60 + int(break_time4_over2_start_min)) > 60 or \
      (((int(break_time4_over2_end_hour)*60 + int(break_time4_over2_end_min)) < \
      (int(break_time4_over2_start_hour)*60 + int(break_time4_over2_start_min))) and \
      (int(break_time4_over2_end_hour)*60 + int(break_time4_over2_end_min) + 1440) - \
      (int(break_time4_over2_start_hour)*60 + int(break_time4_over2_start_min)) > 60):

      # エラーメッセージ出力
      messages.error(request, '常昼残業時間中の休憩時間2が60分を超えています。正しい休憩時間を登録して下さい。ERROR075')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 常昼残業休憩時間3に長すぎる時間を登録しようとした時の処理
    if (int(break_time4_over3_end_hour)*60 + int(break_time4_over3_end_min)) - \
      (int(break_time4_over3_start_hour)*60 + int(break_time4_over3_start_min)) > 15 or \
      (((int(break_time4_over3_end_hour)*60 + int(break_time4_over3_end_min)) < \
      (int(break_time4_over3_start_hour)*60 + int(break_time4_over3_start_min))) and \
      (int(break_time4_over3_end_hour)*60 + int(break_time4_over3_end_min) + 1440) - \
      (int(break_time4_over3_start_hour)*60 + int(break_time4_over3_start_min)) > 15):

      # エラーメッセージ出力
      messages.error(request, '常昼残業時間中の休憩時間3が15分を超えています。正しい休憩時間を登録して下さい。ERROR076')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # POST送信された休憩時間を上書きする 
    member.objects.update_or_create(employee_no = request.session.get('login_No', None), \
                                    defaults = {'break_time1' : break_time1, \
                                    'break_time1_over1' : break_time1_over1, \
                                    'break_time1_over2' : break_time1_over2, \
                                    'break_time1_over3' : break_time1_over3, \
                                    'break_time2' : break_time2, \
                                    'break_time2_over1' : break_time2_over1, \
                                    'break_time2_over2' : break_time2_over2, \
                                    'break_time2_over3' : break_time2_over3, \
                                    'break_time3' : break_time3, \
                                    'break_time3_over1' : break_time3_over1, \
                                    'break_time3_over2' : break_time3_over2, \
                                    'break_time3_over3' : break_time3_over3, \
                                    'break_time4' : break_time4, \
                                    'break_time4_over1' : break_time4_over1, \
                                    'break_time4_over2' : break_time4_over2, \
                                    'break_time4_over3' : break_time4_over3})


  # 休憩データ取得
  break_data = member.objects.get(employee_no = request.session.get('login_No', None))
  break1 = break_data.break_time1
  break1_1 = break_data.break_time1_over1
  break1_2 = break_data.break_time1_over2
  break1_3 = break_data.break_time1_over3
  break2 = break_data.break_time2
  break2_1 = break_data.break_time2_over1
  break2_2 = break_data.break_time2_over2
  break2_3 = break_data.break_time2_over3
  break3 = break_data.break_time3
  break3_1 = break_data.break_time3_over1
  break3_2 = break_data.break_time3_over2
  break3_3 = break_data.break_time3_over3
  break4 = break_data.break_time4
  break4_1 = break_data.break_time4_over1
  break4_2 = break_data.break_time4_over2
  break4_3 = break_data.break_time4_over3

  # フォーム初期値定義
  default_list = {
    'break_time1_start_hour' :  break1[0 : 2],
    'break_time1_start_min' :  break1[2 : 4],
    'break_time1_end_hour' :  break1[4 : 6],
    'break_time1_end_min' :  break1[6 :],
    'break_time1_over1_start_hour' : break1_1[0 : 2],
    'break_time1_over1_start_min' : break1_1[2 : 4],
    'break_time1_over1_end_hour' : break1_1[4 : 6],
    'break_time1_over1_end_min' : break1_1[6 :],
    'break_time1_over2_start_hour' : break1_2[0 : 2],
    'break_time1_over2_start_min' : break1_2[2 : 4],
    'break_time1_over2_end_hour' : break1_2[4 : 6],
    'break_time1_over2_end_min' : break1_2[6 :],
    'break_time1_over3_start_hour' : break1_3[0 : 2],
    'break_time1_over3_start_min' : break1_3[2 : 4],
    'break_time1_over3_end_hour' : break1_3[4 : 6],
    'break_time1_over3_end_min' : break1_3[6 :],
    'break_time2_start_hour' :  break2[0 : 2],
    'break_time2_start_min' :  break2[2 : 4],
    'break_time2_end_hour' :  break2[4 : 6],
    'break_time2_end_min' :  break2[6 :],
    'break_time2_over1_start_hour' : break2_1[0 : 2],
    'break_time2_over1_start_min' : break2_1[2 : 4],
    'break_time2_over1_end_hour' : break2_1[4 : 6],
    'break_time2_over1_end_min' : break2_1[6 :],
    'break_time2_over2_start_hour' : break2_2[0 : 2],
    'break_time2_over2_start_min' : break2_2[2 : 4],
    'break_time2_over2_end_hour' : break2_2[4 : 6],
    'break_time2_over2_end_min' : break2_2[6 :],
    'break_time2_over3_start_hour' : break2_3[0 : 2],
    'break_time2_over3_start_min' : break2_3[2 : 4],
    'break_time2_over3_end_hour' : break2_3[4 : 6],
    'break_time2_over3_end_min' : break2_3[6 :],
    'break_time3_start_hour' :  break3[0 : 2],
    'break_time3_start_min' :  break3[2 : 4],
    'break_time3_end_hour' :  break3[4 : 6],
    'break_time3_end_min' :  break3[6 :],
    'break_time3_over1_start_hour' : break3_1[0 : 2],
    'break_time3_over1_start_min' : break3_1[2 : 4],
    'break_time3_over1_end_hour' : break3_1[4 : 6],
    'break_time3_over1_end_min' : break3_1[6 :],
    'break_time3_over2_start_hour' : break3_2[0 : 2],
    'break_time3_over2_start_min' : break3_2[2 : 4],
    'break_time3_over2_end_hour' : break3_2[4 : 6],
    'break_time3_over2_end_min' : break3_2[6 :],
    'break_time3_over3_start_hour' : break3_3[0 : 2],
    'break_time3_over3_start_min' : break3_3[2 : 4],
    'break_time3_over3_end_hour' : break3_3[4 : 6],
    'break_time3_over3_end_min' : break3_3[6 :],
    'break_time4_start_hour' :  break4[0 : 2],
    'break_time4_start_min' :  break4[2 : 4],
    'break_time4_end_hour' :  break4[4 : 6],
    'break_time4_end_min' :  break4[6 :],
    'break_time4_over1_start_hour' : break4_1[0 : 2],
    'break_time4_over1_start_min' : break4_1[2 : 4],
    'break_time4_over1_end_hour' : break4_1[4 : 6],
    'break_time4_over1_end_min' : break4_1[6 :],
    'break_time4_over2_start_hour' : break4_2[0 : 2],
    'break_time4_over2_start_min' : break4_2[2 : 4],
    'break_time4_over2_end_hour' : break4_2[4 : 6],
    'break_time4_over2_end_min' : break4_2[6 :],
    'break_time4_over3_start_hour' : break4_3[0 : 2],
    'break_time4_over3_start_min' : break4_3[2 : 4],
    'break_time4_over3_end_hour' : break4_3[4 : 6],
    'break_time4_over3_end_min' : break4_3[6 :],
  }

  # フォーム定義
  form = timeForm(default_list)


  # HTMLに渡す辞書
  library_m = {
    'title' : '休憩時間定義',
    'form' : form,
    }

  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/break_time.html', library_m)





#--------------------------------------------------------------------------------------------------------





# 休憩変更定義画面定義
def today_break_time(request): 

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')


  # POST時の処理
  if (request.method == 'POST'):

    # POSTされた値を変数に入れる
    break_time1_start_hour = request.POST['break_time1_start_hour']
    break_time1_start_min = request.POST['break_time1_start_min']
    break_time1_end_hour = request.POST['break_time1_end_hour']
    break_time1_end_min = request.POST['break_time1_end_min']
    break_time1_over1_start_hour = request.POST['break_time1_over1_start_hour']
    break_time1_over1_start_min = request.POST['break_time1_over1_start_min']
    break_time1_over1_end_hour = request.POST['break_time1_over1_end_hour']
    break_time1_over1_end_min = request.POST['break_time1_over1_end_min']
    break_time1_over2_start_hour = request.POST['break_time1_over2_start_hour']
    break_time1_over2_start_min = request.POST['break_time1_over2_start_min']
    break_time1_over2_end_hour = request.POST['break_time1_over2_end_hour']
    break_time1_over2_end_min = request.POST['break_time1_over2_end_min']
    break_time1_over3_start_hour = request.POST['break_time1_over3_start_hour']
    break_time1_over3_start_min = request.POST['break_time1_over3_start_min']
    break_time1_over3_end_hour = request.POST['break_time1_over3_end_hour']
    break_time1_over3_end_min = request.POST['break_time1_over3_end_min']


    # POSTされた値をまとめる
    break_time1 = break_time1_start_hour + break_time1_start_min + \
                  break_time1_end_hour + break_time1_end_min
    break_time1_over1 = break_time1_over1_start_hour + break_time1_over1_start_min + \
                        break_time1_over1_end_hour + break_time1_over1_end_min
    break_time1_over2 = break_time1_over2_start_hour + break_time1_over2_start_min + \
                        break_time1_over2_end_hour + break_time1_over2_end_min
    break_time1_over3 = break_time1_over3_start_hour + break_time1_over3_start_min + \
                        break_time1_over3_end_hour + break_time1_over3_end_min


    # 1直昼休憩時間に長すぎる時間を登録しようとした時の処理
    if (int(break_time1_end_hour)*60 + int(break_time1_end_min)) - \
      (int(break_time1_start_hour)*60 + int(break_time1_start_min)) > 60 or \
      (((int(break_time1_end_hour)*60 + int(break_time1_end_min)) < \
      (int(break_time1_start_hour)*60 + int(break_time1_start_min))) and \
      (int(break_time1_end_hour)*60 + int(break_time1_end_min) + 1440) - \
      (int(break_time1_start_hour)*60 + int(break_time1_start_min)) > 60):

      # エラーメッセージ出力
      messages.error(request, '昼休憩時間が60分を超えています。正しい休憩時間を登録して下さい。ERROR012')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 1直残業休憩時間1に長すぎる時間を登録しようとした時の処理
    if (int(break_time1_over1_end_hour)*60 + int(break_time1_over1_end_min)) - \
      (int(break_time1_over1_start_hour)*60 + int(break_time1_over1_start_min)) > 15 or \
      (((int(break_time1_over1_end_hour)*60 + int(break_time1_over1_end_min)) < \
      (int(break_time1_over1_start_hour)*60 + int(break_time1_over1_start_min))) and \
      (int(break_time1_over1_end_hour)*60 + int(break_time1_over1_end_min) + 1440) - \
      (int(break_time1_over1_start_hour)*60 + int(break_time1_over1_start_min)) > 15):

      # エラーメッセージ出力
      messages.error(request, '残業時間中の休憩時間1が15分を超えています。正しい休憩時間を登録して下さい。ERROR013')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 1直残業休憩時間2に長すぎる時間を登録しようとした時の処理
    if (int(break_time1_over2_end_hour)*60 + int(break_time1_over2_end_min)) - \
      (int(break_time1_over2_start_hour)*60 + int(break_time1_over2_start_min)) > 60 or \
      (((int(break_time1_over2_end_hour)*60 + int(break_time1_over2_end_min)) < \
      (int(break_time1_over2_start_hour)*60 + int(break_time1_over2_start_min))) and \
      (int(break_time1_over2_end_hour)*60 + int(break_time1_over2_end_min) + 1440) - \
      (int(break_time1_over2_start_hour)*60 + int(break_time1_over2_start_min)) > 60):

      # エラーメッセージ出力
      messages.error(request, '残業時間中の休憩時間2が60分を超えています。正しい休憩時間を登録して下さい。ERROR014')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 1直残業休憩時間3に長すぎる時間を登録しようとした時の処理
    if (int(break_time1_over3_end_hour)*60 + int(break_time1_over3_end_min)) - \
      (int(break_time1_over3_start_hour)*60 + int(break_time1_over3_start_min)) > 15 or \
      (((int(break_time1_over3_end_hour)*60 + int(break_time1_over3_end_min)) < \
      (int(break_time1_over3_start_hour)*60 + int(break_time1_over3_start_min))) and \
      (int(break_time1_over3_end_hour)*60 + int(break_time1_over3_end_min) + 1440) - \
      (int(break_time1_over3_start_hour)*60 + int(break_time1_over3_start_min)) > 15):

      # エラーメッセージ出力
      messages.error(request, '残業時間中の休憩時間3が15分を超えています。正しい休憩時間を登録して下さい。ERROR015')
      # このページをリダイレクト
      return redirect(to = '/break_time')


    # 工数データあるか確認
    kosu_data_filter = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None), \
                                                    work_day2 = request.session.get('break_today', None))

    # 工数データある場合の処理
    if kosu_data_filter.count() != 0:

      # 作業内容データの内容を上書きして更新
      Business_Time_graph.objects.update_or_create(employee_no3 = request.session.get('login_No', None), \
                                                  work_day2 = request.session.get('break_today', None), \
                                                  defaults = {'breaktime' : break_time1, \
                                                              'breaktime_over1' : break_time1_over1, \
                                                              'breaktime_over2' : break_time1_over2, \
                                                              'breaktime_over3' : break_time1_over3})

    # 工数データない場合の処理
    else:

      # 従業員番号に該当するmemberインスタンスを取得
      member_instance = member.objects.get(employee_no = request.session.get('login_No', None))

      # 作業内容データの内容を上書きして更新
      Business_Time_graph.objects.update_or_create(employee_no3 = request.session.get('login_No', None), \
                                                  work_day2 = request.session.get('break_today', None), \
                                                  defaults = {'name' : member_instance, \
                                                              'time_work' : '#'*288, \
                                                              'detail_work' : '$'*288, \
                                                              'breaktime' : break_time1, \
                                                              'breaktime_over1' : break_time1_over1, \
                                                              'breaktime_over2' : break_time1_over2, \
                                                              'breaktime_over3' : break_time1_over3})


  # 工数データあるか確認
  break_data_filter = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None), \
                                                  work_day2 = request.session.get('break_today', None))

  # 工数データがある場合の処理
  if break_data_filter.count() != 0:

    # 工数データ取得
    break_data_get = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', None), \
                                                     work_day2 = request.session.get('break_today', None))
    # 休憩データある取得
    break1 = break_data_get.breaktime
    break1_1 = break_data_get.breaktime_over1
    break1_2 = break_data_get.breaktime_over2
    break1_3 = break_data_get.breaktime_over3

    # フォーム初期値定義
    default_list = {
      'break_time1_start_hour' :  break1[0 : 2],
      'break_time1_start_min' :  break1[2 : 4],
      'break_time1_end_hour' :  break1[4 : 6],
      'break_time1_end_min' :  break1[6 :],
      'break_time1_over1_start_hour' : break1_1[0 : 2],
      'break_time1_over1_start_min' : break1_1[2 : 4],
      'break_time1_over1_end_hour' : break1_1[4 : 6],
      'break_time1_over1_end_min' : break1_1[6 :],
      'break_time1_over2_start_hour' : break1_2[0 : 2],
      'break_time1_over2_start_min' : break1_2[2 : 4],
      'break_time1_over2_end_hour' : break1_2[4 : 6],
      'break_time1_over2_end_min' : break1_2[6 :],
      'break_time1_over3_start_hour' : break1_3[0 : 2],
      'break_time1_over3_start_min' : break1_3[2 : 4],
      'break_time1_over3_end_hour' : break1_3[4 : 6],
      'break_time1_over3_end_min' : break1_3[6 :],
      }

  # 工数データがない場合の処理
  else:

    # 空のフォーム初期値定義
    default_list = {}

  # フォーム定義
  form = timeForm(default_list)


  # HTMLに渡す辞書
  library_m = {
    'title' : '休憩変更',
    'form' : form,
    }

  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/today_break_time.html', library_m)





#--------------------------------------------------------------------------------------------------------





# 工数詳細確認画面定義
def detail(request, num):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')
  
  # 指定IDの工数履歴のレコードのオブジェクトを変数に入れる
  obj_get = Business_Time_graph.objects.get(id = num)

  # 作業内容と作業詳細を取得しリストに解凍
  work_list = list(obj_get.time_work)
  detail_list = obj_get.detail_work.split('$')


  # 作業時間リストリセット
  kosu_list = []
  time_list_start = []
  time_list_end = []
  def_list = []
  def_time = []
  detail_time = []

  # 作業内容と作業詳細毎の開始時間と終了時間インデックス取得
  for i in range(288):

    # 最初の要素に作業が入っている場合の処理
    if i == 0 and work_list[i] != '#':

      # 作業時間インデックスリストに要素追加
      kosu_list.append(i)

    # 時間区分毎に前の作業との差異がある場合の処理
    if i != 0 and (work_list[i] != work_list[i - 1] or \
                   detail_list[i] != detail_list[i - 1]):
      
      # 作業時間インデックスに作業時間のインデックス記録
      kosu_list.append(i)

    # 最後の要素に作業が入っている場合の処理
    if i == 287 and work_list[i] != '#':

      # 作業時間インデックスリストに要素追加
      kosu_list.append(i)

  # 作業時間インデックスに要素がある場合の処理
  if len(kosu_list) != 0:

    # 作業時間インデックスを時間表示に修正
    for ind, t in enumerate(kosu_list):

      # 最後以外のループ処理
      if len(kosu_list) - 1 != ind:

        # 作業開始時間をSTRで定義
        time_obj_start = str(int(t)//12).zfill(2) + ':' + str(int(t)%12*5).zfill(2)
        # 作業終了時間をSTRで定義
        time_obj_end = str(int(kosu_list[ind + 1])//12).zfill(2) + ':' \
          + str(int(kosu_list[ind + 1])%12*5).zfill(2)
        
        # 作業開始時間と作業終了時間をリストに追加
        time_list_start.append(time_obj_start)
        time_list_end.append(time_obj_end)

        # 作業開始時間をSTRで定義
        time_obj_start = str(int(t)//12).zfill(2) + ':' + str(int(t)%12*5).zfill(2)


  # 現在使用している工数区分のオブジェクトを取得
  kosu_obj = kosu_division.objects.get(kosu_name = request.session.get('input_def', None))

  # 工数区分登録カウンターリセット
  n = 0
  # 工数区分登録数カウント
  for kosu_num in range(1, 50):
    if eval('kosu_obj.kosu_title_{}'.format(kosu_num)) != None:
      n = kosu_num

  # 工数区分処理用記号リスト用意
  str_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', \
              'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', \
                'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                    'q', 'r', 's', 't', 'u', 'v', 'w', 'x',]
  # リストの長さを工数区分の登録数に応じて調整
  del str_list[n:]

  # 作業無し記号追加
  str_list.append('#')

  # 工数区分の選択リスト作成
  for i, m in enumerate(str_list):

    # 最終ループでない場合の処置
    if i != len(str_list) - 1:

      # 工数区分定義要素を追加
      def_list.append(eval('kosu_obj.kosu_title_{}'.format(i + 1)))

    # 最終ループの場合の処置
    else:
  
      # 作業なし追加
      def_list.append('-')

  # 工数区分辞書作成
  def_library = dict(zip(str_list, def_list))


  # 作業内容と作業詳細リスト作成
  for ind, t in enumerate(kosu_list):

    # 最後以外のループ処理
    if len(kosu_list) - 1 != ind:

      def_time.append(def_library[work_list[t]])
      detail_time.append(detail_list[t])

  # HTML表示用リスト作成
  time_display_list = []
  for k in range(len(time_list_start)):
    for_list = []
    for_list.append(str(time_list_start[k]) + '～' + str(time_list_end[k]))
    for_list.append(def_time[k])
    for_list.append(detail_time[k])
    time_display_list.append(for_list)


  form = input_kosuForm()


  # POST時の処理
  if (request.method == 'POST'):
    
    # 削除開始時間と終了時間のインデント取得
    start_indent = int(request.POST['start_hour'])*12 + int(request.POST['start_min'])/5
    end_indent = int(request.POST['end_hour'])*12 + int(request.POST['end_min'])/5


    # 削除開始時間が削除終了時間より遅い時間の場合の処理
    if start_indent > end_indent:

      # エラーメッセージ出力
      messages.error(request, '削除の開始時間が終了時間よりも遅い時間を指定されましたので処理できません。ERROR011')
      # このページをリダイレクト
      return redirect(to = '/detail/{}'.format(num))


    # 指定された時間の作業内容と作業詳細を消す
    for i in range(int(start_indent), int(end_indent)):
      work_list[i] = '#'
      detail_list[i] = ''

    # 作業詳細リストを文字列に変更
    detail_list_str = ''
    for i, e in enumerate(detail_list):
      if i == len(detail_list) - 1:
        detail_list_str = detail_list_str + detail_list[i]
      else:
        detail_list_str = detail_list_str + detail_list[i] + '$'


    # 変数リセット
    kosu_total = 0

    # 工数の合計を計算
    for k in work_list:

      # 作業内容が入っている場合の処理
      if k != '#':

        # 工数の合計に5分加算
        kosu_total += 5

    # 工数入力OK_NGリセット
    judgement = False

    # 出勤、休出時、工数合計と残業に整合性がある場合の処理
    if (obj_get.work_time == '出勤' or obj_get.work_time == 'シフト出') and \
      kosu_total - int(obj_get.over_time) == 470:

      # 工数入力OK_NGをOKに切り替え
      judgement = True


    # 休出時、工数合計と残業に整合性がある場合の処理
    if obj_get.work_time == '休出' and kosu_total == int(obj_get.over_time):

      # 工数入力OK_NGをOKに切り替え
      judgement = True


    # 早退・遅刻時、工数合計と残業に整合性がある場合の処理
    if obj_get.work_time == '早退・遅刻' and kosu_total != 0:

      # 工数入力OK_NGをOKに切り替え
      judgement = True


    # ログイン者の人員データ取得
    member_obj = member.objects.get(employee_no = request.session.get('login_No', None))


    # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Cで1直の場合の処理
    if (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
      member_obj.shop == 'A1' or member_obj.shop == 'A2') and \
        obj_get.tyoku2 == '1':

      # 半前年休時、工数合計と残業に整合性がある場合の処理
      if obj_get.work_time == '半前年休' and kosu_total - int(obj_get.over_time) == 230:

        # 工数入力OK_NGをOKに切り替え
        judgement = True

      # 半後年休時、工数合計と残業に整合性がある場合の処理
      if obj_get.work_time == '半後年休' and kosu_total - int(obj_get.over_time) == 240:

        # 工数入力OK_NGをOKに切り替え
        judgement = True


    # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Cで2直の場合の処理
    if (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
      member_obj.shop == 'A1' or member_obj.shop == 'A2') and \
        obj_get.tyoku2 == '2':

      # 半前年休時、工数合計と残業に整合性がある場合の処理
      if obj_get.work_time == '半前年休' and kosu_total - int(obj_get.over_time) == 290:

        # 工数入力OK_NGをOKに切り替え
        judgement = True

      # 半後年休時、工数合計と残業に整合性がある場合の処理
      if obj_get.work_time == '半後年休' and kosu_total - int(obj_get.over_time) == 180:

        # 工数入力OK_NGをOKに切り替え
        judgement = True


    # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Cで3直の場合の処理
    if (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
      member_obj.shop == 'A1' or member_obj.shop == 'A2') and \
        obj_get.tyoku2 == '3':

      # 半前年休時、工数合計と残業に整合性がある場合の処理
      if obj_get.work_time == '半前年休' and kosu_total - int(obj_get.over_time) == 230:

        # 工数入力OK_NGをOKに切り替え
        judgement = True

      # 半後年休時、工数合計と残業に整合性がある場合の処理
      if obj_get.work_time == '半後年休' and kosu_total - int(obj_get.over_time) == 240:

        # 工数入力OK_NGをOKに切り替え
        judgement = True


    # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Bで1直の場合の処理
    if (member_obj.shop == 'P' or member_obj.shop == 'R' or \
      member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
        member_obj.shop == 'その他' or member_obj.shop == '組長以上') and \
        obj_get.tyoku2 == '1':

      # 半前年休時、工数合計と残業に整合性がある場合の処理
      if obj_get.work_time == '半前年休' and kosu_total - int(obj_get.over_time) == 220:

        # 工数入力OK_NGをOKに切り替え
        judgement = True

      # 半後年休時、工数合計と残業に整合性がある場合の処理
      if obj_get.work_time == '半後年休' and kosu_total - int(obj_get.over_time) == 250:

        # 工数入力OK_NGをOKに切り替え
        judgement = True


    # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Bで2直の場合の処理
    if (member_obj.shop == 'P' or member_obj.shop == 'R' or \
      member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
        member_obj.shop == 'その他' or member_obj.shop == '組長以上') and \
        obj_get.tyoku2 == '2':

      # 半前年休時、工数合計と残業に整合性がある場合の処理
      if obj_get.work_time == '半前年休' and kosu_total - int(obj_get.over_time) == 230:

        # 工数入力OK_NGをOKに切り替え
        judgement = True

      # 半後年休時、工数合計と残業に整合性がある場合の処理
      if obj_get.work_time == '半後年休' and kosu_total - int(obj_get.over_time) == 240:

        # 工数入力OK_NGをOKに切り替え
        judgement = True


    # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Bで3直の場合の処理
    if (member_obj.shop == 'P' or member_obj.shop == 'R' or \
      member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
        member_obj.shop == 'その他' or member_obj.shop == '組長以上') and \
        obj_get.tyoku2 == '3':

      # 半前年休時、工数合計と残業に整合性がある場合の処理
      if obj_get.work_time == '半前年休' and kosu_total - int(obj_get.over_time) == 275:

        # 工数入力OK_NGをOKに切り替え
        judgement = True

      # 半後年休時、工数合計と残業に整合性がある場合の処理
      if obj_get.work_time == '半後年休' and kosu_total - int(obj_get.over_time) == 195:

        # 工数入力OK_NGをOKに切り替え
        judgement = True


    # 常昼の場合の処理
    if obj_get.tyoku2 == '4':

      # 半前年休時、工数合計と残業に整合性がある場合の処理
      if obj_get.work_time == '半前年休' and kosu_total - int(obj_get.over_time) == 230:

        # 工数入力OK_NGをOKに切り替え
        judgement = True

      # 半後年休時、工数合計と残業に整合性がある場合の処理
      if obj_get.work_time == '半後年休' and kosu_total - int(obj_get.over_time) == 240:

        # 工数入力OK_NGをOKに切り替え
        judgement = True


    # 作業内容データの内容を上書きして更新
    Business_Time_graph.objects.update_or_create(employee_no3 = request.session.get('login_No', None), \
      work_day2 = obj_get.work_day2, defaults = {'time_work' : ''.join(work_list), \
                                                 'detail_work' : detail_list_str, \
                                                 'judgement' : judgement})


    # 指定IDの工数履歴のレコードのオブジェクトを変数に入れる
    obj_get = Business_Time_graph.objects.get(id = num)

    # 作業内容と作業詳細を取得しリストに解凍
    work_list = list(obj_get.time_work)
    detail_list = obj_get.detail_work.split('$')


    # 作業時間リストリセット
    kosu_list = []
    time_list_start = []
    time_list_end = []
    def_list = []
    def_time = []
    detail_time = []

    # 作業内容と作業詳細毎の開始時間と終了時間インデックス取得
    for i in range(288):

      # 最初の要素に作業が入っている場合の処理
      if i == 0 and work_list[i] != '#':

        # 作業時間インデックスリストに要素追加
        kosu_list.append(i)

      # 時間区分毎に前の作業との差異がある場合の処理
      if i != 0 and (work_list[i] != work_list[i - 1] or \
                    detail_list[i] != detail_list[i - 1]):
        
        # 作業時間インデックスに作業時間のインデックス記録
        kosu_list.append(i)

      # 最後の要素に作業が入っている場合の処理
      if i == 287 and work_list[i] != '#':

        # 作業時間インデックスリストに要素追加
        kosu_list.append(i)

    # 作業時間インデックスに要素がある場合の処理
    if len(kosu_list) != 0:

      # 作業時間インデックスを時間表示に修正
      for ind, t in enumerate(kosu_list):

        # 最後以外のループ処理
        if len(kosu_list) - 1 != ind:

          # 作業開始時間をSTRで定義
          time_obj_start = str(int(t)//12).zfill(2) + ':' + str(int(t)%12*5).zfill(2)
          # 作業終了時間をSTRで定義
          time_obj_end = str(int(kosu_list[ind + 1])//12).zfill(2) + ':' \
            + str(int(kosu_list[ind + 1])%12*5).zfill(2)
          
          # 作業開始時間と作業終了時間をリストに追加
          time_list_start.append(time_obj_start)
          time_list_end.append(time_obj_end)

          # 作業開始時間をSTRで定義
          time_obj_start = str(int(t)//12).zfill(2) + ':' + str(int(t)%12*5).zfill(2)


    # 現在使用している工数区分のオブジェクトを取得
    kosu_obj = kosu_division.objects.get(kosu_name = request.session.get('input_def', None))

    # 工数区分登録カウンターリセット
    n = 0
    # 工数区分登録数カウント
    for kosu_num in range(1, 50):
      if eval('kosu_obj.kosu_title_{}'.format(kosu_num)) != None:
        n = kosu_num

    # 工数区分処理用記号リスト用意
    str_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', \
                'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', \
                  'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                      'q', 'r', 's', 't', 'u', 'v', 'w', 'x',]
    # リストの長さを工数区分の登録数に応じて調整
    del str_list[n:]

    # 作業無し記号追加
    str_list.append('#')

    # 工数区分の選択リスト作成
    for i, m in enumerate(str_list):

      # 最終ループでない場合の処置
      if i != len(str_list) - 1:

        # 工数区分定義要素を追加
        def_list.append(eval('kosu_obj.kosu_title_{}'.format(i + 1)))

      # 最終ループの場合の処置
      else:
    
        # 作業なし追加
        def_list.append('-')

    # 工数区分辞書作成
    def_library = dict(zip(str_list, def_list))


    # 作業内容と作業詳細リスト作成
    for ind, t in enumerate(kosu_list):

      # 最後以外のループ処理
      if len(kosu_list) - 1 != ind:

        def_time.append(def_library[work_list[t]])
        detail_time.append(detail_list[t])

    # HTML表示用リスト作成
    time_display_list = []
    for k in range(len(time_list_start)):
      for_list = []
      for_list.append(str(time_list_start[k]) + '～' + str(time_list_end[k]))
      for_list.append(def_time[k])
      for_list.append(detail_time[k])
      time_display_list.append(for_list)


  # HTMLに渡す辞書
  library_m = {
    'title' : '工数詳細',
    'id' : num,
    'day' : obj_get.work_day2,
    'time_display_list' : time_display_list,
    'form' : form,
    }

  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/detail.html', library_m)





#--------------------------------------------------------------------------------------------------------





# 工数履歴画面定義
def delete(request, num):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')
  
  # 指定IDの工数履歴のレコードのオブジェクトを変数に入れる
  obj_get = Business_Time_graph.objects.get(id = num)

  # 作業内容と作業詳細を取得しリストに解凍
  work_list = list(obj_get.time_work)
  detail_list = obj_get.detail_work.split('$')


  # 作業時間リストリセット
  kosu_list = []
  time_list_start = []
  time_list_end = []
  def_list = []
  def_time = []
  detail_time = []

  # 作業内容と作業詳細毎の開始時間と終了時間インデックス取得
  for i in range(288):

    # 最初の要素に作業が入っている場合の処理
    if i == 0 and work_list[i] != '#':

      # 作業時間インデックスリストに要素追加
      kosu_list.append(i)

    # 時間区分毎に前の作業との差異がある場合の処理
    if i != 0 and (work_list[i] != work_list[i - 1] or \
                   detail_list[i] != detail_list[i - 1]):
      
      # 作業時間インデックスに作業時間のインデックス記録
      kosu_list.append(i)

    # 最後の要素に作業が入っている場合の処理
    if i == 287 and work_list[i] != '#':

      # 作業時間インデックスリストに要素追加
      kosu_list.append(i)

  # 作業時間インデックスに要素がある場合の処理
  if len(kosu_list) != 0:

    # 作業時間インデックスを時間表示に修正
    for ind, t in enumerate(kosu_list):

      # 最後以外のループ処理
      if len(kosu_list) - 1 != ind:

        # 作業開始時間をSTRで定義
        time_obj_start = str(int(t)//12).zfill(2) + ':' + str(int(t)%12*5).zfill(2)
        # 作業終了時間をSTRで定義
        time_obj_end = str(int(kosu_list[ind + 1])//12).zfill(2) + ':' \
          + str(int(kosu_list[ind + 1])%12*5).zfill(2)
        
        # 作業開始時間と作業終了時間をリストに追加
        time_list_start.append(time_obj_start)
        time_list_end.append(time_obj_end)

        # 作業開始時間をSTRで定義
        time_obj_start = str(int(t)//12).zfill(2) + ':' + str(int(t)%12*5).zfill(2)


  # 現在使用している工数区分のオブジェクトを取得
  kosu_obj = kosu_division.objects.get(kosu_name = request.session.get('input_def', None))

  # 工数区分登録カウンターリセット
  n = 0
  # 工数区分登録数カウント
  for kosu_num in range(1, 50):
    if eval('kosu_obj.kosu_title_{}'.format(kosu_num)) != None:
      n = kosu_num

  # 工数区分処理用記号リスト用意
  str_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', \
              'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', \
                'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                    'q', 'r', 's', 't', 'u', 'v', 'w', 'x',]
  # リストの長さを工数区分の登録数に応じて調整
  del str_list[n:]

  # 作業無し記号追加
  str_list.append('#')

  # 工数区分の選択リスト作成
  for i, m in enumerate(str_list):

    # 最終ループでない場合の処置
    if i != len(str_list) - 1:

      # 工数区分定義要素を追加
      def_list.append(eval('kosu_obj.kosu_title_{}'.format(i + 1)))

    # 最終ループの場合の処置
    else:
  
      # 作業なし追加
      def_list.append('-')

  # 工数区分辞書作成
  def_library = dict(zip(str_list, def_list))


  # 作業内容と作業詳細リスト作成
  for ind, t in enumerate(kosu_list):

    # 最後以外のループ処理
    if len(kosu_list) - 1 != ind:

      def_time.append(def_library[work_list[t]])
      detail_time.append(detail_list[t])

  # HTML表示用リスト作成
  time_display_list = []
  for k in range(len(time_list_start)):
    for_list = []
    for_list.append(str(time_list_start[k]) + '～' + str(time_list_end[k]))
    for_list.append(def_time[k])
    for_list.append(detail_time[k])
    time_display_list.append(for_list)


  # POST時の処理
  if (request.method == 'POST'):

    # 取得していた指定従業員番号のレコードを削除する
    obj_get.delete()

    # 工数履歴画面をリダイレクトする
    return redirect(to = '/list/1')


  # HTMLに渡す辞書
  library_m = {
    'title' : '工数データ削除',
    'id' : num,
    'time_display_list' : time_display_list,
    'day' : obj_get.work_day2,
    }

  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/delete.html', library_m)





#--------------------------------------------------------------------------------------------------------





# 工数集計画面定義
def total(request): 

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')

  # ログイン者の情報取得
  data = member.objects.get(employee_no = request.session.get('login_No', None))

  # GET時の処理
  if (request.method == 'GET'):
    # 今日の日時を変数に格納
    today = datetime.date.today()

    # フォームの初期値に定義する辞書作成
    start_list = {'kosu_day' : today}

    # フォームに初期値設定し定義
    form = kosu_dayForm(start_list)

    # ログイン者の工数集計データ取得
    kosu_total = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None), \
                                                    work_day2 = today)
    
    # ログイン者の本日の工数集計データがない場合の処理
    if kosu_total.count() == 0:

      # 工数区分定義データ取得
      kosu_obj = kosu_division.objects.get(kosu_name = request.session.get('input_def', None))
    
      # 工数区分定義の数をカウント
      def_num = 0
      for n in range(1, 51):
        if eval('kosu_obj.kosu_title_{}'.format(n)) != None:
          def_num = n

      # 工数区分定義の選択リスト作成
      graph_item = []
      for i in range(def_num):
        graph_item.append(eval('kosu_obj.kosu_title_{}'.format(i + 1)))
      
      # 0が工数区分定義と同じ数入ったリスト作成
      graph_list = list(itertools.repeat(0, def_num))

    # ログイン者の本日の工数集計データがある場合の処理
    if kosu_total.count() >= 1:

      # ログイン者の工数集計データ取得
      graph_data = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', None), \
                                                   work_day2 = today)
      # 工数区分定義データ取得
      kosu_obj = kosu_division.objects.get(kosu_name = graph_data.def_ver2)

      # 工数区分定義の数をカウント
      def_num = 0
      for n in range(1, 51):
        if eval('kosu_obj.kosu_title_{}'.format(n)) != None:
          def_num = n

      # 工数区分定義の選択リスト作成
      graph_item = []
      for i in range(def_num):
        graph_item.append(eval('kosu_obj.kosu_title_{}'.format(i + 1)))

      # 工数データをリストに解凍
      data_list = list(graph_data.time_work)

      # 工数データリスト内の各文字を定義
      str_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', \
                  'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', \
                    'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                        'q', 'r', 's', 't', 'u', 'v', 'w', 'x',]
      # 工数データリスト内の各文字を工数区分定義の数に調整
      del str_list[def_num:]

      # 各工数区分定義の累積工数リスト作成
      str_n = 0
      graph_list = []

      for i in str_list:

        for k in range(288):
          if data_list[k] == i:
            str_n += 5

        graph_list.append(str_n)
        str_n = 0

    # グラフ項目色定義
    color_list = ['plum', 'darkgray', 'slategray', 'steelblue', 'royalblue', 'dodgerblue', 
                  'deepskyblue', 'aqua', 'mediumturquoise', 'lightseagreen', 'springgreen', 'limegreen', 
                  'lawngreen', 'greenyellow', 'gold', 'darkorange', 'burlywood', 'sandybrown', 'lightcoral', 
                  'lightsalmon', 'tomato', 'orangered', 'red', 'deeppink', 'hotpink', 'violet', 'magenta', 
                  'mediumorchid', 'darkviolet', 'mediumpurple', 'mediumblue', 'cadetblue', 'mediumseagreen', 
                  'forestgreen', 'darkkhaki', 'crimson', 'rosybrown', 'dimgray', 'midnightblue', 'darkblue', 
                  'darkslategray', 'darkgreen', 'olivedrab', 'darkgoldenrod', 'sienna', 'firebrick', 'maroon', 
                  'darkmagenta', 'indigo', 'black'] 


  # POST時の処理
  if (request.method == 'POST'):
    # 年間工数選択時処理
    if request.POST['kosu_summarize'] == '3':
      # POST送信された就業日を変数に入れる
      post_day = request.POST['kosu_day']
      # POST送信された就業日の年部分抜き出し
      kosu_year = post_day[: 4]

      # 指定年の工数取得
      kosu_total = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None), \
                                                    work_day2__startswith = kosu_year)


      #指定年に工数入力がない場合の処理
      if kosu_total.count() == 0:

        # 工数区分定義データ取得
        kosu_obj = kosu_division.objects.get(kosu_name = request.session.get('input_def', None))
      
        # 工数区分定義の数をカウント
        def_num = 0
        for n in range(1, 51):
          if eval('kosu_obj.kosu_title_{}'.format(n)) != None:
            def_num = n

        # 工数区分定義の選択リスト作成
        graph_item = []
        for i in range(def_num):
          graph_item.append(eval('kosu_obj.kosu_title_{}'.format(i + 1)))
        
        # 0が工数区分定義と同じ数入ったリスト作成
        graph_list = list(itertools.repeat(0, def_num))


      # 指定年に工数入力がある場合の処理
      graph_list = []
      if kosu_total.count() >= 1:

        # 年の最初の日の工数区分定義でグラフ項目リスト作成
        for v in kosu_total:
          # 工数区分定義データ取得
          kosu_obj = kosu_division.objects.get(kosu_name = v.def_ver2)
          # 工数区分定義の数をカウント
          def_num = 0
          for n in range(1, 51):
            if eval('kosu_obj.kosu_title_{}'.format(n)) != None:
              def_num = n

          # 工数区分定義の選択リスト作成
          graph_item = []
          for i in range(def_num):
            graph_item.append(eval('kosu_obj.kosu_title_{}'.format(i + 1)))

          # 工数データリスト内の各文字を定義
          str_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', \
                      'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', \
                        'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                            'q', 'r', 's', 't', 'u', 'v', 'w', 'x',]
          # 工数データリスト内の各文字を工数区分定義の数に調整
          del str_list[def_num:]
          break

        # 指定年の工数を加算しデータリスト作成
        graph_list = list(itertools.repeat(0, def_num))
        for i in kosu_total:
          # 工数データをリストに解凍
          data_list = list(i.time_work)
          # 各工数区分定義の累積工数リスト作成
          str_n = 0
          graph_year = []
          for i in str_list:

            for k in range(288):
              if data_list[k] == i:
                str_n += 5

            graph_year.append(str_n)
            str_n = 0

          # 各工数区分定義の累積工数リストを日ごとに加算
          for w, v in enumerate(zip(graph_year, graph_list)):
            kosu_sum = sum(v)
            graph_list[w] = kosu_sum


    # 月間工数選択時処理
    if request.POST['kosu_summarize'] == '2':
      # POST送信された就業日を変数に入れる
      post_day = request.POST['kosu_day']
      # POST送信された就業日の年、月部分抜き出し
      kosu_month = post_day[: 7]

      # 指定月の工数取得
      kosu_total = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None), \
                                                    work_day2__startswith = kosu_month)
      
      #指定月に工数入力がない場合の処理
      if kosu_total.count() == 0:

        # 工数区分定義データ取得
        kosu_obj = kosu_division.objects.get(kosu_name = request.session.get('input_def', None))
      
        # 工数区分定義の数をカウント
        def_num = 0
        for n in range(1, 51):
          if eval('kosu_obj.kosu_title_{}'.format(n)) != None:
            def_num = n

        # 工数区分定義の選択リスト作成
        graph_item = []
        for i in range(def_num):
          graph_item.append(eval('kosu_obj.kosu_title_{}'.format(i + 1)))
        
        # 0が工数区分定義と同じ数入ったリスト作成
        graph_list = list(itertools.repeat(0, def_num))


      # 指定月に工数入力がある場合の処理
      graph_list = []
      if kosu_total.count() >= 1:

        # 月の最初の日の工数区分定義でグラフ項目リスト作成
        for v in kosu_total:
          # 工数区分定義データ取得
          kosu_obj = kosu_division.objects.get(kosu_name = v.def_ver2)
          # 工数区分定義の数をカウント
          def_num = 0
          for n in range(1, 51):
            if eval('kosu_obj.kosu_title_{}'.format(n)) != None:
              def_num = n

          # 工数区分定義の選択リスト作成
          graph_item = []
          for i in range(def_num):
            graph_item.append(eval('kosu_obj.kosu_title_{}'.format(i + 1)))

          # 工数データリスト内の各文字を定義
          str_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', \
                      'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', \
                        'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                            'q', 'r', 's', 't', 'u', 'v', 'w', 'x',]
          # 工数データリスト内の各文字を工数区分定義の数に調整
          del str_list[def_num:]
          break

        # 指定月の工数を加算しデータリスト作成
        graph_list = list(itertools.repeat(0, def_num))
        for i in kosu_total:
          # 工数データをリストに解凍
          data_list = list(i.time_work)
          # 各工数区分定義の累積工数リスト作成
          str_n = 0
          graph_month = []
          for i in str_list:

            for k in range(288):
              if data_list[k] == i:
                str_n += 5

            graph_month.append(str_n)
            str_n = 0

          # 各工数区分定義の累積工数リストを日ごとに加算
          for w, v in enumerate(zip(graph_month, graph_list)):
            kosu_sum = sum(v)
            graph_list[w] = kosu_sum


    # フォームにPOSTした値を設定し定義
    form = kosu_dayForm(request.POST)

    # ログイン者の工数集計データ取得
    kosu_total = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None), \
                                                    work_day2 = request.POST['kosu_day'])

    # ログイン者の本日の工数集計データがない場合の処理
    if kosu_total.count() == 0 and request.POST['kosu_summarize'] == '1':
      
      # 工数区分定義データ取得
      kosu_obj = kosu_division.objects.get(kosu_name = request.session.get('input_def', None))
    
      # 工数区分定義の数をカウント
      def_num = 0
      for n in range(1, 51):
        if eval('kosu_obj.kosu_title_{}'.format(n)) != None:
          def_num = n

      # 工数区分定義の選択リスト作成
      graph_item = []
      for i in range(def_num):
        graph_item.append(eval('kosu_obj.kosu_title_{}'.format(i + 1)))
      
      # 0が工数区分定義と同じ数入ったリスト作成
      graph_list = list(itertools.repeat(0, def_num))


    # ログイン者の本日の工数集計データがある場合の処理
    if kosu_total.count() >= 1 and request.POST['kosu_summarize'] == '1':

      # ログイン者の工数集計データ取得
      graph_data = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', None), \
                                                   work_day2 = request.POST['kosu_day'])
      # 工数区分定義データ取得
      kosu_obj = kosu_division.objects.get(kosu_name = graph_data.def_ver2)

      # 工数区分定義の数をカウント
      def_num = 0
      for n in range(1, 51):
        if eval('kosu_obj.kosu_title_{}'.format(n)) != None:
          def_num = n

      # 工数区分定義の選択リスト作成
      graph_item = []
      for i in range(def_num):
        graph_item.append(eval('kosu_obj.kosu_title_{}'.format(i + 1)))

      # 工数データをリストに解凍
      data_list = list(graph_data.time_work)

      # 工数データリスト内の各文字を定義
      str_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', \
                  'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', \
                    'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                        'q', 'r', 's', 't', 'u', 'v', 'w', 'x',]
      # 工数データリスト内の各文字を工数区分定義の数に調整
      del str_list[def_num:]

      # 各工数区分定義の累積工数リスト作成
      str_n = 0
      graph_list = []

      for i in str_list:

        for k in range(288):
          if data_list[k] == i:
            str_n += 5

        graph_list.append(str_n)
        str_n = 0

    # グラフ項目色定義
    color_list = ['plum', 'darkgray', 'slategray', 'steelblue', 'royalblue', 'dodgerblue', 
                  'deepskyblue', 'aqua', 'mediumturquoise', 'lightseagreen', 'springgreen', 'limegreen', 
                  'lawngreen', 'greenyellow', 'gold', 'darkorange', 'burlywood', 'sandybrown', 'lightcoral', 
                  'lightsalmon', 'tomato', 'orangered', 'red', 'deeppink', 'hotpink', 'violet', 'magenta', 
                  'mediumorchid', 'darkviolet', 'mediumpurple', 'mediumblue', 'cadetblue', 'mediumseagreen', 
                  'forestgreen', 'darkkhaki', 'crimson', 'rosybrown', 'dimgray', 'midnightblue', 'darkblue', 
                  'darkslategray', 'darkgreen', 'olivedrab', 'darkgoldenrod', 'sienna', 'firebrick', 'maroon', 
                  'darkmagenta', 'indigo', 'black'] 


    # 並び順が多い順の場合処理
    if request.POST['kosu_order'] == '2':
      # グラフ項目色の要素数を合わせる
      del color_list[def_num:]
      # 項目色と工数を辞書型に統合
      color_library = dict(zip(color_list, graph_list))
      # 工数区分定義と各工数を辞書型に統合
      graph_library = dict(zip(graph_item, graph_list))
      # 工数の多い順に辞書を並び替え
      color_library_tuple = sorted(color_library.items(), key = lambda x : x[1] ,reverse = True)
      graph_library_tuple = sorted(graph_library.items(), key = lambda x : x[1] ,reverse = True)
      #タプル型を辞書型に変換
      color_library = {k : v for k, v in color_library_tuple}
      graph_library = {k : v for k, v in graph_library_tuple}
      # 並び替えた辞書を工数区分定義と工数をリストに分ける
      color_list = color_library.keys()
      graph_item = graph_library.keys()
      graph_list = graph_library.values()


  # HTMLに渡す辞書
  library_m = {
    'title' : '工数集計',
    'data' : data,
    'form' : form,
    'graph_list' : graph_list,
    'graph_item' : graph_item,
    'color_list' : color_list,
    'graph_library' : dict(zip(graph_item, graph_list))
  }

  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/total.html', library_m)





#--------------------------------------------------------------------------------------------------------





# グラフデータ画面定義
def graph(request): 

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')

  # ログイン者の情報取得
  data = member.objects.get(employee_no = request.session.get('login_No', None))
  # ログイン者に権限がなければメインページに戻る
  if data.administrator == False:
    return redirect(to = '/')
  
  # グラフデータ一覧用オブジェクト取得
  obj = Business_Time_graph.objects.all().order_by('work_day2').reverse()

  # 人員の全てのオブジェクトを取得
  obj2 = member.objects.all()
  # 班員の従業員番号リスト作成
  choices_list = [('','')]
  for i in obj2:
    choices_list.append((i.employee_no, i.employee_no))

  # フォームの初期状態定義
  form = team_kosuForm()
  # フォームの選択肢定義
  form.fields['employee_no6'].choices = choices_list


  # POST時の処理
  if (request.method == 'POST'):
    # POST後のフォーム状態定義
    form = team_kosuForm(request.POST)
    # フォームの選択肢定義
    form.fields['employee_no6'].choices = choices_list

    # グラフデータ一覧用オブジェクト取得
    obj = Business_Time_graph.objects.filter(employee_no3__contains = request.POST['employee_no6'], \
                                             work_day2__contains = request.POST['team_day'])


  # HTMLに渡す辞書
  library_m = {
    'title' : 'グラフデータ',
    'obj' : obj,
    'form' : form
  }

  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/graph.html', library_m)





#--------------------------------------------------------------------------------------------------------





# カレンダー画面定義
def schedule(request): 

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')
  
  # 本日の日付取得
  today = datetime.date.today()


  # GET時の処理
  if (request.method == 'GET'):
    # 本日の年取得
    year = today.year
    # 本日の月取得
    month = today.month

    # 表示月をセッションに登録
    request.session['update_year'] = year
    request.session['update_month'] = month

    # GET時のカレンダー設定フォームの初期値設定
    default_list = {'year' : year, 'month' : month}
    # GET時のカレンダー設定フォーム定義
    form2 = schedule_timeForm(default_list)

    # GETされた月の初日取得
    select_month = datetime.date(year, month, 1)
    # GETされた月の初日の曜日取得
    week_day = select_month.weekday()

    # GETされた月の最終日取得
    if month == 12:
      month_end = 1
      year_end = year + 1
    else:
      month_end = month + 1
      year_end = year

    select_month = datetime.date(year_end, month_end, 1)
    month_day_end = select_month - datetime.timedelta(days = 1)
    day_end = month_day_end.day

    # カレンダー表示日付変数リセット
    day_list = list(itertools.repeat('', 37))

    # 1週目の日付設定
    if week_day == 6:
      day_list[0] = 1
      day_list[1] = 2
      day_list[2] = 3
      day_list[3] = 4
      day_list[4] = 5
      day_list[5] = 6
      day_list[6] = 7

    if week_day == 0:
      day_list[1] = 1
      day_list[2] = 2
      day_list[3] = 3
      day_list[4] = 4
      day_list[5] = 5
      day_list[6] = 6

    if week_day == 1:
      day_list[2] = 1
      day_list[3] = 2
      day_list[4] = 3
      day_list[5] = 4
      day_list[6] = 5

    if week_day == 2:
      day_list[3] = 1
      day_list[4] = 2
      day_list[5] = 3
      day_list[6] = 4

    if week_day == 3:
      day_list[4] = 1
      day_list[5] = 2
      day_list[6] = 3

    if week_day == 4:
      day_list[5] = 1
      day_list[6] = 2

    if week_day == 5:
      day_list[6] = 1

    # 基準日指定
    start_day = day_list[6]

    # 2～5週目の日付設定
    for i in range(7, 37):
      day_list[i] = start_day + 1
      start_day += 1
      if start_day == day_end:
        break

    # 勤務フォーム初期値定義
    form_default_list = {}
    for i in range(37):
      if day_list[i] != '':
        day_filter = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None), \
                                                        work_day2 = datetime.date(year, month, day_list[i]))
        if day_filter.count() > 0:
          day_get = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', None), \
                                                    work_day2 = datetime.date(year, month, day_list[i]))
          form_default_list[('day{}'.format(i + 1))] = day_get.work_time

    # 勤務フォーム定義
    form = scheduleForm(form_default_list)


  # カレンダー更新時の処理
  if "time_update" in request.POST:

    # 年取得
    year = int(request.POST['year'])
    # 月取得
    month = int(request.POST['month'])

    # 表示月をセッションに登録
    request.session['update_year'] = year
    request.session['update_month'] = month

    # POST後のカレンダー設定フォームの初期値設定
    default_list = {'year' : year, 'month' : month}
    # POST後のカレンダー設定フォーム定義
    form2 = schedule_timeForm(default_list)

    # POSTされた月の初日取得
    select_month = datetime.date(year, month, 1)
    # POSTされた月の初日の曜日取得
    week_day = select_month.weekday()

    # POSTされた月の最終日取得
    if month == 12:
      month_end = 1
      year_end = year + 1
    else:
      month_end = month + 1
      year_end = year

    select_month = datetime.date(year_end, month_end, 1)
    month_day_end = select_month - datetime.timedelta(days = 1)
    day_end = month_day_end.day

    # カレンダー表示日付リセット
    day_list = list(itertools.repeat('', 37))

    # 1週目の日付設定
    if week_day == 6:
      day_list[0] = 1
      day_list[1] = 2
      day_list[2] = 3
      day_list[3] = 4
      day_list[4] = 5
      day_list[5] = 6
      day_list[6] = 7

    if week_day == 0:
      day_list[1] = 1
      day_list[2] = 2
      day_list[3] = 3
      day_list[4] = 4
      day_list[5] = 5
      day_list[6] = 6

    if week_day == 1:
      day_list[2] = 1
      day_list[3] = 2
      day_list[4] = 3
      day_list[5] = 4
      day_list[6] = 5

    if week_day == 2:
      day_list[3] = 1
      day_list[4] = 2
      day_list[5] = 3
      day_list[6] = 4

    if week_day == 3:
      day_list[4] = 1
      day_list[5] = 2
      day_list[6] = 3

    if week_day == 4:
      day_list[5] = 1
      day_list[6] = 2

    if week_day == 5:
      day_list[6] = 1

    # 基準日指定
    start_day = day_list[6]

    # 2～5週目の日付設定
    for i in range(7, 37):
      day_list[i] = start_day + 1
      start_day += 1
      if start_day == day_end:
        break

    # 勤務フォーム初期値定義
    form_default_list = {}
    for i in range(37):
      if day_list[i] != '':
        day_filter = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None), \
                                                        work_day2 = datetime.date(year, month, day_list[i]))
        if day_filter.count() > 0:
          day_get = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', None), \
                                                    work_day2 = datetime.date(year, month, day_list[i]))
          form_default_list[('day{}'.format(i + 1))] = day_get.work_time

    # 勤務フォーム定義
    form = scheduleForm(form_default_list)

    # カレンダー設定フォーム定義
    form2 = schedule_timeForm(request.POST)


  # 勤務登録時の処理
  if "work_update" in request.POST:

    # カレンダー設定フォーム定義
    form2 = schedule_timeForm(request.POST)

    # カレンダーの年、月取得
    year = request.session.get('update_year', '')
    month = request.session.get('update_month', '')
    
    # 月の初日取得
    select_month = datetime.date(year, month, 1)
    # 月の初日の曜日取得
    week_day = select_month.weekday()

    # 月の最終日取得
    if month == 12:
      month_end = 1
      year_end = year + 1
    else:
      month_end = month + 1
      year_end = year

    select_month = datetime.date(year_end, month_end, 1)
    month_day_end = select_month - datetime.timedelta(days = 1)
    day_end = month_day_end.day

    # カレンダー表示日付リセット
    day_list = list(itertools.repeat('', 37))

    # 1週目の日付設定
    if week_day == 6:
      day_list[0] = 1
      day_list[1] = 2
      day_list[2] = 3
      day_list[3] = 4
      day_list[4] = 5
      day_list[5] = 6
      day_list[6] = 7

    if week_day == 0:
      day_list[1] = 1
      day_list[2] = 2
      day_list[3] = 3
      day_list[4] = 4
      day_list[5] = 5
      day_list[6] = 6

    if week_day == 1:
      day_list[2] = 1
      day_list[3] = 2
      day_list[4] = 3
      day_list[5] = 4
      day_list[6] = 5

    if week_day == 2:
      day_list[3] = 1
      day_list[4] = 2
      day_list[5] = 3
      day_list[6] = 4

    if week_day == 3:
      day_list[4] = 1
      day_list[5] = 2
      day_list[6] = 3

    if week_day == 4:
      day_list[5] = 1
      day_list[6] = 2

    if week_day == 5:
      day_list[6] = 1

    # 基準日指定
    start_day = day_list[6]

    # 2～5週目の日付設定
    for i in range(7, 37):
      day_list[i] = start_day + 1
      start_day += 1
      if start_day == day_end:
        break

    # 就業を上書き
    for i in range(37):
      if day_list[i] != '':

        # 工数データがあるか確認
        work_filter = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None), \
                                                         work_day2 = datetime.date(year, month, day_list[i]))

        # 工数データがある場合の処理
        if work_filter.count() != 0:

          # 工数データ取得
          work_get = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', None), \
                                                     work_day2 = datetime.date(year, month, day_list[i]))
          # ログイン者の情報取得
          member_obj = member.objects.get(employee_no = request.session.get('login_No', None))


          # 工数データをリストに解凍
          kosu_def = list(work_get.time_work)

          # 変数リセット
          kosu_total = 0

          # 工数の合計を計算
          for k in kosu_def:

            # 作業内容が入っている場合の処理
            if k != '#':

              # 工数の合計に5分加算
              kosu_total += 5


          # 工数入力OK_NGリセット
          judgement = False

          # 出勤、休出時、工数合計と残業に整合性がある場合の処理
          if (eval('request.POST["day{}"]'.format(i + 1)) == '出勤' or \
              eval('request.POST["day{}"]'.format(i + 1)) == 'シフト出') and \
              kosu_total - int(work_get.over_time) == 470:

            # 工数入力OK_NGをOKに切り替え
            judgement = True


          # 休出時、工数合計と残業に整合性がある場合の処理
          if eval('request.POST["day{}"]'.format(i + 1)) == '休出' and kosu_total == int(work_get.over_time):

            # 工数入力OK_NGをOKに切り替え
            judgement = True


          # 早退・遅刻時、工数合計と残業に整合性がある場合の処理
          if eval('request.POST["day{}"]'.format(i + 1)) == '早退・遅刻' and kosu_total != 0:

            # 工数入力OK_NGをOKに切り替え
            judgement = True


          # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Cで1直の場合の処理
          if (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
            member_obj.shop == 'A1' or member_obj.shop == 'A2') and \
              work_get.tyoku2 == '1':

            # 半前年休時、工数合計と残業に整合性がある場合の処理
            if eval('request.POST["day{}"]'.format(i + 1)) == '半前年休' and \
              kosu_total - int(work_get.over_time) == 230:

              # 工数入力OK_NGをOKに切り替え
              judgement = True

            # 半後年休時、工数合計と残業に整合性がある場合の処理
            if eval('request.POST["day{}"]'.format(i + 1)) == '半後年休' and \
              kosu_total - int(work_get.over_time) == 240:

              # 工数入力OK_NGをOKに切り替え
              judgement = True


          # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Cで2直の場合の処理
          if (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
            member_obj.shop == 'A1' or member_obj.shop == 'A2') and \
              work_get.tyoku2 == '2':

            # 半前年休時、工数合計と残業に整合性がある場合の処理
            if eval('request.POST["day{}"]'.format(i + 1)) == '半前年休' and \
              kosu_total - int(work_get.over_time) == 290:

              # 工数入力OK_NGをOKに切り替え
              judgement = True

            # 半後年休時、工数合計と残業に整合性がある場合の処理
            if eval('request.POST["day{}"]'.format(i + 1)) == '半後年休' and \
              kosu_total - int(work_get.over_time) == 180:

              # 工数入力OK_NGをOKに切り替え
              judgement = True


          # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Cで3直の場合の処理
          if (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
            member_obj.shop == 'A1' or member_obj.shop == 'A2') and \
              work_get.tyoku2 == '3':

            # 半前年休時、工数合計と残業に整合性がある場合の処理
            if eval('request.POST["day{}"]'.format(i + 1)) == '半前年休' and \
              kosu_total - int(work_get.over_time) == 230:

              # 工数入力OK_NGをOKに切り替え
              judgement = True

            # 半後年休時、工数合計と残業に整合性がある場合の処理
            if eval('request.POST["day{}"]'.format(i + 1)) == '半後年休' and \
              kosu_total - int(work_get.over_time) == 240:

              # 工数入力OK_NGをOKに切り替え
              judgement = True


          # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Bで1直の場合の処理
          if (member_obj.shop == 'P' or member_obj.shop == 'R' or \
            member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
              member_obj.shop == 'その他' or member_obj.shop == '組長以上') and \
              work_get.tyoku2 == '1':

            # 半前年休時、工数合計と残業に整合性がある場合の処理
            if eval('request.POST["day{}"]'.format(i + 1)) == '半前年休' and \
              kosu_total - int(work_get.over_time) == 220:

              # 工数入力OK_NGをOKに切り替え
              judgement = True

            # 半後年休時、工数合計と残業に整合性がある場合の処理
            if eval('request.POST["day{}"]'.format(i + 1)) == '半後年休' and \
              kosu_total - int(work_get.over_time) == 250:

              # 工数入力OK_NGをOKに切り替え
              judgement = True


          # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Bで2直の場合の処理
          if (member_obj.shop == 'P' or member_obj.shop == 'R' or \
            member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
              member_obj.shop == 'その他' or member_obj.shop == '組長以上') and \
              work_get.tyoku2 == '2':

            # 半前年休時、工数合計と残業に整合性がある場合の処理
            if eval('request.POST["day{}"]'.format(i + 1)) == '半前年休' and \
              kosu_total - int(work_get.over_time) == 230:

              # 工数入力OK_NGをOKに切り替え
              judgement = True

            # 半後年休時、工数合計と残業に整合性がある場合の処理
            if eval('request.POST["day{}"]'.format(i + 1)) == '半後年休' and \
              kosu_total - int(work_get.over_time) == 240:

              # 工数入力OK_NGをOKに切り替え
              judgement = True


          # ログイン者の登録ショップが三組三交替Ⅱ甲乙丙番Bで3直の場合の処理
          if (member_obj.shop == 'P' or member_obj.shop == 'R' or \
            member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
              member_obj.shop == 'その他' or member_obj.shop == '組長以上') and \
              work_get.tyoku2 == '3':

            # 半前年休時、工数合計と残業に整合性がある場合の処理
            if eval('request.POST["day{}"]'.format(i + 1)) == '半前年休' and \
              kosu_total - int(work_get.over_time) == 275:

              # 工数入力OK_NGをOKに切り替え
              judgement = True

            # 半後年休時、工数合計と残業に整合性がある場合の処理
            if eval('request.POST["day{}"]'.format(i + 1)) == '半後年休' and \
              kosu_total - int(work_get.over_time) == 195:

              # 工数入力OK_NGをOKに切り替え
              judgement = True


          # 常昼の場合の処理
          if work_get.tyoku2 == '4':

            # 半前年休時、工数合計と残業に整合性がある場合の処理
            if eval('request.POST["day{}"]'.format(i + 1)) == '半前年休' and \
              kosu_total - int(work_get.over_time) == 230:

              # 工数入力OK_NGをOKに切り替え
              judgement = True

            # 半後年休時、工数合計と残業に整合性がある場合の処理
            if eval('request.POST["day{}"]'.format(i + 1)) == '半後年休' and \
              kosu_total - int(work_get.over_time) == 240:

              # 工数入力OK_NGをOKに切り替え
              judgement = True


          # 就業を上書き
          Business_Time_graph.objects.update_or_create(employee_no3 = request.session.get('login_No', ''), \
            work_day2 = datetime.date(year, month, day_list[i]), \
              defaults = {'work_time' : eval('request.POST["day{}"]'.format(i + 1)), \
                          'judgement' : judgement})

          # 更新後の就業を取得
          record_del = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', ''), \
                                                       work_day2 = datetime.date(year, month, day_list[i]))

          # 更新後、就業が消されていて工数データが空であればレコードを消す
          if record_del.work_time == '' and record_del.over_time == 0 and \
            record_del.time_work == '#'*288:

            # レコード削除
            record_del.delete()

        # 工数データがなくPOSTした値が空欄でない場合の処理
        if eval('request.POST["day{}"]'.format(i + 1)) != '' and work_filter.count() == 0:

          # 従業員番号に該当するmemberインスタンスを取得
          member_instance = member.objects.get(employee_no = request.session.get('login_No', None))

          # 就業データ作成(空の工数データも入れる)
          Business_Time_graph.objects.update_or_create(employee_no3 = request.session.get('login_No', ''), \
            work_day2 = datetime.date(year, month, day_list[i]), \
              defaults = {'name' : member_instance, \
                          'work_time' : eval('request.POST["day{}"]'.format(i + 1)), \
                          'time_work' : '#'*288, \
                          'detail_work' : '$'*288, \
                          'over_time' : 0})


    # 勤務フォーム初期値リセット
    form_default_list = {}

    # 勤務フォーム初期値定義
    for i in range(37):

      # 日付リストに日付が入っている場合の処理
      if day_list[i] != '':

        # 対応する日付に工数データがあるか確認
        day_filter = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None), \
                                                        work_day2 = datetime.date(year, month, day_list[i]))

        # 対応する日付に工数データがある場合の処理
        if day_filter.count() != 0:

          # 対応する日付の工数データを取得
          day_get = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', None), \
                                                    work_day2 = datetime.date(year, month, day_list[i]))
          
          # 就業データを初期値リストに入れる
          form_default_list[('day{}'.format(i + 1))] = day_get.work_time

    # 勤務フォーム定義
    form = scheduleForm(form_default_list)



  # 入力工数表示リセット
  time_list1 = []
  time_list1 = []
  time_list2 = []
  time_list3 = []
  time_list4 = []
  time_list5 = []
  time_list6 = []
  time_list7 = []
  time_list8 = []
  time_list9 = []
  time_list10 = []
  time_list11 = []
  time_list12 = []
  time_list13 = []
  time_list14 = []
  time_list15 = []
  time_list16 = []
  time_list17 = []
  time_list18 = []
  time_list19 = []
  time_list20 = []
  time_list21 = []
  time_list22 = []
  time_list23 = []
  time_list24 = []
  time_list25 = []
  time_list26 = []
  time_list27 = []
  time_list28 = []
  time_list29 = []
  time_list30 = []
  time_list31 = []
  time_list32 = []
  time_list33 = []
  time_list34 = []
  time_list35 = []
  time_list36 = []
  time_list37 = []
  title_list = ['time_list1', 'time_list2', 'time_list3', 'time_list4', \
                'time_list5', 'time_list6', 'time_list7', 'time_list8', \
                'time_list9', 'time_list10', 'time_list11', 'time_list12', \
                'time_list13', 'time_list14', 'time_list15', 'time_list16', \
                'time_list17', 'time_list18', 'time_list19', 'time_list20', \
                'time_list21', 'time_list22', 'time_list23', 'time_list24', \
                'time_list25', 'time_list26', 'time_list27', 'time_list28', \
                'time_list29', 'time_list30', 'time_list31', 'time_list32', \
                'time_list33', 'time_list34', 'time_list35', 'time_list36', \
                'time_list37'
                ]
    
  # 工数入力データ取得
  for i, k in  enumerate(title_list):

    # 日付リストの該当要素が空でない場合の処理
    if day_list[i] != '':
      # ログイン者の工数データを該当日でフィルター 
      graph_data_filter = Business_Time_graph.objects.filter(employee_no3 = \
                          request.session.get('login_No', None), \
                          work_day2 = datetime.date(year, month, day_list[i]))

      # 工数データがない場合の処理
      if graph_data_filter.count() == 0:

        # カレンダー工数表示リストに空の値を入れる
        for p in range(4):
          eval(k).append('　')

      # 工数データがある場合の処理
      if graph_data_filter.count() != 0:

        # ログイン者の該当日の工数データ取得
        graph_data_get = Business_Time_graph.objects.get(employee_no3 = \
                        request.session.get('login_No', None), \
                          work_day2 =datetime.date(year, month, day_list[i]))
        # 作業内容リストに解凍
        data_list = list(graph_data_get.time_work)
       
        # 表示時間インデックスリセット
        start_index1 = 0
        end_index1 = 0
        start_index2 = 0
        end_index2 = 0
        start_index3 = 0
        end_index3 = 0
        start_index4 = 0
        end_index4 = 0
        loop_stop = 0

        # 工数データを文字に変換するため工数の開始、終了時間のインデックス取得
        for t in range(288):
          if data_list[t] != '#':
            start_index1 = t
            break
          if t == 287:
            loop_stop = 1

        if loop_stop == 0:
          for t in range(start_index1 + 1, 288):
            if data_list[t] == '#':
              end_index1 = t
              break
            if t == 287 and data_list[t] != '#':
              end_index1 = 288
              loop_stop = 1

          if loop_stop == 0:
            for t in range(end_index1 + 1, 288):
              if data_list[t] != '#':
                start_index2 = t
                break
              if t == 287:
                loop_stop = 1

            if loop_stop == 0:
              for t in range(start_index2 + 1, 288):
                if data_list[t] == '#':
                  end_index2 = t
                  break
                if t == 287 and data_list[t] != '#':
                  end_index2 = 288
                  loop_stop = 1

              if loop_stop == 0:
                for t in range(end_index2 + 1, 288):
                  if data_list[t] != '#':
                    start_index3 = t
                    break
                  if t == 287:
                    loop_stop = 1
    
                if loop_stop == 0:
                  for t in range(start_index3 + 1, 288):
                    if data_list[t] == '#':
                      end_index3 = t
                      break
                    if t == 287 and data_list[t] != '#':
                      end_index3 = 288
                      loop_stop = 1

                  if loop_stop == 0:
                    for t in range(end_index3 + 1, 288):
                      if data_list[t] != '#':
                        start_index4 = t
                        break
                      if t == 287:
                        loop_stop = 1
        
                    if loop_stop == 0:
                      for t in range(start_index4 + 1, 288):
                        if data_list[t] == '#':
                          end_index4 = t
                          break
                        if t == 287 and data_list[t] != '#':
                          end_index4 = 288

        # 取得したインデックスを時間表示に変換
        if start_index1 != 0 or end_index1 != 0:
          start_hour1 = start_index1//12
          start_min1 = (start_index1%12)*5
          end_hour1 =end_index1//12
          end_min1 = (end_index1%12)*5
          eval(k).append('{}:{}～{}:{}'.format(start_hour1, str(start_min1).zfill(2), \
                                              end_hour1, str(end_min1).zfill(2)))
        else:
          eval(k).append('　')
          
        if start_index2 != 0 or end_index2 != 0:
          start_hour2 = start_index2//12
          start_min2 = (start_index2%12)*5
          end_hour2 =end_index2//12
          end_min2 = (end_index2%12)*5
          eval(k).append('{}:{}～{}:{}'.format(start_hour2, str(start_min2).zfill(2), \
                                              end_hour2, str(end_min2).zfill(2)))
        else:
          eval(k).append('　')

        if start_index3 != 0 or end_index3 != 0:
          start_hour3 = start_index3//12
          start_min3 = (start_index3%12)*5
          end_hour3 =end_index3//12
          end_min3 = (end_index3%12)*5
          eval(k).append('{}:{}～{}:{}'.format(start_hour3, str(start_min3).zfill(2), \
                                              end_hour3, str(end_min3).zfill(2)))
        else:
          eval(k).append('　')
          
        if start_index4 != 0 or end_index4 != 0:
          start_hour4 = start_index4//12
          start_min4 = (start_index4%12)*5
          end_hour4 =end_index4//12
          end_min4 = (end_index4%12)*5
          eval(k).append('{}:{}～{}:{}'.format(start_hour4, str(start_min4).zfill(2), \
                                              end_hour4, str(end_min4).zfill(2)))
        else:
          eval(k).append('　')


  # 入力できる日付範囲を表示月に制限
  min_day = str(datetime.date(year, month, 1))
  max_day = str(month_day_end)

  # 日付の初期値指定
  if datetime.date(year, month, 1) <= today and today <= month_day_end:
    default_day = str(today)

  if datetime.date(year, month, 1) >= today:
    default_day = min_day

  if today >= month_day_end:
    default_day = max_day


  # 工数入力OKリスト作成
  OK_NG_list = []
  for ok_ng in range(37):
    if day_list[ok_ng] != '':
      OK_NG_filter = Business_Time_graph.objects.filter(employee_no3 = request.session.get('login_No', None), \
                                                       work_day2 = datetime.date(year, month, day_list[ok_ng]))
      if OK_NG_filter.count() != 0:
        
        OK_NG_obj = Business_Time_graph.objects.get(employee_no3 = request.session.get('login_No', None), \
                                                    work_day2 = datetime.date(year, month, day_list[ok_ng]))
        if OK_NG_obj.judgement == True:
          OK_NG_list.append(OK_NG_obj.judgement)
        else:
          OK_NG_list.append(False)
      else:
        OK_NG_list.append(False)
    else:
      OK_NG_list.append(False)



  # HTMLに渡す辞書
  library_m = {
    'title' : '勤務入力',
    'form' : form,
    'form2' : form2,
    'day_list' : day_list,
    'min_day' : min_day,
    'max_day' : max_day,
    'default_day' : default_day,
    'OK_NG_list' : OK_NG_list,
    'time_list1': time_list1,
    'time_list2': time_list2,
    'time_list3': time_list3,
    'time_list4': time_list4,
    'time_list5': time_list5,
    'time_list6': time_list6,
    'time_list7': time_list7,
    'time_list8': time_list8,
    'time_list9': time_list9,
    'time_list10': time_list10,
    'time_list11': time_list11,
    'time_list12': time_list12,
    'time_list13': time_list13,
    'time_list14': time_list14,
    'time_list15': time_list15,
    'time_list16': time_list16,
    'time_list17': time_list17,
    'time_list18': time_list18,
    'time_list19': time_list19,
    'time_list20': time_list20,
    'time_list21': time_list21,
    'time_list22': time_list22,
    'time_list23': time_list23,
    'time_list24': time_list24,
    'time_list25': time_list25,
    'time_list26': time_list26,
    'time_list27': time_list27,
    'time_list28': time_list28,
    'time_list29': time_list29,
    'time_list30': time_list30,
    'time_list31': time_list31,
    'time_list32': time_list32,
    'time_list33': time_list33,
    'time_list34': time_list34,
    'time_list35': time_list35,
    'time_list36': time_list36,
    'time_list37': time_list37, 
  }



  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/schedule.html', library_m)





#--------------------------------------------------------------------------------------------------------

