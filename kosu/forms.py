from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from.models import member
from.models import kosu_division
from.models import administrator_data
from.models import inquiry_data





class memberForm(forms.ModelForm):
  class Meta:
    model = member
    fields = ['employee_no', 'name', 'shop', 'authority', 'administrator', 'break_time1', \
              'break_time1_over1', 'break_time1_over2', 'break_time1_over3', 'break_time2', \
              'break_time2_over1', 'break_time2_over2', 'break_time2_over3', 'break_time3', \
              'break_time3_over1', 'break_time3_over2', 'break_time3_over3', 'break_time4', \
              'break_time4_over1', 'break_time4_over2', 'break_time4_over3']

    widgets = {'employee_no': forms.NumberInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'name': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'shop': forms.Select(attrs={'class' : 'form-control custom-border', 'style' : 'width: 200px;'}),
               'authority' : forms.CheckboxInput(attrs={'class' : 'form-check-input'}),
               'administrator' : forms.CheckboxInput(attrs={'class' : 'form-check-input'}),
               }


class input_kosuForm(forms.Form):
  tyoku_list = [
    ('', ''),
    ('1', '1直'), 
    ('2', '2直'), 
    ('3', '3直'), 
    ('4', '常昼')]

  employment_list = [
    ('', ''),
    ('出勤', '出勤'),
    ('シフト出', 'シフト出'),
    ('休出', '休出'),
    ('半前年休', '半前年休'),
    ('半後年休', '半後年休'),
    ('早退', '早退・遅刻'),
    ]


  tyoku2 = forms.ChoiceField(label = '直', choices = tyoku_list, required = False, widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 90px;'}))
  tomorrow_check = forms.BooleanField(label = '翌日', required = False, widget = forms.CheckboxInput(attrs = {'class' : 'form-check-input'}))
  kosu_def_list = forms.ChoiceField(label = '工数区分', required = False, widget = forms.Select(attrs = {'class' : 'form-control custom-border', 'style' : 'width : 210px;'}))
  work_detail = forms.CharField(label = '作業詳細', required = False, widget = forms.TextInput(attrs = {'class' : 'form-control custom-border', 'placeholder' : '未入力可 メモで使用', 'style' : 'width : 210px;'}))
  over_work = forms.IntegerField(label = '残業', widget = forms.NumberInput(attrs = {'class' : 'form-control custom-border', 'style' : 'width : 80px;'}), required = False)
  work = forms.ChoiceField(label = '勤務', choices = employment_list, required = False, widget = forms.Select(attrs = {'class' : 'form-control custom-border', 'style' : 'width : 90px;'}))
  break_change = forms.BooleanField(label = '休憩変更', required = False, widget = forms.CheckboxInput(attrs = {'class' : 'form-check-input'}))



class loginForm(forms.Form):
  employee_no4 = forms.IntegerField(label = '従業員番号', widget = forms.NumberInput(attrs = {'class' : 'form-control custom-border', 'min' : 0, 'style' : 'width : 200px;'}), required = False)



class kosu_dayForm(forms.Form):
  order_list = [
    (1, '標準'),
    (2, '多い順'),
  ]

  summarize_list = [
    (1, '指定なし'),
    (2, '月間工数'),
    (3, '年間工数'),
  ]

  kosu_order = forms.ChoiceField(label = '並び順', choices = order_list, widget = forms.Select(attrs = {'class' : 'form-control custom-border', 'style' : 'width : 100px;'}))
  kosu_summarize = forms.ChoiceField(label = '期間指定', choices = summarize_list, widget = forms.Select(attrs = {'class' : 'form-control custom-border', 'style' : 'width : 100px;'}))



class member_findForm(forms.Form):
  shop_list = [
    ('', ''),
    ('P', 'プレス'),
    ('R', '成形'),
    ('W1', '301ボデ'),
    ('W2', '302ボデ'),
    ('T1', '301塗装'),
    ('T2', '302塗装'),
    ('A1', '301組立'),
    ('A2', '302組立'),
    ('その他', 'その他'),
    ('組長以上', '組長以上')
    ]
    
  employee_no6 = forms.IntegerField(label = '従業員番号', required = False, widget = forms.NumberInput(attrs = {'class' : 'form-control custom-border', 'min' : 0, 'style' : 'width : 200px;'}))
  shop2 = forms.ChoiceField(label = 'ショップ', choices = shop_list, required = False, widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}))



