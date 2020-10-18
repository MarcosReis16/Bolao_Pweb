from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, nome_player, login_player, password, **extra_fields):
        
        usuario = self.model(nome_player=nome_player, login_player=login_player, **extra_fields)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        usuario.set_password(password)
        usuario.cadastrar(using=self._db)

        return usuario

    def create_user(self, nome_player, login_player, password = None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(nome_player, login_player, password, **extra_fields)

    def create_superuser(self, nome_player, login_player, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True or extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(nome_player, login_player, password, **extra_fields)