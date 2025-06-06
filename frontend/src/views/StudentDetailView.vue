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
            {{ student ? student.full_name : 'Студент' }}
          </li>
        </ol>
      </nav>
    </div>

    <!-- Загрузка -->
    <div v-if="loading" class="d-flex justify-content-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="alert alert-danger" role="alert">
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ error }}
      <div class="mt-2">
        <button class="btn btn-outline-danger btn-sm" @click="loadStudent">
          <i class="bi bi-arrow-clockwise me-1"></i>
          Попробовать снова
        </button>
      </div>
    </div>

    <!-- Детали студента -->
    <div v-else-if="student" class="row g-4">
      <!-- Основная информация -->
      <div class="col-lg-8">
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-header bg-white border-bottom">
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex align-items-center">
                <div class="bg-primary rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 50px; height: 50px;">
                  <i class="bi bi-person-fill text-white fs-4"></i>
                </div>
                <div>
                  <h4 class="mb-1 fw-bold text-gray-900">{{ student.full_name }}</h4>
                  <p class="text-gray-600 mb-0">
                    <i class="bi bi-building me-1"></i>
                    {{ student.club_name }} • {{ student.city }}
                  </p>
                </div>
              </div>
              <div class="text-end">
                <div class="d-flex gap-2">
                  <button class="btn btn-outline-primary btn-sm" @click="editStudent">
                    <i class="bi bi-pencil me-1"></i>
                    Редактировать
                  </button>
                  <button 
                    class="btn btn-outline-danger btn-sm" 
                    data-bs-toggle="modal" 
                    data-bs-target="#studentDeleteModal"
                  >
                    <i class="bi bi-trash me-1"></i>
                    Удалить
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-6">
                <div class="d-flex align-items-center mb-3">
                  <i class="bi bi-person text-primary me-2"></i>
                  <div>
                    <small class="text-gray-600">Полное имя</small>
                    <div class="fw-medium">{{ student.full_name }}</div>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="d-flex align-items-center mb-3">
                  <i class="bi bi-calendar text-primary me-2"></i>
                  <div>
                    <small class="text-gray-600">Возраст</small>
                    <div class="fw-medium">{{ student.age }} лет ({{ formatDate(student.birth_date) }})</div>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="d-flex align-items-center mb-3">
                  <i class="bi bi-telephone text-primary me-2"></i>
                  <div>
                    <small class="text-gray-600">Телефон</small>
                    <div class="fw-medium">
                      <a :href="`tel:${student.phone}`" class="text-decoration-none">
                        {{ student.phone }}
                      </a>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="d-flex align-items-center mb-3">
                  <i class="bi bi-geo-alt text-primary me-2"></i>
                  <div>
                    <small class="text-gray-600">Город</small>
                    <div class="fw-medium">{{ student.city }}</div>
                  </div>
                </div>
              </div>
              <div class="col-md-6" v-if="student.address">
                <div class="d-flex align-items-center mb-3">
                  <i class="bi bi-house text-primary me-2"></i>
                  <div>
                    <small class="text-gray-600">Адрес</small>
                    <div class="fw-medium">{{ student.address }}</div>
                  </div>
                </div>
              </div>
              <div class="col-md-6" v-if="student.workplace">
                <div class="d-flex align-items-center mb-3">
                  <i class="bi bi-briefcase text-primary me-2"></i>
                  <div>
                    <small class="text-gray-600">Место работы</small>
                    <div class="fw-medium">{{ student.workplace }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- История аттестаций -->
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-bottom">
            <h5 class="card-title mb-0">
              <i class="bi bi-award me-2 text-primary"></i>
              История аттестаций
            </h5>
          </div>
          <div class="card-body">
            <div v-if="student.attestations && student.attestations.length > 0">
              <div v-for="attestation in student.attestations" :key="attestation.id" class="d-flex align-items-center justify-content-between py-3 border-bottom">
                <div class="d-flex align-items-center">
                  <div class="bg-success rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px;">
                    <i class="bi bi-trophy-fill text-white"></i>
                  </div>
                  <div>
                    <div class="fw-medium">{{ attestation.level.display_name }}</div>
                    <small class="text-gray-600">{{ formatDate(attestation.date) }} • {{ attestation.city }}</small>
                  </div>
                </div>
                <span class="badge bg-success">Сдано</span>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <i class="bi bi-award text-gray-400 fs-1"></i>
              <p class="text-gray-500 mt-2 mb-0">Аттестации пока не проводились</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Боковая панель -->
      <div class="col-lg-4">
        <!-- Статистика -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-header bg-white border-bottom">
            <h6 class="card-title mb-0">Статистика</h6>
          </div>
          <div class="card-body">
            <div class="row g-3 text-center">
              <div class="col-6">
                <div class="bg-primary bg-opacity-10 rounded-3 p-3 mb-2">
                  <i class="bi bi-calendar-check text-primary fs-4"></i>
                </div>
                <div class="fw-bold text-gray-900">{{ student.years_of_practice }}</div>
                <small class="text-gray-600">{{ getYearsText(student.years_of_practice) }} занятий</small>
              </div>
              <div class="col-6">
                <div class="bg-success bg-opacity-10 rounded-3 p-3 mb-2">
                  <i class="bi bi-award text-success fs-4"></i>
                </div>
                <div class="fw-bold text-gray-900">{{ student.attestations?.length || 0 }}</div>
                <small class="text-gray-600">аттестаций</small>
              </div>
            </div>
          </div>
        </div>

        <!-- Текущий уровень -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-header bg-white border-bottom">
            <h6 class="card-title mb-0">Текущий уровень</h6>
          </div>
          <div class="card-body text-center">
            <div v-if="student.current_level_display">
              <div class="bg-warning bg-opacity-10 rounded-3 p-4 mb-3">
                <i class="bi bi-trophy text-warning" style="font-size: 2rem;"></i>
              </div>
              <h4 class="fw-bold text-gray-900 mb-1">{{ student.current_level_display }}</h4>
              <small class="text-gray-600">
                Последняя аттестация: 
                {{ student.last_attestation_date ? formatDate(student.last_attestation_date) : 'Нет данных' }}
              </small>
            </div>
            <div v-else class="py-3">
              <i class="bi bi-question-circle text-gray-400 fs-1"></i>
              <p class="text-gray-500 mt-2 mb-0">Уровень не определен</p>
            </div>
          </div>
        </div>

        <!-- Информация о следующей аттестации -->
        <div class="card border-0 shadow-sm" v-if="student.next_attestation_eligible">
          <div class="card-header bg-white border-bottom">
            <h6 class="card-title mb-0">Следующая аттестация</h6>
          </div>
          <div class="card-body">
            <div v-if="student.next_attestation_eligible.eligible" class="text-success">
              <i class="bi bi-check-circle me-2"></i>
              <strong>Может сдавать аттестацию</strong>
              <div class="mt-2">
                <small class="text-gray-600">
                  {{ student.next_attestation_eligible.next_level ? `Следующий уровень: ${student.next_attestation_eligible.next_level}` : student.next_attestation_eligible.reason }}
                </small>
              </div>
            </div>
            <div v-else class="text-warning">
              <i class="bi bi-clock me-2"></i>
              <strong>Пока не готов</strong>
              <div class="mt-2">
                <small class="text-gray-600">{{ student.next_attestation_eligible.reason }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно удаления -->
    <StudentDeleteModal
      :student="student"
      @delete="handleDelete"
      @success="handleSuccess"
      @error="handleError"
    />

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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { studentsAPI } from '@/services/api'
import type { StudentDetail } from '@/types'
import StudentDeleteModal from '@/components/StudentDeleteModal.vue'

const route = useRoute()
const router = useRouter()

const student = ref<StudentDetail | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const successMessage = ref('')
const errorMessage = ref('')

const loadStudent = async () => {
  try {
    loading.value = true
    error.value = null
    
    const studentId = Number(route.params.id)
    if (!studentId) {
      throw new Error('Некорректный ID студента')
    }
    
    student.value = await studentsAPI.getDetail(studentId)
  } catch (err: any) {
    error.value = err.response?.data?.message || err.message || 'Ошибка загрузки студента'
    console.error('Error loading student:', err)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ru-RU')
}

const getYearsText = (years: number) => {
  if (years === 1) return 'год'
  if (years >= 2 && years <= 4) return 'года'
  return 'лет'
}

const editStudent = () => {
  if (student.value) {
    router.push({ name: 'student-edit', params: { id: student.value.id } })
  }
}

// Обработчики для модального окна удаления
const handleDelete = async (studentId: number) => {
  try {
    loading.value = true
    await studentsAPI.deleteStudent(studentId)
    
    const studentName = student.value?.full_name || 'Студент'
    successMessage.value = `${studentName} успешно удален`
    
    // Закрываем модальное окно
    const modal = document.getElementById('studentDeleteModal')
    if (modal) {
      const bootstrapModal = (window as any).bootstrap.Modal.getInstance(modal)
      if (bootstrapModal) {
        bootstrapModal.hide()
      }
    }
    
    // Перенаправляем на главную страницу через некоторое время
    setTimeout(() => {
      router.push('/dashboard')
    }, 2000)
    
  } catch (err: any) {
    errorMessage.value = err.response?.data?.message || err.message || 'Ошибка удаления студента'
    console.error('Error deleting student:', err)
  } finally {
    loading.value = false
  }
}

const handleSuccess = (message: string) => {
  successMessage.value = message
}

const handleError = (message: string) => {
  errorMessage.value = message
}

onMounted(() => {
  loadStudent()
})
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style> 