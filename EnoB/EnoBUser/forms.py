from django import forms
from .models import EnoB_user

class RegisterForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': '이메일을 입력해주세요.'
        },
        max_length=64, label='이메일'
    )

    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호'
    )

    re_password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호 확인'
    )
    
    username = forms.CharField(
        error_messages={
            'required': '이름을 입력하세요.'
        },
        max_length=64, label='이름'
    )

    phone = forms.CharField(
        error_messages={
            'required': '핸드폰 번호를 입력해주세요.'
        },
        max_length=64, label = '핸드폰 번호'
    )

    birth = forms.CharField(
        error_messages={
            'required': '생년월일을 입력해주세요. ex)19940112'
        },
        max_length=64, label = '생년월일'
    )

    sex = forms.CharField(
        error_messages={
            'required': '성별을 입력해주세요.'
        },
        max_length=64, label = '성별'
    )

    

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        username = cleaned_data.get('username')
        phone = cleaned_data.get('phone')
        birth= cleaned_data.get('birth')
        sex = cleaned_data.get('sex')

        if password and re_password:
            if password != re_password:
                self.add_error('password', '비밀번호가 서로 다릅니다.')
                self.add_error('re_password', '비밀번호가 서로 다릅니다.')
            else:
                user = EnoB_user(
                    email = email,
                    password = password,
                    username = username,
                    phone = phone,
                    birth = birth,
                    sex = sex
                )
                user.save()