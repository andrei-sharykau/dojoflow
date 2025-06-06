<template>
  <div class="container-fluid py-4">
    <!-- Навигация -->
    <div class="mb-4">
      <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <router-link to="/dashboard" class="text-decoration-none">Главная</router-link>
          </li>
          <li class="breadcrumb-item active" aria-current="page">
            {{ isEditing ? 'Редактирование студента' : 'Добавить студента' }}
          </li>
        </ol>
      </nav>
    </div>

    <!-- Заголовок -->
    <div class="mb-4">
      <h1 class="h3 fw-bold text-gray-900">
        {{ isEditing ? 'Редактировать студента' : 'Добавить студента' }}
      </h1>
      <p class="text-gray-600">
        {{ isEditing ? 'Изменение данных занимающегося' : 'Создание нового занимающегося' }}
      </p>
    </div>

    <!-- Загрузка -->
    <div v-if="initialLoading" class="d-flex justify-content-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>

    <!-- Ошибка загрузки -->
    <div v-else-if="loadError" class="alert alert-danger" role="alert">
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ loadError }}
    </div>

    <!-- Форма -->
    <div v-else class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <form @submit.prevent="handleSubmit">
              <!-- Клуб -->
              <div class="mb-4">
                <label for="club" class="form-label fw-medium">
                  Клуб <span class="text-danger">*</span>
                </label>
                <select 
                  id="club"
                  v-model="form.club" 
                  class="form-select"
                  :class="{ 'is-invalid': errors.club }"
                  required
                >
                  <option value="">Выберите клуб</option>
                  <option 
                    v-for="club in clubs" 
                    :key="club.id" 
                    :value="club.id"
                  >
                    {{ club.name }} ({{ club.city }})
                  </option>
                </select>
                <div v-if="errors.club" class="invalid-feedback">
                  {{ errors.club }}
                </div>
              </div>

              <!-- Персональная информация -->
              <h5 class="mb-3 text-primary">
                <i class="bi bi-person me-2"></i>
                Персональная информация
              </h5>
              
              <div class="row">
                <div class="col-md-4 mb-3">
                  <label for="lastName" class="form-label fw-medium">
                    Фамилия <span class="text-danger">*</span>
                  </label>
                  <input 
                    id="lastName"
                    v-model="form.last_name" 
                    type="text" 
                    class="form-control"
                    :class="{ 'is-invalid': errors.last_name }"
                    required
                  >
                  <div v-if="errors.last_name" class="invalid-feedback">
                    {{ errors.last_name }}
                  </div>
                </div>
                
                <div class="col-md-4 mb-3">
                  <label for="firstName" class="form-label fw-medium">
                    Имя <span class="text-danger">*</span>
                  </label>
                  <input 
                    id="firstName"
                    v-model="form.first_name" 
                    type="text" 
                    class="form-control"
                    :class="{ 'is-invalid': errors.first_name }"
                    required
                  >
                  <div v-if="errors.first_name" class="invalid-feedback">
                    {{ errors.first_name }}
                  </div>
                </div>
                
                <div class="col-md-4 mb-3">
                  <label for="middleName" class="form-label fw-medium">Отчество</label>
                  <input 
                    id="middleName"
                    v-model="form.middle_name" 
                    type="text" 
                    class="form-control"
                  >
                </div>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="birthDate" class="form-label fw-medium">
                    Дата рождения <span class="text-danger">*</span>
                  </label>
                  <input 
                    id="birthDate"
                    v-model="form.birth_date" 
                    type="date" 
                    class="form-control"
                    :class="{ 'is-invalid': errors.birth_date }"
                    required
                  >
                  <div v-if="errors.birth_date" class="invalid-feedback">
                    {{ errors.birth_date }}
                  </div>
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="phone" class="form-label fw-medium">
                    Телефон <span class="text-danger">*</span>
                  </label>
                  <input 
                    id="phone"
                    v-model="form.phone" 
                    type="tel" 
                    class="form-control"
                    :class="{ 'is-invalid': errors.phone }"
                    placeholder="+375 хх ххххххх"
                    required
                  >
                  <div v-if="errors.phone" class="invalid-feedback">
                    {{ errors.phone }}
                  </div>
                </div>
              </div>

              <!-- Контактная информация -->
              <h5 class="mb-3 mt-4 text-primary">
                <i class="bi bi-geo-alt me-2"></i>
                Контактная информация
              </h5>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="city" class="form-label fw-medium">
                    Город <span class="text-danger">*</span>
                  </label>
                  <input 
                    id="city"
                    v-model="form.city" 
                    type="text" 
                    class="form-control"
                    :class="{ 'is-invalid': errors.city }"
                    required
                  >
                  <div v-if="errors.city" class="invalid-feedback">
                    {{ errors.city }}
                  </div>
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="workplace" class="form-label fw-medium">Место работы</label>
                  <input 
                    id="workplace"
                    v-model="form.workplace" 
                    type="text" 
                    class="form-control"
                  >
                </div>
              </div>

              <div class="mb-3">
                <label for="address" class="form-label fw-medium">
                  Адрес <span class="text-danger">*</span>
                </label>
                <textarea 
                  id="address"
                  v-model="form.address" 
                  class="form-control"
                  :class="{ 'is-invalid': errors.address }"
                  rows="2"
                  placeholder="Укажите адрес проживания"
                ></textarea>
                <div v-if="errors.address" class="invalid-feedback">
                  {{ errors.address }}
                </div>
              </div>

              <!-- Информация о занятиях -->
              <h5 class="mb-3 mt-4 text-primary">
                <i class="bi bi-calendar-check me-2"></i>
                Информация о занятиях
              </h5>
              
              <div class="row">
                <div class="col-md-12 mb-3">
                  <label for="startDate" class="form-label fw-medium">
                    Дата начала занятий <span class="text-danger">*</span>
                  </label>
                  <input 
                    id="startDate"
                    v-model="form.start_date" 
                    type="date" 
                    class="form-control"
                    :class="{ 'is-invalid': errors.start_date }"
                    required
                  >
                  <div v-if="errors.start_date" class="invalid-feedback">
                    {{ errors.start_date }}
                  </div>
                </div>
              </div>

              <!-- Кнопки -->
              <div class="d-flex justify-content-end gap-2 mt-4 pt-3 border-top">
                <button 
                  type="button" 
                  class="btn btn-outline-secondary"
                  @click="handleCancel"
                  :disabled="loading"
                >
                  Отмена
                </button>
                <button 
                  type="submit" 
                  class="btn btn-primary"
                  :disabled="loading"
                >
                  <span 
                    v-if="loading" 
                    class="spinner-border spinner-border-sm me-2"
                    role="status"
                    aria-hidden="true"
                  ></span>
                  {{ loading ? (isEditing ? 'Сохранение...' : 'Создание...') : (isEditing ? 'Сохранить изменения' : 'Создать студента') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Уведомления -->
    <div v-if="successMessage" class="position-fixed top-0 end-0 p-3" style="z-index: 1100;">
      <div class="alert alert-success alert-dismissible" role="alert">
        <i class="bi bi-check-circle me-2"></i>
        {{ successMessage }}
        <button type="button" class="btn-close" @click="successMessage = ''"></button>
      </div>
    </div>

    <div v-if="errorMessage" class="position-fixed top-0 end-0 p-3" style="z-index: 1100;">
      <div class="alert alert-danger alert-dismissible" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ errorMessage }}
        <button type="button" class="btn-close" @click="errorMessage = ''"></button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { studentsService, clubsAPI } from '@/services/api'
