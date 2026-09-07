from api.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from api.models import UserManagement
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from ..serializers import UserRegisterationSerializer,UserLoginSerializer,UserProfileSerializer,ChangeUserSerializer,SendResetPasswordEmailSerializer,UserPasswordResetSerializer,UserManagementListSerializer
from django.contrib.auth.hashers import check_password
from ..utils import Util
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from random import randint, randrange
from rest_framework.decorators import api_view, permission_classes

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'accessToken': str(refresh.access_token),
    }

class UserRegisterView(APIView):
    def post(self,request,format=None):
        password=request.data['password']
        password2=request.data['password2']
        email=request.data['email']

        if UserManagement.objects.filter(email=email).exists():
            return Response({"status":False,"msg":"Email already exists"},status=status.HTTP_400_BAD_REQUEST)
        serializer =UserRegisterationSerializer(data=request.data)

        if password !=password2:
            return Response({"status":False,"msg":"Password and confirm password did not match"},status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            print("password",password)
           
            token=get_tokens_for_user(user)
            body=f"""
            Welcome to Trueread!
            Here is your email and password to login into trueread.net/auth/login
            email: {user} 
            password:{password}
            """
            data={
                "email_subject":"Login Details",
                "email_body":body,
                "to_email":user
            }
            Util.send_email(data)
            return Response({"token":token,"msg":"Registred successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UsermanagementList(APIView):
    def get(self,request,format=None):
        users=UserManagement.objects.all()
        serializer=UserManagementListSerializer(users,many=True)
        return Response(serializer.data)
        
    
  

# class UserLoginView(APIView):
#     renderer_classes=[UserRenderer]
#     def post(self,request,format=None):
        
#         serializer=UserLoginSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             email=serializer.data.get('email')
#             password=serializer.data.get('password')
#             full_name=serializer.data.get('full_name')
            
#             user=authenticate(email=email,password=password)
            
#             if user is None:
#                 return Response({"status":False,"msg":"Email or Password did not match"},status=status.HTTP_400_BAD_REQUEST)
#             userdata=UserManagement.objects.get(email=user)
#             data={
#                 "email":userdata.email,
#                 "full_name":userdata.full_name,
#                 "is_admin":userdata.is_admin,
#                 "profile_pic":userdata.profile_pic,
#                 "agency":userdata.ofc_agency
#             }
          

#             if user is not None:
#                 token=get_tokens_for_user(user)
#                 return Response({"accessToken":token['accessToken'],"user":data},status=status.HTTP_200_OK)
#             return Response({"status":False,"msg":"Email or Password did not match"},status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_200_OK)


class UserLoginView(APIView):
   renderer_classes=[UserRenderer]
   def post(self,request,format=None):
 
    serializer=UserLoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email=serializer.data.get('email')
        password=serializer.data.get('password')
        full_name=serializer.data.get('full_name')
        
        user=authenticate(email=email,password=password)
        # print(user)
        print("user",user,type(user))
 
        if user is None:
            return Response({"status":False,"msg":"Email or Password did not match"},status=status.HTTP_400_BAD_REQUEST)
        userdata=UserManagement.objects.get(email=user)
        data={
        "email":userdata.email,
        "full_name":userdata.full_name,
        "is_admin":userdata.is_admin,
        "profile_pic":userdata.profile_pic,
        "designation":userdata.designation,
        "division":userdata.ofc_division,
        "agency":userdata.ofc_agency,
        "discomuser":userdata.ofc_discom
        }
 



        if user is not None:
            token=get_tokens_for_user(user)
            return Response({"status":True,"message":"Login successfully!","accessToken":token['accessToken'],"user":data},status=status.HTTP_200_OK)
        return Response({"status":False,"msg":"Email or Password did not match"},status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_200_OK)






class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response({"data":{"full_name":serializer.data["full_name"], "is_admin":serializer.data["is_admin"],"email":serializer.data["email"],"profile_pic":serializer.data['profile_pic'],"agency":serializer.data['ofc_agency'],'discomuser':serializer.data['ofc_discom']}}, status=status.HTTP_200_OK)


# class ChangeUserPassword(APIView):

#     permission_classes=[IsAuthenticated]
#     def post(self,request,format=None):
#         emailuser=request.user
#         currentpassword=request.user.password
#         print("request.user",request.user)

#         serializer=ChangeUserSerializer(data=request.data,context={"user":request.user,"currentpassword":currentpassword})
#         if serializer.is_valid(raise_exception=True):
        
#              return Response({"msg":"Password changed successfully"},status=status.HTTP_200_OK)

#         return Response("serializer.errors",status=status.HTTP_200_OK)

class ChangeUserPassword(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        user=request.user
        currentpassword=request.user.password
        password=request.data['password']
        password2=request.data['password2']
        oldpassword=request.data['oldpassword']
        print("request.user",request.user)
        if not check_password(oldpassword,currentpassword):
             return Response({"status":"error","msg":"Old Password did not match"},status=status.HTTP_400_BAD_REQUEST)
        if password !=password2:
            return Response({"status":"error","msg":"Password and confirm password did not match"},status=status.HTTP_200_OK)

        user.set_password(password)
        user.save()
        return Response({"status":"success","msg":"Password Changed Successfully"},status=status.HTTP_200_OK)


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# class SendResetPasswordEmail(APIView):
#     renderer_classes=[UserRenderer]
#     def post(self,request,format=None):
#         random_with_N_digits(4)
#         serializer=SendResetPasswordEmailSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             return Response({"msg":"Password Reset Link Sent.Please check your Email!"},status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SendResetPasswordEmail(APIView):
    def post(self,request,format=None):
        email=request.data['email']
        if UserManagement.objects.filter(email=email).exists():
            user=UserManagement.objects.get(email=email)
            print(user)
            print('uid only',user.id)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('encoded uid',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('password reset token',token)

            link="http://trueread.net/auth/new-password/"+uid+'/'+token
            print('password reset link',link)
            #send Email
            body="Click the following link to reset your password "+link
            data={
                "email_subject":"Reset your password",
                "email_body":body,
                "to_email":user.email
            }
            Util.send_email(data)
            return Response({"msg":"Password reset link sent successfully"})
        return Response({"msg":"Email does not exist!"},status=status.HTTP_400_BAD_REQUEST)
        


# class UserPasswordResetView(APIView):
#     def post(self,request,uid,token,format=None):
#         password=request.data['password']
#         password2=request.data['password2']
        
#         serializer=UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
#         if serializer.is_valid(raise_exception=True):
#             return Response({"msg":"Password Reset Successfully"},status=status.HTTP_200_OK)

#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
    def post(self,request,uid,token,format=None):
        try:
            password=request.data['password']
            password2=request.data['password2']
            if password != password2:
                return Response({"status":False,"msg":"Password and Confirm Password doesn't match"})
            id = smart_str(urlsafe_base64_decode(uid))
            user = UserManagement.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"status":False,"msg":"'Token is not Valid or Expired'"},status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)
            user.save()
            return Response({"status":True,"msg":"Password Reset Successfully"})
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise Response({"status":False,"msg":"'Token is not Valid or Expired'"},status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
def usermanagementupdate(request):
    newdata = request.data
    id=newdata['id']
    try:
        id = UserManagement.objects.get(id=id)
        serializer = UserManagementListSerializer(
            id, data=newdata, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "User Updated"}, status=status.HTTP_200_OK)
        return Response({"status": False, "message": "Something wrong(from api)"}, status=status.HTTP_200_OK)
    except UserManagement.DoesNotExist:
        return Response({"status": False, "message": "MR Does not Exist(from api)"}, status=status.HTTP_200_OK)
    
        