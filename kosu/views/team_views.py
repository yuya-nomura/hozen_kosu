from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from dateutil.relativedelta import relativedelta
import datetime
import itertools
from .. import forms
from ..models import member
from ..models import Business_Time_graph
from ..models import team_member
from ..models import kosu_division
from ..models import administrator_data
from ..forms import teamForm
from ..forms import team_kosuForm



#--------------------------------------------------------------------------------------------------------



# 班員設定画面定義
def team(request):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')
  
  # ログイン者の情報取得
  data = member.objects.get(employee_no = request.session.get('login_No', None))
  # ログイン者に権限がなければメインページに戻る
  if data.authority == False:
    return redirect(to = '/')
  
  # ログイン者の班員情報取得
  data2 = team_member.objects.filter(employee_no5 = request.session.get('login_No', None))


  # ログイン者の班員登録がない場合の処理
  if data2.count() == 0:

    # ログイン者が組長以上か確認
    if data.shop == '組長以上':
      # 組長以上なら人員登録のオブジェクトを全て取得
      member_obj = member.objects.all().order_by('employee_no')
    else:
      # そうでないならログイン者と同じショップの人員のオブジェクトを取得
      member_obj = member.objects.filter(shop = data.shop).order_by('employee_no')

    # 人員登録のある従業員番号の選択リスト作成
    choices_list = [('','')]
    for i in member_obj:
      choices_list.append((i.employee_no, str(i.name)))
    # フォーム初期値を用意
    employee_no_list = {'employee_no5' : request.session.get('login_No', None)}
    # フォームを用意
    form = teamForm(employee_no_list)
    # フォームの選択肢定義
    form.fields['member1'].choices = choices_list
    form.fields['member2'].choices = choices_list
    form.fields['member3'].choices = choices_list
    form.fields['member4'].choices = choices_list
    form.fields['member5'].choices = choices_list
    form.fields['member6'].choices = choices_list
    form.fields['member7'].choices = choices_list
    form.fields['member8'].choices = choices_list
    form.fields['member9'].choices = choices_list
    form.fields['member10'].choices = choices_list


    # POST時の処理
    if (request.method == 'POST'):
      # POST送信された値を変数に入れる
      member1 = request.POST['member1']
      member2 = request.POST['member2']
      member3 = request.POST['member3']
      member4 = request.POST['member4']
      member5 = request.POST['member5']
      member6 = request.POST['member6']
      member7 = request.POST['member7']
      member8 = request.POST['member8']
      member9 = request.POST['member9']
      member10 = request.POST['member10']

      # POSTされた値をモデルのそれぞれのフィールドに入れる
      new = team_member(employee_no5 = request.session.get('login_No', None), \
                        member1 = member1, member2 = member2, member3 = member3, \
                        member4 = member4, member5 = member5, member6 = member6, \
                        member7 = member7, member8 = member8, member9 = member9, \
                        member10 = member10)
      # 新しいレコードを作成しセーブする
      new.save()

      # 班員メイン画面をリダイレクトする
      return redirect(to = '/team_main')


  # ログイン者の班員登録がある場合の処理
  if data2.count() >= 1:
    # ログイン者の班員登録のオブジェクトを取得
    obj = team_member.objects.get(employee_no5 = request.session.get('login_No', None))

    # ログイン者が組長以上か確認
    if data.shop == '組長以上':
      # 組長以上なら人員登録のオブジェクトを全て取得
      member_obj = member.objects.all().order_by('employee_no')
    else:
      # そうでないならログイン者と同じショップの人員のオブジェクトを取得
      member_obj = member.objects.filter(shop = data.shop).order_by('employee_no')

    # 人員登録のある従業員番号の選択リスト作成
    choices_list = [('','')]
    for i in member_obj:
      choices_list.append((i.employee_no, str(i.name)))
    # フォーム初期値を用意
    form_list = {'employee_no5' : request.session.get('login_No', None), \
                 'member1' : obj.member1, \
                 'member2' : obj.member2, \
                 'member3' : obj.member3, \
                 'member4' : obj.member4, \
                 'member5' : obj.member5, \
                 'member6' : obj.member6, \
                 'member7' : obj.member7, \
                 'member8' : obj.member8, \
                 'member9' : obj.member9, \
                 'member10' : obj.member10}
    # フォームを用意
    form = teamForm(form_list)
    # フォームの選択肢定義
    form.fields['member1'].choices = choices_list
    form.fields['member2'].choices = choices_list
    form.fields['member3'].choices = choices_list
    form.fields['member4'].choices = choices_list
    form.fields['member5'].choices = choices_list
    form.fields['member6'].choices = choices_list
    form.fields['member7'].choices = choices_list
    form.fields['member8'].choices = choices_list
    form.fields['member9'].choices = choices_list
    form.fields['member10'].choices = choices_list

    # POST時の処理
    if (request.method == 'POST'):

      # 指定IDのレコードにPOST送信された値を上書きする
      team_member.objects.update_or_create(employee_no5 = request.session.get('login_No', None), \
          defaults = {'member1' : request.POST['member1'], 'member2' : request.POST['member2'], \
                      'member3' : request.POST['member3'], 'member4' : request.POST['member4'], \
                      'member5' : request.POST['member5'], 'member6' : request.POST['member6'], \
                      'member7' : request.POST['member7'], 'member8' : request.POST['member8'], \
                      'member9' : request.POST['member9'], 'member10' : request.POST['member10']})

      # 班員メイン画面をリダイレクトする
      return redirect(to = '/team_main')

  # HTMLに渡す辞書
  library_m = {
    'title' : '班員設定',
    'data' : data,
    'form' : form,
    }

  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/team.html', library_m)



