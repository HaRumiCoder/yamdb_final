from rest_framework import mixins, viewsets


class ListOrCreateOrDeleteViewsSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass
