from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# from datetime import datetime
# import datetime

# Create your models here.
 
from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import forms
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
# from jsonfield import JSONField


import uuid

# from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin
# from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
# Create your models here.


class Roles(models.Model):
    company_id = models.CharField(max_length=101)
    role_name = models.CharField(max_length=100)

    dashboard = models.BooleanField(default=False)
    chatapp = models.BooleanField(default=True)
    campaigns = models.BooleanField(default=False)
    projects = models.BooleanField(default=False)
    finance = models.BooleanField(default=False)
    aiwriter = models.BooleanField(default=False)



class Category(models.Model):  # The Category table name that inherits models.Model
    name = models.CharField(max_length=100)  # Like a varchar

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.name  # name to be shown when called


class TodoList(models.Model):  # Todolist able name that inherits models.Model
    title = models.CharField(max_length=250)  # a varchar
    content = models.TextField(blank=True)  # a text field
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))  # a date
    start_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))  # a date
    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))  # a date
    category = models.CharField(max_length=250)
    creator = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE, null=True)

    class Meta:
       ordering = ["-created"]  # ordering by the created field

    def __str__(self):
       return self.title  # name to be shown when called


class Company(models.Model):
    company = models.CharField(max_length=150)
    company_uuid = models.CharField(max_length=100, null=True)
    workspace = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='workspace1')
    timestamp = models.DateTimeField(auto_now=True)


class WorkSpaceConnection(models.Model):
    space = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # user_files = models.URLField(null=True)
    user_files = models.ImageField(default='default.jpg', upload_to='profile_pics')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    role = models.ForeignKey(Roles, on_delete=models.DO_NOTHING, default=1, related_name="RoleProfile")
    fcm_token = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Group(models.Model):
    title = models.TextField(max_length=420)
    description = models.TextField(max_length=420)
    admin = models.ForeignKey(User, related_name="admin", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    group_type = models.BooleanField(default=False)
    room = models.UUIDField(default=uuid.uuid4, unique=True)

    class Meta:
        ordering = ("created",)
        verbose_name = "Group"
        verbose_name_plural = "Groups"


class Friends(models.Model):

    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friends")
    timestamp = models.DateTimeField(auto_now=True)
    room = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return f"{self.user1}"

    class Meta:
        ordering = ("timestamp",)


class Messages(models.Model):
    room = models.ForeignKey(
        Friends, on_delete=models.CASCADE, related_name="room_id")
    description = models.TextField()
    sender_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender"
    )
    time = models.TimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    reply = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    upload_file = models.FileField(
        blank=True, null=True, upload_to='messages_files')



    class Meta:

        ordering = ("timestamp",)




class Connection(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="Connection")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default='1')
    # timestamp = models.DateTimeField(auto_now=True)
    # class Meta:
    #     ordering = ("timestamp",)


class SeenGroupMessages(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="SeenGroupMessages")
    message_id = models.ForeignKey(
        Connection, on_delete=models.CASCADE, related_name="SeenGroupMessage" )
    seen = models.BooleanField(default=False)
    
