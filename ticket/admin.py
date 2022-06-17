from django.contrib import admin
from . models import Brand, Event, Ticket,Vendor, Wishlist
# Register your models here.

 
    
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id','user','title','image','description')  

class EventAdmin(admin.ModelAdmin):
    list_display = ('title','brand','available','end','start','outdoor','image','description',)  
    
class TicketAdmin(admin.ModelAdmin):
    list_display = ('event','type','fee','paid','available') 
    
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name',) 
    
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user','ticket','paid','units','amount','start','end','order_no')  


admin.site.register(Brand,BrandAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(Ticket,TicketAdmin)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(Wishlist,WishlistAdmin)