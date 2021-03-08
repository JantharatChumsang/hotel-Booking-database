from django.shortcuts import render, HttpResponse , redirect
from django.http import HttpResponse
from datetime import datetime
from .models import *
import csv
from django.db.models import Q
from django.urls import reverse , reverse_lazy
from django.shortcuts import render ,HttpResponse
from django.views.generic import ListView, FormView, View , DeleteView
from .forms import AvailabilityForm
from blogapp.booking_functions.availability import check_availability
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .form_regis import NewUSerForm
from django.db import connection


# Create your views here.

def RoomListView(request):

    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)
    
    room_values = room_categories.values()

    room_list = []
    for room_category in room_categories:
        room = room_categories.get(room_category)
        room_url = reverse('RoomDetailView' , kwargs ={'category' : room_category} )

        room_list.append( (room , room_url ))
    context = {
        "room_list" : room_list,
    }
    return render(request , 'blogapp/room_list_views.html' , context)

#class BookingList(ListView):
    
    #model = Booking
    #print('model')
class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'blogapp/booking_cancel_view.html'
    success_url = reverse_lazy('BookingListView')

class BookingList(ListView):
    model = Booking

    template_name = 'blogapp/booking_list_view.html'
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()            
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list
# class TotalPayment(ListView):
#     template_name = 'blogapp/total.html'
#     def get_queryset(self, *args, **kwargs):

        
#         if self.request.user.is_staff:
#             with connection.cursor() as cursor:
#                 cursor.execute( " select sum(ad.total) "
#                                 " from (select (br2.cost  * (DATE_PART('day' , check_out ::date ) - DATE_PART('day' , check_in ::date))) as total "
# 		                        " from blogapp_booking bb2 "
#                                 " join blogapp_room br2 on bb2.room_id = br2.id"
# 		                        " join blogapp_room br2 on bb2.room_id = br2.id) as ad "
#                                 " ") 
#                 row = dictfetchall(cursor)
#                 column_name = [col[0] for col in cursor.description]

#             data = dict()
#             data['column_name'] = column_name
#             data['data'] = row

#             return data
#         else:
#             user=self.request.user
#             with connection.cursor() as cursor:
#                 cursor.execute( " select sum(ad.total) "
#                                 " from (select au.username ,(br2.cost  * (DATE_PART('day' , check_out ::date ) - DATE_PART('day' , check_in ::date))) as total "
# 		                        " from blogapp_booking bb2 "
#                                 " join blogapp_room br2 on bb2.room_id = br2.id"
# 		                        " join auth_user au on au.id = bb2.user_id) as ad "
#                                 " where ad.username = '%s' "  %(user) ) 
#                 row = dictfetchall(cursor)
#                 column_name = [col[0] for col in cursor.description]

#             data = dict()
#             data['column_name'] = column_name
#             data['data'] = row

#            return data

def total(request ,*args, **kwargs):
    user= request.user
    with connection.cursor() as cursor:
        cursor.execute( " select sum(ad.total) "
                                " from (select au.username ,(br2.cost  * (DATE_PART('day' , check_out ::date ) - DATE_PART('day' , check_in ::date))) as total "
		                        " from blogapp_booking bb2 "
                                " join blogapp_room br2 on bb2.room_id = br2.id"
		                        " join auth_user au on au.id = bb2.user_id) as ad "
                                " where ad.username = '%s' "  %(user) ) 
        row = dictfetchall(cursor)
        column_name = [col[0] for col in cursor.description]

    total = dict()
    total['column_name'] = column_name
    total['data'] = row

    return render(request , 'blogapp/total.html' , total)






class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=category)
        
        if len(room_list) > 0:
            room = room_list[0]
            category = dict(room.ROOM_CATEGORIES).get(room.category, None)
            form = AvailabilityForm()
            context = {
                'room_category' : category,
                'form': form,
            }
            return render(request , 'blogapp/room_detail_views.html' , context)
        else:
            return HttpResponse('Category does not exit')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:
            room = available_rooms[0]
            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of rooms are booked!! Try another one')


# class BookingView(FormView):
#     form_class = AvailabilityForm
#     template_name = 'availability_form.html'

