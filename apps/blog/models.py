from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel, SEOModel


class Category(BaseModel, SEOModel):
    """
    مدل دسته بندی مقالات
    
    مقالات را می توان در دسته بندی های مختلف قرار داد
    """
    name = models.CharField(
        max_length=100, 
        verbose_name=_('نام'),
        help_text=_('نام دسته بندی مثل: برنامه نویسی')
    )
    slug = models.SlugField(
        max_length=100, 
        unique=True,
        verbose_name=_('اسلاگ'),
        help_text=_('نام انگلیسی برای URL مثل: programming')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('توضیحات'),
        help_text=_('توضیح کوتاه درباره این دسته بندی')
    )
    color = models.CharField(
        max_length=7, 
        default='#007bff',
        verbose_name=_('رنگ'),
        help_text=_('رنگ دسته بندی به صورت HEX مثل: #007bff')
    )
    
    class Meta:
        verbose_name = _('دسته بندی')
        verbose_name_plural = _('دسته بندی ها')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """
        لینک صفحه این دسته بندی
        """
        return reverse('blog:category', kwargs={'slug': self.slug})


class Tag(BaseModel):
    """
    مدل تگ های مقالات
    
    هر مقاله می تواند چندین تگ داشته باشد
    """
    name = models.CharField(
        max_length=50, 
        verbose_name=_('نام'),
        help_text=_('نام تگ مثل: Django')
    )
    slug = models.SlugField(
        max_length=50, 
        unique=True,
        verbose_name=_('اسلاگ'),
        help_text=_('نام انگلیسی برای URL')
    )
    
    class Meta:
        verbose_name = _('تگ')
        verbose_name_plural = _('تگ ها')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Post(BaseModel, SEOModel):
    """
    مدل مقالات وبلاگ
    
    هر مقاله شامل عنوان، محتوا، تصویر، دسته بندی و تگ است
    """
    title = models.CharField(
        max_length=200, 
        verbose_name=_('عنوان'),
        help_text=_('عنوان مقاله')
    )
    slug = models.SlugField(
        max_length=200, 
        unique=True,
        verbose_name=_('اسلاگ'),
        help_text=_('نام انگلیسی برای URL')
    )
    excerpt = models.TextField(
        max_length=300,
        verbose_name=_('خلاصه'),
        help_text=_('خلاصه کوتاه مقاله (حداکثر 300 کاراکتر)')
    )
    content = models.TextField(
        verbose_name=_('محتوا'),
        help_text=_('محتوای کامل مقاله')
    )
    featured_image = models.ImageField(
        upload_to='blog/posts/', 
        verbose_name=_('تصویر شاخص'),
        help_text=_('تصویر اصلی مقاله')
    )
    
    # روابط
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        verbose_name=_('دسته بندی'),
        help_text=_('دسته بندی این مقاله')
    )
    tags = models.ManyToManyField(
        Tag, 
        blank=True,
        verbose_name=_('تگ ها'),
        help_text=_('تگ های مربوط به این مقاله')
    )
    
    # آمار
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('تعداد بازدید'),
        help_text=_('تعداد بازدید این مقاله')
    )
    
    # تنظیمات انتشار
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_('مقاله ویژه'),
        help_text=_('آیا این مقاله ویژه است؟')
    )
    published_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاریخ انتشار'),
        help_text=_('تاریخ انتشار مقاله')
    )
    
    class Meta:
        verbose_name = _('مقاله')
        verbose_name_plural = _('مقالات')
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
        اگر slug وارد نشده، از عنوان ایجاد می کنیم
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """
        لینک صفحه این مقاله
        """
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        """
        افزایش تعداد بازدید
        """
        self.views_count += 1
        self.save(update_fields=['views_count'])


class Comment(BaseModel):
    """
    مدل نظرات مقالات
    
    کاربران می توانند برای مقالات نظر بگذارند
    """
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('مقاله'),
        help_text=_('مقاله مربوط به این نظر')
    )
    name = models.CharField(
        max_length=100, 
        verbose_name=_('نام'),
        help_text=_('نام نظر دهنده')
    )
    email = models.EmailField(
        verbose_name=_('ایمیل'),
        help_text=_('ایمیل نظر دهنده')
    )
    website = models.URLField(
        blank=True,
        verbose_name=_('وب سایت'),
        help_text=_('وب سایت نظر دهنده (اختیاری)')
    )
    content = models.TextField(
        verbose_name=_('متن نظر'),
        help_text=_('متن نظر')
    )
    
    # نظر والد برای پاسخ به نظرات
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name=_('پاسخ به'),
        help_text=_('اگر این نظر پاسخ به نظر دیگری است')
    )
    
    class Meta:
        verbose_name = _('نظر')
        verbose_name_plural = _('نظرات')
        ordering = ['created_at']
    
    def __str__(self):
        return f'{self.name} - {self.post.title}'