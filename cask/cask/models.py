from django.db import models


class CheckIn(models.Model):
    bottle = models.ForeignKey("spirits.Bottle", on_delete=models.CASCADE)
    location = models.ForeignKey("world.Location", null=True, on_delete=models.CASCADE)
    notes = models.TextField(null=True)
    flavor_profiles = models.ManyToManyField("spirits.FlavorProfile")
    friends = models.ManyToManyField("auth.User")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bottle.name


class Follower(models.Model):
    from_user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="following"
    )
    to_user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("from_user", "to_user"),)