#     def form_valid(self, form):
#         data = form.cleaned_data
#         room_list = Room.objects.filter(category=data['room_category'])
#         available_rooms = []
#         for room in room_list:
#             if check_availability(room, data['check_in'], data['check_out']):
#                 available_rooms.append(room)

#         if len(available_rooms) > 0:
#             room = available_rooms[0]
#             booking = Booking.objects.create(
#                 user = self.request.user,
#                 room = room,
#                 check_in = data['check_in'],
#                 check_out = data['check_out'],
#             )
#             booking.save()
#             return HttpResponse(booking)
#         else:
#             return HttpResponse('All of This category of room are booked!! Try anothor one')
#             #return HttpResponse(room_list)

def signup_view(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    else:
        form = NewUSerForm()
    return render(request, 'blogapp/signup.html', { 'form': form })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'blogapp/login.html', { 'form': form })

def logout_view(request):
    if request.method == 'POST':
            logout(request)
            return redirect('/')
            
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [name[0].replace(" ", "_").lower() for name in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def PDF(request ,*args, **kwargs):
    user= request.user
    with connection.cursor() as cursor:
        cursor.execute( " select bb.user_id , au.first_name as name , au.last_name as surname , br.category as room_booked "
		                " , br.cost as price "  
		                " , (check_out - check_in ) as period_of_days "
		                " , bb.check_in  , bb.check_out  "
		                " , (cost  * (DATE_PART( 'day' , check_out ::date ) - DATE_PART('day' , check_in ::date))) as amount "
        		        " from blogapp_booking bb join blogapp_room br on bb.room_id = br.id "
		                " join auth_user au on au.id = bb.user_id "
                        " where au.username = '%s' " %(user)) 
        row = dictfetchall(cursor)
        column_name = [col[0] for col in cursor.description]
    
        cursor.execute( 
                        " select sum(ad.total) "
                        " from (select au.username ,(br2.cost  * (DATE_PART('day' , check_out ::date ) - DATE_PART('day' , check_in ::date))) as total "
		                " from blogapp_booking bb2 "
                        " join blogapp_room br2 on bb2.room_id = br2.id"
		                " join auth_user au on au.id = bb2.user_id) as ad "
                        " where ad.username = '%s' "  %(user) )
        row1 = dictfetchall(cursor)
        column_name1 = [col[0] for col in cursor.description]

    data = dict()
    data['column_name'] = column_name
    data['data'] = row

    data['data1'] = row1
    data['column_name1'] = column_name1

    return render(request, 'blogapp/pdf.html', data)







def about(request):
    return render(request ,"blogapp/about.html" )

def post_details(request,id):

    #get only one post
    single_post = Room.objects.get(pk=id)
    return render(request, 'blogapp/post-details.html' ,{'single_post' : single_post})

def table(request):
    table_obj = Room.objects.all()
    

    return render(request , 'blogapp/table.html' , {'table_obj'  : table_obj} )

def export_csv(request):
    #Define http entity header
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] =  'attachment; filename= "blog.csv"'

    writer = csv.writer(response)

    #Define column header
    writer.writerow(['Post' , 'Date_Created' , 'Date_Updated'])

    #Query selected fields to ready saved as a csv file
    post_objs = Room.objects.all().values_list('title' , 'date_create' , 'date_update')

    #Finally interate feilds to be ready saved as a csv field
    for post_obj in post_objs:
        writer.writerow(post_obj)

    return response

def test(request):
    post = Room.objects.all()
    return render(request, 'blogapp/test.html' ,{'post' : post})

def index(request):
    post = Room.objects.all()
    return render(request, 'blogapp/index.html' ,{'post' : post})

def rooms(request):
    post = Room.objects.all()
    return render(request, 'blogapp/rooms.html' ,{'post' : post})

def room_details(request):
    post = Room.objects.all()
    return render(request, 'blogapp/room-details.html' ,{'post' : post})

def blog(request):
    post = Room.objects.all()
    return render(request, 'blogapp/blog.html' ,{'post' : post})

def blog_details(request):
    post = Room.objects.all()
    return render(request, 'blogapp/blog-details.html' ,{'post' : post})

def contact(request):
    post = Room.objects.all()
    return render(request, 'blogapp/contact.html' ,{'post' : post})

