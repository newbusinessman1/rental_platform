from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    for name in ['Host', 'Guest']:
        Group.objects.get_or_create(name=name)

def delete_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Host', 'Guest']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),  # у тебя уже есть auth
    ]

    operations = [
        migrations.RunPython(create_groups, delete_groups),
    ]