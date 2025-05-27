<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const showClubDropdown = ref(false)

const currentClub = computed(() => {
  // Получаем текущий клуб из query параметра или первый доступный
  const clubId = router.currentRoute.value.query.club
  if (clubId) {
    return authStore.userClubs.find(club => club.id === Number(clubId))
  }
  return authStore.userClubs[0] || null
})

async function logout() {
  await authStore.logout()
  router.push('/login')
}

function selectClub(club: any) {
  showClubDropdown.value = false
  // Обновляем URL с выбранным клубом
  router.push({ 
    name: router.currentRoute.value.name || 'dashboard', 
    query: { club: club.id } 
  })
}

onMounted(async () => {
  // Инициализация auth store теперь происходит в router guard
  // Здесь можно добавить другую логику инициализации приложения
})
</script>

<template>
  <div id="app" class="min-vh-100 bg-gray-50">
    <!-- Индикатор загрузки при инициализации -->
    <div v-if="!authStore.initialized && authStore.loading" class="d-flex justify-content-center align-items-center min-vh-100">
      <div class="text-center">
        <div class="spinner-border text-primary mb-3" role="status">
          <span class="visually-hidden">Загрузка...</span>
        </div>
        <p class="text-gray-600">Инициализация приложения...</p>
      </div>
    </div>

    <!-- Основное приложение -->
    <div v-else>
      <!-- Хедер -->
      <nav v-if="authStore.isAuthenticated" class="navbar navbar-expand-lg navbar-light bg-white shadow-sm border-bottom">
        <div class="container-fluid">
          <!-- Логотип -->
          <div class="navbar-brand d-flex align-items-center">
            <div class="d-inline-flex align-items-center justify-content-center bg-primary rounded-2 me-2" style="width: 32px; height: 32px;">
              <div class="logo-icon" style="width: 18px; height: 18px;"></div>
            </div>
            <span class="fw-semibold text-gray-900">DojoFlow</span>
          </div>
          
          <!-- Выбор клуба -->
          <div v-if="authStore.userClubs.length > 1" class="dropdown me-auto ms-3">
            <button 
              class="btn btn-outline-secondary btn-sm dropdown-toggle" 
              type="button" 
              data-bs-toggle="dropdown"
              @click="showClubDropdown = !showClubDropdown"
            >
              {{ currentClub?.name || 'Выберите клуб' }}
            </button>
            <ul class="dropdown-menu" :class="{ show: showClubDropdown }">
              <li v-for="club in authStore.userClubs" :key="club.id">
                <button 
                  class="dropdown-item d-flex justify-content-between align-items-center"
                  :class="{ active: currentClub?.id === club.id }"
                  @click="selectClub(club)"
                >
                  <div>
                    <div class="fw-medium">{{ club.name }}</div>
                    <small class="text-gray-600">{{ club.city }}</small>
                  </div>
                  <small class="text-gray-600">{{ club.students_count }} студентов</small>
                </button>
              </li>
            </ul>
          </div>
          
          <!-- Название клуба если только один -->
          <div v-else-if="currentClub" class="me-auto ms-3">
            <span class="badge bg-light text-gray-700 fs-6">{{ currentClub.name }}</span>
          </div>
          
          <!-- Правая часть: Пользователь и выход -->
          <div class="d-flex align-items-center">
            <!-- Информация о пользователе -->
            <div class="d-flex align-items-center me-3">
              <!-- Аватар -->
              <div class="bg-primary rounded-circle d-flex align-items-center justify-content-center me-2" style="width: 32px; height: 32px;">
                <i class="bi bi-person-fill text-white"></i>
              </div>
              <!-- Информация -->
              <div class="text-start">
                <div class="fw-medium text-gray-900 small">
                  {{ authStore.user?.first_name }} {{ authStore.user?.last_name }}
                </div>
                <div class="d-flex align-items-center">
                  <span v-if="authStore.isSuperuser" class="badge bg-primary me-1" style="font-size: 0.65rem;">
                    Админ
                  </span>
                  <small class="text-gray-600">{{ authStore.user?.username }}</small>
                </div>
              </div>
            </div>
            
            <!-- Кнопка выхода -->
            <button
              @click="logout"
              class="btn btn-outline-danger btn-sm"
              title="Выйти из системы"
            >
              <i class="bi bi-box-arrow-right"></i>
            </button>
          </div>
        </div>
      </nav>

      <!-- Основной контент -->
      <main class="flex-grow-1">
        <router-view />
      </main>
    </div>

    <!-- Глобальные уведомления -->
    <div v-if="authStore.error" class="position-fixed top-0 end-0 p-3" style="z-index: 1050;">
      <div class="alert alert-danger alert-dismissible d-flex align-items-center" role="alert">
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        <div>{{ authStore.error }}</div>
        <button 
          type="button" 
          class="btn-close" 
          @click="authStore.clearError()"
        ></button>
      </div>
    </div>
    
    <!-- Overlay для закрытия dropdown -->
    <div v-if="showClubDropdown" @click="showClubDropdown = false" class="position-fixed top-0 start-0 w-100 h-100" style="z-index: 1040;"></div>
  </div>
</template>

<style>
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
