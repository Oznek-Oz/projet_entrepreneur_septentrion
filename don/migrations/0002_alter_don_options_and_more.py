# Generated by Django 5.2.4 on 2025-07-20 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("don", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="don",
            options={"verbose_name": "Don", "verbose_name_plural": "Dons"},
        ),
        migrations.RenameField(
            model_name="don",
            old_name="nom_carte",
            new_name="transaction_id",
        ),
        migrations.RemoveField(
            model_name="don",
            name="cvv",
        ),
        migrations.RemoveField(
            model_name="don",
            name="expiration",
        ),
        migrations.RemoveField(
            model_name="don",
            name="numero_carte",
        ),
        migrations.AddField(
            model_name="don",
            name="message",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="don",
            name="methode",
            field=models.CharField(
                choices=[
                    ("orange_money", "Orange Money"),
                    ("mtn_money", "MTN Mobile Money"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="don",
            name="telephone",
            field=models.CharField(default="", max_length=20),
            preserve_default=False,
        ),
    ]
