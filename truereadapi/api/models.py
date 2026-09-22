from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# ============================================================
# REFERENCE TABLES
# ============================================================


class Abnormality(models.Model):
    abnormality_id = models.SmallAutoField(primary_key=True)
    abnormality_code = models.CharField(max_length=100, unique=True)
    abnormality_label = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_provisional = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "abnormality"

    def __str__(self):
        return self.abnormality_label


class Agency(models.Model):
    agency_id = models.SmallAutoField(primary_key=True)
    agency_code = models.CharField(max_length=30, unique=True)
    agency_name = models.CharField(max_length=100)
    agency_type = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    is_provisional = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "agency"

    def __str__(self):
        return self.agency_name


class ImageCheck(models.Model):
    image_check_id = models.SmallAutoField(primary_key=True)
    check_code = models.CharField(max_length=30, unique=True)
    check_label = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_provisional = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "image_check"

    def __str__(self):
        return self.check_label


class MeterPhase(models.Model):
    meter_phase_id = models.SmallAutoField(primary_key=True)
    phase_code = models.CharField(max_length=10, unique=True)
    phase_label = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_provisional = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "meter_phase"

    def __str__(self):
        return self.phase_label


class MeterStatus(models.Model):
    meter_status_id = models.SmallAutoField(primary_key=True)
    status_code = models.CharField(max_length=20, unique=True)
    status_label = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_provisional = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "meter_status"

    def __str__(self):
        return self.status_label


class OcrException(models.Model):
    ocr_exception_id = models.SmallAutoField(primary_key=True)
    exception_code = models.CharField(max_length=100, unique=True)
    exception_label = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_provisional = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "ocr_exception"

    def __str__(self):
        return self.exception_label


class OcrStatus(models.Model):
    ocr_status_id = models.SmallAutoField(primary_key=True)
    status_code = models.CharField(max_length=20, unique=True)
    status_label = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_provisional = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "ocr_status"

    def __str__(self):
        return self.status_label


# ============================================================
# OFFICE
# ============================================================


class Office(models.Model):
    office_id = models.AutoField(primary_key=True)

    discom_name = models.CharField(max_length=50)

    zone_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    circle_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    division_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    division_code = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    subdivision_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    subdivision_code = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    section_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    section_code = models.CharField(max_length=20)

    agency_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    agency = models.ForeignKey(
        Agency,
        on_delete=models.DO_NOTHING,
        db_column="agency_id",
        null=True,
        blank=True,
        related_name="offices",
    )

    is_provisional = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "office"

    def __str__(self):
        return self.section_name or str(self.office_id)


# ============================================================
# METER READER
# ============================================================


class MeterReader(models.Model):
    meter_reader_id = models.AutoField(primary_key=True)

    reader_code = models.CharField(max_length=20)

    reader_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    phone_no = models.CharField(
        max_length=15,
        null=True,
        blank=True,
    )

    photo_img_key = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    office = models.ForeignKey(
        Office,
        on_delete=models.DO_NOTHING,
        db_column="office_id",
        null=True,
        blank=True,
        related_name="meter_readers",
    )

    created_at = models.DateTimeField()

    is_provisional = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "meter_reader"

    def __str__(self):
        return self.reader_name or self.reader_code


# ============================================================
# METER READING
# ============================================================


