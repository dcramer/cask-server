from django.db import models


class Location(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class Country(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Region(models.Model):
    name = models.CharField(max_length=128)
    country = models.ForeignKey("cask.Country")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("name", "country"),)


class Distillery(models.Model):
    name = models.CharField(max_length=128, unique=True)
    country = models.ForeignKey("cask.Country")
    region = models.ForeignKey("cask.Region")
    created_at = models.DateTimeField(auto_now_add=True)


class Brand(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CaskType(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SpiritType(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Bottle(models.Model):
    distillery = models.ForeignKey("cask.Distillery")
    brand = models.ForeignKey("cask.Brand")
    spirit_type = models.ForeignKey("cask.SpiritType")
    age = models.PositiveSmallIntegerField(null=True)
    distillation_date = models.DateTimeField(null=True)
    bottle_date = models.DateTimeField(null=True)
    abv = models.DecimalField(max_digits=2)
    created_at = models.DateTimeField(auto_now_add=True)


# class BottleCask(models.Model):
#     cask_type = models.ForeignKey("cask.CaskType")


class FlavorProfile(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CheckIn(models.Model):
    bottle = models.ForeignKey("cask.Bottle")
    location = models.ForeignKey("cask.Location", null=True)
    notes = models.TextField(null=True)
    flavor_profiles = models.ManyToManyField("cask.FlavorProfile")
    friends = models.ManyToManyField("auth.User")
    created_at = models.DateTimeField(auto_now_add=True)


class Follower(models.Model):
    from_user = models.ForeignKey("auth.User")
    to_user = models.ForeignKey("auth.User")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("from_user", "to_user"),)
