from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields): #Methode nur für diese Datei, also interne Verwendung
        if not email:
            raise ValueError("The email address is required")

        email = self.normalize_email(email) #alles wird klein geschrieben
        user = self.model(email=email, **extra_fields) #das wird model, speicher alle felder
        user.set_password(password) #password wird gehash und nicht direkt gespeichert. 
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        self._validate_superuser_flags(extra_fields)

        return self._create_user(email, password, **extra_fields)

    @staticmethod #decorator, kein self nötig, prüft ausschließlich ubergebene Dictionary
    def _validate_superuser_flags(extra_fields): #überprüfen Admineinstellungen
        if extra_fields.get("is_staf") is not True:
            raise ValueError("A superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("A superuser must have is_superuser=True")

    

        