class inputdayForm(forms.Form):
  tomorrow_check = forms.BooleanField(label = '日跨ぎ', required = False, widget = forms.CheckboxInput(attrs = {'class' : 'form-check-input'}))
  kosu_def_list = forms.ChoiceField(label = '工数区分', required = False, widget = forms.Select(attrs = {'class' : 'form-control custom-border', 'style' : 'width : 210px;'}))



class teamForm(forms.Form):
  member1 = forms.ChoiceField(label = 'メンバー従業員番号1', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)
  member2 = forms.ChoiceField(label = 'メンバー従業員番号2', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)
  member3 = forms.ChoiceField(label = 'メンバー従業員番号3', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)
  member4 = forms.ChoiceField(label = 'メンバー従業員番号4', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)
  member5 = forms.ChoiceField(label = 'メンバー従業員番号5', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)
  member6 = forms.ChoiceField(label = 'メンバー従業員番号6', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)
  member7 = forms.ChoiceField(label = 'メンバー従業員番号7', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)
  member8 = forms.ChoiceField(label = 'メンバー従業員番号8', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)
  member9 = forms.ChoiceField(label = 'メンバー従業員番号9', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)
  member10 = forms.ChoiceField(label = 'メンバー従業員番号10', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)
  member11 = forms.ChoiceField(label = 'メンバー従業員番号11', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)
  member12 = forms.ChoiceField(label = 'メンバー従業員番号12', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)
  member13 = forms.ChoiceField(label = 'メンバー従業員番号13', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)
  member14 = forms.ChoiceField(label = 'メンバー従業員番号14', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)
  member15 = forms.ChoiceField(label = 'メンバー従業員番号15', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)

  follow = forms.BooleanField(label = 'フォローON/OFF', required = False, widget = forms.CheckboxInput(attrs = {'class' : 'form-check-input'}))



