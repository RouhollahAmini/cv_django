from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, BaseModel


class Profile(TimeStampedModel):
    """
    مدل پروفایل شخصی
    
    این مدل اطلاعات شخصی کاربر را نگهداری می کند
    فقط یک پروفایل در سیستم وجود دارد
    """
    # اطلاعات شخصی
    name = models.CharField(
        max_length=100, 
        verbose_name=_('نام'),
        help_text=_('نام کامل شما')
    )
    job_title = models.CharField(
        max_length=100, 
        verbose_name=_('عنوان شغلی'),
        help_text=_('مثل: توسعه دهنده فول استک')
    )
    bio = models.TextField(
        verbose_name=_('بیوگرافی'),
        help_text=_('توضیح کوتاه درباره خودتان')
    )
    birth_date = models.CharField(
        max_length=50, 
        verbose_name=_('تاریخ تولد'),
        help_text=_('مثل: 9 بهمن 1375')
    )
    location = models.CharField(
        max_length=100, 
        verbose_name=_('محل سکونت'),
        help_text=_('مثل: ایران، تهران')
    )
    
    # اطلاعات تماس
    email = models.EmailField(
        verbose_name=_('ایمیل'),
        help_text=_('آدرس ایمیل شما')
    )
    phone = models.CharField(
        max_length=20, 
        verbose_name=_('تلفن'),
        help_text=_('شماره تلفن همراه')
    )
    skype = models.CharField(
        max_length=100, 
        verbose_name=_('اسکایپ'),
        help_text=_('نام کاربری اسکایپ')
    )
    
    # فایلها
    avatar = models.ImageField(
        upload_to='avatars/', 
        verbose_name=_('تصویر پروفایل'),
        help_text=_('تصویر پروفایل شما')
    )
    resume_file = models.FileField(
        upload_to='resumes/', 
        verbose_name=_('فایل رزومه'),
        help_text=_('فایل PDF رزومه شما')
    )
    
    # شبکه های اجتماعی
    facebook_url = models.URLField(
        blank=True, 
        verbose_name=_('لینک فیسبوک'),
        help_text=_('آدرس صفحه فیسبوک شما')
    )
    twitter_url = models.URLField(
        blank=True, 
        verbose_name=_('لینک توییتر'),
        help_text=_('آدرس صفحه توییتر شما')
    )
    linkedin_url = models.URLField(
        blank=True, 
        verbose_name=_('لینک لینکدین'),
        help_text=_('آدرس صفحه لینکدین شما')
    )
    
    class Meta:
        verbose_name = _('پروفایل')
        verbose_name_plural = _('پروفایل')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """
        فقط یک پروفایل در سیستم مجاز است
        """
        if not self.pk and Profile.objects.exists():
            raise ValueError('فقط یک پروفایل مجاز است')
        super().save(*args, **kwargs)


class Service(BaseModel):
    """
    مدل خدمات
    
    خدماتی که ارائه می دهید (مثل طراحی وب، برنامه نویسی و...)
    """
    title = models.CharField(
        max_length=100, 
        verbose_name=_('عنوان'),
        help_text=_('عنوان خدمت مثل: طراحی وب سایت')
    )
    description = models.TextField(
        verbose_name=_('توضیحات'),
        help_text=_('توضیح کامل درباره این خدمت')
    )
    icon = models.ImageField(
        upload_to='services/', 
        verbose_name=_('آیکون'),
        help_text=_('آیکون مربوط به این خدمت')
    )
    
    class Meta:
        verbose_name = _('خدمت')
        verbose_name_plural = _('خدمات')
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.title


class Testimonial(BaseModel):
    """
    مدل نظرات مشتریان
    
    نظرات و بازخوردهای مشتریان درباره کار شما
    """
    name = models.CharField(
        max_length=100, 
        verbose_name=_('نام'),
        help_text=_('نام مشتری')
    )
    comment = models.TextField(
        verbose_name=_('نظر'),
        help_text=_('نظر مشتری درباره کار شما')
    )
    avatar = models.ImageField(
        upload_to='testimonials/', 
        verbose_name=_('تصویر'),
        help_text=_('تصویر مشتری')
    )
    rating = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('امتیاز'),
        help_text=_('امتیاز از 1 تا 5')
    )
    
    class Meta:
        verbose_name = _('نظر مشتری')
        verbose_name_plural = _('نظرات مشتریان')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.name} - {self.rating} ستاره'


class Client(BaseModel):
    """
    مدل مشتریان
    
    لوگو و اطلاعات مشتریانی که با آنها کار کرده اید
    """
    name = models.CharField(
        max_length=100, 
        verbose_name=_('نام'),
        help_text=_('نام شرکت یا مشتری')
    )
    logo = models.ImageField(
        upload_to='clients/', 
        verbose_name=_('لوگو'),
        help_text=_('لوگو شرکت یا مشتری')
    )
    url = models.URLField(
        blank=True, 
        verbose_name=_('آدرس وب سایت'),
        help_text=_('آدرس وب سایت مشتری')
    )
    
    class Meta:
        verbose_name = _('مشتری')
        verbose_name_plural = _('مشتریان')
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.name