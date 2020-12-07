import uuid
import data_list
from django.db import models
from django.contrib.auth.models import AbstractUser as BaseAbstractUser
from django.core import validators
from django.utils.translation import gettext_lazy as _
from emanagement import utils


class Countrie(models.Model):
    name = models.CharField(max_length=30)
    sortname = models.CharField(max_length=3)
    phone_code = models.IntegerField(max_length=6)

class State(models.Model):
    name = models.CharField(max_length=20)
    country = models.ForeignKey(Countrie, on_delete=models.CASCADE)

class City(models.Model):
    name = models.CharField(max_length=20)
    state = models.ForeignKey(State, on_delete=models.CASCADE)



class AbstractUser(BaseAbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=20,
        validators=[
            validators.RegexValidator(regex=r"^[A-Za-z ]+$", message=_("Enter Valid First Name."))],
        null=True,
    )
    middle_name = models.CharField(
        verbose_name=_("Middle Name"),
        max_length=20,
        validators=[
            validators.RegexValidator(regex=r"^[A-Za-z ]+$", message=_("Enter Valid Middle Name."))],
        null=True,
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=20,
        validators=[
            validators.RegexValidator(regex=r"^[A-Za-z]+$", message=_("Enter Valid Last Name."))],
        null=True,
    )

    email = models.EmailField(
        verbose_name=_('email'),
        max_length=30,
        unique=True,
    )
    date_of_birth = models.DateField(
        verbose_name=_("Data of Birth"),
        null=True,
        validators=[utils.age]
    )
    phone_number = models.CharField(verbose_name=_("Phone Number"),
                                    max_length=13,
                                    null=True,
                                    validators=[validators.RegexValidator(
                                        regex=r"^[4-9]\d{9}$", message=_("Enter Valid Phone Number.")), ]
                                    )
    country = models.ForeignKey(Countrie, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    pincode = models.CharField(verbose_name=_("Pincode"), max_length=6,
                               null=True,
                               )
    full_address = models.TextField(verbose_name=_("Full Address"),
                                    null=True,
                                    max_length=50,
                                    )
    profile = models.FileField(upload_to=utils.pic_upload,
                               default='user.jpg', blank=True,
                               validators=[validators.FileExtensionValidator(
                                   allowed_extensions=validators.get_available_image_extensions(),
                                   message=_(
                                       "Select valid Cover Image.")
                               ), utils.profile_size
                               ],)
   
    class Meta(BaseAbstractUser.Meta):
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.
    Username and password are required. Other fields are optional.
    """
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'