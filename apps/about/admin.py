from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Profile, Service, Testimonial, Client


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای مدیریت پروفایل
    """
    list_display = ['name', 'job_title', 'email', 'phone', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'job_title', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    # تقسیم بندی فیلدها در صفحه ویرایش
    fieldsets = (
        (_('اطلاعات شخصی'), {
            'fields': ('name', 'job_title', 'bio', 'birth_date', 'location')
        }),
        (_('اطلاعات تماس'), {
            'fields': ('email', 'phone', 'skype')
        }),
        (_('فایلها'), {
            'fields': ('avatar', 'resume_file')
        }),
        (_('شبکه های اجتماعی'), {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url')
        }),
        (_('تاریخ ها'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # این بخش به صورت بسته نمایش داده می شود
        })
    )
    
    def has_add_permission(self, request):
        """
        فقط اجازه ایجاد یک پروفایل
        """
        return not Profile.objects.exists()


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای مدیریت خدمات
    """
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']  # امکان ویرایش مستقیم در لیست
    ordering = ['order', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('اطلاعات خدمت'), {
            'fields': ('title', 'description', 'icon')
        }),
        (_('تنظیمات نمایش'), {
            'fields': ('order', 'is_active')
        }),
        (_('تاریخ ها'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای مدیریت نظرات مشتریان
    """
    list_display = ['name', 'rating_stars', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['name', 'comment']
    list_editable = ['is_active']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('اطلاعات نظر'), {
            'fields': ('name', 'comment', 'avatar', 'rating')
        }),
        (_('تنظیمات نمایش'), {
            'fields': ('is_active',)
        }),
        (_('تاریخ ها'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def rating_stars(self, obj):
        """
        نمایش امتیاز به صورت ستاره
        """
        stars = '⭐' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: gold;">{}</span>', stars)
    rating_stars.short_description = _('امتیاز')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای مدیریت مشتریان
    """
    list_display = ['name', 'url', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'url']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('اطلاعات مشتری'), {
            'fields': ('name', 'logo', 'url')
        }),
        (_('تنظیمات نمایش'), {
            'fields': ('order', 'is_active')
        }),
        (_('تاریخ ها'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )