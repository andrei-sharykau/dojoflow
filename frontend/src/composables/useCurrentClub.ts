import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export function useCurrentClub() {
  const router = useRouter()
  const authStore = useAuthStore()

  const currentClub = computed(() => {
    const clubId = router.currentRoute.value.query.club
    
    if (clubId) {
      const foundClub = authStore.userClubs.find(club => club.id === Number(clubId))
      return foundClub || null
    }
    
    return authStore.userClubs[0] || null
  })

  const currentClubId = computed(() => currentClub.value?.id || null)
  
  const currentClubStudentsCount = computed(() => currentClub.value?.students_count || 0)

  function selectClub(clubId: number) {
    router.push({ 
      name: router.currentRoute.value.name || 'dashboard', 
      query: { club: clubId } 
    })
  }

  function ensureClubSelected() {
    if (!currentClub.value && authStore.userClubs.length > 0 && !router.currentRoute.value.query.club) {
      const firstClub = authStore.userClubs[0]
      selectClub(firstClub.id)
    }
  }

  return {
    currentClub,
    currentClubId,
    currentClubStudentsCount,
    selectClub,
    ensureClubSelected,
    userClubs: computed(() => authStore.userClubs)
  }
} 