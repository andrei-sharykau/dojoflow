/**
 * Улучшенный композабл для работы со студентами
 */

import { ref, computed, watch } from 'vue'
import { studentsService } from '@/services/api/students'
import { useNotifications } from '@/composables/useNotifications'
import { usePagination } from '@/composables/usePagination'
import type { 
  Student, 
  StudentDetail, 
  StudentCreateUpdate, 
  StudentFilters,
  StudentStatistics,
  PaginatedResponse 
} from '@/types'

export interface UseStudentsOptions {
  autoLoad?: boolean
  defaultFilters?: Partial<StudentFilters>
  pageSize?: number
}

export function useStudents(options: UseStudentsOptions = {}) {
  const { autoLoad = true, defaultFilters = {}, pageSize = 20 } = options
  
  // Сервисы
  const { showSuccess, showError } = useNotifications()
  const pagination = usePagination({ pageSize })

  // Состояние
  const students = ref<Student[]>([])
  const currentStudent = ref<StudentDetail | null>(null)
  const statistics = ref<StudentStatistics | null>(null)
  const loading = ref(false)
  const saving = ref(false)
  const deleting = ref(false)
  const error = ref<string | null>(null)

  // Фильтры
  const filters = ref<StudentFilters>({
    search: '',
    club: undefined,
    city: '',
    level: undefined,
    age_min: undefined,
    age_max: undefined,
    start_date_from: undefined,
    start_date_to: undefined,
    last_attestation_from: undefined,
    last_attestation_to: undefined,
    ordering: '-created_at',
    ...defaultFilters
  })

  // Вычисляемые свойства
  const isEmpty = computed(() => students.value.length === 0 && !loading.value)
  const hasError = computed(() => error.value !== null)
  const totalStudents = computed(() => pagination.total.value)
  const currentPage = computed(() => pagination.currentPage.value)
  const totalPages = computed(() => pagination.totalPages.value)
  const hasNextPage = computed(() => pagination.hasNext.value)
  const hasPreviousPage = computed(() => pagination.hasPrevious.value)

  // Методы загрузки
  const loadStudents = async (page = 1, resetData = false) => {
    try {
      loading.value = true
      error.value = null

      const params = {
        ...filters.value,
        page,
        page_size: pageSize
      }

      const response = await studentsService.getStudents(params)
      
      if (resetData || page === 1) {
        students.value = response.results
      } else {
        students.value.push(...response.results)
      }

      pagination.setFromResponse(response)
    } catch (err: any) {
      error.value = err.message || 'Ошибка загрузки студентов'
      showError(error.value)
    } finally {
      loading.value = false
    }
  }

  const loadStudent = async (id: number) => {
    try {
      loading.value = true
      error.value = null
      currentStudent.value = await studentsService.getDetail(id)
    } catch (err: any) {
      error.value = err.message || 'Ошибка загрузки студента'
      showError(error.value)
    } finally {
      loading.value = false
    }
  }

  const loadStatistics = async () => {
    try {
      statistics.value = await studentsService.getStatistics(filters.value)
    } catch (err: any) {
      console.error('Ошибка загрузки статистики:', err)
    }
  }

  // CRUD операции
  const createStudent = async (data: StudentCreateUpdate): Promise<StudentDetail | null> => {
    try {
      saving.value = true
      error.value = null

      const newStudent = await studentsService.createStudent(data)
      
      // Добавляем в начало списка
      students.value.unshift(newStudent as Student)
      pagination.incrementTotal()
      
      showSuccess('Студент успешно создан')
      return newStudent
    } catch (err: any) {
      error.value = err.message || 'Ошибка создания студента'
      showError(error.value)
      return null
    } finally {
      saving.value = false
    }
  }

  const updateStudent = async (id: number, data: Partial<StudentCreateUpdate>): Promise<StudentDetail | null> => {
    try {
      saving.value = true
      error.value = null

      const updatedStudent = await studentsService.updateStudent(id, data)
      
      // Обновляем в списке
      const index = students.value.findIndex(s => s.id === id)
      if (index !== -1) {
        students.value[index] = updatedStudent as Student
      }
      
      // Обновляем текущего студента
      if (currentStudent.value?.id === id) {
        currentStudent.value = updatedStudent
      }
      
      showSuccess('Студент успешно обновлен')
      return updatedStudent
    } catch (err: any) {
      error.value = err.message || 'Ошибка обновления студента'
      showError(error.value)
      return null
    } finally {
      saving.value = false
    }
  }

  const deleteStudent = async (id: number): Promise<boolean> => {
    try {
      deleting.value = true
      error.value = null

      await studentsService.deleteStudent(id)
      
      // Удаляем из списка
      students.value = students.value.filter(s => s.id !== id)
      pagination.decrementTotal()
      
      // Очищаем текущего студента
      if (currentStudent.value?.id === id) {
        currentStudent.value = null
      }
      
      showSuccess('Студент успешно удален')
      return true
    } catch (err: any) {
      error.value = err.message || 'Ошибка удаления студента'
      showError(error.value)
      return false
    } finally {
      deleting.value = false
    }
  }

  // Фильтрация и поиск
  const updateFilters = (newFilters: Partial<StudentFilters>) => {
    filters.value = { ...filters.value, ...newFilters }
    pagination.reset()
    loadStudents(1, true)
  }

  const search = (query: string) => {
    updateFilters({ search: query })
  }

  const filterByClub = (clubId: number | undefined) => {
    updateFilters({ club: clubId })
  }

  const filterByLevel = (level: number | undefined) => {
    updateFilters({ level })
  }

  const resetFilters = () => {
    filters.value = { ...defaultFilters }
    pagination.reset()
    loadStudents(1, true)
  }

  // Пагинация
  const nextPage = () => {
    if (hasNextPage.value) {
      loadStudents(currentPage.value + 1)
    }
  }

  const previousPage = () => {
    if (hasPreviousPage.value) {
      loadStudents(currentPage.value - 1)
    }
  }

  const goToPage = (page: number) => {
    if (page >= 1 && page <= totalPages.value) {
      loadStudents(page)
    }
  }

  // Массовые операции
  const bulkDelete = async (ids: number[]): Promise<boolean> => {
    try {
      deleting.value = true
      const result = await studentsService.bulkDelete(ids)
      
      // Удаляем из списка
      students.value = students.value.filter(s => !ids.includes(s.id))
      pagination.decrementTotal(result.deleted)
      
      showSuccess(`Удалено студентов: ${result.deleted}`)
      
      if (result.errors.length > 0) {
        showError(`Ошибки: ${result.errors.join(', ')}`)
      }
      
      return true
    } catch (err: any) {
      error.value = err.message || 'Ошибка массового удаления'
      showError(error.value)
      return false
    } finally {
      deleting.value = false
    }
  }

  const bulkUpdate = async (ids: number[], data: Partial<StudentCreateUpdate>): Promise<boolean> => {
    try {
      saving.value = true
      const result = await studentsService.bulkUpdate(ids, data)
      
      // Перезагружаем данные
      await loadStudents(currentPage.value, true)
      
      showSuccess(`Обновлено студентов: ${result.updated}`)
      
      if (result.errors.length > 0) {
        showError(`Ошибки: ${result.errors.join(', ')}`)
      }
      
      return true
    } catch (err: any) {
      error.value = err.message || 'Ошибка массового обновления'
      showError(error.value)
      return false
    } finally {
      saving.value = false
    }
  }

  // Специальные методы
  const transferStudent = async (id: number, newClubId: number): Promise<boolean> => {
    try {
      saving.value = true
      const updatedStudent = await studentsService.transferStudent(id, newClubId)
      
      // Обновляем в списке
      const index = students.value.findIndex(s => s.id === id)
      if (index !== -1) {
        students.value[index] = updatedStudent as Student
      }
      
      showSuccess('Студент успешно переведен')
      return true
    } catch (err: any) {
      error.value = err.message || 'Ошибка перевода студента'
      showError(error.value)
      return false
    } finally {
      saving.value = false
    }
  }

  const checkAttestationEligibility = async (id: number) => {
    try {
      return await studentsService.checkAttestationEligibility(id)
    } catch (err: any) {
      showError('Ошибка проверки права на аттестацию')
      return null
    }
  }

  // Экспорт/импорт
  const exportStudents = async (format: 'csv' | 'xlsx' = 'csv'): Promise<boolean> => {
    try {
      loading.value = true
      const blob = await studentsService.exportStudents(filters.value, format)
      
      // Создаем ссылку для скачивания
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `students.${format}`
      link.click()
      window.URL.revokeObjectURL(url)
      
      showSuccess('Данные успешно экспортированы')
      return true
    } catch (err: any) {
      showError('Ошибка экспорта данных')
      return false
    } finally {
      loading.value = false
    }
  }

  const importStudents = async (file: File): Promise<boolean> => {
    try {
      loading.value = true
      const result = await studentsService.importStudents(file, (progress) => {
        console.log(`Импорт: ${progress}%`)
      })
      
      showSuccess(`Импортировано: ${result.success} из ${result.total}`)
      
      if (result.errors.length > 0) {
        showError(`Ошибки: ${result.errors.join(', ')}`)
      }
      
      // Перезагружаем данные
      await loadStudents(1, true)
      return true
    } catch (err: any) {
      showError('Ошибка импорта данных')
      return false
    } finally {
      loading.value = false
    }
  }

  // Автозагрузка
  if (autoLoad) {
    loadStudents()
    loadStatistics()
  }

  // Наблюдатели
  watch(
    () => filters.value,
    () => {
      loadStatistics()
    },
    { deep: true }
  )

  return {
    // Состояние
    students,
    currentStudent,
    statistics,
    loading,
    saving,
    deleting,
    error,
    filters,
    
    // Вычисляемые свойства
    isEmpty,
    hasError,
    totalStudents,
    currentPage,
    totalPages,
    hasNextPage,
    hasPreviousPage,
    
    // Методы загрузки
    loadStudents,
    loadStudent,
    loadStatistics,
    
    // CRUD операции
    createStudent,
    updateStudent,
    deleteStudent,
    
    // Фильтрация
    updateFilters,
    search,
    filterByClub,
    filterByLevel,
    resetFilters,
    
    // Пагинация
    nextPage,
    previousPage,
    goToPage,
    
    // Массовые операции
    bulkDelete,
    bulkUpdate,
    
    // Специальные методы
    transferStudent,
    checkAttestationEligibility,
    
    // Экспорт/импорт
    exportStudents,
    importStudents
  }
} 