# Generated by Django 2.2.2 on 2019-07-14 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("presentation_manager", "0005_auto_20190714_1629")]

    operations = [
        migrations.AddField(
            model_name="presentation",
            name="format",
            field=models.CharField(
                choices=[("49235f37aa173b3d48eb6d856229e4c4", "PDF")],
                max_length=32,
                null=True,
            ),
        )
    ]