class visited(models.Model):
    cookie = models.CharField(max_length=150)
    ip = models.GenericIPAddressField(
        max_length=150, blank=False)  # add unique=True
    country = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    region = models.CharField(max_length=150, blank=True)
    postal = models.CharField(max_length=150, blank=True)
    latitude = models.CharField(max_length=150, blank=True)
    longitude = models.CharField(max_length=150, blank=True)
    org = models.CharField(max_length=150, blank=True)
    timezone = models.CharField(max_length=150, blank=True)
    platform = models.CharField(max_length=150, blank=True)
    utm_source = models.CharField(max_length=150, blank=True, null=True,)
    utm_medium = models.CharField(max_length=150, blank=True, null=True)
    utm_campaign = models.CharField(max_length=150, blank=True, null=True)
    utm_term = models.CharField(max_length=150, blank=True, null=True)
    utm_content = models.CharField(max_length=150, blank=True, null=True)
    companyId = models.CharField(max_length=150, blank=True, null=True)
    is_bot = models.CharField(max_length=10, blank=True, null=True)
    device_type = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(max_length=20, blank=True, null=True)
    mime_type = models.CharField(max_length=150, blank=True, null=True)
    plugins = models.CharField(max_length=150, blank=True, null=True)
    avail_height = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    depth = models.IntegerField(blank=True, null=True)
    browser = models.CharField(max_length=20, blank=True, null=True)
    network_type = models.CharField(max_length=20, blank=True, null=True)
    rtt = models.IntegerField(blank=True, null=True)
    downlink = models.FloatField(blank=True, null=True)
    save_data = models.CharField(max_length=20, blank=True, null=True)
    device_memory = models.IntegerField(blank=True, null=True)
    hardware_concurrency = models.IntegerField(blank=True, null=True)
    times_visited = models.IntegerField(default=0)
    # pages_visited = JSONField(default=dict)

    #notification = models.CharField(max_length=50, blank=True, null=True)

    allow_notification = models.BooleanField(default=False)
    fcm_token = models.CharField(max_length=201, null=True, blank=True)
    #notification = models.CharField(max_length=150, blank=True, null=True)

    # class Meta:
    #unique_together = ["cookie", "ip"]

    def __str__(self):
        return str(self.cookie)


class LiveChatMessages(models.Model):
    description = models.TextField()
    sender = models.ForeignKey(visited, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    direction = models.BooleanField()
    seen = models.BooleanField(default=False)

    @staticmethod
    def give_chats(room):
        l = []

        instance = Connection.objects.filter(
            group=Group.objects.get(room=room))
        for i in instance:
            data = {}
            data['message'] = i.description
            data['sender'] = i.sender.username
            data['timestamp'] = i.timestamp
            # data['reply'] = i.reply
            # data['upload_file'] = i.upload_file
            # data['pic'] = i.sender.profile.user_files.url
            l.append(data)
        return l


class leads(models.Model):
    visited = models.OneToOneField(
        visited, on_delete=models.CASCADE, null=True)


class deals(models.Model):
    leads = models.OneToOneField(
        leads, on_delete=models.CASCADE, null=True)
    
class Brand(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='faculty', default='pix.jpg')
    description = models.TextField()

    
    class Meta:
        db_table = 'Brand'
        managed = True
        verbose_name = ("Brand")
        verbose_name_plural = ("Brands")

    def __str__(self):
        return self.title

    
class Event(models.Model):
    title = models.CharField(max_length=50) 
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    available =  models.BooleanField()
    end = models.DateField(blank=True, null=True)
    start = models.DateField(blank=True, null=True)
    outdoor =  models.BooleanField()    
    image = models.ImageField(upload_to='faculty', default='pix.jpg')
    description = models.TextField()
    

  
    class Meta:
        db_table = 'Event'
        managed = True
        verbose_name = ("Event")
        verbose_name_plural = ("Events")

    def __str__(self):
        return self.title
 
      
class Ticket(models.Model): 
    type = models.CharField(max_length=20)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)   
    fee = models.IntegerField()
    paid =  models.BooleanField(default=False)
    available =  models.BooleanField()
    
    class Meta:
        db_table = 'Ticket'
        managed = True
        verbose_name = ("Ticket")
        verbose_name_plural = ("Tickets")

    def __str__(self):
        return self.type  
 

        
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    paid =  models.BooleanField(default=False)
    units = models.IntegerField(default=1)
    amount = models.IntegerField()
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    order_no = models.CharField(max_length=50)


    class Meta:
        db_table = 'wishlist'
        managed = True
        verbose_name = 'wishlist'
        verbose_name_plural = 'Whishlist'

    def __str__(self):
        return self.user.username
    
class Vendor(models.Model): 
    name = models.CharField(max_length=20)


    class Meta:
        db_table = 'Vendor'
        managed = True
        verbose_name = ("Vendor")
        verbose_name_plural = ("Vendors")

    def __str__(self):
            return self.name   
        
  