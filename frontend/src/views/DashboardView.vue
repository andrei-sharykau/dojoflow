<template>
  <div class="container-fluid py-4">
    <!-- Заголовок -->
    <div class="mb-4">
      <h1 class="h3 fw-bold text-gray-900 mb-1">Студенты</h1>
      <p class="text-gray-600 mb-0">
        {{ currentClub ? `Клуб: ${currentClub.name}` : 'Управление студентами' }}
      </p>
    </div>

    <!-- Статистика -->
    <div class="row g-3 mb-4">
      <div class="col-md-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="bg-primary bg-opacity-10 rounded-3 p-3">
                  <i class="bi bi-people-fill text-primary fs-4"></i>
                </div>
              </div>
              <div class="ms-3">
                <h6 class="text-gray-600 mb-1">Всего студентов</h6>
                <h3 class="fw-bold text-gray-900 mb-0">{{ totalStudents }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="bg-success bg-opacity-10 rounded-3 p-3">
                  <i class="bi bi-building text-success fs-4"></i>
                </div>
              </div>
              <div class="ms-3">
                <h6 class="text-gray-600 mb-1">Клубы</h6>
                <h3 class="fw-bold text-gray-900 mb-0">{{ authStore.userClubs.length }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="bg-warning bg-opacity-10 rounded-3 p-3">
                  <i class="bi bi-award text-warning fs-4"></i>
                </div>
              </div>
              <div class="ms-3">
                <h6 class="text-gray-600 mb-1">В выбранном клубе</h6>
                <h3 class="fw-bold text-gray-900 mb-0">{{ currentClubStudentsCount }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Поиск -->
    <div class="row mb-4" v-if="currentClub">
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

    <!-- Таблица студентов -->
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white border-bottom">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h5 class="card-title mb-1">Список студентов</h5>
            <p class="text-gray-600 mb-0 small">
              {{ currentClub ? `Студенты клуба "${currentClub.name}"` : 'Выберите клуб для просмотра студентов' }}
            </p>
          </div>
          <div class="d-flex align-items-center">
            <button type="button" class="btn btn-primary btn-sm me-2" v-if="currentClub">
              <i class="bi bi-plus-lg me-1"></i>
              Добавить студента
            </button>
            <span class="badge bg-success">{{ authStore.userClubs.length }} активных клубов</span>
          </div>
        </div>
      </div>
      
      <div class="card-body">
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

        <!-- Заглушка для пустого состояния -->
        <div v-else-if="!currentClub" class="text-center py-5">
          <div class="mb-4">
            <i class="bi bi-building text-gray-400" style="font-size: 4rem;"></i>
          </div>
          <h5 class="text-gray-900 mb-2">Выберите клуб</h5>
          <p class="text-gray-600 mb-0">
            Выберите клуб в заголовке для просмотра студентов
          </p>
        </div>

        <!-- Заглушка для студентов -->
        <div v-else-if="students.length === 0" class="text-center py-5">
          <div class="mb-4">
            <i class="bi bi-people text-gray-400" style="font-size: 4rem;"></i>
          </div>
          <h5 class="text-gray-900 mb-2">
            {{ searchQuery ? 'Студенты не найдены' : 'Нет студентов' }}
          </h5>
          <p class="text-gray-600 mb-4">
            {{ searchQuery ? 'Попробуйте изменить критерии поиска' : `Начните с добавления первого студента в клуб ${currentClub.name}` }}
          </p>
          <button type="button" class="btn btn-primary" v-if="!searchQuery">
            <i class="bi bi-plus-lg me-2"></i>
            Добавить студента
          </button>
        </div>

        <!-- Таблица студентов -->
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
                <th class="border-0">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in students" :key="student.id" class="cursor-pointer" @click="$router.push(`/students/${student.id}`)">
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
                  <a :href="`tel:${student.phone}`" class="text-decoration-none" @click.stop>
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
                <td class="border-0">
                  <div class="btn-group" role="group">
                    <button 
                      type="button" 
                      class="btn btn-sm btn-outline-primary"
                      @click.stop="$router.push(`/students/${student.id}`)"
                      title="Просмотр деталей"
                    >
                      <i class="bi bi-eye"></i>
                    </button>
                    <button 
                      type="button" 
                      class="btn btn-sm btn-outline-secondary"
                      @click.stop
                      title="Редактировать"
                    >
                      <i class="bi bi-pencil"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Пагинация -->
          <div v-if="pagination.count > students.length" class="d-flex justify-content-center mt-4">
            <nav>
              <ul class="pagination pagination-sm">
                <li class="page-item" :class="{ disabled: !pagination.previous }">
                  <button class="page-link" @click="loadPreviousPage" :disabled="!pagination.previous">
                    Предыдущая
                  </button>
                </li>
                <li class="page-item" :class="{ disabled: !pagination.next }">
                  <button class="page-link" @click="loadNextPage" :disabled="!pagination.next">
                    Следующая
                  </button>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { studentsAPI } from '../services/api'
import type { Student } from '../types'

const authStore = useAuthStore()
const router = useRouter()

// Состояние
const students = ref<Student[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const searchQuery = ref('')
const currentPage = ref(1)
const pagination = ref({
  count: 0,
  next: null as string | null,
  previous: null as string | null,
})

const currentClub = computed(() => {
  const clubId = router.currentRoute.value.query.club
  if (clubId) {
    return authStore.userClubs.find(club => club.id === Number(clubId))
  }
  return authStore.userClubs[0] || null
})

const totalStudents = computed(() => {
  return authStore.userClubs.reduce((total, club) => total + club.students_count, 0)
})

const currentClubStudentsCount = computed(() => {
  return currentClub.value?.students_count || 0
})

// Функции
const loadStudents = async (page = 1, search?: string) => {
  if (!currentClub.value) return

  loading.value = true
  error.value = null
  
  try {
    const params: any = {
      club: currentClub.value.id,
      page
    }
    
    if (search) {
      params.search = search
    }

    const response = await studentsAPI.getAll(params)
    students.value = response.results
    pagination.value = {
      count: response.count,
      next: response.next,
      previous: response.previous,
    }
  } catch (err) {
    error.value = 'Ошибка при загрузке студентов'
    console.error('Error loading students:', err)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ru-RU')
}

const clearSearch = () => {
  searchQuery.value = ''
  currentPage.value = 1
  loadStudents()
}

const loadNextPage = () => {
  if (pagination.value.next) {
    currentPage.value++
    loadStudents(currentPage.value, searchQuery.value || undefined)
  }
}

const loadPreviousPage = () => {
  if (pagination.value.previous) {
    currentPage.value--
    loadStudents(currentPage.value, searchQuery.value || undefined)
  }
}

// Debounced поиск
let searchTimeout: NodeJS.Timeout
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    loadStudents(1, searchQuery.value || undefined)
  }, 300)
}

// Наблюдатели
watch(currentClub, (newClub) => {
  if (newClub) {
    searchQuery.value = ''
    currentPage.value = 1
    loadStudents()
  } else {
    students.value = []
  }
}, { immediate: true })

onMounted(async () => {
  // Загружаем данные пользователя, если они не загружены
  if (!authStore.user) {
    await authStore.loadUser()
  }
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