class MeterReading(models.Model):
    reading_id = models.BigAutoField(primary_key=True)

    consumer_account_no = models.CharField(max_length=20)

    office = models.ForeignKey(
        Office,
        on_delete=models.DO_NOTHING,
        db_column="office_id",
        related_name="meter_readings",
    )

    billing_month = models.DateField()

    read_at = models.DateTimeField()

    agency = models.ForeignKey(
        Agency,
        on_delete=models.DO_NOTHING,
        db_column="agency_id",
        null=True,
        blank=True,
        related_name="meter_readings",
    )

    meter_reader = models.ForeignKey(
        MeterReader,
        on_delete=models.DO_NOTHING,
        db_column="meter_reader_id",
        null=True,
        blank=True,
        related_name="meter_readings",
    )

    billing_area_code = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    consumer_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    tariff_category = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    meter_serial_no = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    meter_type = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    meter_phase = models.ForeignKey(
        MeterPhase,
        on_delete=models.DO_NOTHING,
        db_column="meter_phase_id",
        null=True,
        blank=True,
        related_name="meter_readings",
    )

    meter_multiplication_factor = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )

    previous_read_date = models.DateField(
        null=True,
        blank=True,
    )

    previous_reading = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    meter_status = models.ForeignKey(
        MeterStatus,
        on_delete=models.DO_NOTHING,
        db_column="meter_status_id",
        null=True,
        blank=True,
        related_name="meter_readings",
    )

    # --------------------------------------------------------
    # KWH
    # --------------------------------------------------------

    kwh_reading = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    kwh_ocr_reading = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    kwh_ocr_status = models.ForeignKey(
        OcrStatus,
        on_delete=models.DO_NOTHING,
        db_column="kwh_ocr_status_id",
        null=True,
        blank=True,
        related_name="kwh_readings",
    )

    kwh_ocr_exception = models.ForeignKey(
        OcrException,
        on_delete=models.DO_NOTHING,
        db_column="kwh_ocr_exception_id",
        null=True,
        blank=True,
        related_name="kwh_readings",
    )

    kwh_img_key = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    kwh_parameter_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    kwh_img_check = models.ForeignKey(
        ImageCheck,
        on_delete=models.DO_NOTHING,
        db_column="kwh_img_check_id",
        null=True,
        blank=True,
        related_name="meter_readings",
    )

    # --------------------------------------------------------
    # READING METADATA
    # --------------------------------------------------------

    reader_remark = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    abnormality = models.ForeignKey(
        Abnormality,
        on_delete=models.DO_NOTHING,
        db_column="abnormality_id",
        null=True,
        blank=True,
        related_name="meter_readings",
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    is_spoofed = models.BooleanField(
        null=True,
        blank=True,
    )

    change_type = models.SmallIntegerField(
        null=True,
        blank=True,
    )

    uploaded_at = models.DateTimeField()

    synced_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    content_hash = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = "meter_reading"

    def __str__(self):
        return self.consumer_account_no


# ============================================================
# METER READING DETAIL
# ============================================================


class MeterReadingDetail(models.Model):
    reading = models.OneToOneField(
        MeterReading,
        on_delete=models.CASCADE,
        db_column="reading_id",
        primary_key=True,
        related_name="detail",
    )

    # --------------------------------------------------------
    # MD
    # --------------------------------------------------------

    md_reading = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )

    md_ocr_reading = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )

    md_ocr_status = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    md_ocr_exception = models.ForeignKey(
        OcrException,
        on_delete=models.DO_NOTHING,
        db_column="md_ocr_exception_id",
        null=True,
        blank=True,
        related_name="md_details",
    )

    md_img_key = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    md_parameter_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    # --------------------------------------------------------
    # POWER FACTOR
    # --------------------------------------------------------

    pf_reading = models.DecimalField(
        max_digits=4,
        decimal_places=3,
        null=True,
        blank=True,
    )

    pf_ocr_reading = models.DecimalField(
        max_digits=4,
        decimal_places=3,
        null=True,
        blank=True,
    )

    pf_ocr_status = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    pf_ocr_exception = models.ForeignKey(
        OcrException,
        on_delete=models.DO_NOTHING,
        db_column="pf_ocr_exception_id",
        null=True,
        blank=True,
        related_name="pf_details",
    )

    pf_img_key = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    pf_parameter_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    # --------------------------------------------------------
    # KVAH / KVA
    # --------------------------------------------------------

    kvah_reading = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    kvah_ocr_reading = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    kvah_ocr_status = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    kvah_img_key = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    calculated_kvah = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    calculated_kva = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    # --------------------------------------------------------
    # EKWH / EKVAH
    # --------------------------------------------------------

    ekwh_reading = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    ekwh_ocr_reading = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    ekwh_img_key = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    ekvah_reading = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    ekvah_ocr_reading = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    ekvah_img_key = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = "meter_reading_detail"


# ============================================================
# OCR OVERRIDE
# ============================================================


class OcrOverride(models.Model):
    reading = models.OneToOneField(
        MeterReading,
        on_delete=models.CASCADE,
        db_column="reading_id",
        primary_key=True,
        related_name="ocr_override",
    )

    overridden_ocr_reading = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    overridden_ocr_status = models.ForeignKey(
        OcrStatus,
        on_delete=models.DO_NOTHING,
        db_column="overridden_ocr_status_id",
        null=True,
        blank=True,
        related_name="ocr_overrides",
    )

    overridden_ocr_exception = models.ForeignKey(
        OcrException,
        on_delete=models.DO_NOTHING,
        db_column="overridden_ocr_exception_id",
        null=True,
        blank=True,
        related_name="ocr_overrides",
    )

    changed_by = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = "ocr_override"

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
        managed = False

class NotificationMani(models.Model):
    id = models.BigAutoField(primary_key=True)

    message_type = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    notification_criteria = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    location_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    notification_status = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    message_image_url = models.CharField(
        max_length=350,
        null=True,
        blank=True,
    )

    message_title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    message_content = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    message_schedule_type = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    Message_delivery_date_time = models.DateTimeField(
        db_column="Message_delivery_date_time",
    )

    scheduled_time = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = "notification_main"


class NotificationRecipients(models.Model):
    id = models.BigAutoField(primary_key=True)

    mr_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    mr_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    mr_token_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    mr_mobile_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    mr_location_section_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    message_image_url = models.CharField(
        max_length=350,
        null=True,
        blank=True,
    )

    message_delivery_status = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    message_title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    message_content = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    mr_agency = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    notification_id = models.ForeignKey(
        NotificationMani,
        on_delete=models.DO_NOTHING,
        db_column="notification_id_id",
        related_name="recipients",
    )

    class Meta:
        managed = False
        db_table = "notification_recepients"        
        
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