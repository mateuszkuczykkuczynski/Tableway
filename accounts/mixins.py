from rest_framework.mixins import UpdateModelMixin


class PutOnlyMixin(object):
    """
    A mixin that provides functionality for handling PUT requests only.

    Overrides the `update` method to ensure that the update flag is set to True.
    The `perform_update` method is responsible for saving the serialized data.
    """
    def update(self, request, *args, **kwargs):
        """
        Overrides the update method to set the 'update' flag to True.
        Calls the `update` method from the UpdateModelMixin.
        """
        kwargs['update'] = True
        return UpdateModelMixin.update(self, request, *args, **kwargs)

    def perform_update(self, serializer):
        """
        Saves the serialized data.
        """
        serializer.save()
