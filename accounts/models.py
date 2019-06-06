from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Represents a user's profile
    """

    class Meta:
        verbose_name = 'نمایه کاربری'
        verbose_name_plural = 'نمایه کاربری'

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='حساب کاربری')
    # important fields that are stored in User model:
    #   first_name, last_name, email, date_joined

    mobile = models.CharField('تلفن همراه', max_length=11)

    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = ((MALE, 'مرد'), (FEMALE, 'زن'))
    gender = models.IntegerField('جنسیت', choices=GENDER_CHOICES, null=True, blank=True)

    birth_date = models.DateField('تاریخ تولد', null=True, blank=True)
    address = models.TextField('آدرس', null=True, blank=True)
    profile_image = models.ImageField('تصویر', upload_to='users/profile_images/', null=True, blank=True)

    # fields related to tickets
    balance = models.IntegerField('اعتبار', default=0)

    def __str__(self):
        return self.user.get_full_name()

    def get_balance_display(self):
        return '{} تومان'.format(self.balance)

    # behaviors
    def deposit(self, amount):
        self.balance += amount
        self.save()

    def spend(self, amount):
        if self.balance < amount:
            return False
        self.balance -= amount
        self.save()
        return True
