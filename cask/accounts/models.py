from django.db import models
from uuid import uuid4


class Follower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    from_user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="following"
    )
    to_user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("from_user", "to_user"),)
