# Generated by Django 4.1.7 on 2023-04-20 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enotes', '0008_remove_notes_notetitle_notes_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='notes',
            name='tags',
        ),
        migrations.AddField(
            model_name='notes',
            name='tags',
            field=models.ManyToManyField(to='enotes.tag'),
        ),
    ]
