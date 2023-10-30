from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404,  JsonResponse
from django.views import generic
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import FollowerSignUpForm, CreatorSignUpForm
from chats.models import ChatModel, image
import uuid
from .helper import send_forget_password_mail
from .models import User,User, UserProfile,Creator,users_feedback
from django.utils import timezone



def LandingPageView(request):
    
    #template_name = "new_landing.html"
    
    follower_png = image.objects.get(image_name = 'Follower')
    Creator_png = image.objects.get(image_name = 'Creator')
    return render(request, 'new_landing.html', context={'follower_png': follower_png, 'Creator_png':Creator_png })


def register(request):
    if request.user.is_authenticated:
        return redirect('/chat')
   

    return render(request, 'new_register.html')


class Follower_register(CreateView):
   
    model = User
    form_class = FollowerSignUpForm
    template_name = 'new_follower_register.html'

    def form_valid(self, form):
        print("hello world")
        user = form.save()
        login(self.request, user, backend='chats.authenticate.EmailAuthBackend')
        return redirect('/')


class Creator_register(CreateView):
    # print("hello ap bye bye ycp111111")
    model = User
    form_class = CreatorSignUpForm
    template_name = 'new_creator_register.html'

    
    def form_valid(self, form):
        # print("hello ap bye bye ycp")
        user = form.save()
        login(self.request, user, backend='chats.authentication.EmailAuthBackend')
        return redirect('/')
    


def login_request(request):
    if request.user.is_authenticated:
        return redirect('/chat')
    
    if request.method == 'POST':
        # form = AuthenticationForm(data=request.POST)
        # if form.is_valid():
        # email = form.cleaned_data.get('username') 
        # password = form.cleaned_data.get('password')

        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = authenticate(username=email, password=password)
        #print("user", user)
        if user is not None:
            if user.is_active:
                login(request, user, backend='chats.authentication.EmailAuthBackend')
                return redirect('/chat')
            else:
                return HttpResponse('Disabled Account')
        else:
            messages.error(request, "Invalid username or password")
    else:
        messages.error(request, "Invalid username or password")
    return render(request, 'login.html')


def Logout(request):
    logout(request)
    return redirect('/')


def ChangePassword(request, token):
    context = {}
    try:
        profile_obj = get_object_or_404(User, token=token)
        context = {'user_id': profile_obj.id}
        if request.method == 'POST':
            
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/chats/change-password/{token}/')
            if new_password != confirm_password:
                messages.success(request, 'both should be equal.')
                return redirect(f'/chats/change-password/{token}/')
            try:
                validate_password(new_password, profile_obj)
            except Exception as e:
                for error in e:
                    messages.success(request, error)
                    
                    return redirect(f'/chats/change-password/{token}/')
            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.token = ""
            user_obj.save()
            messages.success(request, "Login with new password id")
            return redirect('/chats/login/')
    except Exception as e:
        raise Http404("url not found")
    return render(request, 'change-password.html', context)


def ForgetPassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('username')
            print(email)
            if not email:
                messages.success(request, 'Please Enter email')
                return redirect('/chats/forget-password/')
            
            if not User.objects.filter(email=email).first():
                
                messages.success(request, 'No user found with this email.')
                return redirect('/chats/forget-password/')
            
            user_obj = User.objects.get(email=email)
            
            
            token = str(uuid.uuid4())
            # profile_obj = User.objects.get(email=user_obj)
            user_obj.token = token
            user_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent. Please check your your email.')
            return redirect('/chats/forget-password/')
    except Exception as e:
        print(e)
    return render(request, 'forget-password.html')


@login_required
def chat(request):
    try:
        UserProfile_obj = UserProfile.objects.filter(user_id=request.user.id).all().order_by('-is_session_opened', '-last_message')
    except Exception as e:
        print(e)


    return render(request, 'chatlist.html', context={'friends': UserProfile_obj})


ALLOWED_EXTENSIONS = ['.m4a','.ogg','.mp3','.jpg', '.jpeg', '.png', '.mp4','.avi','.mov','.pdf','.doc','.docx', '.html', '.txt']

