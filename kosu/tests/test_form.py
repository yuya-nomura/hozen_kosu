import datetime
from bs4 import BeautifulSoup
from django.test import TestCase, Client
from django.urls import reverse
from kosu.models import member, kosu_division, Business_Time_graph, team_member, administrator_data, inquiry_data
from ..utils import round_time





# 各ページリンクテスト
class Page_form(TestCase):
    # 初期データ作成
    @classmethod
    def setUpTestData(cls):       
        # memberダミーデータ
        cls.member = member.objects.create(
            employee_no = 111,
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
        cls.administrator_data = administrator_data.objects.create(
            menu_row = 20,
            administrator_employee_no1 = '111',
            administrator_employee_no2 = '',
            administrator_employee_no3 = '',
            )

        # kosu_divisionダミーデータ
        cls.kosu_division = kosu_division.objects.create(
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
        cls.Business_Time_graph = Business_Time_graph.objects.create(
            employee_no3 = 111,
            name = cls.member,
            def_ver2 = cls.kosu_division.kosu_name,
            work_day2 = '2000-01-01',
            tyoku2 = '4',
            time_work = '################################################################################################AAAAAAAAAAAABBBBBBBBBBBBCCCCCCCCCCCCDDDDDDDDDDDD$$$$$$$$$$$$EEEEEEEEEEEEFFFFFFFFFFFFGGGGGGGGGGGGHHHHHHHHHHHHIIIIIIIIIIJJJJJJJJJJJJ##############################################################',
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
        cls.team_member = team_member.objects.create(
            employee_no5 = 111,
            member1 = '',
            member2 = 111,
            member3 = '',
            member4 = 111,
            member5 = '',
            member6 = 111,
            member7 = '',
            member8 = 111,
            member9 = '',
            member10 = 111,
            member11 = '',
            member12 = 111,
            member13 = '',
            member14 = 111,
            member15 = '',
            )

        # inquiry_dataダミーデータ
        cls.inquiry_data = inquiry_data.objects.create(
            employee_no2 = 111,
            name = cls.member,
            content_choice = '問い合わせ',
            inquiry = '',
            answer = '回答'
            )
        


    # 初期データ
    def setUp(self):
        # テストクライアント初期化
        self.client = Client()

        # セッション定義
        self.session = self.client.session
        self.session['login_No'] = self.member.employee_no
        self.session['input_def'] =  self.kosu_division.kosu_name
        self.session['day'] =  self.Business_Time_graph.work_day2
        self.session['break_today'] =  self.Business_Time_graph.work_day2
        self.session.save()



    # 工数登録ページ現在時刻表示チェック(日付またぎ無し)
    def test_input_now_time_post_not_over_day(self):        
        # URLに対してPOST送信するデータ定義 
        response = self.client.post(reverse('input'), {
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
        # URLに対してPOST送信するデータ定義 
        response = self.client.post(reverse('input'), {
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
        # フォームデータ定義(工数データ有の場合)
        form_data = {
            'work_day' : self.Business_Time_graph.work_day2,
            'work' : self.Business_Time_graph.work_time,
            'tyoku2' : self.Business_Time_graph.tyoku2,
            'over_work' : '150',
            'over_time_correction' : '残業のみ修正',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('input'), form_data)
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

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('input'), form_data2)
        # リクエストのレスポンスステータスコードが302(リダイレクト)であることを確認
        self.assertEqual(response.status_code, 302)

        # テストユーザーの工数データ取得
        updated_entry = Business_Time_graph.objects.get(employee_no3 = self.member.employee_no, \
                                                        work_day2 = datetime.datetime.strptime(self.Business_Time_graph.work_day2, '%Y-%m-%d').date() + datetime.timedelta(days = 1))
        # 残業時間が90に更新されていることを確認
        self.assertEqual(updated_entry.over_time, 90)



    # 工数登録ページ工数入力チェック
    def test_input_kosu_post(self):
        # フォームデータ定義(工数データ有、日またぎ無しの場合)
        form_data = {
            'work_day' : self.Business_Time_graph.work_day2,
            'work' : self.Business_Time_graph.work_time,
            'tyoku2' : self.Business_Time_graph.tyoku2,
            'start_time': '18:50',
            'end_time': '19:20',
            'kosu_def_list': 'A',
            'work_detail': 'トライ',
            'over_work' : '135',
            'Registration' : '工数登録',
            }
        
        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('input'), form_data)
        # リクエストのレスポンスステータスコードが302(リダイレクト)であることを確認
        self.assertEqual(response.status_code, 302)

        # テストユーザーの工数データ取得
        updated_entry = Business_Time_graph.objects.get(employee_no3 = self.member.employee_no, \
                                                        work_day2 = self.Business_Time_graph.work_day2)
        # 作業内容が更新されていることを確認
        self.assertEqual(updated_entry.time_work, '################################################################################################AAAAAAAAAAAABBBBBBBBBBBBCCCCCCCCCCCCDDDDDDDDDDDD$$$$$$$$$$$$EEEEEEEEEEEEFFFFFFFFFFFFGGGGGGGGGGGGHHHHHHHHHHHHIIIIIIIIIIJJJJJJJJJJJJAA$$$A########################################################')
        # 残業時間が135に更新されていることを確認
        self.assertEqual(updated_entry.over_time, 135)
        # 整合性がOKに更新されていることを確認
        self.assertEqual(updated_entry.judgement, True)


        # フォームデータ2定義(工数データ有、日またぎ有の場合)
        form_data2 = {
            'work_day' : self.Business_Time_graph.work_day2,
            'work' : self.Business_Time_graph.work_time,
            'tyoku2' : self.Business_Time_graph.tyoku2,
            'start_time': '23:50',
            'end_time': '0:20',
            'tomorrow_check':True,
            'kosu_def_list': 'B',
            'work_detail': 'トライ',
            'over_work' : '150',
            'Registration' : '工数登録',
            }
        
        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('input'), form_data2)
        # リクエストのレスポンスステータスコードが302(リダイレクト)であることを確認
        self.assertEqual(response.status_code, 302)
        
        # テストユーザーの工数データ取得
        updated_entry = Business_Time_graph.objects.get(employee_no3 = self.member.employee_no, \
                                                        work_day2 = self.Business_Time_graph.work_day2)
        # 作業内容が更新されていることを確認
        self.assertEqual(updated_entry.time_work, 'BBBB############################################################################################AAAAAAAAAAAABBBBBBBBBBBBCCCCCCCCCCCCDDDDDDDDDDDD$$$$$$$$$$$$EEEEEEEEEEEEFFFFFFFFFFFFGGGGGGGGGGGGHHHHHHHHHHHHIIIIIIIIIIJJJJJJJJJJJJAA$$$A######################################################BB')
        # 整合性がNGに更新されていることを確認
        self.assertEqual(updated_entry.judgement, False)


        # フォームデータ2定義(工数データ無し、日またぎ無しの場合)
        form_data3 = {
            'work_day' : datetime.datetime.strptime(self.Business_Time_graph.work_day2, '%Y-%m-%d').date() + datetime.timedelta(days = 2),
            'work' : self.Business_Time_graph.work_time,
            'tyoku2' : self.Business_Time_graph.tyoku2,
            'start_time': '8:00',
            'end_time': '9:00',
            'kosu_def_list': 'A',
            'work_detail': 'トライ',
            'over_work' : '30',
            'Registration' : '工数登録',
            }
        
        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('input'), form_data3)
        # リクエストのレスポンスステータスコードが302(リダイレクト)であることを確認
        self.assertEqual(response.status_code, 302)

        # テストユーザーの工数データ取得
        updated_entry = Business_Time_graph.objects.get(employee_no3 = self.member.employee_no, \
                                                        work_day2 = datetime.datetime.strptime(self.Business_Time_graph.work_day2, '%Y-%m-%d').date() + datetime.timedelta(days = 2))
        # 作業内容が更新されていることを確認
        self.assertEqual(updated_entry.time_work, '################################################################################################AAAAAAAAAAAA####################################################################################################################################################################################')
        # 残業時間が30に更新されていることを確認
        self.assertEqual(updated_entry.over_time, 30)
        # 整合性がNGに更新されていることを確認
        self.assertEqual(updated_entry.judgement, False)
        # 休憩時間が読み込まれていることを確認
        self.assertEqual(updated_entry.breaktime, '#12001300')


        # フォームデータ2定義(工数データ無し、日またぎ無しの場合)
        form_data4 = {
            'work_day' : datetime.datetime.strptime(self.Business_Time_graph.work_day2, '%Y-%m-%d').date() + datetime.timedelta(days = 3),
            'work' : self.Business_Time_graph.work_time,
            'tyoku2' : self.Business_Time_graph.tyoku2,
            'start_time': '23:30',
            'end_time': '0:30',
            'tomorrow_check':True,
            'kosu_def_list': 'A',
            'work_detail': 'トライ',
            'over_work' : '30',
            'Registration' : '工数登録',
            }
        
        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('input'), form_data4)
        # リクエストのレスポンスステータスコードが302(リダイレクト)であることを確認
        self.assertEqual(response.status_code, 302)

        # テストユーザーの工数データ取得
        updated_entry = Business_Time_graph.objects.get(employee_no3 = self.member.employee_no, \
                                                        work_day2 = datetime.datetime.strptime(self.Business_Time_graph.work_day2, '%Y-%m-%d').date() + datetime.timedelta(days = 3))
        # 作業内容が更新されていることを確認
        self.assertEqual(updated_entry.time_work, 'AAAAAA####################################################################################################################################################################################################################################################################################AAAAAA')
        # 残業時間が30に更新されていることを確認
        self.assertEqual(updated_entry.over_time, 30)
        # 整合性がNGに更新されていることを確認
        self.assertEqual(updated_entry.judgement, False)
        # 休憩時間が読み込まれていることを確認
        self.assertEqual(updated_entry.breaktime, '#12001300')



    # 当日休憩変更ページ登録チェック
    def test_today_break_time_post(self):
        # フォームデータ定義(工数データ有の場合)
        form_data = {
            'start_time1': '13:00',
            'end_time1': '14:00',
            'start_time2': '17:00',
            'end_time2': '17:15',
            'start_time3': '22:00',
            'end_time3': '22:15',
            'start_time4': '23:55',
            'end_time4': '0:10',
            'today_break' : '休憩時間登録',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('today_break_time'), form_data)
        # リクエストのレスポンスステータスコードが302(リダイレクト)であることを確認
        self.assertEqual(response.status_code, 302)

        # テストユーザーの工数データ取得
        updated_entry = Business_Time_graph.objects.get(employee_no3 = self.member.employee_no, \
                                                        work_day2 = self.Business_Time_graph.work_day2)

        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.breaktime, '#13001400')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.breaktime_over1, '#17001715')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.breaktime_over2, '#22002215')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.breaktime_over3, '#23550010')



    # 休憩変更ページ登録チェック
    def test_break_time_post(self):
        # フォームデータ定義(工数データ有の場合)
        form_data = {
            'start_time1': '13:00',
            'end_time1': '14:00',
            'start_time2': '17:00',
            'end_time2': '17:15',
            'start_time3': '22:00',
            'end_time3': '22:15',
            'start_time4': '23:55',
            'end_time4': '0:10',
            'start_time5': '13:00',
            'end_time5': '14:00',
            'start_time6': '17:00',
            'end_time6': '17:15',
            'start_time7': '22:00',
            'end_time7': '22:15',
            'start_time8': '23:55',
            'end_time8': '0:10',
            'start_time9': '13:00',
            'end_time9': '14:00',
            'start_time10': '17:00',
            'end_time10': '17:15',
            'start_time11': '22:00',
            'end_time11': '22:15',
            'start_time12': '23:55',
            'end_time12': '0:10',
            'start_time13': '13:00',
            'end_time13': '14:00',
            'start_time14': '17:00',
            'end_time14': '17:15',
            'start_time15': '22:00',
            'end_time15': '22:15',
            'start_time16': '23:55',
            'end_time16': '0:10',
            'break_change' : '休憩時間登録',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('break_time'), form_data)
        # リクエストのレスポンスステータスコードが302(リダイレクト)であることを確認
        self.assertEqual(response.status_code, 302)

        # テストユーザーの工数データ取得
        updated_entry = member.objects.get(employee_no = self.member.employee_no)

        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time1, '#13001400')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time1_over1, '#17001715')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time1_over2, '#22002215')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time1_over3, '#23550010')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time2, '#13001400')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time2_over1, '#17001715')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time2_over2, '#22002215')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time2_over3, '#23550010')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time3, '#13001400')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time3_over1, '#17001715')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time3_over2, '#22002215')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time3_over3, '#23550010')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time4, '#13001400')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time4_over1, '#17001715')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time4_over2, '#22002215')
        # 休憩時間が更新されていることを確認
        self.assertEqual(updated_entry.break_time4_over3, '#23550010')



    # 工数履歴ページ検索チェック
    def test_kosu_list_post(self):
        # Business_Time_graphダミーデータ
        self.Business_Time_graph = Business_Time_graph.objects.create(
            employee_no3 = 111,
            name = self.member,
            def_ver2 = self.kosu_division.kosu_name,
            work_day2 = '2000-01-02',
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
        
        self.Business_Time_graph = Business_Time_graph.objects.create(
            employee_no3 = 111,
            name = self.member,
            def_ver2 = self.kosu_division.kosu_name,
            work_day2 = '2000-01-03',
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
        

        # フォームデータ定義(工数データ有の場合)
        form_data = {
            'kosu_day': self.Business_Time_graph.work_day2,
            'kosu_find': '検索',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('kosu_list', args = [1]), form_data)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)

        data = response.context['data']
        # レコードが1つのみであることを確認
        self.assertEqual(len(data), 1)
        # レコードのwork_day2フィールドの値がフォーム送信値を一致するか確認
        self.assertEqual(data[0].work_day2.strftime('%Y-%m-%d'), self.Business_Time_graph.work_day2)


        # フォームデータ定義(工数データ無しの場合)
        form_data2 = {
            'kosu_day': datetime.datetime.strptime(self.Business_Time_graph.work_day2, '%Y-%m-%d').date() + datetime.timedelta(days = 10),
            'kosu_find': '検索',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('kosu_list', args = [1]), form_data2)
        # レスポンスが成功（ステータスコード200）であることを確認します。
        self.assertEqual(response.status_code, 200)

        data = response.context['data']
        # レコードがないことを確認
        self.assertEqual(len(data), 0)


        # フォームデータ定義(工数データ無しの場合)
        form_data3 = {
            'kosu_day': '',
            'kosu_find': '検索',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('kosu_list', args = [1]), form_data3)
        # レスポンスが成功（ステータスコード200）であることを確認します。
        self.assertEqual(response.status_code, 200)

        data = response.context['data']
        # レコードが3つであることを確認
        self.assertEqual(len(data), 3)



    # 工数詳細ページ工数削除チェック
    def test_detail_post(self):
        # フォームデータ定義
        form_data = {
            'start_time': '13:00',
            'end_time': '14:00',
            'kosu_delete' : '工数削除',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('detail', args = [self.Business_Time_graph.id]), form_data)
        # リクエストのレスポンスステータスコードが302(リダイレクト)であることを確認
        self.assertEqual(response.status_code, 302)

        # テストユーザーの工数データ取得
        updated_entry = Business_Time_graph.objects.get(employee_no3 = self.member.employee_no, \
                                                        work_day2 = self.Business_Time_graph.work_day2)
        # 作業内容が更新されていることを確認
        self.assertEqual(updated_entry.time_work, '################################################################################################AAAAAAAAAAAABBBBBBBBBBBBCCCCCCCCCCCCDDDDDDDDDDDD$$$$$$$$$$$$############FFFFFFFFFFFFGGGGGGGGGGGGHHHHHHHHHHHHIIIIIIIIIIJJJJJJJJJJJJ##############################################################')



    # 工数詳細ページ工数項目削除チェック
    def test_detail_item_delete(self):
        # フォームデータ定義
        form_data = {
            'item_delete' : '1',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('detail', args = [self.Business_Time_graph.id]), form_data)
        # リクエストのレスポンスステータスコードが302(リダイレクト)であることを確認
        self.assertEqual(response.status_code, 302)

        # テストユーザーの工数データ取得
        updated_entry = Business_Time_graph.objects.get(employee_no3 = self.member.employee_no, \
                                                        work_day2 = self.Business_Time_graph.work_day2)
        # 作業内容が更新されていることを確認
        self.assertEqual(updated_entry.time_work, '############################################################################################################BBBBBBBBBBBBCCCCCCCCCCCCDDDDDDDDDDDD$$$$$$$$$$$$EEEEEEEEEEEEFFFFFFFFFFFFGGGGGGGGGGGGHHHHHHHHHHHHIIIIIIIIIIJJJJJJJJJJJJ##############################################################')



    # 工数詳細ページ工数項目削除チェック
    def test_detail_item_edit(self):
        # フォームデータ定義
        form_data = {
            'start_time1' : '7:30',
            'end_time1' : '8:30',
            'item_edit': '変更1',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('detail', args = [self.Business_Time_graph.id]), form_data)
        # リクエストのレスポンスステータスコードが302(リダイレクト)であることを確認
        self.assertEqual(response.status_code, 302)

        # テストユーザーの工数データ取得
        updated_entry = Business_Time_graph.objects.get(employee_no3 = self.member.employee_no, \
                                                        work_day2 = self.Business_Time_graph.work_day2)
        # 作業内容が更新されていることを確認
        self.assertEqual(updated_entry.time_work, '##########################################################################################AAAAAAAAAAAA######BBBBBBBBBBBBCCCCCCCCCCCCDDDDDDDDDDDD$$$$$$$$$$$$EEEEEEEEEEEEFFFFFFFFFFFFGGGGGGGGGGGGHHHHHHHHHHHHIIIIIIIIIIJJJJJJJJJJJJ##############################################################')



    # 工数削除ページ工数削除チェック
    def test_delete_post(self):
        # フォームデータ定義
        form_data = {
            'kosu_delete' : '工数データ削除',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('delete', args = [self.Business_Time_graph.id]), form_data)
        # リクエストのレスポンスステータスコードが302(リダイレクト)であることを確認
        self.assertEqual(response.status_code, 302)

        # テストユーザーの工数データ取得
        updated_entry = Business_Time_graph.objects.filter(employee_no3 = self.member.employee_no, \
                                                           work_day2 = self.Business_Time_graph.work_day2)
        # レコードがないことを確認
        self.assertEqual(updated_entry.count(), 0)



    # 工数集計ページ検索チェック
    def test_total_post(self):
        # Business_Time_graphダミーデータ
        for day in range(1, 400):
            self.Business_Time_graph = Business_Time_graph.objects.create(
                employee_no3 = 111,
                name = self.member,
                def_ver2 = self.kosu_division.kosu_name,
                work_day2 = datetime.datetime.strptime('2000-01-01', '%Y-%m-%d').date() + datetime.timedelta(days = day),
                tyoku2 = '4',
                time_work = '################################################################################################AAAAAAAAAAAABBBBBBBBBBBBCCCCCCCCCCCCDDDDDDDDDDDD$$$$$$$$$$$$EEEEEEEEEEEEFFFFFFFFFFFFGGGGGGGGGGGGHHHHHHHHHHHHIIIIIIIIIIJJJJJJJJJJJJ##############################################################',
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


        # フォームデータ定義
        form_data = {
            'kosu_day' : self.Business_Time_graph.work_day2,
            'kosu_order': '1',
            'kosu_summarize' : '1',
            'kosu_find': '検索',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('total'), form_data)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)

        # 集計値が正しいか確認
        graph_list = list(response.context['graph_list'])
        expected_list = [60, 60, 60, 60, 60, 60, 60, 60, 50, 60]
        self.assertEqual(graph_list, expected_list)


        # フォームデータ定義
        form_data2 = {
            'kosu_day' : self.Business_Time_graph.work_day2,
            'kosu_order': '2',
            'kosu_summarize' : '1',
            'kosu_find': '検索',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('total'), form_data2)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)

        # 集計値が正しいか確認
        graph_list = list(response.context['graph_list'])
        expected_list = [60, 60, 60, 60, 60, 60, 60, 60, 60, 50]
        self.assertEqual(graph_list, expected_list)


        # フォームデータ定義
        form_data3 = {
            'kosu_day' : '2000-01-01',
            'kosu_order': '1',
            'kosu_summarize' : '2',
            'kosu_find': '検索',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('total'), form_data3)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)

        # 集計値が正しいか確認
        graph_list = list(response.context['graph_list'])
        expected_list = [1860, 1860, 1860, 1860, 1860, 1860, 1860, 1860, 1550, 1860]
        self.assertEqual(graph_list, expected_list)


        # フォームデータ定義
        form_data4 = {
            'kosu_day' : '2000-01-01',
            'kosu_order': '2',
            'kosu_summarize' : '2',
            'kosu_find': '検索',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('total'), form_data4)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)

        # 集計値が正しいか確認
        graph_list = list(response.context['graph_list'])
        expected_list = [1860, 1860, 1860, 1860, 1860, 1860, 1860, 1860, 1860, 1550]
        self.assertEqual(graph_list, expected_list)


        # フォームデータ定義
        form_data5 = {
            'kosu_day' : '2000-01-01',
            'kosu_order': '1',
            'kosu_summarize' : '3',
            'kosu_find': '検索',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('total'), form_data5)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)

        # 集計値が正しいか確認
        graph_list = list(response.context['graph_list'])
        expected_list = [21960, 21960, 21960, 21960, 21960, 21960, 21960, 21960, 18300, 21960]
        self.assertEqual(graph_list, expected_list)


        # フォームデータ定義
        form_data6 = {
            'kosu_day' : '2000-01-01',
            'kosu_order': '2',
            'kosu_summarize' : '3',
            'kosu_find': '検索',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('total'), form_data6)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)

        # 集計値が正しいか確認
        graph_list = list(response.context['graph_list'])
        expected_list = [21960, 21960, 21960, 21960, 21960, 21960, 21960, 21960, 21960, 18300]
        self.assertEqual(graph_list, expected_list)



    # 勤務入力ページ表示切替チェック
    def test_schedule_change(self):

        # フォームデータ定義
        form_data = {
            'year' : '2000',
            'month': '1',
            'time_update': '表示切替',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('schedule'), form_data)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)

        # 集計値が正しいか確認
        day_list = list(response.context['day_list'])
        expected_list = ['', '', '', '', '', '', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
        self.assertEqual(day_list, expected_list)


        # フォームデータ定義
        form_data2 = {
            'year' : '2000',
            'month': '2',
            'time_update': '表示切替',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('schedule'), form_data2)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)

        # 集計値が正しいか確認
        day_list = list(response.context['day_list'])
        expected_list = ['', '', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, '', '', '', '', '', '']
        self.assertEqual(day_list, expected_list)



    # 勤務入力ページ勤務登録チェック
    def test_schedule_post(self):

        # フォームデータ定義
        form_data = {
            'year' : '2000',
            'month': '1',
            'time_update': '表示切替',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('schedule'), form_data)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)

        # フォームデータ2定義
        form_data2 = {
            'day7': '休日',
            'day8': '休日',
            'day9': '',
            'day10': '',
            'day11': '',
            'day12': '',
            'day13': '',
            'day14': '',
            'day15': '',
            'day16': '',
            'day17': '',
            'day18': '',
            'day19': '',
            'day20': '',
            'day21': '',
            'day22': '',
            'day23': '',
            'day24': '',
            'day25': '',
            'day26': '',
            'day27': '',
            'day28': '',
            'day29': '',
            'day30': '',
            'day31': '',
            'day32': '',
            'day33': '',
            'day34': '',
            'day35': '',
            'day36': '',
            'day37': '',
            'work_update': '勤務登録',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('schedule'), form_data2)
        # リクエストのレスポンスステータスコードが302(リダイレクト)であることを確認
        self.assertEqual(response.status_code, 200)

        # テストユーザーの工数データ取得
        updated_entry1 = Business_Time_graph.objects.get(employee_no3 = self.member.employee_no, \
                                                        work_day2 = '2000-01-01')
        updated_entry2 = Business_Time_graph.objects.get(employee_no3 = self.member.employee_no, \
                                                        work_day2 = '2000-01-02')
        # 作業内容が更新されていることを確認
        self.assertEqual(updated_entry1.work_time, '休日')
        self.assertEqual(updated_entry2.work_time, '休日')



    # 残業管理ページ表示切替チェック
    def test_over_time_change(self):

        # フォームデータ定義
        form_data = {
            'year': '2000',
            'month': '1',
            'date_change': '表示切替',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('over_time'), form_data)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)

        # 集計値が正しいか確認
        week_list = list(response.context['week_list'])
        expected_list = ['土', '日', '月', '火', '水', '木', '金', '土', '日', '月', '火', '水', '木', '金', '土', '日', '月', '火', '水', '木', '金', '土', '日', '月', '火', '水', '木', '金', '土', '日', '月']
        self.assertEqual(week_list, expected_list)


        # フォームデータ定義
        form_data2 = {
            'year': '2000',
            'month': '2',
            'date_change': '表示切替',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('over_time'), form_data2)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)

        # 集計値が正しいか確認
        week_list = list(response.context['week_list'])
        expected_list = ['火', '水', '木', '金', '土', '日', '月', '火', '水', '木', '金', '土', '日', '月', '火', '水', '木', '金', '土', '日', '月', '火', '水', '木', '金', '土', '日', '月', '火']
        self.assertEqual(week_list, expected_list)



    #工数区分定義確認ページ表示切替チェック
    def test_kosu_def_change(self):

        # フォームデータ定義
        form_data = {
            'kosu_def_list': '工数区分名1',
            'def_find': '検索',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('kosu_def'), form_data)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['def1'], '定義1')
        self.assertEqual(response.context['def2'], '作業内容1')


        # フォームデータ定義
        form_data2 = {
            'kosu_def_list': '工数区分名2',
            'def_find': '検索',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('kosu_def'), form_data2)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['def1'], '定義2')
        self.assertEqual(response.context['def2'], '作業内容2')



    #工数区分定義切替ページ切替チェック
    def test_def_Ver_change(self):

        # kosu_divisionダミーデータ
        self.kosu_division = kosu_division.objects.create(
            kosu_name = 'トライ定義2',
            kosu_title_1 = '工数区分名A',
            kosu_division_1_1 = '定義A',
            kosu_division_2_1 = '作業内容A',
            kosu_title_2 = '工数区分名B',
            kosu_division_1_2 = '定義B',
            kosu_division_2_2 = '作業内容B',
            kosu_title_3 = '工数区分名C',
            kosu_division_1_3 = '定義C',
            kosu_division_2_3 = '作業内容C',
            kosu_title_4 = '工数区分名D',
            kosu_division_1_4 = '定義D',
            kosu_division_2_4 = '作業内容D',
            kosu_title_5 = '工数区分名E',
            kosu_division_1_5 = '定義E',
            kosu_division_2_5 = '作業内容E',
            kosu_title_6 = '工数区分名F',
            kosu_division_1_6 = '定義F',
            kosu_division_2_6 = '作業内容F',
            kosu_title_7 = '工数区分名G',
            kosu_division_1_7 = '定義G',
            kosu_division_2_7 = '作業内容G',
            kosu_title_8 = '工数区分名H',
            kosu_division_1_8 = '定義H',
            kosu_division_2_8 = '作業内容H',
            kosu_title_9 = '工数区分名I',
            kosu_division_1_9 = '定義I',
            kosu_division_2_9 = '作業内容I',
            kosu_title_10 = '工数区分名J',
            kosu_division_1_10 = '定義J',
            kosu_division_2_10 = '作業内容J',
            )

        # フォームデータ定義
        form_data = {
            'versionchoice': 'トライ定義',
            'def_change': '検索',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('kosu_Ver'), form_data)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)

        # セッションデータを確認
        session = self.client.session
        self.assertEqual(session['input_def'], 'トライ定義')


        # フォームデータ定義
        form_data2 = {
            'versionchoice': 'トライ定義2',
            'def_change': '検索',
            }

        # URLに対してPOSTリクエスト送信
        response = self.client.post(reverse('kosu_Ver'), form_data2)
        # レスポンスが成功（ステータスコード200）であることを確認
        self.assertEqual(response.status_code, 200)

        # セッションデータを確認
        session = self.client.session
        self.assertEqual(session['input_def'], 'トライ定義2')


















