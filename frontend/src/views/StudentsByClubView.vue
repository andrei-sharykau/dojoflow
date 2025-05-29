<template>
  <div class="container-fluid py-4">
    <!-- Заголовок -->
    <div class="mb-4">
      <h1 class="h3 fw-bold text-gray-900 mb-1">Студенты по клубам</h1>
      <p class="text-gray-600 mb-0">Список занимающихся в разрезе клуба</p>
    </div>

    <!-- Поиск -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="input-group">
          <span class="input-group-text">
            <i class="bi bi-search"></i>
          </span>
          <input
            v-model="searchQuery"
            type="text"
            class="form-control"
            placeholder="Поиск по имени, фамилии или телефону..."
            @input="debouncedSearch"
          />
          <button 
            v-if="searchQuery" 
            class="btn btn-outline-secondary" 
            type="button"
            @click="clearSearch"
          >
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
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
    </div>

    <!-- Список клубов со студентами -->
    <div v-else>
      <!-- Пустое состояние -->
      <div v-if="clubsWithStudents.length === 0" class="text-center py-5">
        <div class="mb-4">
          <i class="bi bi-people text-gray-400" style="font-size: 4rem;"></i>
        </div>
        <h5 class="text-gray-900 mb-2">Студенты не найдены</h5>
        <p class="text-gray-600 mb-0">
          {{ searchQuery ? 'Попробуйте изменить критерии поиска' : 'В ваших клубах пока нет студентов' }}
        </p>
      </div>

      <!-- Клубы со студентами -->
      <div v-else class="row g-4">
        <div v-for="club in clubsWithStudents" :key="club.id" class="col-12">
          <div class="card border-0 shadow-sm">
            <!-- Заголовок клуба -->
            <div class="card-header bg-white border-bottom">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h5 class="card-title mb-1 d-flex align-items-center">
                    <i class="bi bi-building me-2 text-primary"></i>
                    {{ club.name }}
                  </h5>
                  <p class="text-gray-600 mb-0 small">
                    {{ club.city }} • {{ club.students_count }} студентов
                  </p>
                </div>
                <span class="badge bg-primary">{{ club.students_count }}</span>
              </div>
            </div>

            <!-- Список студентов -->
            <div class="card-body">
              <div v-if="club.students.length === 0" class="text-center py-3">
                <i class="bi bi-people text-gray-400 fs-2"></i>
                <p class="text-gray-500 mb-0 mt-2">
                  {{ searchQuery ? 'Студенты не найдены по запросу' : 'В клубе пока нет студентов' }}
                </p>
              </div>

              <div v-else class="table-responsive">
                <table class="table table-hover mb-0">
                  <thead class="table-light">
                    <tr>
                      <th class="border-0">Студент</th>
                      <th class="border-0">Возраст</th>
                      <th class="border-0">Телефон</th>
                      <th class="border-0">Уровень</th>
                      <th class="border-0">Начало занятий</th>
                      <th class="border-0">Последняя аттестация</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="student in club.students" :key="student.id" class="cursor-pointer" @click="$router.push(`/students/${student.id}`)">
                      <td class="border-0">
                        <div class="d-flex align-items-center">
                          <div class="bg-primary rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px;">
                            <i class="bi bi-person-fill text-white"></i>
                          </div>
                          <div>
                            <div class="fw-medium text-gray-900">{{ student.full_name }}</div>
                            <small class="text-gray-600">{{ student.city }}</small>
                          </div>
                        </div>
                      </td>
                      <td class="border-0">
                        <span class="badge bg-light text-gray-700">{{ student.age }} лет</span>
                      </td>
                      <td class="border-0">
                        <a :href="`tel:${student.phone}`" class="text-decoration-none">
                          {{ student.phone }}
                        </a>
                      </td>
                      <td class="border-0">
                        <span class="badge bg-success">{{ student.current_level_display }}</span>
                      </td>
                      <td class="border-0">
                        <small class="text-gray-600">{{ formatDate(student.start_date) }}</small>
                      </td>
                      <td class="border-0">
                        <small class="text-gray-600">
                          {{ student.last_attestation_date ? formatDate(student.last_attestation_date) : 'Нет данных' }}
                        </small>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Итоговая статистика -->
      <div v-if="clubsWithStudents.length > 0" class="row mt-4">
        <div class="col-12">
          <div class="card border-0 bg-light">
            <div class="card-body">
              <div class="row text-center">
                <div class="col-md-4">
                  <h4 class="fw-bold text-primary mb-1">{{ totalClubs }}</h4>
                  <small class="text-gray-600">Клубов</small>
                </div>
                <div class="col-md-4">
                  <h4 class="fw-bold text-success mb-1">{{ totalStudents }}</h4>
                  <small class="text-gray-600">Студентов</small>
                </div>
                <div class="col-md-4">
                  <h4 class="fw-bold text-warning mb-1">{{ averageStudentsPerClub }}</h4>
                  <small class="text-gray-600">Студентов на клуб</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { clubsAPI } from '../services/api'
import type { ClubWithStudents } from '../types'

// Состояние
const clubsWithStudents = ref<ClubWithStudents[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const searchQuery = ref('')

// Вычисляемые свойства
const totalClubs = computed(() => clubsWithStudents.value.length)
const totalStudents = computed(() => 
  clubsWithStudents.value.reduce((sum, club) => sum + club.students_count, 0)
)
const averageStudentsPerClub = computed(() => 
  totalClubs.value > 0 ? Math.round(totalStudents.value / totalClubs.value) : 0
)

// Функции
const loadStudentsByClub = async (search?: string) => {
  loading.value = true
  error.value = null
  
  try {
    clubsWithStudents.value = await clubsAPI.getStudentsByClub(search)
  } catch (err) {
    error.value = 'Ошибка при загрузке данных'
    console.error('Error loading students by club:', err)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ru-RU')
}

const clearSearch = () => {
  searchQuery.value = ''
  loadStudentsByClub()
}

// Debounced поиск
let searchTimeout: NodeJS.Timeout
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadStudentsByClub(searchQuery.value || undefined)
  }, 300)
}

// Инициализация
onMounted(() => {
  loadStudentsByClub()
})
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}

.cursor-pointer:hover {
  background-color: var(--bs-gray-50) !important;
}
</style> 