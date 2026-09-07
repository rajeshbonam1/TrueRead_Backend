from rest_framework import serializers
from .models import Consumers,MeterReaderRegistration, SupervisorLogin,UserManagement,NotificationMani,notificatio_recepients
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from .utils import Util
from rest_framework.exceptions import APIException





class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Consumers
        fields="__all__"
        
    pass

class MeterReaderRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeterReaderRegistration
        fields = ['id','mrId','mrName','section','mrPhone','mrPhoto','androidToken','discom','zone','circle','division','subdivision','sectioncode']

class SupervisorLoginSerializer(serializers.ModelSerializer):
    location = serializers.BooleanField(read_only=True)
    class Meta:
        model = SupervisorLogin
        fields = [
            'id',
            'supervisor_number',
            'ofc_division',
            'ofc_subdivision',
            'supervisor_name',
            'is_admin',
            'location',
        ]    

class ConsumerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Consumers
        fields='__all__'
        
        
class ConsumerWiseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Consumers
        fields='__all__'
        
class MridSerializer(serializers.ModelSerializer):
    class Meta:
        model=Consumers
        fields= ['ofc_section','mr_id']


class UserRegisterationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    
    class Meta:
        model=UserManagement
        # fields='__all__'
        fields=['ofc_discom','ofc_zone','ofc_circle','ofc_division','ofc_subdivision','ofc_section','ofc_agency','full_name','address','email','password','password2','mobile_number','designation','profile_pic','is_active','is_admin']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self,attrs):
            password=attrs.get('password')  
            password2=attrs.get('password2')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            return attrs
    def create(self,validated_data):
        return UserManagement.objects.create_user(**validated_data)
    
    
class FailedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumers
        fields = ['id', 'rdng_img', 'prsnt_rdng', 'prsnt_ocr_rdng']
    
    
        
class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=UserManagement
        fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserManagement
    fields = ['id', 'full_name','email','is_admin','profile_pic','ofc_agency','ofc_discom']

class ChangeUserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=255,style={"input_style":"password"},write_only=True)
    password2=serializers.CharField(max_length=255,style={"input_style":"password"},write_only=True)
    oldpassword=serializers.CharField(max_length=255,style={"input_style":"password"},write_only=True)
    
    class Meta:
        model=UserManagement
        fields=['password','password2','oldpassword']
    
    def validate(self, attrs):
        password=attrs['password']
        password2=attrs['password2']
        oldpassword=attrs['oldpassword']
        user=self.context['user']
        currentpassword=self.context['currentpassword']
        print("currentpassword",currentpassword)
        print("oldpassword",oldpassword)
        # if not user.check_password(oldpassword):
        #     raise serializers.ValidationError("Old password did not match")
        if not check_password(oldpassword,currentpassword):
             res=serializers.ValidationError({"error":"Old password did not match"})
             res.status_code=200
             raise res
            # raise APIException({"error":"Old password did not match"},)
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs

class SendResetPasswordEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    
    def validate(self,attrs):
        email=attrs['email']
        if UserManagement.objects.filter(email=email).exists():
            user=UserManagement.objects.get(email=email)
            print(user)
            print('uid only',user.id)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('encoded uid',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('password reset token',token)
            link = f"http://localhost:3000/api/user/reset/{uid}/{token}"
            print('password reset link',link)
            #send Email
            body = f"Click the following link to reset your password{link}"
            data={
                "email_subject":"Reset your password",
                "email_body":body,
                "to_email":user.email
            }
            Util.send_email(data)
            return attrs

        else:
            raise serializers.ValidationError("You are not a registered User")

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = UserManagement.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')


class Serail(serializers.Serializer):
    # mr_id=serializers.CharField()
    id=serializers.CharField()
    total=serializers.CharField()
    ok=serializers.CharField()
    passed=serializers.CharField()
    failed=serializers.CharField()
    # count_prsntrdngocrexcep_parameters_incorrect=serializers.IntegerField()
    md=serializers.CharField()
    dl=serializers.CharField()
    # count_prsntmtrstatus_door_locked=serializers.IntegerField()
    pass

class NotificationManiSerializer(serializers.ModelSerializer):
    # location_id = serializers.JSONField(required=False, initial=dict)
    class Meta:
        model=NotificationMani
        fields=['id','message_type','notification_criteria','location_id','notification_status','message_title','message_content','message_image_url','message_schedule_type','Message_delivery_date_time','scheduled_time']
class NotificationRecepientsSerializer(serializers.ModelSerializer):
    class Meta:
        model=notificatio_recepients
        fields=['notification_id','mr_id','mr_name','mr_token_id','mr_mobile_number','mr_location_section_id','message_delivery_status','message_title','message_content','message_image_url','mr_agency']


class UserManagementListSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserManagement
        fields='__all__'
    pass

class ConsumersMeterRegistration(serializers.Serializer):

    id=serializers.IntegerField()
    mrId=serializers.CharField()
    cons_ac_no=serializers.CharField()
    rdng_date=serializers.CharField()
    prsnt_mtr_status=serializers.CharField()
    prsnt_ocr_rdng=serializers.CharField()
    prsnt_rdng=serializers.CharField()
    ocr_pf_reading=serializers.CharField()
    cons_name=serializers.CharField()
    prsnt_md_rdng_ocr=serializers.CharField()
    rdng_ocr_status=serializers.CharField()
    rdng_img=serializers.CharField()
    prsnt_md_rdng=serializers.CharField()
    mrPhoto=serializers.CharField()
    total_count=serializers.IntegerField()
    prsnt_rdng_ocr_excep=serializers.CharField()
    reading_parameter_type=serializers.CharField()



#ghulam
class UserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserManagement
        fields=['email','ofc_discom','ofc_zone','ofc_circle','ofc_division','is_admin','designation','full_name']