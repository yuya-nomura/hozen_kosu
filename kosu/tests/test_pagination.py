from django.test import TestCase, Client
from django.urls import reverse
from kosu.models import member, administrator_data



# ページネーションテスト
class MemberPaginationTest(TestCase):
    # 初期データ作成
    @classmethod
    def setUpTestData(cls):
        # 100人のメンバーを作成
        for member_id in range(100):
            member.objects.create(
                employee_no=member_id,
                name='test',
                shop='その他',
                authority=True,
                administrator=True,
                break_time1='#10401130',
                break_time1_over1='#15101520',
                break_time1_over2='#20202110',
                break_time1_over3='#01400150',
                break_time2='#17501840',
                break_time2_over1='#22302240',
                break_time2_over2='#03400430',
                break_time2_over3='#09000910',
                break_time3='#01400230',
                break_time3_over1='#07050715',
                break_time3_over2='#12151305',
                break_time3_over3='#17351745',
                break_time4='#12001300',
                break_time4_over1='#19001915',
                break_time4_over2='#01150215',
                break_time4_over3='#06150630',
            )
        
        # administrator_dataダミーデータ
        cls.administrator_data = administrator_data.objects.create(
            menu_row=20,
            administrator_employee_no1='1',
            administrator_employee_no2='',
            administrator_employee_no3='',
        )



    # 初期データ
    def setUp(self):
        # テストクライアント初期化
        self.client = Client()

        # セッション定義
        self.session = self.client.session
        self.session['login_No'] = 1
        self.session.save()



    # 人員一覧で1ページに表示するデータ数チェック
    def test_pagination_is_working(self):
        # 必要なページ数
        total_pages = (100 // self.administrator_data.menu_row) + 1

        # 1ページ毎にテスト
        for page_num in range(1, total_pages + 1):
            # 各ページのレスポンスをGETリクエストで取得
            response = self.client.get(reverse('member', kwargs={'num': page_num}))
            # レスポンスのステータスコードが200（成功）であることを確認
            self.assertEqual(response.status_code, 200)
            # コンテキストに 'data' が含まれているかを確認
            self.assertTrue('data' in response.context)
            # 各ページに表示される期待されるアイテム数を計算
            expected_items = self.administrator_data.menu_row if page_num < total_pages else (100 % self.administrator_data.menu_row)
            # 実際のアイテム数と期待されるアイテム数が一致するかを確認
            self.assertEqual(len(response.context['data']), expected_items)



    # 人員一覧で各ページのページネーション表示が正しいかテスト
    def test_pagination_links(self):
        # 必要なページ数
        total_pages = (100 // self.administrator_data.menu_row) + 1

        # 1ページ毎にテスト
        for page_num in range(1, total_pages + 1):
            # 各ページのレスポンスをGETリクエストで取得
            response = self.client.get(reverse('member', kwargs={'num': page_num}))
            # レスポンスのステータスコードが200（成功）であることを確認
            self.assertEqual(response.status_code, 200)

            # 1ページ目以降の場合、最初のページと前のページのリンクの存在を確認
            if page_num > 1:
                # 最初のページのリンク
                self.assertContains(response, reverse('member', kwargs={'num': 1}))
                # 前のページのリンク
                self.assertContains(response, reverse('member', kwargs={'num': page_num - 1}))

            # 最後のページ以前の場合、次のページと最後のページのリンクの存在を確認
            if page_num < total_pages:
                # 次のページのリンク
                self.assertContains(response, reverse('member', kwargs={'num': page_num + 1}))
                # 最後のページのリンク
                self.assertContains(response, reverse('member', kwargs={'num': total_pages}))

