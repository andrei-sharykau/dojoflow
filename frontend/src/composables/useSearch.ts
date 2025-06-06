/**
 * Composable для поиска с debounce
 */
import { ref, computed, watch } from 'vue'

interface UseSearchOptions {
  debounceMs?: number
  onSearch?: (query: string) => void | Promise<void>
}

export function useSearch(options: UseSearchOptions = {}) {
  const { debounceMs = 300, onSearch } = options
  
  const searchQuery = ref('')
  const isSearching = ref(false)
  
  let searchTimeout: number | null = null
  
  const debouncedSearch = () => {
    if (searchTimeout) {
      clearTimeout(searchTimeout)
    }
    
    searchTimeout = setTimeout(async () => {
      if (onSearch) {
        isSearching.value = true
        try {
          await onSearch(searchQuery.value)
        } finally {
          isSearching.value = false
        }
      }
    }, debounceMs)
  }
  
  const clearSearch = () => {
    searchQuery.value = ''
    if (searchTimeout) {
      clearTimeout(searchTimeout)
    }
    if (onSearch) {
      onSearch('')
    }
  }
  
  const performSearch = async (query: string) => {
    searchQuery.value = query
    if (onSearch) {
      isSearching.value = true
      try {
        await onSearch(query)
      } finally {
        isSearching.value = false
      }
    }
  }
  
  // Автоматически вызывать поиск при изменении query
  watch(searchQuery, debouncedSearch)
  
  return {
    searchQuery,
    isSearching,
    debouncedSearch,
    clearSearch,
    performSearch
  }
} 