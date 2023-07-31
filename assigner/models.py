from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from common.enums import (
    GENDER_CHOICES,
    ROLE_CHOICES,
)
from common.utils import (
    unique_slug_generator,
)


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password):
        user = self.model(email=self.normalize_email(email), password=password)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.role = "SU"
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, db_index=True
    )
    slug = models.SlugField(unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(unique=True, max_length=10, null=True, blank=True)
    email = models.EmailField(
        verbose_name="email address", unique=True, null=True, blank=True
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")
    date_of_birth = models.DateField(null=True, blank=True)
    profile_pic = models.URLField(max_length=500, null=True, blank=True)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default="U")
    joined_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f"{self.full_name}--{self.email}"

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        if self.is_blocked:
            return False
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.role == "SU" and not self.is_blocked

    @property
    def is_superuser(self):
        return self.is_superuser == "SU"

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "All Users"


@receiver(pre_save, sender=User)
def user_pre_save_receiver(sender, instance=User, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_projects"
    )
    contributors = models.ManyToManyField(User, related_name="contributed_projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    assignee = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
