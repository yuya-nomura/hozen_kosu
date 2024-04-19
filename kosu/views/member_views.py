from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .. import forms
from ..models import member
from ..models import administrator_data
from ..forms import memberForm
from ..forms import member_findForm





#--------------------------------------------------------------------------------------------------------





# 人員一覧画面定義
def member_page(request, num): 

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:

    return redirect(to = '/login')


  # ログイン者の情報取得
  data = member.objects.get(employee_no = request.session.get('login_No', None))

  # ログイン者に権限がなければメインページに戻る
  if data.authority == False:

    return redirect(to = '/')


  # 設定データ取得
  page_num = administrator_data.objects.order_by("id").last()



  # POST時の処理
  if (request.method == 'POST'):

    # POST送信時のフォームの状態(POSTした値は入ったまま)
    form = member_findForm(request.POST)

    # POSTした値を変数に入れる
    find = request.POST['shop2']
    find2 = request.POST['employee_no6']
    request.session['find_shop'] = find
    request.session['find_employee_no'] = find2

    # 就業日とログイン者の従業員番号でフィルターをかけて一致したものを変数に入れる
    data2 = member.objects.filter(shop__contains = find, \
            employee_no__contains = find2).order_by('employee_no')
    page = Paginator(data2, page_num.menu_row)


  else:

    # フォームの初期値設定
    form_default = {'shop2' : request.session.get('find_shop', ''), \
                    'employee_no6' : request.session.get('find_employee_no', '')}
  
    # POST送信していない時のフォームの状態(空のフォーム)
    form = member_findForm(form_default)

    # 人員の一覧のオブジェクトを変数に入れる
    data2 = member.objects.filter(shop__contains = request.session.get('find_shop', ''), \
            employee_no__contains = request.session.get('find_employee_no', '')).order_by('employee_no')
    page = Paginator(data2, page_num.menu_row)



  # HTMLに渡す辞書
  library_m = {
    'title' : '人員一覧',
    'form' : form,
    'data': page.get_page(num),
    'num' : num
  }



  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/member.html', library_m)





#--------------------------------------------------------------------------------------------------------





# 人員登録画面定義
def member_new(request):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')


  # ログイン者の情報取得
  data = member.objects.get(employee_no = request.session.get('login_No', None))

  # ログイン者に権限がなければメインページに戻る
  if data.authority == False:

    return redirect(to = '/')



  # POST時の処理
  if (request.method == 'POST'):

    # POST送信された値を変数に入れる
    employee_no = request.POST['employee_no']
    # POST送信された値でフィルターをかけ一致したオブジェクトを取得
    data2 = member.objects.filter(employee_no = employee_no)


    # POST送信された従業員番号が既に登録されている場合の処理
    if data2.count() >= 1:
      # エラーメッセージ出力
      messages.error(request, '入力した従業員番号はすでに登録があるので登録できません。ERROR020')
      # このページをリダイレクト
      return redirect(to = '/new')

    # 登録ショップが三組三交替Ⅱ甲乙丙番Cの場合の休憩初期値登録
    if request.POST['shop'] == 'W1' or request.POST['shop'] == 'W2' \
      or request.POST['shop'] == 'A1' or request.POST['shop'] == 'A2':
      
      # 1直休憩時間初期値定義
      break1_1 = '11401240'
      break1_2 = '17201735'
      break1_3 = '23350035'
      break1_4 = '04350450'

      # 2直休憩時間初期値定義
      break2_1 = '14101510'
      break2_2 = '22002215'
      break2_3 = '04150515'
      break2_4 = '09150930'

      # 3直休憩時間初期値定義
      break3_1 = '23500050'
      break3_2 = '06400655'
      break3_3 = '12551355'
      break3_4 = '17551810'

      # 常昼休憩時間初期値定義
      break4_1 = '12001300'
      break4_2 = '19001915'
      break4_3 = '01150215'
      break4_4 = '06150630'

    # 登録ショップが三組三交替Ⅱ甲乙丙番Bか常昼の場合の休憩初期値登録
    else:

      # 1直休憩時間初期値定義
      break1_1 = '10401130'
      break1_2 = '15101520'
      break1_3 = '20202110'
      break1_4 = '01400150'

      # 2直休憩時間初期値定義
      break2_1 = '17501840'
      break2_2 = '22302240'
      break2_3 = '03400430'
      break2_4 = '09000910'

      # 3直休憩時間初期値定義
      break3_1 = '01400230'
      break3_2 = '07050715'
      break3_3 = '12151305'
      break3_4 = '17351745'

      # 常昼休憩時間初期値定義
      break4_1 = '12001300'
      break4_2 = '19001915'
      break4_3 = '01150215'
      break4_4 = '06150630'


    # POSTされた値をメンバーデータに入れる   
    new = member(employee_no = request.POST['employee_no'], name = request.POST['name'], \
                 shop = request.POST['shop'], authority =  'authority' in request.POST, \
                 administrator = 'administrator' in request.POST, break_time1 = break1_1, \
                 break_time1_over1 = break1_2, break_time1_over2 = break1_3, \
                 break_time1_over3 = break1_4, break_time2 = break2_1, \
                 break_time2_over1 = break2_2, break_time2_over2 = break2_3, \
                 break_time2_over3 = break2_4, break_time3 = break3_1, \
                 break_time3_over1 = break3_2, break_time3_over2 = break3_3, \
                 break_time3_over3 = break3_4, break_time4 = break4_1, \
                 break_time4_over1 = break4_2, break_time4_over2 = break4_3, \
                 break_time4_over3 = break4_4)
    
    # 新しいレコードを作成しセーブする
    new.save()
    # 人員一覧画面をリダイレクトする
    return redirect(to = '/member/1')
  

  # HTMLに渡す辞書
  library_m = {
    'title': '人員登録',
    'data' : data,
    'form': memberForm(),
  }

  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/member_new.html', library_m)



