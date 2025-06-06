/**
 * Composable для пагинации
 */
import { ref, computed } from 'vue'
import { PAGINATION } from '@/constants/ui'

export interface PaginationData {
  count: number
  next: string | null
  previous: string | null
  results?: any[]
}

export interface PaginationOptions {
  initialPageSize?: number
  pageSizeOptions?: number[]
}

export function usePagination(options: PaginationOptions = {}) {
  const { 
    initialPageSize = PAGINATION.DEFAULT_PAGE_SIZE,
    pageSizeOptions = PAGINATION.PAGE_SIZE_OPTIONS 
  } = options

  const currentPage = ref(1)
  const pageSize = ref(initialPageSize)
  const totalCount = ref(0)
  const hasNext = ref(false)
  const hasPrevious = ref(false)

  /**
   * Обновляет данные пагинации
   */
  const updatePagination = (data: PaginationData) => {
    totalCount.value = data.count
    hasNext.value = !!data.next
    hasPrevious.value = !!data.previous
  }

  /**
   * Переходит на следующую страницу
   */
  const nextPage = () => {
    if (hasNext.value) {
      currentPage.value++
    }
  }

  /**
   * Переходит на предыдущую страницу
   */
  const previousPage = () => {
    if (hasPrevious.value) {
      currentPage.value--
    }
  }

  /**
   * Переходит на конкретную страницу
   */
  const goToPage = (page: number) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
    }
  }

  /**
   * Изменяет размер страницы
   */
  const changePageSize = (newSize: number) => {
    pageSize.value = newSize
    currentPage.value = 1 // Сбрасываем на первую страницу
  }

  /**
   * Сбрасывает пагинацию
   */
  const reset = () => {
    currentPage.value = 1
    totalCount.value = 0
    hasNext.value = false
    hasPrevious.value = false
  }

  // Вычисляемые свойства
  const totalPages = computed(() => {
    return Math.ceil(totalCount.value / pageSize.value)
  })

  const startItem = computed(() => {
    return (currentPage.value - 1) * pageSize.value + 1
  })

  const endItem = computed(() => {
    const end = currentPage.value * pageSize.value
    return Math.min(end, totalCount.value)
  })

  const isFirstPage = computed(() => {
    return currentPage.value === 1
  })

  const isLastPage = computed(() => {
    return currentPage.value === totalPages.value
  })

  return {
    // State
    currentPage: computed(() => currentPage.value),
    pageSize: computed(() => pageSize.value),
    totalCount: computed(() => totalCount.value),
    totalPages,
    hasNext: computed(() => hasNext.value),
    hasPrevious: computed(() => hasPrevious.value),
    startItem,
    endItem,
    isFirstPage,
    isLastPage,
    pageSizeOptions,

    // Actions
    updatePagination,
    nextPage,
    previousPage,
    goToPage,
    changePageSize,
    reset,
  }
} 