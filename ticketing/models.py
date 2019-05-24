from django.db import models


class Movie(models.Model):
    """
    Represents a movie
    """

    class Meta:
        verbose_name = 'فیلم'
        verbose_name_plural = 'فیلم'

    name = models.CharField('عنوان', max_length=100)
    director = models.CharField('کارگردان', max_length=50)
    year = models.IntegerField('سال تولید')
    length = models.IntegerField('مدت زمان')
    description = models.TextField('توضیح فیلم')

    def __str__(self):
        return self.name


class Cinema(models.Model):
    """
    Represents a cinema (movie theater)
    """

    class Meta:
        verbose_name = 'سینما'
        verbose_name_plural = 'سینما'

    name = models.CharField('نام', max_length=50)
    city = models.CharField('شهر', max_length=30, default='تهران')
    capacity = models.IntegerField('گنجایش')
    phone = models.CharField('تلفن', max_length=30, blank=True)
    address = models.TextField('آدرس')

    def __str__(self):
        return self.name


class ShowTime(models.Model):
    """
    Represents a movie show in a cinema at a specific time
    """

    class Meta:
        verbose_name = 'سانس'
        verbose_name_plural = 'سانس'

    # read more about on_delete from
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.ForeignKey.on_delete
    # choices are PROTECT, CASCADE, SET_NULL, SET_DEFAULT, SET(), DO_NOTHING
    movie = models.ForeignKey('Movie', on_delete=models.PROTECT, verbose_name='فیلم')
    cinema = models.ForeignKey('Cinema', on_delete=models.PROTECT, verbose_name='سینما')

    start_time = models.DateTimeField('زمان شروع نمایش')
    price = models.IntegerField('قیمت')
    salable_seats = models.IntegerField('صندلی‌های قابل فروش')
    free_seats = models.IntegerField('صندلی‌های خالی')

    SALE_NOT_STARTED = 1
    SALE_OPEN = 2
    TICKETS_SOLD = 3
    SALE_CLOSED = 4
    MOVIE_PLAYED = 5
    SHOW_CANCELED = 6
    status_choices = (
        (SALE_NOT_STARTED, 'فروش آغاز نشده'),
        (SALE_OPEN, 'در حال فروش بلیت'),
        (TICKETS_SOLD, 'بلیت‌ها تمام شد'),
        (SALE_CLOSED, 'فروش بلیت بسته شد'),
        (MOVIE_PLAYED, 'فیلم پخش شد'),
        (SHOW_CANCELED, 'سانس لغو شد'),
    )
    status = models.IntegerField('وضعیت', choices=status_choices, default=SALE_NOT_STARTED)

    def __str__(self):
        return '{} - {} - {}'.format(self.movie, self.cinema, self.start_time)

    def get_price_display(self):
        return '{} تومان'.format(self.price)

    def is_full(self):
        """
        Returns True if all seats are sold
        """
        return self.free_seats == 0

    def open_sale(self):
        """
        Opens ticket sale
        If sale was opened before, raises an exception
        """
        if self.status == ShowTime.SALE_NOT_STARTED:
            self.status = ShowTime.SALE_OPEN
            self.save()
        else:
            raise Exception('Sale has been started before')

    def close_sale(self):
        """
        Closes ticket sale
        If sale is not open, raises an exception
        """
        if self.status == ShowTime.SALE_OPEN:
            self.status = ShowTime.SALE_CLOSED
            self.save()
        else:
            raise Exception('Sale is not open')

    def expire_showtime(self, is_canceled=False):
        """
        Expires showtime and updates the status
        :param is_canceled: A boolean indicating whether the show is canceled or not, default is False
        """
        if self.status not in (ShowTime.MOVIE_PLAYED, ShowTime.SHOW_CANCELED):
            self.status = ShowTime.SHOW_CANCELED if is_canceled else ShowTime.MOVIE_PLAYED
            self.save()
        else:
            raise Exception('Show has been expired before')
