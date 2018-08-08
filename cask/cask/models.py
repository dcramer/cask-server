from django.conf import settings
from django.db import models
from uuid import uuid4


class CheckIn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    bottle = models.ForeignKey("spirits.Bottle", on_delete=models.CASCADE)
    location = models.ForeignKey("world.Location", null=True, on_delete=models.CASCADE)
    notes = models.TextField(null=True)
    flavor_profiles = models.ManyToManyField("spirits.FlavorProfile")
    friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="friend_checkins"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.bottle.name
