from django.urls import path
from . import views
from .views import *



urlpatterns = [
    #path('url-name' , function-name)
    
    path('room_List/',RoomListView, name='RoomListView'),
    path('booking_list/', BookingList.as_view(), name='BookingListView'),
    path('total/', views.total, name='total'),
    #path('book/', BookingView.as_view(), name='bookingview'),
    path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),
    path('about' , views.about ,name='about'),
    path('post-details/<int:id>' , views.post_details, name="post-details"),
    path('table' , views.table , name = 'table'),
    path('export-csv' , views.export_csv , name="export-csv"),
    path('test' , views.test , name="test"),
    path('' , views.index , name = "index"),
    
    path('rooms' , views.rooms , name = "rooms"),
    path('room-details' , views.room_details , name = "room-details"),
    path('blog' , views.blog , name = "blog"),
    path('blog-details' , views.blog_details , name = "blog-details"),
    path('contact' , views.contact , name = "contact"),
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('booking/cancel/<pk>' , CancelBookingView.as_view() , name='CancelBookingView'),
    path('pdf' , views.PDF , name='pdf')
   
    
]