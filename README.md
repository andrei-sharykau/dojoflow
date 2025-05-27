# DojoFlow - Система учета занимающихся Айкидо

Система для управления учениками в клубах Айкидо с поддержкой множественных клубов и ролевой модели доступа.

## Структура базы данных

### Модели

#### 1. Club (Клуб)
Представляет клуб Айкидо.

**Поля:**
- `name` - Название клуба (CharField, max_length=200)
- `city` - Город (CharField, max_length=100)
- `created_at` - Дата создания записи (DateTimeField, auto_now_add=True)

**Связи:**
- `students` - Обратная связь к модели Student (ForeignKey)
- `admins` - Обратная связь к модели ClubAdmin (ForeignKey)

#### 2. AttestationLevel (Уровень аттестации)
Фиксированные уровни аттестации в Айкидо.

**Поля:**
- `level` - Код уровня (CharField, max_length=5, choices)
- `order` - Порядковый номер для сортировки (PositiveIntegerField, unique=True)

**Доступные уровни:**
- 10ky, 9ky, 8ky, 7ky, 6ky, 5ky, 4ky, 3ky, 2ky, 1ky (кю)
- 1dan, 2dan, 3dan, 4dan, 5dan, 6dan, 7dan (дан)

**Связи:**
- `students` - Обратная связь к модели Student (ForeignKey current_level)

#### 3. Student (Занимающийся)
Основная модель для хранения информации о занимающихся.

**Персональная информация:**
- `last_name` - Фамилия (CharField, max_length=100)
- `first_name` - Имя (CharField, max_length=100)
- `middle_name` - Отчество (CharField, max_length=100, blank=True)
- `birth_date` - Дата рождения (DateField)

**Контактная информация:**
- `city` - Город (CharField, max_length=100)
- `address` - Адрес (TextField)
- `phone` - Телефон (CharField, max_length=17, с валидацией)
- `workplace` - Место работы (CharField, max_length=200, blank=True)

**Информация о занятиях:**
- `club` - Клуб (ForeignKey to Club, on_delete=PROTECT)
- `start_date` - Дата начала занятий (DateField)
- `current_level` - Текущий уровень аттестации (ForeignKey to AttestationLevel, on_delete=PROTECT)
- `last_attestation_date` - Дата последней аттестации (DateField, null=True, blank=True)

**Системные поля:**
- `created_at` - Дата создания записи (DateTimeField, auto_now_add=True)
- `updated_at` - Дата обновления записи (DateTimeField, auto_now=True)

**Связи:**
- `attestations` - Обратная связь к модели Attestation (ForeignKey)

#### 4. Attestation (Аттестация)
Хранит информацию о проведенных аттестациях.

**Поля:**
- `student` - Занимающийся (ForeignKey to Student, on_delete=CASCADE)
- `level` - Уровень аттестации (ForeignKey to AttestationLevel, on_delete=PROTECT)
- `date` - Дата аттестации (DateField)
- `city` - Место проведения (CharField, max_length=100)
- `notes` - Примечания (TextField, blank=True)
- `created_at` - Дата создания записи (DateTimeField, auto_now_add=True)

**Ограничения:**
- `unique_together = ['student', 'level']` - Один студент не может иметь две аттестации одного уровня

#### 5. ClubAdmin (Администратор клуба)
Связывает пользователей Django с клубами для ролевого доступа.

**Поля:**
- `user` - Пользователь (OneToOneField to User, on_delete=CASCADE)
- `club` - Клуб (ForeignKey to Club, on_delete=CASCADE)

## Система прав доступа

### Суперпользователь (is_superuser=True)
- Полный доступ ко всем данным
- Может видеть и редактировать всех студентов из всех клубов
- Может изменять клуб у студента
- Может управлять администраторами клубов
- Может управлять уровнями аттестации

### Администратор клуба (ClubAdmin)
- Видит только студентов своего клуба
- Может добавлять, редактировать и удалять студентов только в своем клубе
- НЕ может изменить клуб у студента (поле заблокировано)
- Может добавлять и редактировать аттестации только для студентов своего клуба
- НЕ может управлять администраторами клубов
- НЕ может управлять уровнями аттестации

## Установка и настройка

### Требования
- Python 3.13+
- PostgreSQL
- Poetry для управления зависимостями

### Установка

1. **Клонирование репозитория:**
```bash
git clone <repository-url>
cd dojoflow
```

2. **Установка зависимостей:**
```bash
poetry install
```

3. **Настройка базы данных:**
Создайте базу данных PostgreSQL и пользователя:
```sql
CREATE DATABASE dojoflow;
CREATE USER dojoflow WITH PASSWORD 'dojoflowpassword';
GRANT ALL PRIVILEGES ON DATABASE dojoflow TO dojoflow;
```

4. **Применение миграций:**
```bash
poetry run python app/manage.py migrate
```

5. **Инициализация уровней аттестации:**
```bash
poetry run python app/manage.py init_levels
```

6. **Создание суперпользователя:**
```bash
poetry run python app/manage.py createsuperuser
```

7. **Загрузка тестовых данных (опционально):**
```bash
poetry run python app/manage.py load_sample_data
```

8. **Запуск сервера разработки:**
```bash
poetry run python app/manage.py runserver
```

## Использование

### Административный интерфейс
Доступен по адресу: `http://localhost:8000/admin/`

### Тестовые пользователи
После загрузки тестовых данных доступны следующие пользователи:

**Администраторы клубов:**
- `club_admin_moscow` / `admin123` - Администратор клуба "Айкидо Центр" (Москва)
- `club_admin_spb` / `admin123` - Администратор клуба "Додзё Гармония" (Санкт-Петербург)

### Тестовые данные
Система включает тестовые данные:
- 3 клуба в разных городах
- 4 студента с различными уровнями аттестации
- История аттестаций для некоторых студентов
- 2 администратора клубов

## Команды управления

### init_levels
Инициализирует все уровни аттестации в правильном порядке.
```bash
poetry run python app/manage.py init_levels
```

### load_sample_data
Загружает тестовые данные для демонстрации функциональности.
```bash
poetry run python app/manage.py load_sample_data
```

## Особенности реализации

### Валидация данных
- Телефонные номера валидируются регулярным выражением
- Уникальность аттестаций на уровне базы данных
- Защита от удаления связанных записей (PROTECT)

### Безопасность
- Администраторы клубов не могут видеть данные других клубов
- Поле "клуб" заблокировано для администраторов клубов
- Уровни аттестации защищены от изменения обычными пользователями

### Интернационализация
- Интерфейс на русском языке
- Временная зона: Europe/Moscow
- Локаль: ru-ru

## Структура файлов

```
dojoflow/
├── app/
│   ├── config/           # Настройки Django
│   │   ├── migrations/   # Миграции базы данных
│   │   ├── management/   # Команды управления
│   │   │   └── commands/
│   │   ├── models.py     # Модели данных
│   │   ├── admin.py      # Административный интерфейс
│   │   └── ...
│   └── manage.py
├── pyproject.toml        # Зависимости Poetry
└── README.md
```

## Дальнейшее развитие

Возможные направления для расширения функциональности:
- Web API (Django REST Framework)
- Фронтенд интерфейс
- Система уведомлений
- Отчеты и статистика
- Импорт/экспорт данных
- Система платежей
- Календарь занятий и аттестаций
