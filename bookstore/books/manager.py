from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

class UserManager(BaseUserManager):
    # use_in_migrations = True

    def create_user(self, username ,password, **extra_fields):
        print('Hiii')
        if not username:
            raise ValueError('Username is required........')
        user = self.model(username = username,  
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        # user = self.model(username = username , **extra_fields)
        # user.set_password(password)
        # user.save()
        

        return self.create_user(username, password, **extra_fields)