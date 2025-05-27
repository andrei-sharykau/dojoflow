from django.core.management.base import BaseCommand
from dojoflow.models import AttestationLevel


class Command(BaseCommand):
    help = 'Инициализация уровней аттестации'

    def handle(self, *args, **options):
        levels_data = [
            ('10ky', 1),
            ('9ky', 2),
            ('8ky', 3),
            ('7ky', 4),
            ('6ky', 5),
            ('5ky', 6),
            ('4ky', 7),
            ('3ky', 8),
            ('2ky', 9),
            ('1ky', 10),
            ('1dan', 11),
            ('2dan', 12),
            ('3dan', 13),
            ('4dan', 14),
            ('5dan', 15),
            ('6dan', 16),
            ('7dan', 17),
        ]

        created_count = 0
        for level, order in levels_data:
            level_obj, created = AttestationLevel.objects.get_or_create(
                level=level,
                defaults={'order': order}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Создан уровень: {level_obj}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Уровень уже существует: {level_obj}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Инициализация завершена. Создано новых уровней: {created_count}'
            )
        ) 