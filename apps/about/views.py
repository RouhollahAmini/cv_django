from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import logging

from .models import Profile, Service, Testimonial, Client

# تنظیم logger برای ثبت خطاها
logger = logging.getLogger(__name__)


class AboutView(TemplateView):
    """
    View صفحه درباره من
    
    این view اطلاعات پروفایل، خدمات، نظرات و مشتریان را نمایش می دهد
    """
    template_name = 'about/index.html'
    
    @method_decorator(cache_page(60 * 15))  # کش کردن برای 15 دقیقه
    def dispatch(self, *args, **kwargs):
        """
        این متد قبل از اجرای get یا post اجرا می شود
        اینجا کش را فعال می کنیم
        """
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
        این متد داده هایی که به template ارسال می شود را آماده می کند
        """
        context = super().get_context_data(**kwargs)
        
        try:
            # دریافت اطلاعات پروفایل (فقط یکی وجود دارد)
            profile = Profile.objects.first()
            
            # دریافت خدمات فعال به ترتیب order
            services = Service.active.all()
            
            # دریافت نظرات فعال
            testimonials = Testimonial.active.all()
            
            # دریافت مشتریان فعال
            clients = Client.active.all()
            
            # اضافه کردن داده ها به context
            context.update({
                'profile': profile,
                'services': services,
                'testimonials': testimonials,
                'clients': clients,
            })
            
        except Exception as e:
            # در صورت بروز خطا، خطا را لاگ می کنیم
            logger.error(f'خطا در بارگذاری صفحه درباره من: {str(e)}')
            
            # داده های خالی برای جلوگیری از خطا
            context.update({
                'profile': None,
                'services': [],
                'testimonials': [],
                'clients': [],
            })
        
        return context


# Function-based view برای سازگاری با کدهای قدیمی
def about_view(request):
    """
    همان AboutView ولی به صورت function
    """
    view = AboutView.as_view()
    return view(request)