@login_required
@csrf_exempt
def chatPage(request, id):
    try:

        UserProfile_obj = UserProfile.objects.filter(user_id=request.user.id).all().order_by('-is_session_opened', '-last_message')
        
    except Exception as e:
        print(e)
    try:
        UserProfile.objects.filter(Follower_id=id, user_id=request.user.id).update(message_seen=True)
    except Exception as e:
        print(e)
    user_obj = User.objects.get(id=id)
    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
    if request.method == 'POST':
        if request.FILES.get('fileInput'):
            file = request.FILES['fileInput']
            if not any(file.name.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                messages.error(request, 'Invalid file type. Only JPG, JPEG, and PNG files are allowed.')
                return JsonResponse({'success': False, 'message': 'Invalid file type.'})
            chat = ChatModel.objects.create(sender=request.user.username, thread_name=thread_name, file=file)
            chat.save()
            file_url = chat.file.url
            file_name = chat.file.name

            response_data = {
                'success': True,
                'message': 'File uploaded successfully.',
                'file_url': file_url,
                'file_name': file_name
                
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'success': False, 'message': 'No file provided.'})
    
    session_opened = UserProfile.objects.get(user = request.user , Follower = user_obj).is_session_opened
    print("session_status",session_opened)
        

    message_objs = ChatModel.objects.filter(thread_name=thread_name).all().order_by('timestamp')

    # last_message =  ChatModel.objects.filter(thread_name=thread_name).latest('timestamp').message

    try:
        if users_feedback.objects.filter(Creator = id, Follower = request.user.id).latest('id').Rating:
            Is_Rating_given = True 
            
        else :
            Is_Rating_given = False
    except Exception as e:
        Is_Rating_given = False

    return render(request, 'main_chat_test.html', context={'user': user_obj, 'UserProfile_obj': UserProfile_obj, 'msgs': message_objs, 'session_status' : session_opened , 'Is_Rating_given' : Is_Rating_given })


def search(request):
    return render(request, 'search_users.html')


def search_users(request):
    search_query = request.GET.get('search', '')
    creators = Creator.objects.filter(user__first_name__icontains=search_query)
    search_results = [{'first_name': creator.user.first_name, 'last_name': creator.user.last_name,
                       'image_url': creator.user.image.url, 'id': creator.user_id, 'username': creator.user.username,
                       'profession': creator.Professional_label} for creator in creators]
    return JsonResponse(search_results, safe=False)


import razorpay
from django.conf import settings 
import json

from django.http import HttpResponseBadRequest
from chats.helper import send_PaymentSuccess_mail_to_Follower,send_PaymentSuccess_mail_to_Creator
from django.db.models import Count, Q
from django.http import HttpResponseNotFound

def creator_profile(request, username):

    try:
        creator_obj1 = get_object_or_404(User, username=username)

        opened_sessions_count =  users_feedback.objects.filter(Q(session_status = "Open") & Q(Creator=creator_obj1)).count()

        id = creator_obj1.id
        creator_profile = Creator.objects.get(user= creator_obj1)
        amount = creator_profile.amount

        
        if opened_sessions_count  >= creator_profile.opened_sessions:
            QueueFull = True
        else: 
            QueueFull = False    
        
        try:
            user1 = request.user
            print(user1)
            user2   = creator_obj1
            print(user2)
            if UserProfile.objects.filter(user = user1, Follower = user2): 
                userprofile_obj = UserProfile.objects.filter(user = user1, Follower = user2).latest('id')
                session_status = userprofile_obj.is_session_opened 
            else:
                # userprofile_obj = UserProfile.objects.create(user = user1, Follower = user2)
                session_status = False
            

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            response = client.order.create({
            'amount': amount * 100,  # Amount in paise (e.g., ₹500 = 50000 paise)
            'currency': 'INR',
            'payment_capture': '1'  # Auto-capture payments after successful redirection
        })
            
            callback_url = "http://" + "127.0.0.1:8000" + "/callback/" + str(id) + "/" + str(request.user.id) + "/"
            order_id = response['id']
            print("order_id",order_id)
           
            api_key = settings.RAZORPAY_KEY_ID
            Order.objects.create(order_id=order_id, amount = amount, Creator=creator_obj1,Follower=request.user)
            
            

            return render(request, 'creator_profile.html', {'profile': creator_profile ,'callback_url': callback_url, 'order_id':order_id, 'api_key':api_key ,'session_status':session_status, 'creator_id':id,'QueueFull':QueueFull })
        
        except Exception as e:
            print(e)
            return render(request, 'creator_profile.html', {'profile': creator_profile ,'creator_id':id})
            

    except Exception as e:
        session_status = False
        print(e)

    
from .constants import PaymentStatus
from chats.models import Order

@csrf_exempt

