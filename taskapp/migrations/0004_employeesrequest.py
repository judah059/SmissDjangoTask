# Generated by Django 4.0.2 on 2022-02-21 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0003_alter_departments_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeesRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('average_time', models.CharField(default=0, max_length=120)),
                ('name', models.CharField(max_length=100)),
                ('sum_time', models.DecimalField(decimal_places=3, max_digits=12)),
            ],
        ),
    ]
