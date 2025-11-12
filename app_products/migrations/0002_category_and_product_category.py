from django.db import migrations, models


def seed_categories(apps, schema_editor):
    Category = apps.get_model('app_products', 'Category')
    defaults = [
        'Fruits',
        'Légumes',
        'Produits laitiers',
        'Viandes',
        'Céréales',
        'Boissons locales',
    ]
    for name in defaults:
        Category.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Catégorie',
                'verbose_name_plural': 'Catégories',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='products', to='app_products.category'),
        ),
        migrations.RunPython(seed_categories, reverse_code=migrations.RunPython.noop),
    ]