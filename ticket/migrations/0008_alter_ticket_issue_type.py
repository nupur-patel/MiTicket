# Generated by Django 4.0 on 2021-12-27 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0007_ticket_issue_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='issue_type',
            field=models.TextField(default=''),
        ),
    ]
