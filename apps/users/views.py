from rest_framework.viewsets import GenericViewSet
from apps.users.models import User
from apps.users.serializers import UserSerializer
from rest_framework import mixins
# Create your views here.
class UserReisterAPI(GenericViewSet,
              mixins.ListModelMixin,
              mixins.CreateModelMixin,
              mixins.RetrieveModelMixin,
              mixins.UpdateModelMixin,
              mixins.DestroyModelMixin,
              ):
    queryset = User.objects.all()
    serializer_class = UserSerializer