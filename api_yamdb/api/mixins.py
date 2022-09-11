from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from users.permissions import IsAdminOrReadOnly


class CategoryAndGenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
