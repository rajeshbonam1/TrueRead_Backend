from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
# Create your models here.

#  Custom User Manager

class Consumers(models.Model):
    ofc_discom=models.CharField(max_length=300,null=True,blank=True)
    ofc_zone=models.CharField(max_length=300,null=True,blank=True)
    ofc_circle= models.CharField(max_length=300,null=True,blank=True)
    ofc_division=models.CharField(max_length=300,null=True,blank=True)
    ofc_sub_div_code= models.CharField(max_length=300,null=True,blank=True)
    ofc_subdivision=models.CharField(max_length=300,null=True,blank=True)
    ofc_section=models.CharField(max_length=300, null=True,blank=True)
    mr_unit=models.CharField(max_length=300, null=True,blank=True)
    bl_area_code=models.CharField(max_length=300, null=True,blank=True)
    bl_agnc_type=models.CharField(max_length=300,null=True,blank=True)
    bl_agnc_name= models.CharField(max_length=300,null=True,blank=True)
    mr_id= models.CharField(max_length=300,null=True,blank=True)
    mr_ph_no=models.CharField(max_length=300, null=True,blank=True)
    cons_ac_no= models.CharField(max_length=300, null=True,blank=True)
    cons_name= models.CharField(max_length=300,null=True,blank=True)
    cons_address= models.CharField(max_length=300,null=True,blank=True)
    cons_ph_no=models.CharField(max_length=300,null=True,blank=True)
    cons_vill_name=models.CharField(max_length=300,null=True,blank=True)
    cons_fdr_name=models.CharField(max_length=300,null=True,blank=True)
    con_dtc=models.CharField(max_length=300,null=True,blank=True)
    con_trf_cat=models.CharField(max_length=300,null=True,blank=True)
    con_mtr_sl_no= models.CharField(max_length=300, null=True,blank=True)
    con_mtr_phs= models.CharField(max_length=300,null=True,blank=True)
    rdng_inc_deci=models.CharField(max_length=300,null=True,blank=True)
    rdng_req_val= models.CharField(max_length=300,null=True,blank=True)
    prev_rdng=models.CharField(max_length=300,null=True,blank=True)
    prev_md= models.CharField(max_length=300,null=True,blank=True)
    prev_pf_rdng=models.CharField(max_length=300,null=True,blank=True)
    prev_rdng_date=models.CharField(max_length=300,null=True,blank=True)
    prev_bl_mnth=models.CharField(max_length=300,null=True,blank=True)
    prev_rdng_status=models.CharField(max_length=300,null=True,blank=True)
    bl_mnth= models.CharField(max_length=300,null=True,blank=True)
    rdng_date= models.CharField(max_length=300,null=True,blank=True)
    geo_lat=models.CharField(max_length=300,null=True,blank=True)
    geo_long=models.CharField(max_length=300,null=True,blank=True)
    prsnt_mtr_status=models.CharField(max_length=300,null=True,blank=True)
    abnormality= models.CharField(max_length=300,null=True,blank=True)
    mr_rmrk= models.CharField(max_length=300,null=True,blank=True)
    mtr_excep_img= models.CharField(max_length=300,null=True,blank=True)
    rdng_ocr_status=models.CharField(max_length=300,null=True,blank=True)
    prsnt_ocr_rdng=models.CharField(max_length=300,null=True,blank=True)
    prsnt_rdng=models.CharField(max_length=300, null=True,blank=True)
    prsnt_rdng_ocr_excep=models.CharField(max_length=300,null=True,blank=True)
    rdng_img= models.CharField(max_length=300,null=True,blank=True)
    ocr_md_status= models.CharField(max_length=300,null=True,blank=True)
    prsnt_md_rdng_ocr=models.CharField(max_length=300,null=True,blank=True)
    prsnt_md_rdng=models.CharField(max_length=300,null=True,blank=True)
    md_ocr_excep=models.CharField(max_length=300,null=True,blank=True)
    md_img=models.CharField(max_length=300,null=True,blank=True)
    ocr_pf_status=models.CharField(max_length=300,null=True,blank=True)
    ocr_pf_reading= models.CharField(max_length=300,null=True,blank=True)
    pf_image=models.CharField(max_length=300,null=True,blank=True)
    pf_manual_reading=models.CharField(max_length=300,null=True,blank=True)
    pf_ocr_exception=models.CharField(max_length=300,null=True,blank=True)
    ai_mdl_ver=models.CharField(max_length=300,null=True,blank=True)
    ph_name= models.CharField(max_length=300,null=True,blank=True)
    cmra_res=models.CharField(max_length=300,null=True,blank=True)
    andr_ver= models.CharField(max_length=300,null=True,blank=True)
    data_sync_date=models.CharField(max_length=300,null=True,blank=True)
    qc_req= models.CharField(max_length=300,null=True,blank=True)
    ba_cons_id=models.CharField(max_length=300,null=True,blank=True)
    ba_ac_id= models.CharField(max_length=300,null=True,blank=True)
    ba_prsnt_rdng_status= models.CharField(max_length=300,null=True,blank=True)
    ba_mrc= models.CharField(max_length=300,null=True,blank=True)
    ba_mru=models.CharField(max_length=300,null=True,blank=True)
    ba_subdiv=models.CharField(max_length=300,null=True,blank=True)
    ba_div= models.CharField(max_length=300,null=True,blank=True)
    ba_geo_lati=models.CharField(max_length=300,null=True,blank=True)
    ba_geo_long=models.CharField(max_length=300,null=True,blank=True)
    ba_agnc_id=models.CharField(max_length=300,null=True,blank=True)
    ba_bl_id= models.CharField(max_length=300,null=True,blank=True)
    ba_bl_date= models.CharField(max_length=300,null=True,blank=True)
    ba_prev_rdng_status=models.CharField(max_length=300,null=True,blank=True)
    qc_done=models.CharField(max_length=300,null=True,blank=True)
    qc_done_user_id=models.CharField(max_length=300,null=True,blank=True)
    qc_date= models.CharField(max_length=300,null=True,blank=True)
    qc_flag=models.CharField(max_length=300,null=True,blank=True)
    qc_rmrk= models.CharField(max_length=300,null=True,blank=True)
    ai_retrain= models.CharField(max_length=300,null=True,blank=True)
    ocr_status= models.CharField(max_length=300,null=True,blank=True)
    uploaded_datetime=models.DateTimeField(auto_now_add=True)
    is_object_meter=models.CharField(max_length=300,null=True,blank=True)
    mr_success_feedback=models.CharField(max_length=300,null=True,blank=True)
    reading_parameter_type=models.CharField(max_length=300,null=True,blank=True)
    md_reading_parameter_type=models.CharField(max_length=300,null=True,blank=True)
    pf_reading_parameter_type=models.CharField(max_length=300,null=True,blank=True)
    bill_month_dt=models.DateField(null=True,blank=True)
    prsnt_rdng_ocr_odv=models.CharField(max_length=100,null=True,blank=True)
    rdng_ocr_status_odv=models.CharField(max_length=100,null=True,blank=True)
    rdng_ocr_status_changed_by=models.CharField(max_length=100,null=True,blank=True)
    date_qc= models.CharField(max_length=300,null=True,blank=True)
    kvah_manual = models.CharField( max_length= 200, null=True,  blank=True)
    kvah_Status = models.CharField( max_length= 200, null=True,  blank=True)
    mtr_sr_no = models.CharField( max_length= 200, null=True,  blank=True)
   

    #qc fields
    abnormalities_confirm=models.CharField(max_length=300,null=True,blank=True)
    ocrexception_confirm=models.CharField(max_length=300,null=True,blank=True)
    qc_recommendation=models.CharField(max_length=300,null=True,blank=True)
    qc_report_action=models.CharField(max_length=300,null=True,blank=True)
    qc_meter_status=models.CharField(max_length=300,null=True,blank=True)
    qc_ocr_status=models.CharField(max_length=300,null=True,blank=True)
    reading_date_db=models.DateField(null=True,blank=True)
    manual_update_flag=models.CharField( max_length=50,null=True,blank=True)
    prsnt_ocr_excep_old_values=models.CharField( max_length=50,null=True,blank=True)
    
    #kvah readings
    kvah_rdng = models.CharField( max_length=200, null=True, blank=True)
    kvah_img = models.CharField( max_length= 200, null=True,  blank=True)
    kvah_manual = models.CharField( max_length= 200, null=True,  blank=True)
    kvah_Status = models.CharField( max_length= 200, null=True,  blank=True)

    #spoofed_status
    is_spoofed = models.BooleanField(default=False)

    #ekwh and ekvah data
    ekwh_img = models.CharField( max_length=300, null=True, blank=True)
    ekwh_ocr_rdng = models.CharField( max_length=300, null=True, blank=True)
    ekwh_manual_rdng = models.CharField( max_length=300, null=True, blank=True)
    ekvah_img = models.CharField( max_length=300, null=True, blank=True)
    ekvah_ocr_rdng = models.CharField( max_length=300, null=True, blank=True)
    ekvah_manual_rdng = models.CharField( max_length=300, null=True, blank=True)

    #ekvah 
    calculatedkvah = models.CharField(max_length=300, null=True, blank=True)
    calculatedkva = models.CharField(max_length=300, null=True, blank=True)

 
    

    
    class Meta:
        db_table='readingmaster'



