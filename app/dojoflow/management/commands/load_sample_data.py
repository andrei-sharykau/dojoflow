from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date, datetime
from dojoflow.models import Club, AttestationLevel, Student, Attestation, ClubAdmin


class Command(BaseCommand):
    help = 'Загрузка тестовых данных'

    def handle(self, *args, **options):
        # Создаем клубы
        club1, created = Club.objects.get_or_create(
            name="Айкидо Центр",
            city="Москва"
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Создан клуб: {club1}'))

        club2, created = Club.objects.get_or_create(
            name="Додзё Гармония",
            city="Санкт-Петербург"
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Создан клуб: {club2}'))

        club3, created = Club.objects.get_or_create(
            name="Путь воина",
            city="Екатеринбург"
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Создан клуб: {club3}'))

        # Получаем уровни аттестации
        level_10ky = AttestationLevel.objects.get(level='10ky')
        level_5ky = AttestationLevel.objects.get(level='5ky')
        level_1ky = AttestationLevel.objects.get(level='1ky')
        level_1dan = AttestationLevel.objects.get(level='1dan')

        # Создаем студентов
        students_data = [
            {
                'club': club1,
                'last_name': 'Иванов',
                'first_name': 'Алексей',
                'middle_name': 'Петрович',
                'birth_date': date(1990, 5, 15),
                'city': 'Москва',
                'address': 'ул. Ленина, д. 10, кв. 5',
                'phone': '+79161234567',
                'workplace': 'ООО "Технологии"',
                'start_date': date(2020, 9, 1),
                'current_level': level_1ky,
                'last_attestation_date': date(2023, 6, 15),
            },
            {
                'club': club1,
                'last_name': 'Петрова',
                'first_name': 'Мария',
                'middle_name': 'Сергеевна',
                'birth_date': date(1985, 8, 22),
                'city': 'Москва',
                'address': 'пр. Мира, д. 25, кв. 12',
                'phone': '+79167654321',
                'workplace': 'Банк "Развитие"',
                'start_date': date(2019, 3, 15),
                'current_level': level_1dan,
                'last_attestation_date': date(2023, 12, 10),
            },
            {
                'club': club2,
                'last_name': 'Сидоров',
                'first_name': 'Дмитрий',
                'middle_name': 'Александрович',
                'birth_date': date(1992, 12, 3),
                'city': 'Санкт-Петербург',
                'address': 'Невский пр., д. 50, кв. 8',
                'phone': '+78121234567',
                'workplace': 'IT-компания',
                'start_date': date(2021, 1, 10),
                'current_level': level_5ky,
                'last_attestation_date': date(2023, 9, 20),
            },
            {
                'club': club3,
                'last_name': 'Козлова',
                'first_name': 'Анна',
                'middle_name': 'Викторовна',
                'birth_date': date(1988, 4, 18),
                'city': 'Екатеринбург',
                'address': 'ул. Малышева, д. 15, кв. 3',
                'phone': '+73431234567',
                'workplace': 'Медицинский центр',
                'start_date': date(2022, 6, 1),
                'current_level': level_10ky,
                'last_attestation_date': date(2023, 11, 5),
            },
        ]

        created_students = []
        for student_data in students_data:
            student, created = Student.objects.get_or_create(
                last_name=student_data['last_name'],
                first_name=student_data['first_name'],
                middle_name=student_data['middle_name'],
                defaults=student_data
            )
            if created:
                created_students.append(student)
                self.stdout.write(self.style.SUCCESS(f'Создан студент: {student}'))

        # Создаем администраторов клубов
        # Создаем пользователей для администраторов клубов
        admin1_user, created = User.objects.get_or_create(
            username='club_admin_moscow',
            defaults={
                'first_name': 'Сергей',
                'last_name': 'Администратов',
                'email': 'admin.moscow@example.com',
                'is_staff': True,
            }
        )
        if created:
            admin1_user.set_password('admin123')
            admin1_user.save()
            self.stdout.write(self.style.SUCCESS(f'Создан пользователь: {admin1_user}'))

        admin2_user, created = User.objects.get_or_create(
            username='club_admin_spb',
            defaults={
                'first_name': 'Елена',
                'last_name': 'Управляева',
                'email': 'admin.spb@example.com',
                'is_staff': True,
            }
        )
        if created:
            admin2_user.set_password('admin123')
            admin2_user.save()
            self.stdout.write(self.style.SUCCESS(f'Создан пользователь: {admin2_user}'))

        # Создаем записи администраторов клубов
        club_admin1, created = ClubAdmin.objects.get_or_create(
            user=admin1_user,
            club=club1
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Создан администратор клуба: {club_admin1}'))

        club_admin2, created = ClubAdmin.objects.get_or_create(
            user=admin2_user,
            club=club2
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Создан администратор клуба: {club_admin2}'))

        # Создаем несколько аттестаций для студентов
        if created_students:
            for student in created_students[:2]:  # Только для первых двух студентов
                # Создаем историю аттестаций
                if student.current_level.level == '1ky':
                    # Для студента с 1 кю создаем историю аттестаций
                    attestations_data = [
                        (level_10ky, date(2020, 12, 15)),
                        (AttestationLevel.objects.get(level='8ky'), date(2021, 6, 20)),
                        (AttestationLevel.objects.get(level='6ky'), date(2022, 3, 10)),
                        (AttestationLevel.objects.get(level='3ky'), date(2022, 12, 5)),
                        (level_1ky, date(2023, 6, 15)),
                    ]
                elif student.current_level.level == '1dan':
                    # Для студента с 1 дан создаем полную историю
                    attestations_data = [
                        (level_10ky, date(2019, 6, 15)),
                        (AttestationLevel.objects.get(level='7ky'), date(2020, 1, 20)),
                        (AttestationLevel.objects.get(level='4ky'), date(2020, 9, 10)),
                        (level_1ky, date(2021, 6, 5)),
                        (level_1dan, date(2023, 12, 10)),
                    ]
                else:
                    continue

                for level, att_date in attestations_data:
                    attestation, created = Attestation.objects.get_or_create(
                        student=student,
                        level=level,
                        defaults={
                            'date': att_date,
                            'city': student.city,
                            'notes': f'Аттестация на {level}'
                        }
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'Создана аттестация: {attestation}')
                        )

        self.stdout.write(
            self.style.SUCCESS('Загрузка тестовых данных завершена!')
        ) 