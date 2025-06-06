<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { Club } from '@/types'

const authStore = useAuthStore()
const router = useRouter()
const showClubDropdown = ref(false)

const currentClub = computed(() => {
  const clubId = router.currentRoute.value.query.club
  
  if (clubId) {
    const foundClub = authStore.userClubs.find(club => club.id === Number(clubId))
    return foundClub
  }
  
  return authStore.userClubs[0] || null
})

async function logout() {
  await authStore.logout()
  router.push('/login')
}

function selectClub(club: Club) {
  showClubDropdown.value = false
  
  if (currentClub.value?.id === club.id) {
    return
  }
  
  router.push({ 
    name: router.currentRoute.value.name || 'dashboard', 
    query: { club: club.id } 
  })
}

function closeDropdown() {
  showClubDropdown.value = false
}

function handleClickOutside(event: Event) {
  const target = event.target as HTMLElement
  const dropdown = document.querySelector('.club-dropdown')
  
  if (dropdown && !dropdown.contains(target)) {
    showClubDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  
  setTimeout(() => {
    if (!currentClub.value && authStore.userClubs.length > 0 && !router.currentRoute.value.query.club) {
      const firstClub = authStore.userClubs[0]
      router.push({ 
        name: router.currentRoute.value.name || 'dashboard', 
        query: { club: firstClub.id } 
      })
    }
  }, 500)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm border-bottom">
    <div class="container-fluid">
      <!-- Логотип -->
      <div class="navbar-brand d-flex align-items-center">
        <div class="d-inline-flex align-items-center justify-content-center bg-primary rounded-2 me-2" style="width: 32px; height: 32px;">
          <div class="logo-icon" style="width: 18px; height: 18px;"></div>
        </div>
        <span class="fw-semibold text-gray-900">DojoFlow</span>
      </div>
      
      <!-- Выбор клуба -->
      <div class="dropdown position-relative me-auto club-dropdown">
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
              <span class="text-gray-600" style="font-size: 0.75rem;">
                {{ authStore.user?.email }}
              </span>
            </div>
          </div>
        </div>
        
        <!-- Кнопка выхода -->
        <button 
          class="btn btn-outline-danger btn-sm" 
          @click="logout"
          title="Выйти из системы"
        >
          <i class="bi bi-box-arrow-right"></i>
        </button>
      </div>
    </div>
  </nav>
</template> 