class MeterReaderRegistration(models.Model):

    mrId=models.CharField(max_length=200,unique=True)
    mrName=models.CharField(max_length=200,null=True,blank=True)
    
    section=models.CharField(max_length=200,null=True,blank=True)

    discom=models.CharField(max_length=200,null=True,blank=True)
    zone=models.CharField(max_length=200,null=True,blank=True)
    circle=models.CharField(max_length=200,null=True,blank=True)
    division=models.CharField(max_length=200,null=True,blank=True)
    subdivision=models.CharField(max_length=200,null=True,blank=True)
    sectioncode=models.CharField(max_length=200,null=True,blank=True)
    
    mrPhone=models.CharField(max_length=200,null=True,blank=True)
    mrPhoto=models.CharField(max_length=200,null=True,blank=True)
    androidToken=models.CharField(max_length=200,null=True,blank=True)
    uploaded_datetime=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='meterreaderregistration'
        

class Office(models.Model):
    discom=models.CharField(max_length=200)
    zone=models.CharField(max_length=200)
    circlename=models.CharField(max_length=200)
    divisionname=models.CharField(max_length=200)
    divisioncode=models.CharField(max_length=200)
    subdivision=models.CharField(max_length=200)
    subdivisioncode=models.CharField(max_length=200)
    sectionname=models.CharField(max_length=200)
    sectioncode=models.CharField(max_length=200)
    agency=models.CharField(max_length=200,null=True,blank=True)
    agencycode=models.CharField(max_length=200,null=True,blank=True)
    class Meta:
        db_table='office'

