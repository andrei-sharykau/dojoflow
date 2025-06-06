/**
 * Composable для работы с уровнями аттестации
 */
import { ref, computed } from 'vue'
import { useApi } from './useApi'
import { API_ENDPOINTS } from '@/constants/api'

export interface AttestationLevel {
  id: number
  level: string
  display_name: string
  order: number
}

export function useAttestations() {
  const api = useApi()
  
  const attestationLevels = ref<AttestationLevel[]>([])

  const loading = computed(() => api.loading.value)
  const error = computed(() => api.error.value)

  /**
   * Получает уровни аттестации
   */
  const fetchAttestationLevels = async (): Promise<AttestationLevel[]> => {
    const response = await api.get<{results: AttestationLevel[]}>(API_ENDPOINTS.ATTESTATION_LEVELS)
    attestationLevels.value = response.results
    return response.results
  }

  /**
   * Сброс состояния
   */
  const reset = () => {
    attestationLevels.value = []
    api.reset()
  }

  return {
    // State
    attestationLevels: computed(() => attestationLevels.value),
    loading,
    error,
    
    // Actions
    fetchAttestationLevels,
    reset,
  }
} 