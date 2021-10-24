
from django.contrib import admin
from django.urls import path,include
from . import views
from . import settings
from django.conf.urls.static import static 
from django.conf.urls import url
from django.views.static import serve

admin.site.site_header = "iCoder Admin"
admin.site.site_title = "iCoder Admin Panel"
admin.site.index_title = "Welcome to iCoder Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('shop.urls')),
    path('prac/',views.prac, name='prac'),
    path("Json/",views.jsondata,name = "jsondata"),

    path('signup',views.signup,name='signup'),
    path('login',views.userlogin,name='login'),
    path('logout/',views.userlogout,name='logout'),

    path('changepass/', views.MyPasswordChangeView.as_view(), name='changepass'), 
    path('password_change_done/', views.MyPasswordChangeDoneView.as_view(), name='password_change_done'),
    
    path('password_reset/', views.MyPasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/', views.MyPasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/', views.MyPasswordResetCompleteView.as_view(),name='password_reset_complete'),

    url(r'^media/(?P<path>.*)$', serve,{'document_root':  settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