class MyUserManager(BaseUserManager):

    def create_user(self, email, full_name,mobile_number,profile_pic,designation,address,is_active,is_admin,ofc_agency=None,ofc_section=None,ofc_subdivision=None,ofc_division=None,ofc_circle=None,ofc_zone=None,ofc_discom=None,password=None,password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            mobile_number=mobile_number,
            designation=designation,
            address=address,
            ofc_agency=ofc_agency,
            ofc_section=ofc_section,
            ofc_subdivision=ofc_subdivision,
            ofc_division=ofc_division,
            ofc_circle=ofc_circle,
            ofc_zone=ofc_zone,
            ofc_discom=ofc_discom,
            profile_pic=profile_pic,
            is_active=is_active,
            is_admin=is_admin
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email,mobile_number,full_name,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
            mobile_number=mobile_number
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

 #Custom user model

class UserManagement(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    ofc_discom=models.CharField(max_length=100,null=True,blank=True)
    ofc_zone=models.CharField(max_length=100,null=True,blank=True)
    ofc_circle= models.CharField(max_length=200,null=True,blank=True)
    ofc_division=models.CharField(max_length=200,null=True,blank=True)
    ofc_subdivision=models.CharField(max_length=200,null=True,blank=True)
    ofc_section=models.CharField(max_length=200, null=True,blank=True)
    ofc_agency=models.CharField(max_length=200, null=True,blank=True)
    full_name=models.CharField(max_length=200, null=True,blank=True)
    address=models.CharField(max_length=300, null=True,blank=True)
    mobile_number=models.BigIntegerField()
    designation=models.CharField(max_length=300, null=True,blank=True)
    profile_pic=models.CharField(max_length=300, null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']
    def __str__(self):

        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    class Meta:
        db_table='usermanagement'

class NotificationMani(models.Model):
    message_type=models.CharField(max_length=200,null=True,blank=True)
    notification_criteria=models.CharField(max_length=200,null=True,blank=True)
    location_id=models.CharField(max_length=200,null=True,blank=True)
    notification_status=models.CharField(max_length=200,null=True,blank=True)
    message_image_url=models.CharField(max_length=350,null=True,blank=True)
    message_title=models.CharField(max_length=200,null=True,blank=True)
    message_content=models.CharField(max_length=200,null=True,blank=True)
    message_schedule_type=models.CharField(max_length=200,null=True,blank=True)
    Message_delivery_date_time=models.DateTimeField(auto_now_add=True)
    scheduled_time=models.CharField(max_length=200,null=True,blank=True)
    class Meta:
        db_table='notification_main'

    
class notificatio_recepients(models.Model):
    notification_id=models.ForeignKey(NotificationMani,on_delete=models.CASCADE)
    mr_id=models.CharField(max_length=200,null=True,blank=True)
    mr_name=models.CharField(max_length=200,null=True,blank=True)
    mr_token_id=models.CharField(max_length=200,null=True,blank=True)
    mr_mobile_number=models.CharField(max_length=200,null=True,blank=True)
    mr_location_section_id=models.CharField(max_length=200,null=True,blank=True)
    message_image_url=models.CharField(max_length=350,null=True,blank=True)
    message_delivery_status=models.CharField(max_length=200,null=True,blank=True)
    message_title=models.CharField(max_length=200,null=True,blank=True)
    message_content=models.CharField(max_length=200,null=True,blank=True)
    mr_agency=models.CharField(max_length=200,null=True,blank=True)
    class Meta:
        db_table='notification_recepients'        
        
        
from django.db import models

class SupervisorLogin(models.Model):
    id = models.AutoField(primary_key=True)
    supervisor_number = models.CharField(max_length=15, unique=False)
    password = models.CharField(max_length=128)

    ofc_division = models.CharField(max_length=100, null=True, blank=True)
    ofc_subdivision = models.CharField(max_length=100, null=True, blank=True)
    mr_id = models.CharField(max_length=100, null=True, blank=True)
    mr_name = models.CharField(max_length=100, null=True, blank=True)
    mr_number = models.CharField(max_length=100, null=True, blank=True)
    supervisor_name = models.CharField(max_length=100, null=True, blank=True)
    discom = models.CharField(max_length=100, null=True, blank=True)

    is_admin = models.BooleanField(default=True)

    class Meta:
        db_table = "supervisorlogin"

class SupervsiorLocation(models.Model):
    id = models.AutoField(primary_key=True)
    supervisor_number = models.CharField(max_length=15)
    date = models.DateField()
    meta = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table = "supervsiorlocation"
        constraints = [
            models.UniqueConstraint(
                fields=['supervisor_number', 'date'],
                name='unique_supervisor_date'
            )
        ]