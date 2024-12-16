from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.forms import ValidationError
from django.utils import timezone
from ltosim.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models import Max

from ltosim.settings import MAX_LESSON1_LEVELS_ENV, MAX_LESSON2_LEVELS_ENV, MAX_LESSON3_LEVELS_ENV


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_("email address"), unique=True)
    picture = models.ImageField(
        upload_to='images/', blank=True, null=True, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def username(self):
        return self.email

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"


def gen_session_no(lesson_name=None, user=None) -> int:
    today = timezone.now()

    if lesson_name is not None and user is not None:
        filter = Score.objects.filter(user=user, lesson_name=lesson_name)
        max = filter.aggregate(Max('session_no'))
        maximum = max['session_no__max']
        count = filter.count()
        if lesson_name == 'Learn ABC':
            if count > int(MAX_LESSON1_LEVELS_ENV):
                return maximum + 1
        elif lesson_name == 'Spelling':
            if count > int(MAX_LESSON2_LEVELS_ENV):
                return maximum + 1
        else:
            if count > int(MAX_LESSON3_LEVELS_ENV):
                return maximum + 1
    return 1

class Announcement(models.Model):
    title = models.CharField(max_length=255, blank=False, default='')
    description = models.CharField(max_length=255, blank=True)
    content = models.CharField(max_length=2048)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    date_valid = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)
    posted = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Download(models.Model):
    title = models.CharField(max_length=255, blank=False, default='')
    description = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    date = models.DateField(default=timezone.now)
    downloadable = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Score(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    lesson_name = models.CharField(max_length=50)
    time = models.FloatField(default=0)
    summary = models.CharField(max_length=256)

    session_no = models.PositiveIntegerField(default=gen_session_no)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def summarize(self):
        return f"Date: {self.date}, Lesson Name: {self.lesson_name}, Score: {self.score}, Time: {self.time}, Session No. {self.session_no}, Summary: {self.summary}"

    def save(self, *args, **kwargs):
        self.session_no = gen_session_no(self.lesson_name, self.user)
        super().save(*args, **kwargs)  # Call the "real" save() method.

class ReviewerCategories(models.IntegerChoices):
    CAR_TRAFFIC_RULES = 0, "Traffic Rules and Regulations(Car)"
    CAR_ROAD_SIGNAGE = 1, "Road Signage(Car)"
    CAR_VEHICLE_PARTS = 2, "Vehicle Basic Parts(Car)"
    MOTOR_TRAFFIC_RULES = 3, "Traffic Rules and Regulations(Motorcycle)"
    MOTOR_ROAD_SIGNAGE = 4, "Road Signage(Motorcycle)"
    MOTOR_VEHICLE_PARTS = 5, "Vehicle Basic Parts(Motorcycle)"

class Reviewer(models.Model):
    key = models.CharField(max_length=50, blank=False, verbose_name="Title")
    category = models.PositiveSmallIntegerField(choices=ReviewerCategories.choices, default=ReviewerCategories.CAR_TRAFFIC_RULES)
    picture = models.ImageField(
        upload_to='images/', blank=True, null=True, default='')
    content = models.TextField(blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    order_position = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('category', 'order_position')

    def __str__(self):
        return self.key

class Question(models.Model):
    text = models.TextField(blank=False)
    category = models.PositiveSmallIntegerField(choices=ReviewerCategories.choices, default=ReviewerCategories.CAR_TRAFFIC_RULES)
    choice1 = models.CharField(max_length=255)
    choice2 = models.CharField(max_length=255)
    choice3 = models.CharField(max_length=255)
    correct_choice = models.CharField(max_length=255)
    picture = models.ImageField(
        upload_to='images/questions/', blank=True, null=True, default='')

    def clean(self):
        # Check that none of the choices are blank
        if not self.choice1 or not self.choice2 or not self.choice3:
            raise ValidationError("All choices must be provided and cannot be blank.")
        
        # Check that the correct_choice is one of the choices
        if self.correct_choice not in [self.choice1, self.choice2, self.choice3]:
            raise ValidationError("Correct choice must be one of the given choices.")
    
    def save(self, *args, **kwargs):
        self.full_clean()  # This will call clean() and raise ValidationError if validation fails
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text
    
class TopUpRecord(models.Model):
    email = models.EmailField()  # Stores the PlayFab user's email
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.amount} - {self.timestamp}"
