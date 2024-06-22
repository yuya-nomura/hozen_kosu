from django.test import TestCase
from django.urls import reverse
from kosu.models import member
from kosu.models import kosu_division
from kosu.models import Business_Time_graph
from kosu.models import team_member
from kosu.models import administrator_data





class MultiplePagesAccessTestCase(TestCase):
    def setUp(self):        
        # memberオブジェクトの作成
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

        self.administrator_data = administrator_data.objects.create(
            menu_row = 20,
            administrator_employee_no1 = '11111',
            administrator_employee_no2 = '',
            administrator_employee_no3 = '',
            )

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
    


    def test_help(self):
        url = reverse('help')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ヘルプ')



    def test_login(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ログイン')
    


    def test_main(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MENU')



    def test_kosu_main(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('kosu_main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '工数MENU')



    def test_def_main(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('def_main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '工数区分定義MENU')



    def test_member_main(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('member_main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '人員MENU')



    def test_team_main(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('team_main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '班員MENU')



    def test_inquiry_main(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('inquiry_main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '問い合わせMENU')



    def test_administrator(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('administrator')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '管理者MENU')



    def test_input(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()
        url = reverse('input')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'テストユーザーさんの工数登録')



    def test_today_break_time(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session['break_today'] = self.Business_Time_graph.work_day2
        session.save()
        url = reverse('today_break_time')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2000年1月1日の休憩変更')



    def test_break_time(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('break_time')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '休憩時間定義')



    def test_kosu_list(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('kosu_list', args = [1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'テストユーザーさんの工数履歴')



    def test_detail(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()
        url = reverse('detail', args = [self.Business_Time_graph.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2000年1月1日の工数詳細')



    def test_delete(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()
        url = reverse('delete', args = [self.Business_Time_graph.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '工数データ削除')



    def test_graph(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('graph', args = [1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '工数データ')



    def test_total(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()
        url = reverse('total')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'テストユーザーさんの工数集計')



    def test_schedule(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('schedule')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '勤務入力')



    def test_over_time(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('over_time')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '残業管理')



    def test_kosu_def(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()
        url = reverse('kosu_def')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '工数区分定義確認')



    def test_kosu_Ver(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()
        url = reverse('kosu_Ver')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '工数区分定義切り替え')



    def test_def_list(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()
        url = reverse('def_list', args = [1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '工数区分定義一覧')



    def test_def_new(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()
        url = reverse('def_new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '工数区分定義新規登録')



    def test_def_edit(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()
        url = reverse('def_edit', args = [self.kosu_division.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '工数区分定義編集')



    def test_def_delete(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()
        url = reverse('def_delete', args = [self.kosu_division.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '工数区分定義削除')



    def test_member_new(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('member_new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '人員登録')



    def test_member(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('member', args = [1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '人員一覧')



    def test_member_edit(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('member_edit', args = [self.member.employee_no])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '人員編集')



    def test_member_delete(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('member_delete', args = [self.member.employee_no])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '人員削除')



    def test_team(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('team')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'テストユーザーさんの班員設定')



    def test_team_graph(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session['input_def'] = self.kosu_division.kosu_name
        session.save()
        url = reverse('team_graph')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '班員工数グラフ')



    def test_team_kosu(self):
        session = self.client.session
        session['login_No'] = self.member.employee_no
        session.save()
        url = reverse('team_kosu', args = [1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'テストユーザーさん班員工数確認')