#--------------------------------------------------------------------------------------------------------



# 班員工数グラフ確認画面定義
def team_graph(request):
  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')
  
  # ログイン者の情報取得
  data = member.objects.get(employee_no = request.session.get('login_No', None))
  # ログイン者に権限がなければメインページに戻る
  if data.authority == False:
    return redirect(to = '/')

  # ログイン者の班員登録情報取得
  data = team_member.objects.filter(employee_no5 = request.session.get('login_No', None))
  # 班員登録がなければメインページに戻る
  if data.count() == 0:
    return redirect(to = '/')


  # GET時の処理
  if (request.method == 'GET'):
    # 今日の日時を変数に格納
    dt = datetime.datetime.today()
    # 日付のみを変数に入れる
    kosu_today = dt.date()
    # フォーム初期値設定
    default_form = {'team_day' : kosu_today}
    # GET時のフォーム状態設定
    form = team_kosuForm(default_form)


  # POST時の処理
  if (request.method == 'POST'):
    
    # 就業日検索が空で検索された場合の処理
    if request.POST['team_day'] == '':
      # エラーメッセージ出力
      messages.error(request, '日付を指定してから検索して下さい。ERROR27')
      # このページをリダイレクト
      return redirect(to = '/team_graph')
    
    # POSTされた日付を変数に入れる
    kosu_today = request.POST['team_day']
    # GET時のフォーム状態設定
    form = team_kosuForm(request.POST)

  # ログイン者の班員データ取得
  obj = team_member.objects.get(employee_no5 = request.session.get('login_No', None))
  # 班員データに空があった場合0を定義
  for i in range(1, 11):
    if eval('obj.member{}'.format(i)) == '':
      exec('obj_member{}=0'.format(i))
    else:
      exec('obj_member{}=obj.member{}'.format(i, i))
    
  # 班員数、班員の名前リスト取得
  n = 0
  name_list = []
  for i in range(1, 11):
    member_filter =  member.objects.filter(employee_no = eval('obj_member{}'.format(i)))
    if member_filter.count() != 0:
      member_data = member.objects.get(employee_no = eval('obj_member{}'.format(i)))
      name_list.append(member_data.name)
      n = i
    else:
      name_list.append('')

  
  # グラフデータ作成関数定義
  def graph_function(employee_no_data):
    # グラフデータ確認
    graph_filter = Business_Time_graph.objects.filter(employee_no3 = employee_no_data, work_day2 = kosu_today)

    # 指定した人員データ取得
    member_obj = member.objects.get(employee_no = employee_no_data)

    # グラフデータ無い場合の処理
    if graph_filter.count() == 0:
      # 0が288個入ったリスト作成
      graph_list = list(itertools.repeat(0,288))

      # グラフラベルデータ
      graph_item = []
      for i in range(24):
          for k in range(0, 60, 5):
              t = k
              if k == 0:
                t = '00'
              if k == 5:
                t = '05'
              graph_item.append('{}:{}'.format(i, t))

    else:
      # グラフデータ取得
      graph_data = Business_Time_graph.objects.get(employee_no3 = employee_no_data, work_day2 = kosu_today)
      graph_list = list(graph_data.time_work)

      # グラフラベルデータ
      graph_item = []
      for i in range(24):
          for k in range(0, 60, 5):
              if k == 0:
                t = '00'
              if k == 5:
                t = '05'
              else:
                t = k
              graph_item.append('{}:{}'.format(i, t))

      # グラフデータリスト内の各文字を数値に変更
      str_list = ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', \
                    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', \
                      'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                          'q', 'r', 's', 't', 'u', 'v', 'w', 'x',]

      for i in range(288):
        for k, m in enumerate(str_list):
          if graph_list[i]  == m:
            graph_list[i] = k
            break

      # 工数が入力されていない部分を切り捨てデータを見やすく
      if graph_data.tyoku2 != '3':
        for i in range(288):
          if graph_list[i] != 0:
            if i == 0:
              graph_start_index = i
            else:
              graph_start_index = i-1
              break
        
        for i in range(1, 289):
          if graph_list[-i] != 0:
            if i == 1:
              graph_end_index = 289 - i
            else:
              graph_end_index = 290 - i
              break

        if graph_data.tyoku2 == '1':
          if graph_end_index <= 184:
            graph_end_index = 184

        if graph_data.tyoku2 == '2' and (member_obj.shop == 'W1' or member_obj.shop == 'W2' or \
                                        member_obj.shop == 'A1' or member_obj.shop == 'A2'):
          if graph_end_index <= 240:
            graph_end_index = 240

        if graph_data.tyoku2 == '2' and (member_obj.shop == 'P' or member_obj.shop == 'R' or \
                                        member_obj.shop == 'T1' or member_obj.shop == 'T2' or \
                                          member_obj.shop == 'その他' or member_obj.shop == '組長以上'):
          if graph_end_index <= 270:
            graph_end_index = 270

        if graph_data.tyoku2 == '4':
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
              graph_start_index = i-1
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

    return graph_list, graph_item
  

  graph_list1 = []
  graph_item1 = []
  graph_list2 = []
  graph_item2 = []
  graph_list3 = []
  graph_item3 = []
  graph_list4 = []
  graph_item4 = []
  graph_list5 = []
  graph_item5 = []
  graph_list6 = []
  graph_item6 = []
  graph_list7 = []
  graph_item7 = []
  graph_list8 = []
  graph_item8 = []
  graph_list9 = []
  graph_item9 = []
  graph_list10 = []
  graph_item10 = []
  
  if n >= 1 and obj.member1 != '':
    graph_list1, graph_item1 = graph_function(obj.member1)
  if n >= 2 and obj.member2 != '':
    graph_list2, graph_item2 = graph_function(obj.member2)
  if n >= 3 and obj.member3 != '':
    graph_list3, graph_item3 = graph_function(obj.member3)
  if n >= 4 and obj.member4 != '':
    graph_list4, graph_item4 = graph_function(obj.member4)
  if n >= 5 and obj.member5 != '':
    graph_list5, graph_item5 = graph_function(obj.member5)
  if n >= 6 and obj.member6 != '':
    graph_list6, graph_item6 = graph_function(obj.member6)
  if n >= 7 and obj.member7 != '':
    graph_list7, graph_item7 = graph_function(obj.member7)
  if n >= 8 and obj.member8 != '':
    graph_list8, graph_item8 = graph_function(obj.member8)
  if n >= 9 and obj.member9 != '':
    graph_list9, graph_item9 = graph_function(obj.member9)
  if n >= 10 and obj.member10 != '':
    graph_list10, graph_item10 = graph_function(obj.member10)

  # 現在使用している工数区分のオブジェクトを取得
  kosu_obj = kosu_division.objects.get(kosu_name = request.session.get('input_def', None))
  # 工数区分登録カウンターリセット
  def_n = 0
  # 工数区分登録数カウント
  for i in range(1, 51):
    if eval('kosu_obj.kosu_title_{}'.format(i)) != '':
      def_n = i

  # 工数区分の選択リスト作成
  graph_kosu_list = []
  for i in range(1, def_n + 1):
    graph_kosu_list.append(eval('kosu_obj.kosu_title_{}'.format(i)))


  # HTMLに渡す辞書
  library_m = {
    'title' : '班員工数グラフ',
    'form' : form,
    'name_list' : name_list,
    'n' : n,
    'graph_kosu_list' : graph_kosu_list,
    'def_n' : def_n,
    'graph_list1' : graph_list1,
    'graph_item1' : graph_item1,
    'graph_list2' : graph_list2,
    'graph_item2' : graph_item2,
    'graph_list3' : graph_list3,
    'graph_item3' : graph_item3,
    'graph_list4' : graph_list4,
    'graph_item4' : graph_item4,
    'graph_list5' : graph_list5,
    'graph_item5' : graph_item5,
    'graph_list6' : graph_list6,
    'graph_item6' : graph_item6,
    'graph_list7' : graph_list7,
    'graph_item7' : graph_item7,
    'graph_list8' : graph_list8,
    'graph_item8' : graph_item8,
    'graph_list9' : graph_list9,
    'graph_item9' : graph_item9,
    'graph_list10' : graph_list10,
    'graph_item10' : graph_item10,
    }
 
  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/team_graph.html', library_m)



