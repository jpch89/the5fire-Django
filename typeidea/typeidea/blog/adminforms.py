from django import forms


class PostAdminForm(forms.ModelForm):
    # form 的 label 是在修改页面中显示的名称
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