def callback(request, id, rid):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        # print("provider_order_id",provider_order_id)
        # print("payment_id",payment_id)
        # print("signature_id", signature_id)
        order = Order.objects.get(order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()

        follower_obj = User.objects.get(id = rid)

        email = follower_obj.email
        
        send_PaymentSuccess_mail_to_Follower(email,order)
        creator_obj1 = User.objects.get(id = id)
        creator_obj1_Email = creator_obj1.email
        send_PaymentSuccess_mail_to_Creator(creator_obj1_Email,order)
        if verify_signature(request.POST):
            order.payment_status = PaymentStatus.SUCCESS
            # print("payment success",PaymentStatus.SUCCESS)
            order.save()
            # print("sucesss - 1 ")
            user1 = User.objects.get(id = rid) ### follower
            user2 = User.objects.get(id = id) #### Creator
            if not UserProfile.objects.filter(user = user1, Follower = user2 ) :
                # if the user is paying for firsttime
                UserProfile.objects.create(user = user1, Follower = user2 )
                UserProfile.objects.create(user = user2, Follower = user1 )
                

            else:
                
                userprofile_obj = UserProfile.objects.filter(user = user1, Follower = user2).latest('id')
                userprofile_obj.is_session_opened = True
                userprofile_obj.save()
                
            
            creator_profile = Creator.objects.get(user_id=id)
            amount = creator_profile.amount
            users_feedback.objects.create(Creator = user2, Follower = user1, chat_start_time = timezone.now(), amount = amount,)
            url  = f'/chat/{id}/'
            return redirect(url)
        else:
            order.payment_status = PaymentStatus.FAILURE
            order.save()  
            username = User.objects.get(id=id).username
            
            url = f'/{username}/'
            return redirect(url)
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        print("provider_order_id",provider_order_id)
        order = Order.objects.get(order_id=provider_order_id)
        order.payment_id = payment_id
        order.payment_status = PaymentStatus.FAILURE
        order.save()
        
        username = User.objects.get(id=id).username
        
        url = f'/{username}/'
        return redirect(url)
        




# @csrf_exempt
# def paymenthandler(request, id):
 
#     # only accept POST request.
#     if request.method == "POST":
#         try:
           
#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
 
#             # verify the payment signature.
#             result = client.utility.verify_payment_signature(
#                 params_dict)
#             print(result)
#             if result :
#                 # amount = 50000  # Rs. 200
#                 # try:
 
#                 #     # capture the payemt
#                 #     client.payment.capture(payment_id, amount)
 
#                 #     # render success page on successful caputre of payment
#                 user1 = User.objects.get(id = request.user.id)
#                 user2 = User.objects.get(id = id)
#                 UserProfile.objects.create(user = user1, Follower = user2 )
#                 UserProfile.objects.create(user = user2, Follower = user1 )

#                 users_feedback.objects.create(Creator = user2, Follower = user1, chat_start_time = timezone.now())
                

#                 return redirect(f'/chat/{id}/')
#                 # except:
 
#                     # if there is an error while capturing payment.
#                     # return redirect(f'/Creator_profile/{id}/')
#             else:
 
#                 # if signature verification fails.
#                 return redirect(f'/Creator_profile/{id}/')
#         except:
 
#             # if we don't find the required parameters in POST data
#             return redirect(f'/Creator_profile/{id}/')
#     else:
#        # if other than POST request is made.
#         return HttpResponseBadRequest()


def edit_creator_profile(request):
    if request.method == 'POST':
        try :
            creator_obj = Creator.objects.get(user=request.user)
            image_obj = User.objects.get(id = request.user.id)
            if request.FILES.get('profile-pic'):
                print(request.FILES['profile-pic'])
                
                image_obj.image = request.FILES['profile-pic']
                image_obj.save()

        except Exception as e:
            print(e)
    
        creator_obj = Creator.objects.get(user=request.user)

        if request.POST.get('response'):
            creator_obj.allow_messages = True
        elif request.POST.get('response') is None:
            creator_obj.allow_messages = False

        if request.POST.get('profession'):
            print(request.POST.get('profession'))
            creator_obj.Professional_label = request.POST.get('profession')
            creator_obj.save()
        if request.POST.get('about_me'):
            creator_obj.About = request.POST.get('about_me')
            creator_obj.save()

        if request.POST.get('reply_time'):
            creator_obj.reply_time = request.POST.get('reply_time')
            creator_obj.save()

        if request.POST.get('opened_sessions'):
            creator_obj.opened_sessions = request.POST.get('opened_sessions')
            creator_obj.save()
            
        if  request.POST.get('social_profile'):
            creator_obj.Social_Profile = request.POST.get('social_profile')
            creator_obj.save()
        
        if request.POST.get('Service'):
            creator_obj.service = request.POST.get('Service')
            creator_obj.save()
            
        if request.POST.get('name'):
            image_obj.first_name = request.POST.get('name')
            image_obj.save()
        

        new_username = request.POST.get('username')
        if new_username:
            validator = UsernameValidator()  # Create an instance of the validator
            try:
                validator(new_username)  # Run the username through the validator
                
                # Check if the new username is already taken
                if User.objects.filter(username=new_username).exclude(id=image_obj.id).exists():
                    messages.error(request, 'Username is already taken.')

                    return redirect('/profile_edit')
                else:
                    image_obj.username = new_username
                    image_obj.save()  # Save only if the username is valid

                    return redirect('/my_profile/')
                    
                
                
            except ValidationError as ve:
                messages.error(request, ve.message)
                return redirect('/profile_edit/')  # Redirect to profile page on validation error
        
        # try:
        #     image_obj.save()  # Save other profile updates
        #     messages.success(request, 'Profile updated successfully.')  # Display success message
            
        # except Exception as e:
        #     print(e)
        #     messages.error(request, 'An error occurred while updating profile.')
            
        
        creator_obj.save()
        messages.success(request, "profile_updated")
        return redirect('/my_profile/')

    obj = Creator.objects.get(user=request.user)
    return render(request, 'edit_creator_profile.html', {'creator_profile': obj})


from .validator import UsernameValidator
from django.core.exceptions import ValidationError


def Follower_UserName_Edit(request):
    if request.method == 'POST':
        Follower_obj = User.objects.get(id=request.user.id)
        
        # Handle profile picture upload
        profile_pic = request.FILES.get('profile-pic')
        if profile_pic:
            Follower_obj.image = profile_pic

        # Handle first name update
        new_name = request.POST.get('name')
        if new_name:
            Follower_obj.first_name = new_name
        
        # Handle username update with validation
        new_username = request.POST.get('username')
        if new_username:
            validator = UsernameValidator()  # Create an instance of the validator
            try:
                validator(new_username)  # Run the username through the validator
                
                # Check if the new username is already taken
                if User.objects.filter(username=new_username).exclude(id=Follower_obj.id).exists():
                    messages.error(request, 'Username is already taken.')
                else:
                    Follower_obj.username = new_username
                    Follower_obj.save()  # Save only if the username is valid
                    
            except ValidationError as ve:
                messages.error(request, ve.message)
                return redirect('/my_profile/')  # Redirect to profile page on validation error
        
        try:
            Follower_obj.save()  # Save other profile updates
            messages.success(request, 'Profile updated successfully.')  # Display success message
            
        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred while updating profile.')

    return redirect('/my_profile/')

def Update_Password(request):
    if request.method == 'POST':
        CurrentPassword = request.POST.get('CurrentPassword')
        NewPassword = request.POST.get('NewPassword')

        if request.user.check_password(CurrentPassword):
            try:
                validate_password(NewPassword, request.user)
                request.user.set_password(NewPassword)
                request.user.save()
                
                # Re-authenticate the user with the new password
                updated_user = authenticate(username=request.user.username, password=NewPassword)
                if updated_user:
                    login(request, updated_user)  # Log the user back in

                messages.success(request, 'Password changed successfully.')
            except ValidationError as ve:
                for error in ve:
                    messages.error(request, error)

            return redirect('/my_profile/')
        else:
            messages.error(request, 'Current password is incorrect.')

            if request.user.is_Follower:
                
                return redirect('/my_profile/')
            elif request.user.is_Creator :
                return redirect('/profile_edit/')
        
    


def my_profile(request):
    user_obj =  User.objects.get(id = request.user.id)

    if user_obj.is_Creator:
        
        creator_profile_obj = Creator.objects.get(user = user_obj)
        return render(request, 'Creator_my_profile.html', {'profile': creator_profile_obj})
    
    elif user_obj.is_Follower:
        Follower_obj = User.objects.get(id = request.user.id)
        
        return render(request , 'Follower_profile_edit.html', {"profile": Follower_obj })
    
def delete_chat(request , id , chat_id):
    try:
        chat_obj  = ChatModel.objects.get(id = chat_id)
        user_obj = User.objects.get(id = request.user.id)
        if chat_obj.sender == request.user.username:
            chat_obj.delete()
        
    except Exception as e:
        print(e)
    return redirect(f'/chat/{id}/')


def close_session(request, id):
    sender_obj = User.objects.get(id = request.user.id)
    receiver_obj = User.objects.get(id = id)
    
    try:
        # print("zzzzzzzzzzzzzz",sender_obj,receiver_obj)
        i = users_feedback.objects.filter(Creator=sender_obj ,Follower = receiver_obj).latest('id')
        i.session_status = "Close"
        i.save()
        
        # user_feedback_obj.save()
        
    except Exception as e:
        # print("xxxxxxxxxxxxxxxxx",sender_obj,receiver_obj)
        # print("aaaaaaaaaaaaa")
        u = users_feedback.objects.filter(Creator=receiver_obj ,Follower =sender_obj ).latest('id')
        u.session_status = "Close"
        u.save()
        # user_feedback_obj.save()

    #if creator closes the session 
    try:
        if sender_obj.is_Follower or receiver_obj.is_Follower:

            if sender_obj.is_Creator :
                obj = UserProfile.objects.get(user = receiver_obj , Follower = sender_obj)
                obj.is_session_opened = False
                obj.save()
            #if follower closes the session
            else:
                obj = UserProfile.objects.get(user = sender_obj  , Follower = receiver_obj )
                obj.is_session_opened = False
                obj.save()
        else:
            obj = UserProfile.objects.get(user = sender_obj , Follower = receiver_obj)
            obj.is_session_opened = False
            obj.save()
            
    except Exception as e:
        print(e)


    if request.user.id >receiver_obj.id:
        thread_name = f'chat_{request.user.id}-{receiver_obj.id}'
    else:
        thread_name = f'chat_{receiver_obj.id}-{request.user.id}'

    chat = ChatModel.objects.create(sender='info-message', message = "The session was ended", thread_name=thread_name)
    chat.save()
    # print("yes")
   
    return redirect(f'/chat/{id}/')

from chats.models import dashboard as dash
from django.db.models import Avg, Sum, Count

def dashboard(request ):


    creator_obj = User.objects.get(id = request.user.id)

    dashboard_obj = users_feedback.objects.filter(Creator = creator_obj).order_by('-timestamp')

    average_rating = users_feedback.objects.filter(Creator=creator_obj).aggregate(avg_rating=Avg('Rating'))['avg_rating']
    average_rating = round(average_rating, 1) if average_rating else None

    total_amount = users_feedback.objects.filter(Creator=creator_obj).aggregate(sum_amount=Sum('amount'))['sum_amount']

    record_count = users_feedback.objects.filter(Creator=creator_obj).count()

    return render(request , "dashboard.html", {'dashboard_data' : dashboard_obj, 'average_rating': average_rating , 'total_amount': total_amount,'record_count': record_count })

    


def follower_profile_edit(request):
    return render(request , "follower_profile_edit.html")




def user_feedback(request ,id):

    follower = request.user.id
    creator = id

    feedback_obj = users_feedback.objects.filter(Creator = creator, Follower = follower).latest('id')


    if request.method == 'POST':
        
        if request.POST.get('rating'):
            feedback_obj.Rating = request.POST.get('rating')
        else:
            return redirect(f'/chat/{id}/')
            
        if request.POST.get('feedback'):
            feedback_obj.Feedback = request.POST.get('feedback')

        feedback_obj.chat_end_time = timezone.now()
        feedback_obj.session_status = "Close"
        
        feedback_obj.save()

    return redirect(f'/chat/{id}/')
            

def feedback_and_rating(request):
    user_obj = User.objects.get(id = request.user.id)
    user_feedback_obj = users_feedback.objects.filter(Creator = user_obj).order_by('-timestamp')

    return render(request , 'feedback.html', {'user_feedback_obj':user_feedback_obj})
    # return render(request,'feedback.html' )
        
   
   ###########################################################################################
   # ############## Django allauth ###########################################################
   ########################################################################################### 
    
from chats.models import User
from django.shortcuts import render, redirect
from django.views.generic import FormView

from allauth.account.forms import SignupForm
from chats.forms import CreatorSignUpForm, FollowerSignUpForm
from django.http import HttpRequest


class FollowerSignupView(FormView):
    form_class = FollowerSignUpForm
    template_name = 'follower_register.html'

    def form_valid(self, form):
        user = form.save()
        user.is_Follower = True
        user.save()
    
        return redirect('/chat')
    
    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        ret['user_type'] = "is_Follower"
        return ret


class CreatorSignupView(FormView):
    form_class = CreatorSignUpForm
    template_name = 'creator_register.html'

    def form_valid(self, form):
        user = form.save()
        user.is_Creator = True
        user.is_Follower = False
        user.save()

        return redirect('/chat')
    
    

   
    


    

    
