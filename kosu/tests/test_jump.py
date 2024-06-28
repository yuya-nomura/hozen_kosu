from django.test import TestCase, Client
from django.urls import reverse
import os
from kosu.models import member
from kosu.models import kosu_division
from kosu.models import administrator_data
from kosu.models import Business_Time_graph
from kosu.models import team_member
from kosu.models import inquiry_data





class Page_jump(TestCase):
    # ダミーデータ定義
    def setUp(self):        
        # memberダミーデータ
        self.member = member.objects.create(
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
        self.administrator_data = administrator_data.objects.create(
            menu_row = 20,
            administrator_employee_no1 = '111',
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
            employee_no3 = 111,
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
        self.inquiry_data = inquiry_data.objects.create(
            employee_no2 = 111,
            name = self.member,
            content_choice = '問い合わせ',
            inquiry = '',
            answer = '回答'
            )

        # テストクライアント初期化
        self.client = Client()

        # セッション定義
        self.session = self.client.session
        self.session['login_No'] = self.member.employee_no
        self.session['input_def'] =  self.kosu_division.kosu_name
        self.session['day'] =  self.Business_Time_graph.work_day2
        self.session['break_today'] =  self.Business_Time_graph.work_day2
        self.session.save()



    # ログイン画面からヘルプ画面へジャンプテスト
    def test_login_help_jump(self):
        # セッション削除
        session = self.client.session
        del session['login_No']
        session.save()

        # ログインページにアクセス
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        # リンクが含まれているか確認する
        self.assertContains(response, f'href="{reverse('help')}"')
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('help'))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/help.html')



    # ヘルプからログインへジャンプテスト
    def test_help_login_jump(self):
        # ヘルプページにアクセス
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, 200)

        # セッション削除
        session = self.client.session
        del session['login_No']
        session.save()

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('login') + '" class="text-dark h6">ログインページへ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('login'))

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/login.html')



    # ヘルプパスワード入力後に画面切り替わるかテスト
    def test_help_display(self):
        # 環境変数からHELP_PATHを取得
        help_path = os.getenv('HELP_PATH')

        # 特定の値を入力してフォームを送信する
        response = self.client.post(reverse('help'),{
            'help_path': help_path,
            'help_button': '決定'
            }
        )

        # レスポンスが成功したことを確認
        self.assertEqual(response.status_code, 200)
        # display変数がTrueになることを確認
        self.assertTrue(response.context['display'])



    # ログインできるかテスト
    def test_login_jump(self):
        # フォームの値を定義
        data = {
            'employee_no4': self.member.employee_no
            }
        # ログインページにアクセスしてフォームにデータを投稿します
        response = self.client.post(reverse('login'), data)

        # リダイレクトされているかを確認
        self.assertRedirects(response, reverse('main'))



    # MAINから工数MENUへジャンプテスト
    def test_main_kosu_jump(self):
        # メインページにアクセス
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        
        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, 'onclick="location.href=\'/kosu_main\'"')
        # ボタンを押すシミュレーション
        response = self.client.get('/kosu_main')
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/kosu_main.html')



    # 工数MENUからMAINへジャンプテスト
    def test_kosu_main_jump(self):
        # 工数MENUページにアクセス
        response = self.client.get(reverse('kosu_main'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('main') + '">メインMENUへ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('main'))

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/main.html')



    # MAINから工数定義区分MENUへジャンプテスト
    def test_main_def_jump(self):
        # メインページにアクセス
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        
        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, 'onclick="location.href=\'/def_main\'"')
        # ボタンを押すシミュレーション
        response = self.client.get('/def_main')
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/def_main.html')



    # 工数定義区分MENUからMAINへジャンプテスト
    def test_def_main_jump(self):
        # 工数MENUページにアクセス
        response = self.client.get(reverse('def_main'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('main') + '" class="text-success">メインMENUへ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('main'))

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/main.html')



    # MAINから人員MENUへジャンプテスト
    def test_main_member_jump(self):
        # メインページにアクセス
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        
        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, 'onclick="location.href=\'/member_main\'"')
        # ボタンを押すシミュレーション
        response = self.client.get('/member_main')
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/member_main.html')



    # 人員MENUからMAINへジャンプテスト
    def test_member_main_jump(self):
        # 人員MENUページにアクセス
        response = self.client.get(reverse('member_main'))
        self.assertEqual(response.status_code, 200)
        
        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('main') + '" class="text-warning">メインMENUへ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('main'))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/main.html')



    # MAINから班員MENUへジャンプテスト
    def test_main_team_jump(self):
        # メインページにアクセス
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        
        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, 'onclick="location.href=\'/team_main\'"')
        # ボタンを押すシミュレーション
        response = self.client.get('/team_main')
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/team_main.html')



    # 班員MENUからMAINへジャンプテスト
    def test_team_main_jump(self):
        # 班員MENUページにアクセス
        response = self.client.get(reverse('team_main'))
        self.assertEqual(response.status_code, 200)
        
        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('main') + '" class="text-danger">メインMENUへ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('main'))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/main.html')



    # MAINから問い合わせMENUへジャンプテスト
    def test_main_inquiry_jump(self):
        # メインページにアクセス
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        
        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, 'onclick="location.href=\'/inquiry_main\'"')
        # ボタンを押すシミュレーション
        response = self.client.get('/inquiry_main')
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/inquiry_main.html')



    # 問い合わせMENUからMAINへジャンプテスト
    def test_inquiry_main_jump(self):
        # 問い合わせMENUページにアクセス
        response = self.client.get(reverse('inquiry_main'))
        self.assertEqual(response.status_code, 200)
        
        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('main') + '" class="text-pink">メインMENUへ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('main'))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/main.html')



    # MAINから管理者MENUへジャンプテスト
    def test_main_administrator_jump(self):
        # メインページにアクセス
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        
        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, 'onclick="location.href=\'/administrator\'"')
        # ボタンを押すシミュレーション
        response = self.client.get('/administrator')
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/administrator_menu.html')



    # 管理者MENUからMAINへジャンプテスト
    def test_administrator_main_jump(self):
        # 管理者MENUページにアクセス
        response = self.client.get(reverse('administrator'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('main') + '" class="text-dark">メインMENUへ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('main'))

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/main.html')



    # ログアウトテスト
    def test_logout(self):
        # メインページにアクセス
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        # ログアウトボタンを押す
        response = self.client.post(reverse('main'), {
            'btn-blue2': 'ログアウト'
        })

        # ログアウトボタンを押した後に 'login' ページにリダイレクトされることを確認
        self.assertRedirects(response, reverse('login'))
        


    # 工数MENUから工数登録へジャンプテスト
    def test_kosu_MENU_input_jump(self):
        # 工数MENUページにアクセス
        response = self.client.get(reverse('kosu_main'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, 'onclick="location.href=\'/input\'"')
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('input'))

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/input.html')



    # 工数登録から工数MENUへジャンプテスト
    def test_input_kosu_MENU_jump(self):
        # 工数登録ページにアクセス
        response = self.client.get(reverse('input'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('kosu_main') + '" >工数MENUへ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('kosu_main'))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/kosu_main.html')



    # 工数登録から工数履歴へジャンプテスト
    def test_input_kosu_list_jump(self):
        # 工数登録ページにアクセス
        response = self.client.get(reverse('input'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('kosu_list', args = [1]) + '" >履歴へ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('kosu_list', args = [1]))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/kosu_list.html')



    # 工数履歴から工数登録へジャンプテスト
    def test_kosu_list_input_jump(self):
        # 工数履歴ページにアクセス
        response = self.client.get(reverse('kosu_list', args = [1]))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('input') + '" >工数入力へ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('input'))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/input.html')



    # 工数登録から工数編集へジャンプテスト
    def test_input_detail_jump(self):
        # 工数登録ページにアクセス
        response = self.client.get(reverse('input'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('detail', args = [self.Business_Time_graph.id]) + '" >工数編集</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('detail', args = [self.Business_Time_graph.id]))

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/detail.html')



    # 工数編集から工数登録へジャンプテスト
    def test_detail_input_jump(self):
        # 工数編集ページにアクセス
        response = self.client.get(reverse('detail', args = [self.Business_Time_graph.id]))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('input') + '" >工数入力へ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('input'))

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/input.html')



    # 工数登録から当日休憩変更へジャンプテスト
    def test_input_today_break_time(self):
        # 工数登録ページにアクセス
        response = self.client.get(reverse('input'))
        self.assertEqual(response.status_code, 200)

        # 休憩変更登録を押す
        response = self.client.post(reverse('input'), {
            'work_day': self.Business_Time_graph.work_day2,
            'change_display': '休憩変更登録'
        })

        # 休憩変更登録を押した後に 'today_break_time' ページにリダイレクトされることを確認
        self.assertRedirects(response, reverse('today_break_time'))



    # 当日休憩変更から工数登録へジャンプテスト
    def test_today_break_time_input(self):
        # 当日休憩変更ページにアクセス
        response = self.client.get(reverse('today_break_time'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('input') + '" >工数入力へ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('input'))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/input.html')



    # 工数MENUから休憩設定へジャンプテスト
    def test_kosu_MENU_break_time_jump(self):
        # 工数MENUページにアクセス
        response = self.client.get(reverse('kosu_main'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, 'onclick="location.href=\'/break_time\'"')
        # ボタンを押すシミュレーション
        response = self.client.get('/break_time')

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/break_time.html')



    # 休憩設定から工数MENUへジャンプテスト
    def test_break_time_kosu_MENU_jump(self):
        # 休憩設定ページにアクセス
        response = self.client.get(reverse('break_time'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('kosu_main') + '" >工数MENUへ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('kosu_main'))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/kosu_main.html')



    # 工数MENUから工数履歴へジャンプテスト
    def test_kosu_MENU_kosu_list_jump(self):
        # 工数MENUページにアクセス
        response = self.client.get(reverse('kosu_main'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, 'onclick="location.href=\'/list/1\'"')
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('kosu_list', args = [1]))

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/kosu_list.html')



    # 工数履歴から工数MENUへジャンプテスト
    def test_kosu_list_kosu_MENU_jump(self):
        # 工数履歴ページにアクセス
        response = self.client.get(reverse('kosu_list', args = [1]))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('kosu_main') + '" >工数MENUへ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('kosu_main'))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/kosu_main.html')



    # 工数履歴から工数データへジャンプテスト
    def test_kosu_list_graph_jump(self):
        # 工数データページにアクセス
        response = self.client.get(reverse('kosu_list', args = [1]))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('graph', args = [1]) + '" >データ確認</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('graph', args = [1]))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/graph.html')



    # 工数データから工数履歴へジャンプテスト
    def test_graph_kosu_list_jump(self):
        # 工数データページにアクセス
        response = self.client.get(reverse('graph', args = [1]))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('kosu_list', args = [1]) + '" >工数一覧へ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('kosu_list', args = [1]))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/kosu_list.html')



    # 工数データから工数MENUへジャンプテスト
    def test_graph_kosu_main_jump(self):
        # 工数データページにアクセス
        response = self.client.get(reverse('graph', args = [1]))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('kosu_main') + '" >工数MENUへ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('kosu_main'))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/kosu_main.html')



    # 工数履歴から工数詳細へジャンプテスト
    def test_kosu_list_detail_jump(self):
        # 工数履歴ページにアクセス
        response = self.client.get(reverse('kosu_list', args = [1]))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('detail', args=[self.Business_Time_graph.id]) + '">詳細</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('detail', args = [self.Business_Time_graph.id]))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/detail.html')



    # 工数詳細から工数履歴へジャンプテスト
    def test_detail_kosu_list_jump(self):
        # 工数詳細ページにアクセス
        response = self.client.get(reverse('detail', args=[self.Business_Time_graph.id]))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('kosu_list', args = [1]) + '" >履歴へ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('kosu_list', args = [1]))

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/kosu_list.html')



    # 工数履歴から工数削除へジャンプテスト
    def test_kosu_list_delete_jump(self):
        # 工数履歴ページにアクセス
        response = self.client.get(reverse('kosu_list', args = [1]))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('delete', args=[self.Business_Time_graph.id]) + '">削除</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('delete', args = [self.Business_Time_graph.id]))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/delete.html')



    # 工数削除から工数履歴へジャンプテスト
    def test_delete_kosu_list_jump(self):
        # 工数詳細ページにアクセス
        response = self.client.get(reverse('delete', args=[self.Business_Time_graph.id]))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('kosu_list', args = [1]) + '" >履歴へ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('kosu_list', args = [1]))

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/kosu_list.html')



    # 工数MENUから工数集計へジャンプテスト
    def test_kosu_MENU_kosu_total_jump(self):
        # 工数MENUページにアクセス
        response = self.client.get(reverse('kosu_main'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, 'onclick="location.href=\'/total\'"')
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('total'))

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/total.html')



    # 工数集計から工数MENUへジャンプテスト
    def test_total_kosu_MENU_jump(self):
        # 工数集計ページにアクセス
        response = self.client.get(reverse('total'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('kosu_main') + '" >工数MENUへ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('kosu_main'))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/kosu_main.html')



    # 工数MENUから勤務入力へジャンプテスト
    def test_kosu_MENU_kosu_schedule_jump(self):
        # 工数MENUページにアクセス
        response = self.client.get(reverse('kosu_main'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, 'onclick="location.href=\'/schedule\'"')
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('schedule'))

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/schedule.html')



    # 勤務入力から工数MENUへジャンプテスト
    def test_schedule_kosu_MENU_jump(self):
        # 工数集計ページにアクセス
        response = self.client.get(reverse('schedule'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('kosu_main') + '" >工数MENUへ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('kosu_main'))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/kosu_main.html')



    # 工数MENUから残業管理へジャンプテスト
    def test_kosu_MENU_kosu_over_time_jump(self):
        # 工数MENUページにアクセス
        response = self.client.get(reverse('kosu_main'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, 'onclick="location.href=\'/over_time\'"')
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('over_time'))

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/over_time.html')



    # 残業管理から工数MENUへジャンプテスト
    def test_over_time_kosu_MENU_jump(self):
        # 工数集計ページにアクセス
        response = self.client.get(reverse('over_time'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, '<a href="' + reverse('kosu_main') + '" >工数MENUへ</a>', html=True)
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('kosu_main'))
        
        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/kosu_main.html')



    # 工数区分定義MENUから工数区分定義確認へジャンプテスト
    def test_def_MENU_kosu_def_jump(self):
        # 工数区分定義MENUページにアクセス
        response = self.client.get(reverse('def_main'))
        self.assertEqual(response.status_code, 200)

        # HTMLに含まれるボタンが正しく設定されているかを確認
        self.assertContains(response, 'onclick="location.href=\'/kosu_def\'"')
        # ボタンを押すシミュレーション
        response = self.client.get(reverse('kosu_def'))

        # リダイレクトが成功し、ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kosu/kosu_def.html')
