import type { StudentCreateUpdate, StudentDetail, Club } from '@/types'

const route = useRoute()
const router = useRouter()

// Определяем режим: создание или редактирование
const isEditing = computed(() => !!route.params.id)
const studentId = computed(() => isEditing.value ? Number(route.params.id) : null)

// Состояние
const loading = ref(false)
const initialLoading = ref(false)
const loadError = ref<string | null>(null)
const successMessage = ref('')
const errorMessage = ref('')

// Данные
const clubs = ref<Club[]>([])
const student = ref<StudentDetail | null>(null)

// Форма
const form = reactive<StudentCreateUpdate>({
  club: 0,
  last_name: '',
  first_name: '',
  middle_name: '',
  birth_date: '',
  city: '',
  address: '',
  phone: '',
  workplace: '',
  start_date: ''
})

// Ошибки валидации
const errors = ref<Record<string, string>>({})

// Валидация
const validateForm = (): boolean => {
  const newErrors: Record<string, string> = {}

  if (!form.club) newErrors.club = 'Выберите клуб'
  if (!form.last_name.trim()) newErrors.last_name = 'Фамилия обязательна'
  if (!form.first_name.trim()) newErrors.first_name = 'Имя обязательно'
  if (!form.birth_date) newErrors.birth_date = 'Дата рождения обязательна'
  if (!form.phone.trim()) newErrors.phone = 'Телефон обязателен'
  if (!form.city.trim()) newErrors.city = 'Город обязателен'
  if (!form.start_date) newErrors.start_date = 'Дата начала занятий обязательна'

  // Валидация дат
  if (form.birth_date) {
    const birthDate = new Date(form.birth_date)
    const today = new Date()
    if (birthDate > today) {
      newErrors.birth_date = 'Дата рождения не может быть в будущем'
    }
  }

  if (form.start_date) {
    const startDate = new Date(form.start_date)
    const today = new Date()
    if (startDate > today) {
      newErrors.start_date = 'Дата начала занятий не может быть в будущем'
    }
  }

  errors.value = newErrors
  return Object.keys(newErrors).length === 0
}

