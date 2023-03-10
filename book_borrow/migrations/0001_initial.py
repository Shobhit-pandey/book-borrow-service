# Generated by Django 4.1.5 on 2023-01-12 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('available', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('Paperbacks', 'Paperbacks'), ('Hardcover', 'Hardcover'), ('Handmade', 'Handmade')], max_length=50)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_borrow.author')),
            ],
        ),
        migrations.CreateModel(
            name='BookingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_time', models.DateTimeField(auto_now_add=True)),
                ('return_time', models.DateTimeField(null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_borrow.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]