class team_kosuForm(forms.Form):
  employee_no6 = forms.ChoiceField(label = '従業員番号', widget = forms.Select(attrs ={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)



class versionchoiceForm(forms.Form):
  versionchoice = forms.ChoiceField(label = '工数区分定義ver選択', widget = forms.Select(attrs = {'class' : 'form-control custom-border', 'style' : 'width : 210px;'}))



class kosu_divisionForm(forms.ModelForm):
  class Meta:
    model = kosu_division
    fields = ['kosu_name', 'kosu_title_1', 'kosu_division_1_1', 'kosu_division_2_1', \
              'kosu_title_2', 'kosu_division_1_2', 'kosu_division_2_2', \
              'kosu_title_3', 'kosu_division_1_3', 'kosu_division_2_3', \
              'kosu_title_4', 'kosu_division_1_4', 'kosu_division_2_4', \
              'kosu_title_5', 'kosu_division_1_5', 'kosu_division_2_5', \
              'kosu_title_6', 'kosu_division_1_6', 'kosu_division_2_6', \
              'kosu_title_7', 'kosu_division_1_7', 'kosu_division_2_7', \
              'kosu_title_8', 'kosu_division_1_8', 'kosu_division_2_8', \
              'kosu_title_9', 'kosu_division_1_9', 'kosu_division_2_9', \
              'kosu_title_10', 'kosu_division_1_10', 'kosu_division_2_10', \
              'kosu_title_11', 'kosu_division_1_11', 'kosu_division_2_11', \
              'kosu_title_12', 'kosu_division_1_12', 'kosu_division_2_12', \
              'kosu_title_13', 'kosu_division_1_13', 'kosu_division_2_13', \
              'kosu_title_14', 'kosu_division_1_14', 'kosu_division_2_14', \
              'kosu_title_15', 'kosu_division_1_15', 'kosu_division_2_15', \
              'kosu_title_16', 'kosu_division_1_16', 'kosu_division_2_16', \
              'kosu_title_17', 'kosu_division_1_17', 'kosu_division_2_17', \
              'kosu_title_18', 'kosu_division_1_18', 'kosu_division_2_18', \
              'kosu_title_19', 'kosu_division_1_19', 'kosu_division_2_19', \
              'kosu_title_20', 'kosu_division_1_20', 'kosu_division_2_20', \
              'kosu_title_21', 'kosu_division_1_21', 'kosu_division_2_21', \
              'kosu_title_22', 'kosu_division_1_22', 'kosu_division_2_22', \
              'kosu_title_23', 'kosu_division_1_23', 'kosu_division_2_23', \
              'kosu_title_24', 'kosu_division_1_24', 'kosu_division_2_24', \
              'kosu_title_25', 'kosu_division_1_25', 'kosu_division_2_25', \
              'kosu_title_26', 'kosu_division_1_26', 'kosu_division_2_26', \
              'kosu_title_27', 'kosu_division_1_27', 'kosu_division_2_27', \
              'kosu_title_28', 'kosu_division_1_28', 'kosu_division_2_28', \
              'kosu_title_29', 'kosu_division_1_29', 'kosu_division_2_29', \
              'kosu_title_30', 'kosu_division_1_30', 'kosu_division_2_30', \
              'kosu_title_31', 'kosu_division_1_31', 'kosu_division_2_31', \
              'kosu_title_32', 'kosu_division_1_32', 'kosu_division_2_32', \
              'kosu_title_33', 'kosu_division_1_33', 'kosu_division_2_33', \
              'kosu_title_34', 'kosu_division_1_34', 'kosu_division_2_34', \
              'kosu_title_35', 'kosu_division_1_35', 'kosu_division_2_35', \
              'kosu_title_36', 'kosu_division_1_36', 'kosu_division_2_36', \
              'kosu_title_37', 'kosu_division_1_37', 'kosu_division_2_37', \
              'kosu_title_38', 'kosu_division_1_38', 'kosu_division_2_38', \
              'kosu_title_39', 'kosu_division_1_39', 'kosu_division_2_39', \
              'kosu_title_40', 'kosu_division_1_40', 'kosu_division_2_40', \
              'kosu_title_41', 'kosu_division_1_41', 'kosu_division_2_41', \
              'kosu_title_42', 'kosu_division_1_42', 'kosu_division_2_42', \
              'kosu_title_43', 'kosu_division_1_43', 'kosu_division_2_43', \
              'kosu_title_44', 'kosu_division_1_44', 'kosu_division_2_44', \
              'kosu_title_45', 'kosu_division_1_45', 'kosu_division_2_45', \
              'kosu_title_46', 'kosu_division_1_46', 'kosu_division_2_46', \
              'kosu_title_47', 'kosu_division_1_47', 'kosu_division_2_47', \
              'kosu_title_48', 'kosu_division_1_48', 'kosu_division_2_48', \
              'kosu_title_49', 'kosu_division_1_49', 'kosu_division_2_49', \
              'kosu_title_50', 'kosu_division_1_50', 'kosu_division_2_50', ]

    widgets = {'kosu_name': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_title_1': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_1': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_1': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_2': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_2': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_2': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_3': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_3': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_3': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_4': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_4': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_4': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_5': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_5': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_5': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_6': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_6': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_6': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_1': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_1': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_1': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_2': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_2': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_2': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_3': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_3': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_3': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_4': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_4': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_4': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_5': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_5': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_5': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_6': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_6': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_6': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_7': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_7': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_7': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_8': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_8': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_8': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_9': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_9': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_9': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_10': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_10': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_10': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_11': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_11': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_11': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_12': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_12': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_12': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_13': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_13': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_13': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_14': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_14': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_14': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_15': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_15': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_15': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_16': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_16': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_16': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_17': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_17': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_17': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_18': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_18': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_18': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_19': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_19': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_19': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_20': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_20': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_20': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_21': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_21': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_21': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_22': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_22': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_22': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_23': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_23': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_23': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_24': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_24': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_24': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_25': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_25': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_25': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_26': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_26': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_26': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_27': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_27': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_27': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_28': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_28': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_28': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_29': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_29': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_29': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_30': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_30': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_30': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_31': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_31': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_31': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_32': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_32': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_32': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_33': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_33': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_33': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_34': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_34': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_34': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_35': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_35': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_35': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_36': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_36': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_36': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_37': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_37': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_37': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_38': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_38': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_38': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_39': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_39': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_39': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_40': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_40': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_40': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_41': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_41': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_41': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_42': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_42': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_42': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_43': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_43': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_43': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_44': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_44': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_44': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_45': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_45': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_45': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_46': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_46': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_46': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_47': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_47': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_47': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_48': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_48': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_48': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_49': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_49': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_49': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_title_50': forms.TextInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'kosu_division_1_50': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'kosu_division_2_50': forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'})}













class scheduleForm(forms.Form):
  employment_list = [
    ('', ''),
    ('出勤', '出勤'),
    ('シフト出', 'シフト出'),
    ('休出', '休出'),
    ('休日', '休日'),
    ('年休', '年休'),
    ('半前年休', '半前年休'),
    ('半後年休', '半後年休'),
    ('公休', '公休'),
    ('シフト休', 'シフト休'),
    ('代休', '代休'),
    ('早退', '早退・遅刻'),
    ]
  
  day1 = forms.ChoiceField(label = '日1', choices=employment_list, required = False)
  day2 = forms.ChoiceField(label = '月1', choices=employment_list, required = False)
  day3 = forms.ChoiceField(label = '火1', choices=employment_list, required = False)
  day4 = forms.ChoiceField(label = '水1', choices=employment_list, required = False)
  day5 = forms.ChoiceField(label = '木1', choices=employment_list, required = False)
  day6 = forms.ChoiceField(label = '金1', choices=employment_list, required = False)
  day7 = forms.ChoiceField(label = '土1', choices=employment_list, required = False)
  day8 = forms.ChoiceField(label = '日2', choices=employment_list, required = False)
  day9 = forms.ChoiceField(label = '月2', choices=employment_list, required = False)
  day10 = forms.ChoiceField(label = '火2', choices=employment_list, required = False)
  day11 = forms.ChoiceField(label = '水2', choices=employment_list, required = False)
  day12 = forms.ChoiceField(label = '木2', choices=employment_list, required = False)
  day13 = forms.ChoiceField(label = '金2', choices=employment_list, required = False)
  day14 = forms.ChoiceField(label = '土2', choices=employment_list, required = False)
  day15 = forms.ChoiceField(label = '日3', choices=employment_list, required = False)
  day16 = forms.ChoiceField(label = '月3', choices=employment_list, required = False)
  day17 = forms.ChoiceField(label = '火3', choices=employment_list, required = False)
  day18 = forms.ChoiceField(label = '水3', choices=employment_list, required = False)
  day19 = forms.ChoiceField(label = '木3', choices=employment_list, required = False)
  day20 = forms.ChoiceField(label = '金3', choices=employment_list, required = False)
  day21 = forms.ChoiceField(label = '土3', choices=employment_list, required = False)
  day22 = forms.ChoiceField(label = '日4', choices=employment_list, required = False)
  day23 = forms.ChoiceField(label = '月4', choices=employment_list, required = False)
  day24 = forms.ChoiceField(label = '火4', choices=employment_list, required = False)
  day25 = forms.ChoiceField(label = '水4', choices=employment_list, required = False)
  day26 = forms.ChoiceField(label = '木4', choices=employment_list, required = False)
  day27 = forms.ChoiceField(label = '金4', choices=employment_list, required = False)
  day28 = forms.ChoiceField(label = '土4', choices=employment_list, required = False)
  day29 = forms.ChoiceField(label = '日5', choices=employment_list, required = False)
  day30 = forms.ChoiceField(label = '月5', choices=employment_list, required = False)
  day31 = forms.ChoiceField(label = '火5', choices=employment_list, required = False)
  day32 = forms.ChoiceField(label = '水5', choices=employment_list, required = False)
  day33 = forms.ChoiceField(label = '木5', choices=employment_list, required = False)
  day34 = forms.ChoiceField(label = '金5', choices=employment_list, required = False)
  day35 = forms.ChoiceField(label = '土5', choices=employment_list, required = False)
  day36 = forms.ChoiceField(label = '日6', choices=employment_list, required = False)
  day37 = forms.ChoiceField(label = '月6', choices=employment_list, required = False)



class schedule_timeForm(forms.Form):
  year_list = [
    (2024, 2024),
    (2025, 2025),
    (2026, 2026),
    (2027, 2027),
    (2028, 2028),
    (2029, 2029),
    (2030, 2030),
    (2031, 2031),
    (2032, 2032),
    (2033, 2033),
    (2034, 2034),
    (2035, 2035),
    ]
  
  month_list = [
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (11, 11),
    (12, 12),
    (1, 1),
    (2, 2),
    (3, 3),
  ]

  year = forms.ChoiceField(label = '年', choices=year_list, widget = forms.Select(attrs = {'class' : 'form-control custom-border', 'style' : 'width : 80px;'}))
  month = forms.ChoiceField(label = '月', choices=month_list, widget = forms.Select(attrs = {'class' : 'form-control custom-border', 'style' : 'width : 50px;'}))



class administrator_data_Form(forms.ModelForm):
  class Meta:
    model = administrator_data
    fields = [
      'menu_row', 
      'administrator_employee_no1', 
      'administrator_employee_no2', 
      'administrator_employee_no3']

    widgets = {'menu_row' : forms.NumberInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'administrator_employee_no1' : forms.NumberInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'administrator_employee_no2' : forms.NumberInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'administrator_employee_no3' : forms.NumberInput(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'})}



class uploadForm(forms.Form):
  kosu_file = forms.FileField(label = '工数ファイル選択', required = False)
  team_file = forms.FileField(label = '班員ファイル選択', required = False)
  member_file = forms.FileField(label = '人員ファイル選択', required = False)
  def_file = forms.FileField(label = '工数区分定義ファイル選択', required = False)
  inquiry_file = forms.FileField(label = 'お問い合わせファイル選択', required = False)
  setting_file = forms.FileField(label = '設定ファイル選択', required = False)



class inquiryForm(forms.ModelForm):
  class Meta:
    model = inquiry_data
    fields = ['employee_no2', 'content_choice', 'inquiry', 'answer']
    
    widgets = {'content_choice' : forms.Select(attrs={'class' : 'form-control custom-border', 'style' : 'width : 200px;'}),
               'inquiry' : forms.Textarea(attrs={'placeholder': '可能限り具体的に記入下さい。', 'class' : 'form-control custom-border', 'style' : 'width : 350px;'}),
               'answer' : forms.Textarea(attrs={'class' : 'form-control custom-border', 'style' : 'width : 350px;'})}





class inquiry_findForm(forms.Form):
  category_list = [
    ('', ''),
    ('要望', '要望'),
    ('不具合', '不具合'),
    ('問い合わせ' ,'問い合わせ'),
    ]

  category = forms.ChoiceField(label = 'カテゴリー', widget = forms.Select(attrs = {'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), choices = category_list, required = False)
  name_list = forms.ChoiceField(label = '氏名', widget = forms.Select(attrs = {'class' : 'form-control custom-border', 'style' : 'width : 200px;'}), required = False)

