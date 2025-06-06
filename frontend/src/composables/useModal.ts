/**
 * Composable для управления модальными окнами
 */
import { ref, computed } from 'vue'

export interface ModalState {
  isOpen: boolean
  title?: string
  data?: any
}

export function useModal(initialState: ModalState = { isOpen: false }) {
  const state = ref<ModalState>(initialState)

  /**
   * Открывает модальное окно
   */
  const open = (title?: string, data?: any) => {
    state.value = {
      isOpen: true,
      title,
      data,
    }
  }

  /**
   * Закрывает модальное окно
   */
  const close = () => {
    state.value = {
      isOpen: false,
      title: undefined,
      data: undefined,
    }
  }

  /**
   * Переключает состояние модального окна
   */
  const toggle = (title?: string, data?: any) => {
    if (state.value.isOpen) {
      close()
    } else {
      open(title, data)
    }
  }

  return {
    // State
    isOpen: computed(() => state.value.isOpen),
    title: computed(() => state.value.title),
    data: computed(() => state.value.data),
    state: computed(() => state.value),
    
    // Actions
    open,
    close,
    toggle,
  }
} 