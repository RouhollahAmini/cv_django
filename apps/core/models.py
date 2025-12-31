from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    مدل پایه که تاریخ ایجاد و بروزرسانی را به همه مدلها اضافه می کند
    
    این مدل abstract است یعنی جدول جداگانه ای برای آن ساخته نمی شود
    بلکه فقط فیلدهایش به مدلهای دیگر اضافه می شود
    """
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('تاریخ ایجاد'),
        help_text=_('تاریخ و زمان ایجاد رکورد')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('تاریخ بروزرسانی'),
        help_text=_('تاریخ و زمان آخرین بروزرسانی')
    )
    
    class Meta:
        abstract = True  # این مدل abstract است


class ActiveManager(models.Manager):
    """
    Manager سفارشی که فقط رکورdhای فعال را برمی گرداند
    
    استفاده:
    MyModel.active.all()  # فقط رکوردهای فعال
    MyModel.objects.all()  # همه رکوردها
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class BaseModel(TimeStampedModel):
    """
    مدل پایه برای همه مدلهایی که نیاز به فعال/غیرفعال کردن دارند
    
    این مدل شامل:
    - فیلد is_active برای فعال/غیرفعال کردن
    - فیلد order برای مرتب سازی
    - Manager های پیش فرض و فعال
    """
    is_active = models.BooleanField(
        default=True, 
        verbose_name=_('فعال'),
        help_text=_('آیا این رکورد فعال است؟')
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name=_('ترتیب'),
        help_text=_('ترتیب نمایش (عدد کمتر اول نمایش داده می شود)')
    )
    
    # Manager های مختلف
    objects = models.Manager()  # Manager پیش فرض - همه رکوردها
    active = ActiveManager()    # Manager فعال - فقط رکوردهای فعال
    
    class Meta:
        abstract = True
        ordering = ['order', 'created_at']  # مرتب سازی پیش فرض


class SEOModel(models.Model):
    """
    مدل پایه برای SEO
    فیلدهای مربوط به سئو را به مدلها اضافه می کند
    """
    meta_title = models.CharField(
        max_length=60, 
        blank=True,
        verbose_name=_('عنوان متا'),
        help_text=_('عنوان صفحه برای موتورهای جستجو (حداکثر 60 کاراکتر)')
    )
    meta_description = models.TextField(
        max_length=160, 
        blank=True,
        verbose_name=_('توضیحات متا'),
        help_text=_('توضیحات صفحه برای موتورهای جستجو (حداکثر 160 کاراکتر)')
    )
    meta_keywords = models.CharField(
        max_length=255, 
        blank=True,
        verbose_name=_('کلمات کلیدی'),
        help_text=_('کلمات کلیدی با کاما جدا شده')
    )
    
    class Meta:
        abstract = True