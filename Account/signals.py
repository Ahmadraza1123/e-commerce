from django.db.models.signals import post_migrate, post_save
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from .models import User

# 1️⃣ Groups aur permissions create karna
@receiver(post_migrate)
def create_default_groups_with_permissions(sender, **kwargs):
    if sender.name == 'Account':  # Replace with your app name
        groups_permissions = {
            'vendor': [
                'add_category', 'change_category', 'view_category',
                'add_product', 'change_product', 'view_product'
            ],
            'customer': [
                'view_product', 'view_order', 'add_order'
            ],
            'delivery_boy': [
                'view_order', 'change_order'
            ],
        }

        for group_name, perms in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_code in perms:
                try:
                    permission = Permission.objects.get(codename=perm_code)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    print(f"⚠ Permission '{perm_code}' not found, skipping...")
            print(f" Group '{group_name}' updated with permissions.")

# 2️⃣ User create hone par group me add karna
@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created and instance.role:
        group, _ = Group.objects.get_or_create(name=instance.role)
        instance.groups.add(group)
        print(f" User '{instance.username}' added to group '{instance.role}'")
