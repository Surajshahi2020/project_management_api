# Generated by Django 4.2.3 on 2023-08-01 10:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("assigner", "0006_submittedtask"),
    ]

    operations = [
        migrations.AddField(
            model_name="submittedtask",
            name="remarks",
            field=models.TextField(blank=True, null=True),
        ),
    ]