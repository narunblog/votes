from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreatePasswordRetypeSerializer

User = get_user_model()


class MyUserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        extra_kwargs = {
            'email': {
                'validators': [
                    UniqueValidator(queryset=User.objects.all(), message='このメールアドレスはすでに使用されています。')
                ]
            }
        }
