from django.contrib.auth.base_user import BaseUserManager


class CCMSUserManager(BaseUserManager):
    """
    Custom user manager for the City Complaints Management System.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **kwaargs):
        email = self.normalize_email(email)
        user = self.model(email=self.normalize_email(email), **kwaargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwaargs):
        kwaargs.setdefault('is_active', True)
        kwaargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwaargs)

    def create_superuser(self, email, password, **kwaargs):
        kwaargs.setdefault('is_active', True)
        kwaargs.setdefault('is_staff', True)
        kwaargs.setdefault('is_superuser', True)
        return self._create_user(email, password, **kwaargs)
