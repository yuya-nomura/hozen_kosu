from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib import messages
from ..models import member
from ..models import administrator_data
from ..models import inquiry_data
from ..forms import inquiryForm
from ..forms import inquiry_findForm





#--------------------------------------------------------------------------------------------------------





# 問い合わせ入力画面定義
def inquiry_new(request):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:

    return redirect(to = '/login')


  # フォーム定義
  form = inquiryForm()


  # ログイン者の情報取得
  data = member.objects.get(employee_no = request.session.get('login_No', None))


  # POST時の処理
  if (request.method == 'POST'):
    
    # 問い合わせ内容が10文字未満の場合の処理
    if len(request.POST['inquiry']) < 10:

      # エラーメッセージ出力
      messages.error(request, '問い合わせ内容は10文字以上でお願いします。ERROR041')

      # このページをリダイレクト
      return redirect(to = '/inquiry_new')

    # 従業員番号に該当するmemberインスタンスを取得
    member_instance = member.objects.get(employee_no = request.session.get('login_No', None))

    # 問い合わせ内容を変数に入れる
    new = inquiry_data(employee_no2 = request.session.get('login_No', None), \
                       name = member_instance, \
                       content_choice = request.POST['content_choice'], \
                       inquiry = request.POST['inquiry'])
    
    # レコードセーブ
    new.save()

    # このページを読み直す
    return redirect(to='/inquiry_new')



  # HTMLに渡す辞書
  library_m = {
    'title' : '問い合わせ入力',
    'data' : data,
    'form' : form,
    }
  


  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/inquiry_new.html', library_m)





#--------------------------------------------------------------------------------------------------------





# 問い合わせ履歴画面定義
def inquiry_list(request, num):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:

    return redirect(to = '/login')


  # 問い合わせ履歴のある従業員番号リスト作成
  employee_no_list = inquiry_data.objects.values_list('employee_no2', flat=True)\
                     .order_by('employee_no2').distinct()
  
  # 名前リスト定義
  name_list = [['', '']]

  # 従業員番号を名前に変更するループ
  for No in list(employee_no_list):

    # 指定従業員番号で人員情報取得
    name = member.objects.get(employee_no = No)

    # 名前リスト作成
    name_list.append([No, name])




  # POST時の処理
  if (request.method == 'POST'):

    # お問い合わせデータ取得(氏名とカテゴリーで絞り込み)
    data = inquiry_data.objects.filter(content_choice__contains = request.POST['category'], 
                                       employee_no2__contains = request.POST['name_list']).order_by('id').reverse()

    # 設定データ取得
    page_num = administrator_data.objects.order_by("id").last()

    # 1ページごとのデータ取得
    page = Paginator(data, page_num.menu_row)


    # フォーム定義
    form = inquiry_findForm(request.POST)

    # フォーム選択肢定義
    form.fields['name_list'].choices = name_list


  # POST時以外の時の処理
  else:

    # お問い合わせデータ取得
    data = inquiry_data.objects.all().order_by('id').reverse()

    # 設定データ取得
    page_num = administrator_data.objects.order_by("id").last()

    # 1ページごとのデータ取得
    page = Paginator(data, page_num.menu_row)

    # フォーム定義
    form = inquiry_findForm()

    # フォーム選択肢定義
    form.fields['name_list'].choices = name_list



  # HTMLに渡す辞書
  library_m = {
    'title' : '問い合わせ履歴',
    'form' : form,
    'name_list' : name_list,
    'data': page.get_page(num),
    'num' : num
    }
  


  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/inquiry_list.html', library_m)




#--------------------------------------------------------------------------------------------------------





# 問い合わせ詳細画面定義
def inquiry_display(request, num):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:

    return redirect(to = '/login')


  # 指定IDの工数履歴のレコードのオブジェクトを変数に入れる
  obj_get = inquiry_data.objects.get(id = num)

  # ログイン者の情報取得
  data = member.objects.get(employee_no = request.session.get('login_No', None))

  # 本人確認リセット
  himself = False

  # 本人か確認
  if str(obj_get.name) == str(data.name):

    # 本人の場合True
    himself = True



  # お問い合わせ編集処理
  if "Registration" in request.POST:
     
    # お問い合わせ編集ページへ飛ぶ
    return redirect(to = '/inquiry_edit/{}'.format(num))


  print(himself)
  # HTMLに渡す辞書
  library_m = {
    'title' : '問い合わせ詳細',
    'id' : num,
    'obj' : obj_get,
    'data' : data,
    'himself' : himself,
    }
  


  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/inquiry_display.html', library_m)





#--------------------------------------------------------------------------------------------------------





# 問い合わせ編集画面定義
def inquiry_edit(request, num):

  # 未ログインならログインページに飛ぶ
  if request.session.get('login_No', None) == None:

    return redirect(to = '/login')


  # 指定IDの工数履歴のレコードのオブジェクトを変数に入れる
  obj_get = inquiry_data.objects.get(id = num)

  # フォーム初期値定義
  form_default = {'content_choice' : obj_get.content_choice, 
                  'inquiry' : obj_get.inquiry, 
                  'answer' : obj_get.answer}

  # フォーム定義
  form = inquiryForm(form_default)



  # お問い合わせ編集処理
  if "Registration" in request.POST:

    # 工数データ作成し残業書き込み
    inquiry_data.objects.update_or_create(id = num, \
                                          defaults = {'content_choice' : request.POST['content_choice'], \
                                                      'inquiry' : request.POST['inquiry'], \
                                                      'answer' : request.POST['answer']})

    # このページをリダイレクトする
    return redirect(to = '/inquiry_edit/{}'.format(num))



  # お問い合わせ削除処理
  if "delete" in request.POST:

    # 取得したレコード削除
    obj_get.delete()

    # お問い合わせ一覧ページをリダイレクトする
    return redirect(to = '/inquiry_list/1')



  # HTMLに渡す辞書
  library_m = {
    'title' : '問い合わせ編集',
    'id' : num,
    'obj' : obj_get,
    'form' : form,
    }
  


  # 指定したHTMLに辞書を渡して表示を完成させる
  return render(request, 'kosu/inquiry_edit.html', library_m)





#--------------------------------------------------------------------------------------------------------





