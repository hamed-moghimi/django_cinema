from django import forms


class ShowTimeSearchForm(forms.Form):
    movie_name = forms.CharField(label='عنوان فیلم', max_length=100, required=False)
