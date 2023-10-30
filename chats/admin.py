from django.contrib import admin
from chats.models import ChatModel  , ChatNotification , UserProfileModel , UserProfile, dashboard

from chats.models import image

# Register your models here.
admin.site.register(ChatModel)
admin.site.register(UserProfileModel)
admin.site.register(ChatNotification)
#admin.site.register(UserProfile)


from .models import Follower, Creator, User, users_feedback, Order



admin.site.register(User)
admin.site.register(Follower)
admin.site.register(Creator)
admin.site.register(UserProfile)
admin.site.register(dashboard)
admin.site.register(users_feedback)
admin.site.register(Order)
admin.site.register(image)




