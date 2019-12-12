from django import forms

from ticketing.models import Cinema


class ShowTimeSearchForm(forms.Form):
    PRICE_ANY = '0'
    PRICE_UNDER_10 = '1'
    PRICE_10_TO_15 = '2'
    PRICE_15_TO_20 = '3'
    PRICE_ABOVE_20 = '4'
    PRICE_LEVEL_CHOICES = (
        (PRICE_ANY, 'هر قیمتی'),
        (PRICE_UNDER_10, 'تا ۱۰ هزار تومان'),
        (PRICE_10_TO_15, '۱۰ تا ۱۵ هزار تومان'),
        (PRICE_15_TO_20, '۱۵ تا ۲۰ هزار تومان'),
        (PRICE_ABOVE_20, 'بیش از ۲۰ هزار تومان'),
    )

    movie_name = forms.CharField(label='عنوان فیلم', max_length=100, required=False)
    sale_is_open = forms.BooleanField(label='فقط سانس‌های قابل خرید', required=False)
    movie_length_min = forms.IntegerField(label='حداقل زمان فیلم', min_value=0, max_value=200, required=False)
    movie_length_max = forms.IntegerField(label='حداکثر زمان فیلم', min_value=0, max_value=200, required=False)
    cinema = forms.ModelChoiceField(label='سینما', required=False, queryset=Cinema.objects.all())
    price_level = forms.ChoiceField(label='محدوده قیمت', choices=PRICE_LEVEL_CHOICES, required=False)

    def get_price_boundries(self):
        price_level = self.cleaned_data['price_level']
        if price_level == ShowTimeSearchForm.PRICE_UNDER_10:
            return None, 10000
        elif price_level == ShowTimeSearchForm.PRICE_10_TO_15:
            return 10000, 15000
        elif price_level == ShowTimeSearchForm.PRICE_15_TO_20:
            return 15000, 20000
        elif price_level == ShowTimeSearchForm.PRICE_ABOVE_20:
            return 20000, None
        else:
            return None, None
