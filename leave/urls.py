from django.urls import path, include
from . import views

urlpatterns = [
    path("home", views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('apply/leave/', views.apply, name='apply'),
    path('approve/leave/', views.approvelist, name='approve'),
    path('holiday/', views.holidays, name='holiday'),
    path('approved/leave/<int:id>/', views.approve, name='approved'),
    path('reject/leave/<int:id>/', views.rejectleave, name='rejectleave'),
    path('vet/leave/', views.vetlist, name='vet'),
    path('vetting/leave/<int:id>/', views.vet, name='vetting'),
    path('rejectvet/leave/<int:id>/', views.rejectvet, name='rejectvet'),
    path('delete/holiday/<int:id>/', views.delholiday, name='delete_holiday'),

    path('my/leave/', views.myleave, name='myleave'),
    path('statistics/leave/', views.stats, name='stats'),
    path('get_leave_spent/<int:user_id>/', views.get_leave_spent, name='get_leave_spent'),

    path('birthday_celebrants/', views.BirthdayCelebrantView.as_view(), name='birthday_celebrants'),
]
