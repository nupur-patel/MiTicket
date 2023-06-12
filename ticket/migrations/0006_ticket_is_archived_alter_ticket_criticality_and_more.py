# Generated by Django 4.0 on 2021-12-27 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('ticket', '0005_ticket_current_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='criticality',
            field=models.CharField(choices=[('LIGHT', 'Light'), ('MODERATE', 'Moderate'), ('URGENT', 'Urgent'), ('CRITICAL', 'Critical')], max_length=100),
        ),
        migrations.CreateModel(
            name='TicketLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_msg', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('change_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.appuser')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticket.ticket')),
            ],
        ),
    ]
