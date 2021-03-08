from django.db import models
from django.conf import settings 
from django.urls import reverse , reverse_lazy


# Create your models here.

class Room(models.Model):
    ROOM_CATEGORIES=(
        ('Single','Single_Room'),
        ('Double','Double_Room'),
        ('Suite','Suite_Room'),
        ('Deluxe','Deluxe_Room'),
        ('Premier','Premier_Room'),
    )
    number = models.CharField(max_length= 10 )
    category = models.CharField(max_length=7, choices=ROOM_CATEGORIES)
    bed = models.IntegerField()
    capacity = models.IntegerField()
    cost = models.IntegerField()

    def __str__(self):
        return f'{self.number}. {self.category} with {self.bed} for {self.capacity} people'
    
class Booking(models.Model):
    
    user =  models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete = models.CASCADE , null = True)
    room = models.ForeignKey(Room , on_delete = models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f'{self.user}. {self.room} with {self.check_in} for {self.check_out} people'
    
    def get_room_category(self):
        room_categories = dict(self.room.ROOM_CATEGORIES)
        room_category = room_categories.get(self.room.category)
        return room_category

    def get_cancel_booking_url(self):
        return reverse_lazy('CancelBookingView', args=[self.pk, ])
  