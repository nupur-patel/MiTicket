# Generated by Django 4.0 on 2021-12-27 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_ticketcomment_commented_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='current_status',
            field=models.CharField(choices=[('NOT ACKNOLEDGE', 'Not Acknoledge'), ('ACKNOLEDGE', 'Acknoledge'), ('IN DEVELOPMENT', 'In Development'), ('TESTING', 'Testing'), ('DEPLOYED', 'Deployed'), ('CLOSED', 'Closed')], default='NOT ACKNOLEDGE', max_length=100),
        ),
    ]