#--------------------------------------------------------------------------------------------------------



# 班員工数確認画面定義
def team_kosu(request, num):

  # 今日の日時を変数に格納
  dt = datetime.datetime.today()
  # 日付のみを変数に入れる
  kosu_today = dt.date()

  # フォームの初期値に定義する辞書作成
  if request.session.get('find_employee_no', '') != '' or \
    request.session.get('find_team_day', '') != '':

    start_list = {'team_day' : request.session.get('find_team_day', ''), \
                  'employee_no6' : request.session.get('find_employee_no', '')}
    
  else:

    start_list = {'team_day' : kosu_today}


  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')
  

  # ログイン者の情報取得
  data = member.objects.get(employee_no = request.session.get('login_No', None))
  # ログイン者に権限がなければメインページに戻る
  if data.authority == False:
    return redirect(to = '/')


  # ログイン者の班員登録情報取得
  data3 = team_member.objects.filter(employee_no5 = request.session.get('login_No', None))
  # 班員登録がなければメインページに戻る
  if data3.count() == 0:
    return redirect(to = '/')
  

  # フォームの選択肢に使用するログイン者の班員設定のオブジェクト取得
  form_choices = team_member.objects.get(employee_no5 = request.session.get('login_No', None))

  # 選択肢の表示数検出
  for i in range(1, 11):

    # 班員の登録がある場合の処理
    if eval('form_choices.member{}'.format(i)) != '':

      # インデックス記録
      n = i

  # 班員リストリセット
  choices_list = [['','']]
  employee_no_list = []
  name_list =[]

  # 班員リスト作成
  for i in range(n):

    # 班員の選択肢リセット
    choices_element = []

    # 班員の従業員番号リスト作成
    employee_no_list.append(eval('form_choices.member{}'.format(i + 1)))

    # 班員の従業員番号が人員データにあるか確認
    obj_filter = member.objects.filter(employee_no__contains = employee_no_list[i])
    # 班員の従業員番号が人員データにある場合の処理
    if obj_filter.count() == 1:

      # 班員の従業員番号から人員データ取得
      obj_get = member.objects.get(employee_no = employee_no_list[i])
      # 班員の名前リスト作成
      name_list.append(obj_get.name)

    # 班員の従業員番号が人員データにない場合の処理
    else:

      # 班員の名前リストに空を入れる
      name_list.append('')

    # 従業員番号と名前の選択肢作成
    choices_element = choices_element + [employee_no_list[i], name_list[i]]
    # 選択肢を選択肢リストに追加
    choices_list.append(choices_element)


  # 設定データ取得
  page_num = administrator_data.objects.order_by("id").last()


  # POST時の処理
  if (request.method == 'POST'):

    # POST送信時のフォームの状態(POSTした値は入ったまま)
    form = team_kosuForm(request.POST)

    # フォームの選択肢定義
    form.fields['employee_no6'].choices = choices_list

    # POSTした値を変数に入れる
    find = request.POST['employee_no6']
    find2 = request.POST['team_day']
    request.session['find_employee_no'] = find
    request.session['find_team_day'] = find2

    # 就業日と班員の従業員番号でフィルターをかけて一致したものをHTML表示用変数に入れる
    data2 = Business_Time_graph.objects.filter(employee_no3__icontains = find, \
      work_day__contains = find2).order_by('work_day', 'start_hour', 'start_min').reverse()

    page = Paginator(data2, page_num.menu_row)

  # POSTしていない時の処理
  else:

    # POST送信していない時のフォームの状態(今日の日付が入ったフォーム)
    form = team_kosuForm(start_list)

    # フォームの選択肢定義
    form.fields['employee_no6'].choices = choices_list

    # 班員の従業員番号でフィルターをかけて一致したものをHTML表示用変数に入れる
    data2 = Business_Time_graph.objects.filter(Q(employee_no3__icontains = form_choices.member1)|\
      Q(employee_no3__icontains = form_choices.member2)|\
      Q(employee_no3__icontains = form_choices.member3)|\
      Q(employee_no3__icontains = form_choices.member4)|\
      Q(employee_no3__icontains = form_choices.member5)|\
      Q(employee_no3__icontains = form_choices.member6)|\
      Q(employee_no3__icontains = form_choices.member7)|\
      Q(employee_no3__icontains = form_choices.member8)|\
      Q(employee_no3__icontains = form_choices.member9)|\
      Q(employee_no3__icontains = form_choices.member10), \
      employee_no3__icontains = request.session.get('find_employee_no', ''), \
      work_day2__contains = request.session.get('find_team_day', ''))\
      .order_by('work_day2').reverse()
    
    page = Paginator(data2, page_num.menu_row)


  # HTMLに渡す辞書
  library_m = {
    'title' : '班員工数確認',
    'data' : data,
    'data2' : page.get_page(num),
    'form' : form,
    'num' : num,
    }

  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/team_kosu.html', library_m)



