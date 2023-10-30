from django.contrib import admin
from django.urls import path, include

from chats.views import chat,LandingPageView ,chatPage,search_users , close_session, dashboard
from chats.views import search,login_request,creator_profile, edit_creator_profile, my_profile, delete_chat,follower_profile_edit

from chats.views import user_feedback, feedback_and_rating, callback # ,paymenthandler,

from chats.views import Update_Password, Follower_UserName_Edit      
from payment.views import payment_request

from django.urls import path, re_path, include


from chats.views import FollowerSignupView , CreatorSignupView, LandingPageView

import website.views as website 
from django.urls import path

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('chat/', chat, name='home'),
    path('chat/<int:id>/', chatPage, name='chatPage'),
    path('search/', search_users, name='search_users'),
    path('sea/', search, name = 'search'),
    path('', LandingPageView, name = "landingpage"),
    path("chats/", include("chats.urls")),
    path('accounts/', include('allauth.urls')),
    
    #google login and signup
    path('accounts/signup/Follower/', FollowerSignupView.as_view(), name='Follower_signup'),
    path('accounts/signup/Creator/', CreatorSignupView.as_view(), name='Creator_signup'),
   

        


    path('login/',login_request, name='login_main'),
    
   
    path('profile_edit/', edit_creator_profile, name='edit_creator_profile'),
    path('my_profile/', my_profile, name='my_profile'),
    path('delete_chat/<int:id>/<int:chat_id>' ,delete_chat, name = "delete_chat"),
    path('close_session/<int:id>', close_session, name = 'close_session'),
    path('dashboard', dashboard, name = 'dashboard'),
    path('follower_profile_edit/', follower_profile_edit, name='follower_profile_edit'),
    path('user_feedback/<int:id>/', user_feedback, name='user_feedback'),
    path('rating/', feedback_and_rating, name='feedback_and_rating'),
    path('payment', payment_request, name = "payment_request"),
    # path('paymenthandler/<int:id>', paymenthandler, name = "paymenthandler"),
    path('callback/<int:id>/<int:rid>/', callback, name='callback'),

    path('Follower_UserName_Edit/',Follower_UserName_Edit, name ="Follower_UserName_Edit" ),
    path('Update_Password/',Update_Password, name = "Update_Password"),

    
    path('terms_and_conditions/',website.terms_and_conditions , name = "terms_and_conditions"),
    path('privacy_policy/',website.Privacy_Policy , name = "privacy_policy"),
    path('favicon.ico/', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico'))),
    path('<str:username>/', creator_profile, name='creator_profile'),


]


from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
