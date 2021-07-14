# Generated by Django 2.2.4 on 2021-07-14 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_auto_20210714_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='snippets', to='snippets.Language'),
        ),
    ]