#--------------------------------------------------------------------------------------------------------



# 班員工数入力詳細画面定義
def team_detail(request, num):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')
  
  # ログイン者の情報取得
  data = member.objects.get(employee_no = request.session.get('login_No', None))
  # ログイン者に権限がなければメインページに戻る
  if data.authority == False:
    return redirect(to = '/')

  # ログイン者の班員登録情報取得
  data3 = team_member.objects.filter(employee_no5 = request.session.get('login_No', None))
  # 班員登録がなければメインページに戻る
  if data3.count() == 0:
    return redirect(to = '/')


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
    'name' : obj_get.name,
    }

  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/team_detail.html', library_m)



#--------------------------------------------------------------------------------------------------------



# 班員工数入力状況一覧画面定義
def team_calendar(request):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')
  
  # ログイン者の情報取得
  data = member.objects.get(employee_no = request.session.get('login_No', None))
  # ログイン者に権限がなければメインページに戻る
  if data.authority == False:
    return redirect(to = '/')

  # ログイン者の班員登録情報取得
  data3 = team_member.objects.filter(employee_no5 = request.session.get('login_No', None))
  # 班員登録がなければメインページに戻る
  if data3.count() == 0:
    return redirect(to = '/')


  # 曜日指定フォーム初期値定義
  week_default = {'Sunday_check' : True, \
                  'Monday_check' : True, \
                  'Tuesday_check' : True, \
                  'Wednesday_check' : True, \
                  'Thursday_check' : True, \
                  'Friday_check' : True, \
                  'Satuday_check' : True}

  # メンバー指定フォーム初期値定義
  member_default = {'member1_check' : True, \
                    'member2_check' : True, \
                    'member3_check' : True, \
                    'member4_check' : True, \
                    'member5_check' : True, \
                    'member6_check' : True, \
                    'member7_check' : True, \
                    'member8_check' : True, \
                    'member9_check' : True, \
                    'member10_check' : True}



  # 日付指定時の処理
  if "display_day" in request.POST:

    # POSTされた値を日付に設定
    today = datetime.datetime.strptime(request.POST['work_day'], '%Y-%m-%d')

    # POSTされた値をセッションに登録
    request.session['display_day'] = request.POST['work_day']


  # POSTしていない時の処理
  else:

    # セッションに表示日の指定がない場合の処理
    if request.session.get('display_day', None) == None:

      # 今日の日付取得
      today = datetime.date.today()

      # 取得した値をセッションに登録
      request.session['display_day'] = str(today)[0 : 10]
      today = datetime.datetime.strptime(request.session.get('display_day', None), '%Y-%m-%d')

    # セッションに表示日の指定がある場合の処理
    else:

      # 表示日にセッションの値を入れる
      today = datetime.datetime.strptime(request.session.get('display_day', None), '%Y-%m-%d')



  # 前週指定時の処理
  if "back_week" in request.POST:

    # 曜日取得
    week_day_back = today.weekday()


    # 曜日が日曜の場合の処理
    if week_day_back == 6:

      # 1日前の日付を指定日に入れる
      today = today - datetime.timedelta(days=1)


    # 曜日が月曜の場合の処理
    if week_day_back == 0:

      # 2日前の日付を指定日に入れる
      today = today - datetime.timedelta(days=2)


    # 曜日が火曜の場合の処理
    if week_day_back == 1:

      # 3日前の日付を指定日に入れる
      today = today - datetime.timedelta(days=3)


    # 曜日が水曜の場合の処理
    if week_day_back == 2:

      # 4日前の日付を指定日に入れる
      today = today - datetime.timedelta(days=4)


    # 曜日が木曜の場合の処理
    if week_day_back == 3:

      # 5日前の日付を指定日に入れる
      today = today - datetime.timedelta(days=5)


    # 曜日が金曜の場合の処理
    if week_day_back == 4:

      # 6日前の日付を指定日に入れる
      today = today - datetime.timedelta(days=6)


    # 曜日が土曜の場合の処理
    if week_day_back == 5:

      # 7日前の日付を指定日に入れる
      today = today - datetime.timedelta(days=7)


    # 前の週が月をまたぐ場合の処理
    if today.month != datetime.datetime.strptime(request.session.get('display_day', None), '%Y-%m-%d').month:

      # 前月の最終日取得
      today = datetime.datetime(today.year, today.month, 1) + relativedelta(months=1) - relativedelta(days=1) 


    # 取得した値をセッションに登録
    request.session['display_day'] = str(today)[0:10]



  # 次週指定時の処理
  if "next_week" in request.POST:

    # 曜日取得
    week_day_back = today.weekday()


    # 曜日が日曜の場合の処理
    if week_day_back == 6:

      # 7日後の日付を指定日に入れる
      today = today + datetime.timedelta(days=7)


    # 曜日が月曜の場合の処理
    if week_day_back == 0:

      # 6日後の日付を指定日に入れる
      today = today + datetime.timedelta(days=6)


    # 曜日が火曜の場合の処理
    if week_day_back == 1:

      # 5日後の日付を指定日に入れる
      today = today + datetime.timedelta(days=5)


    # 曜日が水曜の場合の処理
    if week_day_back == 2:

      # 4日後の日付を指定日に入れる
      today = today + datetime.timedelta(days=4)


    # 曜日が木曜の場合の処理
    if week_day_back == 3:

      # 3日後の日付を指定日に入れる
      today = today + datetime.timedelta(days=3)


    # 曜日が金曜の場合の処理
    if week_day_back == 4:

      # 2日後の日付を指定日に入れる
      today = today + datetime.timedelta(days=2)


    # 曜日が土曜の場合の処理
    if week_day_back == 5:

      # 1日後の日付を指定日に入れる
      today = today + datetime.timedelta(days=1)


    # 次の週が月をまたぐ場合の処理
    if today.month != datetime.datetime.strptime(request.session.get('display_day', None), '%Y-%m-%d').month:

      # 次月の初日取得
      today = datetime.datetime(today.year, today.month, 1)


    # 取得した値をセッションに登録
    request.session['display_day'] = str(today)[0:10]



  # 表示日の月を取得
  month = today.month

  # フォームの初期値定義
  default_day = str(today)

  # 曜日取得
  week_day = today.weekday()

  # 日付リストリセット
  day_list = []


  # 曜日が日曜の場合の処理
  if week_day == 6:

    # 日付リスト作成
    for d in range(7):

      # リストに日付追加
      day_list.append(today + datetime.timedelta(days = d))


  # 曜日が月曜の場合の処理
  if week_day == 0:

    # 日付リスト作成
    for d in range(7):

      # 設定日より前の日付の処理
      if d == 0:

        # リストに日付追加
        day_list.append(today - datetime.timedelta(days = 1 - d))

      # 設定日以降の日付の処理  
      else:

        # リストに日付追加
        day_list.append(today + datetime.timedelta(days = d - 1))


  # 曜日が火曜の場合の処理
  if week_day == 1:

    # 日付リスト作成
    for d in range(7):

      # 設定日より前の日付の処理
      if d >= 1:

        # リストに日付追加
        day_list.append(today - datetime.timedelta(days = 2 - d))

      # 設定日以降の日付の処理
      else:

        # リストに日付追加
        day_list.append(today + datetime.timedelta(days = d - 2))


  # 曜日が水曜の場合の処理
  if week_day == 2:

    # 日付リスト作成
    for d in range(7):

      # 設定日より前の日付の処理
      if d >= 2:

        # リストに日付追加
        day_list.append(today - datetime.timedelta(days = 3 - d))

      # 設定日以降の日付の処理
      else:

        # リストに日付追加
        day_list.append(today + datetime.timedelta(days = d - 3))


  # 曜日が木曜の場合の処理
  if week_day == 3:

    # 日付リスト作成
    for d in range(7):

      # 設定日より前の日付の処理
      if d >= 3:

        # リストに日付追加
        day_list.append(today - datetime.timedelta(days = 4 - d))

      # 設定日以降の日付の処理
      else:

        # リストに日付追加
        day_list.append(today + datetime.timedelta(days = d - 4))


  # 曜日が金曜の場合の処理
  if week_day == 4:

    # 日付リスト作成
    for d in range(7):

      # 設定日より前の日付の処理
      if d >= 4:

        # リストに日付追加
        day_list.append(today - datetime.timedelta(days = 5 - d))

      # 設定日以降の日付の処理
      else:

        # リストに日付追加
        day_list.append(today + datetime.timedelta(days = d - 5))


  # 曜日が土曜の場合の処理
  if week_day == 5:

    # 日付リスト作成
    for d in range(7):

      # 設定日より前の日付の処理
      if d >= 5:

        # リストに日付追加
        day_list.append(today - datetime.timedelta(days = 6 - d))

      # 設定日以降の日付の処理
      else:

        # リストに日付追加
        day_list.append(today + datetime.timedelta(days = d - 6))


  # 日付リスト整形
  for ind, dd in enumerate(day_list):

    # 指定月と表示月が違う要素の処理
    if month != dd.month:

      # 要素を空にする
      day_list[ind] = ''


  # ログイン者の班員取得
  obj_get = team_member.objects.get(employee_no5 = request.session.get('login_No', None))


  # 班員1人目の従業員番号の人員がいるか確認
  member1_obj_filter = member.objects.filter(employee_no__contains = obj_get.member1)
  # 班員1人目の従業員番号の人員がいる場合の処理
  if member1_obj_filter.count() == 1:

     # 班員1人目の名前取得
    member1_obj_get = member.objects.get(employee_no = obj_get.member1)

  # 班員1人目の従業員番号の人員がいない場合の処理
  else:

    # 班員1人目の名前に空を入れる
    member1_obj_get = ''


  # 班員2人目の従業員番号の人員がいるか確認
  member2_obj_filter = member.objects.filter(employee_no__contains = obj_get.member2)
  # 班員2人目の従業員番号の人員がいる場合の処理
  if member2_obj_filter.count() == 1:

    # 班員2人目の名前取得
    member2_obj_get = member.objects.get(employee_no = obj_get.member2)

  # 班員2人目の従業員番号の人員がいない場合の処理
  else:

    # 班員2人目の名前に空を入れる
    member2_obj_get = ''


  # 班員3人目の従業員番号の人員がいるか確認
  member3_obj_filter = member.objects.filter(employee_no__contains = obj_get.member3)
  # 班員3人目の従業員番号の人員がいる場合の処理
  if member3_obj_filter.count() == 1:

    # 班員3人目の名前取得
    member3_obj_get = member.objects.get(employee_no = obj_get.member3)

  # 班員3人目の従業員番号の人員がいない場合の処理
  else:

    # 班員3人目の名前に空を入れる
    member3_obj_get = ''


  # 班員4人目の従業員番号の人員がいるか確認
  member4_obj_filter = member.objects.filter(employee_no__contains = obj_get.member4)
  # 班員4人目の従業員番号の人員がいる場合の処理
  if member4_obj_filter.count() == 1:

    # 班員4人目の名前取得
    member4_obj_get = member.objects.get(employee_no = obj_get.member4)

  # 班員4人目の従業員番号の人員がいない場合の処理
  else:

    # 班員4人目の名前に空を入れる
    member4_obj_get = ''


  # 班員5人目の従業員番号の人員がいるか確認
  member5_obj_filter = member.objects.filter(employee_no__contains = obj_get.member5)
  # 班員5人目の従業員番号の人員がいる場合の処理
  if member5_obj_filter.count() == 1:

    # 班員5人目の名前取得
    member5_obj_get = member.objects.get(employee_no = obj_get.member5)

  # 班員5人目の従業員番号の人員がいない場合の処理
  else:

    # 班員5人目の名前に空を入れる
    member5_obj_get = ''


  # 班員6人目の従業員番号の人員がいるか確認
  member6_obj_filter = member.objects.filter(employee_no__contains = obj_get.member6)
  # 班員6人目の従業員番号の人員がいる場合の処理
  if member6_obj_filter.count() == 1:

    # 班員6人目の名前取得
    member6_obj_get = member.objects.get(employee_no = obj_get.member6)

  # 班員6人目の従業員番号の人員がいない場合の処理
  else:

    # 班員6人目の名前に空を入れる
    member6_obj_get = ''


  # 班員7人目の従業員番号の人員がいるか確認
  member7_obj_filter = member.objects.filter(employee_no__contains = obj_get.member7)
  # 班員7人目の従業員番号の人員がいる場合の処理
  if member7_obj_filter.count() == 1:

    # 班員7人目の名前取得
    member7_obj_get = member.objects.get(employee_no = obj_get.member7)

  # 班員7人目の従業員番号の人員がいない場合の処理
  else:

    # 班員7人目の名前に空を入れる
    member7_obj_get = ''


  # 班員8人目の従業員番号の人員がいるか確認
  member8_obj_filter = member.objects.filter(employee_no__contains = obj_get.member8)
  # 班員8人目の従業員番号の人員がいる場合の処理
  if member8_obj_filter.count() == 1:

    # 班員8人目の名前取得
    member8_obj_get = member.objects.get(employee_no = obj_get.member8)

  # 班員8人目の従業員番号の人員がいない場合の処理
  else:

    # 班員8人目の名前に空を入れる
    member8_obj_get = ''


  # 班員9人目の従業員番号の人員がいるか確認
  member9_obj_filter = member.objects.filter(employee_no__contains = obj_get.member9)
  # 班員9人目の従業員番号の人員がいる場合の処理
  if member9_obj_filter.count() == 1:

    # 班員9人目の名前取得
    member9_obj_get = member.objects.get(employee_no = obj_get.member9)

  # 班員9人目の従業員番号の人員がいない場合の処理
  else:

    # 班員9人目の名前に空を入れる
    member9_obj_get = ''


  # 班員10人目の従業員番号の人員がいるか確認
  member10_obj_filter = member.objects.filter(employee_no__contains = obj_get.member10)
  # 班員10人目の従業員番号の人員がいる場合の処理
  if member10_obj_filter.count() == 1:

    # 班員10人目の名前取得
    member10_obj_get = member.objects.get(employee_no = obj_get.member10)

  # 班員10人目の従業員番号の人員がいない場合の処理
  else:

    # 班員10人目の名前に空を入れる
    member10_obj_get = ''


  # 取得した班員の名前をHTML送信用の変数に入れる
  member_name1 = member1_obj_get
  member_name2 = member2_obj_get
  member_name3 = member3_obj_get
  member_name4 = member4_obj_get
  member_name5 = member5_obj_get
  member_name6 = member6_obj_get
  member_name7 = member7_obj_get
  member_name8 = member8_obj_get
  member_name9 = member9_obj_get
  member_name10 = member10_obj_get


  # 班員(従業員番号)リストリセット
  member_list = []

  # 選択肢の表示数検出&班員(従業員番号)リスト作成
  for i in range(1, 11):

    # 班員(従業員番号)リストに班員追加
    member_list.append(eval('obj_get.member{}'.format(i)))

    # 班員の登録がある場合の処理
    if eval('obj_get.member{}'.format(i)) != '':

      # インデックス記録
      member_num = i


  # 就業リストリセット
  work_list1 = []
  work_list2 = []
  work_list3 = []
  work_list4 = []
  work_list5 = []
  work_list6 = []
  work_list7 = []
  work_list8 = []
  work_list9 = []
  work_list10 = []

  # 残業リストリセット
  over_time_list1 = []
  over_time_list2 = []
  over_time_list3 = []
  over_time_list4 = []
  over_time_list5 = []
  over_time_list6 = []
  over_time_list7 = []
  over_time_list8 = []
  over_time_list9 = []
  over_time_list10 = []

  # 工数入力リストリセット
  kosu_list1 = []
  kosu_list2 = []
  kosu_list3 = []
  kosu_list4 = []
  kosu_list5 = []
  kosu_list6 = []
  kosu_list7 = []
  kosu_list8 = []
  kosu_list9 = []
  kosu_list10 = []

  # 工数入力OK_NGリストリセット
  ok_ng_list1 = [False, False, False, False, False, False, False]
  ok_ng_list2 = [False, False, False, False, False, False, False]
  ok_ng_list3 = [False, False, False, False, False, False, False]
  ok_ng_list4 = [False, False, False, False, False, False, False]
  ok_ng_list5 = [False, False, False, False, False, False, False]
  ok_ng_list6 = [False, False, False, False, False, False, False]
  ok_ng_list7 = [False, False, False, False, False, False, False]
  ok_ng_list8 = [False, False, False, False, False, False, False]
  ok_ng_list9 = [False, False, False, False, False, False, False]
  ok_ng_list10 = [False, False, False, False, False, False, False]



  # 班員(従業員番号)リストごとに就業、残業、工数入力OK_NGリスト作成
  for ind, m in enumerate(member_list):

    # 班員登録がある場合の処理
    if m != '':

      # 日付リストを使用し日付ごとの就業、残業取得しリスト作成
      for ind2, day in enumerate(day_list):
        kosu_list = []

        # 日付リストが空でない場合の処理
        if day != '':

          # 指定日に工数データあるか確認
          member_obj_filter =Business_Time_graph.objects.filter(employee_no3 = m, work_day2 = day)

          # 指定日に工数データがある場合の処理
          if member_obj_filter.count() != 0:

            # 指定日の工数データ取得
            member_obj_get =Business_Time_graph.objects.get(employee_no3 = m, work_day2 = day)

            # 就業、残業リストに工数データから就業、残業、工数入力OK_NG追加
            exec('work_list{}.append(member_obj_get.work_time)'.format(ind + 1))
            exec('over_time_list{}.append(member_obj_get.over_time)'.format(ind + 1))
            exec('ok_ng_list{}[{}] = member_obj_get.judgement'.format(ind + 1, ind2))

            # 工数データが空の場合の処理
            if member_obj_get.time_work == '#'*288:

              # 空の工数入力リストを作成
              for k in range(4):

                # 工数入力リストに空を入れる
                kosu_list.append('')

            # 工数データが空でない場合の処理
            else:

              # 作業内容リストに解凍
              data_list = list(member_obj_get.time_work)

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
                kosu_list.append('{}:{}～{}:{}'.format(start_hour1, str(start_min1).zfill(2), \
                                                    end_hour1, str(end_min1).zfill(2)))
              else:
                kosu_list.append('')
                
              if start_index2 != 0 or end_index2 != 0:
                start_hour2 = start_index2//12
                start_min2 = (start_index2%12)*5
                end_hour2 =end_index2//12
                end_min2 = (end_index2%12)*5
                kosu_list.append('{}:{}～{}:{}'.format(start_hour2, str(start_min2).zfill(2), \
                                                    end_hour2, str(end_min2).zfill(2)))
              else:
                kosu_list.append('')

              if start_index3 != 0 or end_index3 != 0:
                start_hour3 = start_index3//12
                start_min3 = (start_index3%12)*5
                end_hour3 =end_index3//12
                end_min3 = (end_index3%12)*5
                kosu_list.append('{}:{}～{}:{}'.format(start_hour3, str(start_min3).zfill(2), \
                                                    end_hour3, str(end_min3).zfill(2)))
              else:
                kosu_list.append('')
                
              if start_index4 != 0 or end_index4 != 0:
                start_hour4 = start_index4//12
                start_min4 = (start_index4%12)*5
                end_hour4 =end_index4//12
                end_min4 = (end_index4%12)*5
                kosu_list.append('{}:{}～{}:{}'.format(start_hour4, str(start_min4).zfill(2), \
                                                    end_hour4, str(end_min4).zfill(2)))
              else:
                kosu_list.append('　　　　　')

          # 指定日に工数データがない場合の処理
          else:

            # 就業、残業リストに空追加
            exec('work_list{}.append("")'.format(ind + 1))
            exec('over_time_list{}.append("")'.format(ind + 1))

            # 空の工数入力リストを作成
            for k in range(4):

              # 工数入力リストに空を入れる
              kosu_list.append('　　　　　')

        # 日付リストが空の場合の処理
        else:

          # 就業、残業リストに空追加
          exec('work_list{}.append("")'.format(ind + 1))
          exec('over_time_list{}.append("")'.format(ind + 1))

          # 空の工数入力リストを作成
          for k in range(4):

            # 工数入力リストに空を入れる
            kosu_list.append('　　　　　')

        # 工数入力リストに1日分の入力工数追加
        exec('kosu_list{}.append(kosu_list)'.format(ind + 1))

    # 班員登録がない場合の処理
    else:

      # 空の就業、残業リスト作成
      for b in range(7):

        # 就業、残業リストに空追加
        exec('work_list{}.append("　　　　　")'.format(ind + 1))
        exec('over_time_list{}.append("")'.format(ind + 1))


      for n in range(7):
        kosu_list = []
        # 空の工数入力リストを作成
        for k in range(4):

          # 工数入力リストに空を入れる
          kosu_list.append('　　　　　')
        
        # 工数入力リストに1日分の入力工数追加
        exec('kosu_list{}.append(kosu_list)'.format(ind + 1))


  # 工数入力OK_NGリスト反転
  ok_ng_list1.reverse()
  ok_ng_list2.reverse()
  ok_ng_list3.reverse()
  ok_ng_list4.reverse()
  ok_ng_list5.reverse()
  ok_ng_list6.reverse()
  ok_ng_list7.reverse()
  ok_ng_list8.reverse()
  ok_ng_list9.reverse()
  ok_ng_list10.reverse()

 

  # HTMLに渡す辞書
  library_m = {
    'title' : '班員工数入力状況一覧',
    'default_day' : default_day,
    'member_num' : member_num,
    'day_list' : day_list,
    'member_name1' : member_name1,
    'work_list1' : work_list1,
    'over_time_list1' : over_time_list1,
    'kosu_list1' : kosu_list1,
    'ok_ng_list1' : ok_ng_list1,
    'member_name2' : member_name2,
    'work_list2' : work_list2,
    'over_time_list2' : over_time_list2,
    'kosu_list2' : kosu_list2,
    'ok_ng_list2' : ok_ng_list2,
    'member_name3' : member_name3,
    'work_list3' : work_list3,
    'over_time_list3' : over_time_list3,
    'kosu_list3' : kosu_list3,
    'ok_ng_list3' : ok_ng_list3,
    'member_name4' : member_name4,
    'work_list4' : work_list4,
    'over_time_list4' : over_time_list4,
    'kosu_list4' : kosu_list4,
    'ok_ng_list4' : ok_ng_list4,
    'member_name5' : member_name5,
    'work_list5' : work_list5,
    'over_time_list5' : over_time_list5,
    'kosu_list5' : kosu_list5,
    'ok_ng_list5' : ok_ng_list5,
    'member_name6' : member_name6,
    'work_list6' : work_list6,
    'over_time_list6' : over_time_list6,
    'kosu_list6' : kosu_list6,
    'ok_ng_list6' : ok_ng_list6,
    'member_name7' : member_name7,
    'work_list7' : work_list7,
    'over_time_list7' : over_time_list7,
    'kosu_list7' : kosu_list7,
    'ok_ng_list7' : ok_ng_list7,
    'member_name8' : member_name8,
    'work_list8' : work_list8,
    'over_time_list8' : over_time_list8,
    'kosu_list8' : kosu_list8,
    'ok_ng_list8' : ok_ng_list8,
    'member_name9' : member_name9,
    'work_list9' : work_list9,
    'over_time_list9' : over_time_list9,
    'kosu_list9' : kosu_list9,
    'ok_ng_list9' : ok_ng_list9,
    'member_name10' : member_name10,
    'work_list10' : work_list10,
    'over_time_list10' : over_time_list10,
    'kosu_list10' : kosu_list10,
    'ok_ng_list10' : ok_ng_list10,
    }

  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/team_calendar.html', library_m)





#--------------------------------------------------------------------------------------------------------


