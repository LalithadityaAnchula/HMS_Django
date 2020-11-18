from django.db import models
from django.core.exceptions import ValidationError
from students.models import Document, FeeDetail, RoomDetail, Attendance
from django.conf import settings

# Create your models here.
class Student(models.Model):
    YEAR = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )

    GENDER=(
        ('Male','Male'),
        ('Female','Female'),
    )

    def photo_storage_path(instance, filename):
        extension = filename.split('.')[-1]
        return 'Student-Photos/Year-{}/{}.{}'.format(instance.year, instance.regd_no, extension)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    account_email = models.EmailField(unique=True, null=False)
    regd_no = models.CharField(unique=True, null=False, max_length=20)
    roll_no = models.CharField(unique=True, null=False, max_length=20)
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=True, blank=True)
    year = models.IntegerField(null=False, choices=YEAR)
    branch = models.CharField(max_length=40,null=False)
    gender = models.CharField(max_length=7,choices=GENDER,null=False)
    pwd = models.BooleanField(null=False, default=False)
    community = models.CharField(max_length=25, null=True, blank=True)
    dob = models.DateField(null=False)
    blood_group = models.CharField(max_length=25, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(null=False, max_length=10)
    parents_phone = models.CharField(null=False, max_length=10)
    emergency_phone = models.CharField(null=True, blank=True, max_length=10)
    address = models.TextField(null=False)
    photo = models.ImageField(null=True, blank=True, upload_to=photo_storage_path)
    is_hosteller = models.BooleanField(null=False, default=True)

    def __str__(self):
        return str(self.regd_no)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_hosteller:
            if not RoomDetail.objects.filter(student = self).exists():
                RoomDetail.objects.create(student=self)
            if not Attendance.objects.filter(student = self).exists():
                Attendance.objects.create(student=self)
            if not Document.objects.filter(student = self).exists():
                Document.objects.create(student = self)
            if not FeeDetail.objects.filter(student = self).exists():
                FeeDetail.objects.create(student = self)


class Official(models.Model):
    EMP=(
        ('Caretaker','Caretaker'),
        ('Warden','Warden'),
        ('Deputy Chief-Warden', 'Deputy Chief-Warden'),
        ('Chief-Warden','Chief-Warden'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    account_email = models.EmailField(unique=True, null=False)
    emp_id = models.CharField(unique=True,null=False, max_length=20)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=20,choices=EMP)
    phone = models.CharField(max_length=10, null=False)
    email = models.EmailField(null=True, blank=True)
    block = models.ForeignKey('institute.Block', on_delete=models.SET_NULL, null=True, blank=True)

    def is_chief(self):
        return (self.designation == 'Deputy Chief-Warden' or self.designation == 'Chief-Warden')

    def clean(self):
        if self.is_chief() and self.block != None:
            raise ValidationError('Chief Warden and Deputy Chief Warden cannot be assigned a block.')

    def __str__(self):
        return str(self.emp_id)


class Block(models.Model):
    OPTION=(
          ('1S','One student per Room'),
          ('2S','Two students per Room'),
          ('4S','Four students per Room'),
     )

    GENDER=(
        ('Male','Male'),
        ('Female','Female'),
     )

    block_id = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=50,null=False)
    room_type = models.CharField(max_length=2,choices=OPTION)
    gender = models.CharField(max_length=7,choices=GENDER)
    capacity = models.IntegerField(null=False)

    def __str__(self):
        return self.name

    def short_name(self):
        return self.name.split()[0]

    def student_capacity(self):
        if self.room_type == '4S':   return self.capacity*4
        elif self.room_type == '2S': return self.capacity*2
        elif self.room_type == '1S': return self.capacity

    def students(self):
        return RoomDetail.objects.filter(block=self)

    def caretaker(self):
        return self.official_set.filter(designation='Caretaker').first()

    def warden(self):
        return self.official_set.filter(designation='Warden').first()