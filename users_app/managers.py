from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Manage users authenticated by their email address."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and persist a user with the given credentials."""
        if not email:
            raise ValueError("The email address is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create a regular application user."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create an administrative superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        self._validate_superuser_flags(extra_fields)

        return self._create_user(email, password, **extra_fields)

    @staticmethod
    def _validate_superuser_flags(extra_fields):
        """Ensure required administrative flags are enabled."""
        if extra_fields.get("is_staff") is not True:
            raise ValueError("A superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("A superuser must have is_superuser=True")