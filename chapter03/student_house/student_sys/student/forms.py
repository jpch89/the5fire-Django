from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            'name', 'sex', 'profession',
            'email', 'qq', 'phone',
        )

    # 表单字段校验的方法名必须这么写：clean_字段名
    def clean_qq(self):
        cleaned_data = self.cleaned_data['qq']
        if not cleaned_data.isdigit():
            raise forms.ValidationError('必须是数字！')
        return int(cleaned_data)