// Загрузка данных
const loadData = async () => {
  try {
    initialLoading.value = true
    loadError.value = null

    // Загружаем клубы
    const clubsResponse = await clubsAPI.getAllClubs()
    clubs.value = clubsResponse

    // Если редактирование, загружаем данные студента
    if (isEditing.value && studentId.value) {
      student.value = await studentsService.getDetail(studentId.value)
      
      // Заполняем форму данными студента
      Object.assign(form, {
        club: student.value.club,
        last_name: student.value.last_name,
        first_name: student.value.first_name,
        middle_name: student.value.middle_name || '',
        birth_date: student.value.birth_date,
        city: student.value.city,
        address: student.value.address || '',
        phone: student.value.phone || '',
        workplace: student.value.workplace || '',
        start_date: student.value.start_date
      })
    } else {
      // Режим создания: устанавливаем значения по умолчанию
      const clubId = route.query.club
      if (clubId) {
        form.club = Number(clubId)
      }
      
      // Устанавливаем сегодняшнюю дату как дату начала занятий
      const today = new Date().toISOString().split('T')[0]
      form.start_date = today
    }

  } catch (err: any) {
    loadError.value = err.response?.data?.message || err.message || 'Ошибка загрузки данных'
    console.error('Load error:', err)
  } finally {
    initialLoading.value = false
  }
}

// Обработка отправки формы
const handleSubmit = async () => {
  console.log('StudentCreateView: начинаем обработку формы...')
  
  if (!validateForm()) {
    console.log('StudentCreateView: валидация не прошла')
    return
  }

  try {
    loading.value = true
    errors.value = {}

    const formData = {
      ...form,
      middle_name: form.middle_name || undefined,
      address: form.address || undefined,
      phone: form.phone || undefined,
      workplace: form.workplace || undefined
    }

    console.log('StudentCreateView: отправляем данные:', formData)
    console.log('StudentCreateView: режим редактирования:', isEditing.value)

    let result
    if (isEditing.value && studentId.value) {
      result = await studentsService.updateStudent(studentId.value, formData)
      const studentName = result.full_name || `${result.first_name} ${result.last_name}`.trim()
      successMessage.value = `Данные студента ${studentName} успешно обновлены`
    } else {
      console.log('StudentCreateView: создаем нового студента...')
      result = await studentsService.createStudent(formData)
      console.log('StudentCreateView: студент создан:', result)
      const studentName = result.full_name || `${result.first_name} ${result.last_name}`.trim()
      successMessage.value = `Студент ${studentName} успешно создан`
    }

    // Перенаправляем на страницу студента
    setTimeout(() => {
      router.push({ name: 'student-detail', params: { id: result.id } })
    }, 1500)

  } catch (err: any) {
    console.error('Submit error:', err)
    
    if (err.response?.data) {
      const apiErrors = err.response.data
      if (typeof apiErrors === 'object') {
        // Обработка ошибок валидации с бэкенда
        const newErrors: Record<string, string> = {}
        for (const [field, messages] of Object.entries(apiErrors)) {
          if (Array.isArray(messages)) {
            newErrors[field] = messages[0]
          } else if (typeof messages === 'string') {
            newErrors[field] = messages
          }
        }
        errors.value = newErrors
      } else {
        errorMessage.value = typeof apiErrors === 'string' ? apiErrors : 'Ошибка при сохранении данных'
      }
    } else {
      errorMessage.value = err.message || 'Произошла неизвестная ошибка'
    }
  } finally {
    loading.value = false
  }
}

// Отмена
const handleCancel = () => {
  if (isEditing.value && studentId.value) {
    router.push({ name: 'student-detail', params: { id: studentId.value } })
  } else {
    router.push('/dashboard')
  }
}

// Инициализация
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.form-label {
  color: #374151;
  margin-bottom: 0.5rem;
}

.card {
  border-radius: 0.75rem;
}

.alert {
  border-radius: 0.5rem;
}
</style> 