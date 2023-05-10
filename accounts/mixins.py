from rest_framework.mixins import UpdateModelMixin


class PutOnlyMixin(object):
    def update(self, request, *args, **kwargs):
        kwargs['update'] = True
        return UpdateModelMixin.update(self, request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()
