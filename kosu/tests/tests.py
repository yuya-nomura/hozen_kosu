import datetime
from bs4 import BeautifulSoup
from django.test import TestCase
from django.urls import reverse
from ..utils import round_time
from kosu.models import member
from kosu.models import kosu_division
from kosu.models import Business_Time_graph
from kosu.models import team_member
from kosu.models import administrator_data
from kosu.models import inquiry_data





class MultiplePagesAccessTestCase(TestCase):
    # ダミーデータ定義
    def setUp(self):        
        # memberダミーデータ
        self.member = member.objects.create(
            employee_no = 11111,
            name = 'テストユーザー',
            shop = 'その他',
            authority = True,
            administrator = True,
            break_time1 = '#10401130',
            break_time1_over1 = '#15101520',
            break_time1_over2 = '#20202110',
            break_time1_over3 = '#01400150',
            break_time2 = '#17501840',
            break_time2_over1 = '#22302240',
            break_time2_over2 = '#03400430',
            break_time2_over3 = '#09000910',
            break_time3 = '#01400230',
            break_time3_over1 = '#07050715',
            break_time3_over2 = '#12151305',
            break_time3_over3 = '#17351745',
            break_time4 = '#12001300',
            break_time4_over1 = '#19001915',
            break_time4_over2 = '#01150215',
            break_time4_over3 = '#06150630',
            )

        # administrator_dataダミーデータ
        self.administrator_data = administrator_data.objects.create(
            menu_row = 20,
            administrator_employee_no1 = '11111',
            administrator_employee_no2 = '',
            administrator_employee_no3 = '',
            )

        # kosu_divisionダミーデータ
        self.kosu_division = kosu_division.objects.create(
            kosu_name = 'トライ定義',
            kosu_title_1 = '工数区分名1',
            kosu_division_1_1 = '定義1',
            kosu_division_2_1 = '作業内容1',
            kosu_title_2 = '工数区分名2',
            kosu_division_1_2 = '定義2',
            kosu_division_2_2 = '作業内容2',
            kosu_title_3 = '工数区分名3',
            kosu_division_1_3 = '定義3',
            kosu_division_2_3 = '作業内容3',
            kosu_title_4 = '工数区分名4',
            kosu_division_1_4 = '定義4',
            kosu_division_2_4 = '作業内容4',
            kosu_title_5 = '工数区分名5',
            kosu_division_1_5 = '定義5',
            kosu_division_2_5 = '作業内容5',
            kosu_title_6 = '工数区分名6',
            kosu_division_1_6 = '定義6',
            kosu_division_2_6 = '作業内容6',
            kosu_title_7 = '工数区分名7',
            kosu_division_1_7 = '定義7',
            kosu_division_2_7 = '作業内容7',
            kosu_title_8 = '工数区分名8',
            kosu_division_1_8 = '定義8',
            kosu_division_2_8 = '作業内容8',
            kosu_title_9 = '工数区分名9',
            kosu_division_1_9 = '定義9',
            kosu_division_2_9 = '作業内容9',
            kosu_title_10 = '工数区分名10',
            kosu_division_1_10 = '定義10',
            kosu_division_2_10 = '作業内容10',
        )

        # Business_Time_graphダミーデータ
        self.Business_Time_graph = Business_Time_graph.objects.create(
            employee_no3 = 11111,
            name = self.member,
            def_ver2 = self.kosu_division.kosu_name,
            work_day2 = '2000-01-01',
            tyoku2 = '4',
            time_work = '################################################################################################AAAAAAAAAAAABBBBBBBBBBBBCCCCCCCCCCCCDDDDDDDDDDDD$$$$$$$$$$$$EEEEEEEEEEEEFFFFFFFFFFFFGGGGGGGGGGGGHHHHHHHHHHHHIIIIIIIIIIIIJJJJJJJJJJ##############################################################',
            detail_work = '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$aaa$aaa$aaa$aaa$aaa$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$bbb$bbb$bbb$bbb$bbb$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$',
            over_time = 120,
            breaktime = '#12001300',
            breaktime_over1 = '#19001915',
            breaktime_over2 = '#01150215',
            breaktime_over3 = '#06150630',
            work_time = '出勤',
            judgement = True,
            break_change = False,
            )

        # team_memberダミーデータ
        self.team_member = team_member.objects.create(
            employee_no5 = 11111,
            member1 = '',
            member2 = 11111,
            member3 = '',
            member4 = 11111,
            member5 = '',
            member6 = 11111,
            member7 = '',
            member8 = 11111,
            member9 = '',
            member10 = 11111,
            member11 = '',
            member12 = 11111,
            member13 = '',
            member14 = 11111,
            member15 = '',
            )

        # inquiry_dataダミーデータ
        self.inquiry_data = inquiry_data.objects.create(
            employee_no2 = 11111,
            name = self.member,
            content_choice = '問い合わせ',
            inquiry = '',
            answer = '回答'
            )
    

    # ヘルプページ開きチェック
    def test_help(self):
        # URL定義
        url = reverse('help')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「ヘルプ」という文字列が含まれていることを確認
        self.assertContains(response, 'ヘルプ')



    # ログインページ開きチェック
    def test_login(self):
        # URL定義
        url = reverse('login')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「ログイン」という文字列が含まれていることを確認
        self.assertContains(response, 'ログイン')
    


    # MENUページ開きチェック
    def test_main(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('main')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「MENU」という文字列が含まれていることを確認
        self.assertContains(response, 'MENU')



    # 工数MENUページ開きチェック
    def test_kosu_main(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('kosu_main')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「工数MENU」という文字列が含まれていることを確認
        self.assertContains(response, '工数MENU')



    # 工数区分定義MENUページ開きチェック
    def test_def_main(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('def_main')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「工数区分定義MENU」という文字列が含まれていることを確認
        self.assertContains(response, '工数区分定義MENU')



    # 人員MENUページ開きチェック
    def test_member_main(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('member_main')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「人員MENU」という文字列が含まれていることを確認
        self.assertContains(response, '人員MENU')



    # 班員MENUページ開きチェック
    def test_team_main(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('team_main')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「班員MENU」という文字列が含まれていることを確認
        self.assertContains(response, '班員MENU')



    # 問い合わせMENUページ開きチェック
    def test_inquiry_main(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('inquiry_main')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「問い合わせMENU」という文字列が含まれていることを確認
        self.assertContains(response, '問い合わせMENU')



    # 管理者MENUページ開きチェック
    def test_administrator(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('administrator')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「管理者MENU」という文字列が含まれていることを確認
        self.assertContains(response, '管理者MENU')



    # 工数登録ページ開きチェック
    def test_input(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('input')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「テストユーザーさんの工数登録」という文字列が含まれていることを確認
        self.assertContains(response, 'テストユーザーさんの工数登録')



    # 工数登録ページ現在時刻表示チェック(日付またぎ無し)
    def test_input_now_time_post_not_over_day(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('input')
        
        # 取得したURLに対してPOST送信するデータ定義 
        response = self.client.post(url, {
            'now_time' : '現在時刻',
            'start_time' : '0:00',
            'work' : self.Business_Time_graph.work_time,
            'tyoku2' : self.Business_Time_graph.tyoku2,
            'kosu_def_list' : 'A',
            'work_detail' : 'テスト',
            'break_change' : True,
            'over_work' : 30
        })

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        
        # 現在時刻取得
        now_time = datetime.datetime.now().time()
        expected_time = round_time(now_time).strftime('%H:%M')  # round_time関数を直接使用

        # BeautifulSoupを使ってHTMLレスポンスを解析
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # <input>タグのvalue属性を取得
        end_time_input = soup.find('input', {'id': 'end_time'})
        if end_time_input:
            actual_value = end_time_input.get('value')
        else:
            actual_value = None
        
        # チェックボックスの状態を確認
        tomorrow_check_input = soup.find('input', {'id': 'id_tomorrow_check'})
        if tomorrow_check_input:
            checkbox_checked = tomorrow_check_input.has_attr('checked')
        else:
            checkbox_checked = False

        # value属性が期待する値と一致するか確認
        self.assertEqual(actual_value, expected_time)
        # チェックボックスがチェックされていないことを確認
        self.assertFalse(checkbox_checked)



    # 工数登録ページ現在時刻表示チェック(日付またぎ有)
    def test_input_now_time_post_over_day(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('input')
        
        # 取得したURLに対してPOST送信するデータ定義 
        response = self.client.post(url, {
            'now_time' : '現在時刻',
            'start_time' : '23:55',
            'work' : self.Business_Time_graph.work_time,
            'tyoku2' : self.Business_Time_graph.tyoku2,
            'kosu_def_list' : 'A',
            'work_detail' : 'テスト',
            'break_change' : True,
            'over_work' : 30
        })

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        
        # 現在時刻取得
        now_time = datetime.datetime.now().time()
        expected_time = round_time(now_time).strftime('%H:%M')  # round_time関数を直接使用

        # BeautifulSoupを使ってHTMLレスポンスを解析
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # <input>タグのvalue属性を取得
        end_time_input = soup.find('input', {'id': 'end_time'})
        if end_time_input:
            actual_value = end_time_input.get('value')
        else:
            actual_value = None
        
        # チェックボックスの状態を確認
        tomorrow_check_input = soup.find('input', {'id': 'id_tomorrow_check'})
        if tomorrow_check_input:
            checkbox_checked = tomorrow_check_input.has_attr('checked')
        else:
            checkbox_checked = False

        # value属性が期待する値と一致するか確認
        self.assertEqual(actual_value, expected_time)
        # チェックボックスがチェックされていることを確認
        self.assertTrue(checkbox_checked)



    # 工数登録ページ残業登録チェック
    def test_input_over_time_post(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # フォームデータ定義(工数データ有の場合)
        form_data = {
            'work_day' : self.Business_Time_graph.work_day2,
            'work' : self.Business_Time_graph.work_time,
            'tyoku2' : self.Business_Time_graph.tyoku2,
            'over_work' : '150',
            'over_time_correction' : '残業のみ修正',
            }
        
        # URL定義
        url = reverse('input')
        # 取得したURLに対してPOSTリクエスト送信
        response = self.client.post(url, form_data)
        # リクエストのレスポンスステータスコードが302(リダイレクト)であることを確認
        self.assertEqual(response.status_code, 302)

        # テストユーザーの工数データ取得
        updated_entry = Business_Time_graph.objects.get(employee_no3 = self.member.employee_no, \
                                                        work_day2 = self.Business_Time_graph.work_day2)
        # 残業時間が150に更新されていることを確認
        self.assertEqual(updated_entry.over_time, 150)

        # フォームデータ2定義(工数データ無しの場合)
        form_data2 = {
            'work_day' : datetime.datetime.strptime(self.Business_Time_graph.work_day2, '%Y-%m-%d').date() + datetime.timedelta(days = 1),
            'over_work' : '90',
            'over_time_correction' : '残業のみ修正',
            }

        # 取得したURLに対してPOSTリクエスト送信
        response = self.client.post(url, form_data2)
        # リクエストのレスポンスステータスコードが302(リダイレクト)であることを確認
        self.assertEqual(response.status_code, 302)

        # テストユーザーの工数データ取得
        updated_entry = Business_Time_graph.objects.get(employee_no3 = self.member.employee_no, \
                                                        work_day2 = datetime.datetime.strptime(self.Business_Time_graph.work_day2, '%Y-%m-%d').date() + datetime.timedelta(days = 1))
        # 残業時間が90に更新されていることを確認
        self.assertEqual(updated_entry.over_time, 90)



    # 当日休憩変更ページ開きチェック
    def test_today_break_time(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session['break_today'] = self.Business_Time_graph.work_day2
        session.save()

        # URL定義
        url = reverse('today_break_time')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「2000年1月1日の休憩変更」という文字列が含まれていることを確認
        self.assertContains(response, '2000年1月1日の休憩変更')



    # 休憩変更ページ開きチェック
    def test_break_time(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('break_time')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「休憩時間定義」という文字列が含まれていることを確認
        self.assertContains(response, '休憩時間定義')



    # 工数履歴ページ開きチェック
    def test_kosu_list(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        
        # URL定義
        url = reverse('kosu_list', args = [1])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「休憩時間定義」という文字列が含まれていることを確認
        self.assertContains(response, 'テストユーザーさんの工数履歴')



    # 工数詳細ページ開きチェック
    def test_detail(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('detail', args = [self.Business_Time_graph.id])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「2000年1月1日の工数詳細」という文字列が含まれていることを確認
        self.assertContains(response, '2000年1月1日の工数詳細')



    # 工数データ削除ページ開きチェック
    def test_delete(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('delete', args = [self.Business_Time_graph.id])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「工数データ削除」という文字列が含まれていることを確認
        self.assertContains(response, '工数データ削除')



    # 工数データページ開きチェック
    def test_graph(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('graph', args = [1])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「工数データ」という文字列が含まれていることを確認
        self.assertContains(response, '工数データ')



    # 工数集計ページ開きチェック
    def test_total(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('total')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「テストユーザーさんの工数集計」という文字列が含まれていることを確認
        self.assertContains(response, 'テストユーザーさんの工数集計')



    # 勤務入力ページ開きチェック
    def test_schedule(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('schedule')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「勤務入力」という文字列が含まれていることを確認
        self.assertContains(response, '勤務入力')



    # 残業管理ページ開きチェック
    def test_over_time(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('over_time')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「残業管理」という文字列が含まれていることを確認
        self.assertContains(response, '残業管理')



    # 工数区分定義確認ページ開きチェック
    def test_kosu_def(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('kosu_def')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「工数区分定義確認」という文字列が含まれていることを確認
        self.assertContains(response, '工数区分定義確認')



    # 工数区分定義切り替えページ開きチェック
    def test_kosu_Ver(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('kosu_Ver')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「工数区分定義切り替え」という文字列が含まれていることを確認
        self.assertContains(response, '工数区分定義切り替え')



    # 工数区分定義一覧ページ開きチェック
    def test_def_list(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('def_list', args = [1])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「工数区分定義一覧」という文字列が含まれていることを確認
        self.assertContains(response, '工数区分定義一覧')



    # 工数区分定義新規登録ページ開きチェック
    def test_def_new(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('def_new')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「工数区分定義新規登録」という文字列が含まれていることを確認
        self.assertContains(response, '工数区分定義新規登録')



    # 工数区分定義編集ページ開きチェック
    def test_def_edit(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('def_edit', args = [self.kosu_division.id])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「工数区分定義編集」という文字列が含まれていることを確認
        self.assertContains(response, '工数区分定義編集')



    # 工数区分定義削除ページ開きチェック
    def test_def_delete(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('def_delete', args = [self.kosu_division.id])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「工数区分定義削除」という文字列が含まれていることを確認
        self.assertContains(response, '工数区分定義削除')



    # 人員登録ページ開きチェック
    def test_member_new(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('member_new')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「人員登録」という文字列が含まれていることを確認
        self.assertContains(response, '人員登録')



    # 人員一覧ページ開きチェック
    def test_member(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('member', args = [1])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「人員一覧」という文字列が含まれていることを確認
        self.assertContains(response, '人員一覧')


    # 人員編集ページ開きチェック
    def test_member_edit(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('member_edit', args = [self.member.employee_no])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「人員編集」という文字列が含まれていることを確認
        self.assertContains(response, '人員編集')



    # 人員削除ページ開きチェック
    def test_member_delete(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('member_delete', args = [self.member.employee_no])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「人員削除」という文字列が含まれていることを確認
        self.assertContains(response, '人員削除')



    # 班員設定ページ開きチェック
    def test_team(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('team')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「テストユーザーさんの班員設定」という文字列が含まれていることを確認
        self.assertContains(response, 'テストユーザーさんの班員設定')



    # 班員工数グラフページ開きチェック
    def test_team_graph(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('team_graph')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「班員工数グラフ」という文字列が含まれていることを確認
        self.assertContains(response, '班員工数グラフ')



    # 班員工数確認ページ開きチェック
    def test_team_kosu(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('team_kosu', args = [1])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「テストユーザーさん班員工数確認」という文字列が含まれていることを確認
        self.assertContains(response, 'テストユーザーさん班員工数確認')



    # 工数詳細ページ開きチェック
    def test_team_detail(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('team_detail', args = [self.Business_Time_graph.id])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「テストユーザーさんの工数詳細」という文字列が含まれていることを確認
        self.assertContains(response, 'テストユーザーさんの工数詳細')



    # 班員工数入力状況一覧ページ開きチェック
    def test_team_calendar(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('team_calendar')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「班員工数入力状況一覧」という文字列が含まれていることを確認
        self.assertContains(response, '班員工数入力状況一覧')



    # 班員残業管理ページ開きチェック
    def test_team_over_time(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('team_over_time')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「班員残業管理」という文字列が含まれていることを確認
        self.assertContains(response, '班員残業管理')



    # 工数入力可否(ショップ単位)ページ開きチェック
    def test_class_list(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('class_list')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「工数入力可否(ショップ単位)」という文字列が含まれていることを確認
        self.assertContains(response, '工数入力可否(ショップ単位)')



    # 工数詳細ページ開きチェック
    def test_class_detail(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()

        # URL定義
        url = reverse('class_detail', args = [self.Business_Time_graph.id])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「テストユーザーさんの工数詳細」という文字列が含まれていることを確認
        self.assertContains(response, 'テストユーザーさんの工数詳細')



    # 問い合わせ入力ページ開きチェック
    def test_inquiry_new(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('inquiry_new')
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「問い合わせ入力」という文字列が含まれていることを確認
        self.assertContains(response, '問い合わせ入力')



    # 問い合わせ履歴ページ開きチェック
    def test_inquiry_list(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('inquiry_list', args = [1])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「問い合わせ履歴」という文字列が含まれていることを確認
        self.assertContains(response, '問い合わせ履歴')



    # 問い合わせ詳細ページ開きチェック
    def test_inquiry_display(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('inquiry_display', args = [self.inquiry_data.id])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「問い合わせ詳細」という文字列が含まれていることを確認
        self.assertContains(response, '問い合わせ詳細')



    # 問い合わせ編集ページ開きチェック
    def test_inquiry_edit(self):
        # セッション定義
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()

        # URL定義
        url = reverse('inquiry_edit', args = [self.inquiry_data.id])
        # URLに対してGETリクエスト送信
        response = self.client.get(url)

        # リクエストのレスポンスステータスコードが200(OK)であることを確認
        self.assertEqual(response.status_code, 200)
        # レスポンスコンテンツに「問い合わせ編集」という文字列が含まれていることを確認
        self.assertContains(response, '問い合わせ編集')


















