# Generated by Django 2.2.4 on 2021-03-16 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactApp', '0002_resume'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resume',
            options={'ordering': ('status', '-publish_date'), 'verbose_name': '简历', 'verbose_name_plural': '简历'},
        ),
        migrations.AlterField(
            model_name='resume',
            name='birth',
            field=models.DateField(default='2021-03-16', max_length=20, verbose_name='出生日期'),
        ),
    ]