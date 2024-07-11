# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Organisation

@receiver(post_save, sender=User)
def create_user_organization(sender, instance, created, **kwargs):

    if created:
        org_name = f"{instance.first_name}'s Organisation"
        organisation = Organisation.objects.create(name=org_name)
        organisation.users.add(instance)
        instance.default_organisation = organisation
        instance.save()
      