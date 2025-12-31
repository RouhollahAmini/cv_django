from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class ContactMessage(TimeStampedModel):
    """
    مدل پیام های تماس
    
    پیام هایی که کاربران از طریق فرم تماس ارسال می کنند
    """
    # اطلاعات فرستنده
    name = models.CharField(
        max_length=100, 
        verbose_name=_('نام'),
        help_text=_('نام فرستنده پیام')
    )
    email = models.EmailField(
        verbose_name=_('ایمیل'),
        help_text=_('ایمیل فرستنده پیام')
    )
    phone = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name=_('تلفن'),
        help_text=_('شماره تلفن فرستنده (اختیاری)')
    )
    
    # محتوای پیام
    subject = models.CharField(
        max_length=200, 
        verbose_name=_('موضوع'),
        help_text=_('موضوع پیام')
    )
    message = models.TextField(
        verbose_name=_('پیام'),
        help_text=_('متن پیام')
    )
    
    # وضعیت پیام
    STATUS_CHOICES = [
        ('new', _('جدید')),
        ('read', _('خوانده شده')),
        ('replied', _('پاسخ داده شده')),
        ('archived', _('آرشیو شده')),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name=_('وضعیت'),
        help_text=_('وضعیت پیام')
    )
    
    # یادداشت ادمین
    admin_notes = models.TextField(
        blank=True,
        verbose_name=_('یادداشت ادمین'),
        help_text=_('یادداشت داخلی برای ادمین')
    )
    
    class Meta:
        verbose_name = _('پیام تماس')
        verbose_name_plural = _('پیام های تماس')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.name} - {self.subject}'
    
    def mark_as_read(self):
        """
        علامت گذاری پیام به عنوان خوانده شده
        """
        if self.status == 'new':
            self.status = 'read'
            self.save(update_fields=['status'])
    
    def mark_as_replied(self):
        """
        علامت گذاری پیام به عنوان پاسخ داده شده
        """
        self.status = 'replied'
        self.save(update_fields=['status'])


class ContactInfo(TimeStampedModel):
    """
    مدل اطلاعات تماس
    
    اطلاعات تماس که در صفحه تماس نمایش داده می شود
    """
    # اطلاعات تماس
    address = models.TextField(
        verbose_name=_('آدرس'),
        help_text=_('آدرس کامل')
    )
    phone = models.CharField(
        max_length=20, 
        verbose_name=_('تلفن'),
        help_text=_('شماره تلفن')
    )
    email = models.EmailField(
        verbose_name=_('ایمیل'),
        help_text=_('آدرس ایمیل')
    )
    
    # ساعات کاری
    working_hours = models.TextField(
        verbose_name=_('ساعات کاری'),
        help_text=_('ساعات کاری مثل: شنبه تا چهارشنبه 9 تا 17')
    )
    
    # موقعیت جغرافیایی برای نقشه
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        null=True, 
        blank=True,
        verbose_name=_('عرض جغرافیایی'),
        help_text=_('عرض جغرافیایی برای نمایش در نقشه')
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        null=True, 
        blank=True,
        verbose_name=_('طول جغرافیایی'),
        help_text=_('طول جغرافیایی برای نمایش در نقشه')
    )
    
    # تنظیمات
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('فعال'),
        help_text=_('آیا این اطلاعات فعال است؟')
    )
    
    class Meta:
        verbose_name = _('اطلاعات تماس')
        verbose_name_plural = _('اطلاعات تماس')
    
    def __str__(self):
        return f'اطلاعات تماس - {self.email}'
    
    def save(self, *args, **kwargs):
        """
        فقط یک رکورد اطلاعات تماس فعال مجاز است
        """
        if self.is_active:
            # غیرفعال کردن سایر رکوردها
            ContactInfo.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)