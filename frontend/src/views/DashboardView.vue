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
                <h6 class="text-gray-600 mb-1">Аттестации</h6>
                <h3 class="fw-bold text-gray-900 mb-0">0</h3>
              </div>
            </div>
          </div>
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
              Информация о всех зарегистрированных студентах
            </p>
          </div>
          <div class="d-flex align-items-center">
            <button type="button" class="btn btn-primary btn-sm me-2">
              <i class="bi bi-plus-lg me-1"></i>
              Добавить студента
            </button>
            <span class="badge bg-success">{{ authStore.userClubs.length }} активных клубов</span>
          </div>
        </div>
      </div>
      
      <div class="card-body">
        <!-- Заглушка для пустого состояния -->
        <div v-if="!currentClub" class="text-center py-5">
          <div class="mb-4">
            <i class="bi bi-building text-gray-400" style="font-size: 4rem;"></i>
          </div>
          <h5 class="text-gray-900 mb-2">Выберите клуб</h5>
          <p class="text-gray-600 mb-0">
            Выберите клуб в заголовке для просмотра студентов
          </p>
        </div>

        <!-- Заглушка для студентов -->
        <div v-else class="text-center py-5">
          <div class="mb-4">
            <i class="bi bi-people text-gray-400" style="font-size: 4rem;"></i>
          </div>
          <h5 class="text-gray-900 mb-2">Нет студентов</h5>
          <p class="text-gray-600 mb-4">
            Начните с добавления первого студента в клуб {{ currentClub.name }}
          </p>
          <button type="button" class="btn btn-primary">
            <i class="bi bi-plus-lg me-2"></i>
            Добавить студента
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

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

onMounted(async () => {
  // Загружаем данные пользователя, если они не загружены
  if (!authStore.user) {
    await authStore.loadUser()
  }
})
</script> 