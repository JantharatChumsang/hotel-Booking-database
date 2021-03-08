import datetime
from blogapp.models import Room


def find_total_room_charge(request, check_in, check_out, category):
    days = check_out-check_in
    room_category = Room.objects.get(category=category)
    total = days.days * room_category.cost
    return total
