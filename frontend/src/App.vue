<script setup lang="ts">
import { onMounted, ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const showClubDropdown = ref(false)

const currentClub = computed(() => {
  // Получаем текущий клуб из query параметра или первый доступный
  const clubId = router.currentRoute.value.query.club
  console.log('currentClub computed: clubId from URL =', clubId, 'available clubs =', authStore.userClubs.length)
  
  if (clubId) {
    const foundClub = authStore.userClubs.find(club => club.id === Number(clubId))
    console.log('Found club by ID:', foundClub?.name || 'not found')
    return foundClub
  }
  
  const firstClub = authStore.userClubs[0] || null
  console.log('Using first club:', firstClub?.name || 'no clubs')
  return firstClub
})

async function logout() {
  await authStore.logout()
  router.push('/login')
}

function selectClub(club: any) {
  console.log('selectClub вызвана для клуба:', club.name)
  
  showClubDropdown.value = false
  
  // Если выбирается тот же клуб, ничего не делаем
  if (currentClub.value?.id === club.id) {
    console.log('Клуб уже выбран, пропускаем')
    return
  }
  
  console.log('Переключаем клуб с', currentClub.value?.name, 'на', club.name)
  
  // Обновляем URL с выбранным клубом
  router.push({ 
    name: router.currentRoute.value.name || 'dashboard', 
    query: { club: club.id } 
  }).then(() => {
    console.log('URL обновлен, новый клуб:', club.name)
  }).catch(err => {
    console.error('Ошибка при обновлении URL:', err)
  })
}

function closeDropdown() {
  showClubDropdown.value = false
}

// Обработчик клика вне области dropdown
function handleClickOutside(event: Event) {
  const target = event.target as HTMLElement
  const dropdown = document.querySelector('.dropdown')
  
  if (dropdown && !dropdown.contains(target)) {
    showClubDropdown.value = false
  }
}

onMounted(async () => {
  // Инициализация auth store теперь происходит в router guard
  // Здесь можно добавить другую логику инициализации приложения
  
  // Добавляем обработчик клика вне области
  document.addEventListener('click', handleClickOutside)
  
  // Автоматически выбираем первый клуб, если не выбран и есть клубы
  setTimeout(() => {
    if (!currentClub.value && authStore.userClubs.length > 0 && !router.currentRoute.value.query.club) {
      const firstClub = authStore.userClubs[0]
      console.log('Автоматически выбираем первый клуб:', firstClub.name)
      router.push({ 
        name: router.currentRoute.value.name || 'dashboard', 
        query: { club: firstClub.id } 
      })
    }
  }, 500) // Небольшая задержка для завершения инициализации
})

onUnmounted(() => {
  // Удаляем обработчик клика вне области
  document.removeEventListener('click', handleClickOutside)
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
          <div class="dropdown ms-3 position-relative">
            <button 
              class="btn btn-outline-primary dropdown-toggle d-flex align-items-center" 
              type="button"
              @click.stop="showClubDropdown = !showClubDropdown"
              :class="{ 'btn-primary text-white': currentClub }"
            >
              <i class="bi bi-building me-2"></i>
              <div class="text-start">
                <div class="fw-medium">
                  {{ currentClub?.name || 'Выберите клуб' }}
                </div>
                <div class="small opacity-75" v-if="currentClub">
                  {{ currentClub.city }} • {{ currentClub.students_count }} студентов
                </div>
              </div>
            </button>
            <ul 
              v-show="showClubDropdown" 
              class="dropdown-menu dropdown-menu-end shadow show position-absolute" 
              style="min-width: 300px; top: 100%; right: 0; z-index: 1050;"
              @click.stop
            >
              <li class="dropdown-header d-flex justify-content-between align-items-center">
                <span class="fw-medium">Ваши клубы</span>
                <span class="badge bg-primary">{{ authStore.userClubs.length }}</span>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li v-for="club in authStore.userClubs" :key="club.id">
                <button 
                  class="dropdown-item d-flex justify-content-between align-items-center py-3 w-100 border-0 bg-transparent"
                  :class="{ 
                    'active': currentClub?.id === club.id,
                    'bg-light': currentClub?.id === club.id 
                  }"
                  @click="selectClub(club)"
                  type="button"
                >
                  <div class="d-flex align-items-center">
                    <div class="bg-primary rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 36px; height: 36px;">
                      <i class="bi bi-building text-white"></i>
                    </div>
                    <div>
                      <div class="fw-medium text-gray-900">{{ club.name }}</div>
                      <small class="text-gray-600">{{ club.city }}</small>
                    </div>
                  </div>
                  <div class="text-end">
                    <div class="badge bg-success mb-1">{{ club.students_count }}</div>
                    <div class="small text-gray-600">студентов</div>
                  </div>
                </button>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li>
                <div class="dropdown-item-text small text-gray-600 text-center">
                  <i class="bi bi-info-circle me-1"></i>
                  Переключение между клубами обновляет список студентов
                </div>
              </li>
            </ul>
          </div>
          
          <!-- Навигационные ссылки -->
          <div class="navbar-nav flex-row me-auto ms-4">
            <router-link 
              to="/dashboard" 
              class="nav-link me-3"
              :class="{ 'fw-bold text-primary': $route.name === 'dashboard' }"
            >
              <i class="bi bi-house me-1"></i>
              Главная
            </router-link>
            <router-link 
              to="/attestations" 
              class="nav-link"
              :class="{ 'fw-bold text-primary': $route.name === 'attestations' }"
            >
              <i class="bi bi-award me-1"></i>
              Аттестации
            </router-link>
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
    
    <!-- Overlay для закрытия dropdown (опционально, у нас есть обработчик клика) -->
    <div v-if="showClubDropdown" @click="closeDropdown" class="position-fixed top-0 start-0 w-100 h-100" style="z-index: 1040; background-color: transparent;"></div>
  </div>
</template>

<style>
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
