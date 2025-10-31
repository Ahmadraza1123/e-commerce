from django.db.models.signals import post_migrate, post_save
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

# 1️⃣ Create groups + permissions after migrations
@receiver(post_migrate)
def create_default_groups_with_permissions(sender, **kwargs):
    if sender.name == 'Account':  # <-- your app name
        groups_permissions = {
            'admin': [
                'add_user', 'change_user', 'delete_user', 'view_user',
                'add_product', 'change_product', 'delete_product', 'view_product',
                'add_order', 'change_order', 'delete_order', 'view_order',
            ],
            'vendor': [
                'add_category', 'change_category', 'view_category',
                'add_product', 'change_product', 'view_product'
            ],
            'customer': [
                'view_product', 'add_order', 'view_order'
            ],
            'delivery_boy': [
                'view_order', 'change_order'
            ],
        }

        for group_name, perms in groups_permissions.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            for perm_code in perms:
                permission = Permission.objects.filter(codename=perm_code).first()
                if permission:
                    group.permissions.add(permission)
                else:
                    print(f"⚠ Permission '{perm_code}' not found, skipping...")
            print(f"✅ Group '{group_name}' updated with permissions.")


# 2️⃣ Automatically assign default group to new users
@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    if created and not instance.groups.exists():
        default_group = Group.objects.get(name='customer')  # default group
        instance.groups.add(default_group)
        print(f"👤 User '{instance.username}' added to default group 'customer'")
