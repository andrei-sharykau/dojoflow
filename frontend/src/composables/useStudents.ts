/**
 * Composable для работы со студентами
 */

import { ref, computed, reactive } from 'vue'
import { studentsService } from '@/services/api'
import type { 
  Student, 
  StudentDetail, 
  StudentCreateUpdate, 
  StudentFilters, 
  StudentStatistics,
  PaginatedResponse 
} from '@/types'

export function useStudents() {
  const students = ref<Student[]>([])
  const currentStudent = ref<StudentDetail | null>(null)
  const statistics = ref<StudentStatistics | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  
  // Пагинация
  const pagination = reactive({
    page: 1,
    pages: 1,
    count: 0,
    page_size: 20,
    has_next: false,
    has_previous: false
  })

  // Фильтры
  const filters = reactive<StudentFilters>({
    search: '',
    club: undefined,
    city: '',
    level: undefined
  })

  const hasStudents = computed(() => students.value.length > 0)
  const isEmpty = computed(() => !isLoading.value && !hasStudents.value)

  // Загрузка списка студентов
  const loadStudents = async (params?: Partial<StudentFilters>) => {
    try {
      isLoading.value = true
      error.value = null
      
      const searchParams = {
        ...filters,
        ...params,
        page: pagination.page,
        page_size: pagination.page_size
      }
      
      const response = await studentsService.getStudents(searchParams)
      
      students.value = response.results
      Object.assign(pagination, response.pagination)
      
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка загрузки студентов'
      students.value = []
    } finally {
      isLoading.value = false
    }
  }

  // Загрузка деталей студента
  const loadStudent = async (id: number) => {
    try {
      isLoading.value = true
      error.value = null
      
      currentStudent.value = await studentsService.getDetail(id)
      
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка загрузки студента'
      currentStudent.value = null
    } finally {
      isLoading.value = false
    }
  }

  // Создание студента
  const createStudent = async (data: StudentCreateUpdate) => {
    try {
      isLoading.value = true
      error.value = null
      
      const student = await studentsService.createStudent(data)
      
      // Добавляем в начало списка
      students.value.unshift(student)
      pagination.count++
      
      return student
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка создания студента'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Обновление студента
  const updateStudent = async (id: number, data: Partial<StudentCreateUpdate>) => {
    try {
      isLoading.value = true
      error.value = null
      
      const student = await studentsService.updateStudent(id, data)
      
      // Обновляем в списке
      const index = students.value.findIndex(s => s.id === id)
      if (index !== -1) {
        students.value[index] = student
      }
      
      // Обновляем текущего студента если он открыт
      if (currentStudent.value?.id === id) {
        // Перезагружаем детали
        await loadStudent(id)
      }
      
      return student
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка обновления студента'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Удаление студента
  const deleteStudent = async (id: number) => {
    try {
      isLoading.value = true
      error.value = null
      
      await studentsService.deleteStudent(id)
      
      // Удаляем из списка
      const index = students.value.findIndex(s => s.id === id)
      if (index !== -1) {
        students.value.splice(index, 1)
        pagination.count--
      }
      
      // Очищаем текущего студента если он был удален
      if (currentStudent.value?.id === id) {
        currentStudent.value = null
      }
      
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка удаления студента'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Поиск студентов
  const searchStudents = async (searchQuery: string) => {
    filters.search = searchQuery
    pagination.page = 1
    await loadStudents()
  }

  // Фильтрация по клубу
  const filterByClub = async (clubId: number | undefined) => {
    filters.club = clubId
    pagination.page = 1
    await loadStudents()
  }

  // Очистка фильтров
  const clearFilters = async () => {
    Object.assign(filters, {
      search: '',
      club: undefined,
      city: '',
      level: undefined
    })
    pagination.page = 1
    await loadStudents()
  }

  // Загрузка статистики
  const loadStatistics = async (filterParams?: StudentFilters) => {
    try {
      statistics.value = await studentsService.getStatistics(filterParams)
    } catch (err: any) {
      console.error('Error loading statistics:', err)
      statistics.value = null
    }
  }

  // Перевод студента в другой клуб
  const transferStudent = async (studentId: number, newClubId: number) => {
    try {
      isLoading.value = true
      error.value = null
      
      const student = await studentsService.transferStudent(studentId, newClubId)
      
      // Обновляем в списке
      const index = students.value.findIndex(s => s.id === studentId)
      if (index !== -1) {
        students.value[index] = student
      }
      
      return student
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка перевода студента'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Пагинация
  const goToPage = async (page: number) => {
    pagination.page = page
    await loadStudents()
  }

  const nextPage = async () => {
    if (pagination.has_next) {
      await goToPage(pagination.page + 1)
    }
  }

  const prevPage = async () => {
    if (pagination.has_previous) {
      await goToPage(pagination.page - 1)
    }
  }

  return {
    // Состояние
    students: computed(() => students.value),
    currentStudent: computed(() => currentStudent.value),
    statistics: computed(() => statistics.value),
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    pagination: computed(() => pagination),
    filters: computed(() => filters),
    hasStudents,
    isEmpty,
    
    // Методы
    loadStudents,
    loadStudent,
    createStudent,
    updateStudent,
    deleteStudent,
    searchStudents,
    filterByClub,
    clearFilters,
    loadStatistics,
    transferStudent,
    
    // Пагинация
    goToPage,
    nextPage,
    prevPage
  }
} 