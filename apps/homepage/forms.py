from django import forms


def generate_attr(name):
    return {'placeholder': "{0:s}".format(name), 'class': 'form-control'}


class UserMessageForm(forms.Form):
    action = '/homepage/#contact'

    name = forms.CharField(label="", widget=forms.TextInput(attrs=generate_attr('名字')), max_length=16)
    contact = forms.CharField(label="", widget=forms.TextInput(attrs=generate_attr('电话或微信')), max_length=16)
    comment_attr = generate_attr('留言')
    comment_attr['rows'] = '5'
    comment = forms.CharField(label="", widget=forms.Textarea(attrs=comment_attr), max_length=128)