#--------------------------------------------------------------------------------------------------------



# 人員編集画面定義
def member_edit(request, num):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')

  # ログイン者の情報取得
  data = member.objects.get(employee_no = request.session.get('login_No', None))
  # ログイン者に権限がなければメインページに戻る
  if data.authority == False:
    return redirect(to = '/')

  # 指定従業員番号のレコードのオブジェクトを変数に入れる
  obj = member.objects.get(employee_no = num)
  # GET時の処理
  if (request.method == 'GET'):
    # 編集前の従業員番号をセッションに記憶
    request.session['edit_No'] = num


  # POST時の処理
  if (request.method == 'POST'):

    # POST送信された従業員番号を変数に入れる
    find = request.POST['employee_no']

    # 人員登録データの内、従業員番号がPOST送信された値と等しいレコードのオブジェクトを取得
    data = member.objects.filter(employee_no = find)

    if 'authority' in request.POST == '':
      authority = False
    else:
      authority = True

    if 'administrator' in request.POST == '':
      administrator = False
    else:
      administrator = True

    # 編集した従業員番号の登録がすでにあるかチェック
    if int(request.session.get('edit_No', None)) != int(request.POST['employee_no']) \
      and data.count() >= 1:
      # エラーメッセージ出力
      messages.error(request, '入力した従業員番号はすでに登録があるので登録できません。ERROR021')
      # このページをリダイレクト
      return redirect(to = '/member_edit/{}'.format(num))


    # 指定従業員番号のレコードにPOST送信された値を上書きする
    member.objects.update_or_create(employee_no = request.POST['employee_no'], \
                                    defaults = {'employee_no' : find, \
                                                'name' : request.POST['name'], \
                                                'shop' : request.POST['shop'], \
                                                'authority' : authority, \
                                                'administrator' : administrator})

    # 工数履歴画面をリダイレクトする
    return redirect(to = '/member/1')

  # HTMLに渡す辞書
  library_m = {
    'title' : '人員編集',
    'employee_no' : num,
    'data' : data,
    'form' : memberForm(instance = obj),
    }

  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/member_edit.html', library_m)



#--------------------------------------------------------------------------------------------------------



# 人員削除画面定義
def member_delete(request, num):
  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:
    return redirect(to = '/login')
  
  # ログイン者の情報取得
  data = member.objects.get(employee_no = request.session.get('login_No', None))
  
  # ログイン者に権限がなければメインページに戻る
  if data.authority == False:
    return redirect(to = '/')

  # 指定従業員番号のレコードのオブジェクトを変数に入れる
  obj = member.objects.get(employee_no = num)


  # POST時の処理
  if (request.method == 'POST'):

    # 取得していた指定従業員番号のレコードを削除する
    obj.delete()

    # 工数履歴画面をリダイレクトする
    return redirect(to = '/member/1')

  # HTMLに渡す辞書
  library_m = {
    'title' : '人員削除',
    'employee_no' : num,
    'obj' : obj,
    }

  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/member_delete.html', library_m)



#--------------------------------------------------------------------------------------------------------
