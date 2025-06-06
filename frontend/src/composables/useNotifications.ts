/**
 * Composable для управления уведомлениями
 */
import { ref, computed } from 'vue'
import { NOTIFICATION_TYPES } from '@/constants/ui'

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
  persistent?: boolean
}

export interface NotificationOptions {
  title: string
  message?: string
  duration?: number
  persistent?: boolean
}

export function useNotifications() {
  const notifications = ref<Notification[]>([])

  /**
   * Добавляет уведомление
   */
  const addNotification = (
    type: Notification['type'], 
    options: NotificationOptions
  ): string => {
    const id = `notification-${Date.now()}-${Math.random()}`
    
    const notification: Notification = {
      id,
      type,
      title: options.title,
      message: options.message,
      duration: options.duration ?? 5000,
      persistent: options.persistent ?? false,
    }

    notifications.value.push(notification)

    // Автоматически удаляем через указанное время, если не persistent
    if (!notification.persistent && notification.duration && notification.duration > 0) {
      setTimeout(() => {
        removeNotification(id)
      }, notification.duration)
    }

    return id
  }

  /**
   * Удаляет уведомление
   */
  const removeNotification = (id: string): void => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index !== -1) {
      notifications.value.splice(index, 1)
    }
  }

  /**
   * Очищает все уведомления
   */
  const clearNotifications = (): void => {
    notifications.value = []
  }

  /**
   * Показывает успешное уведомление
   */
  const success = (options: NotificationOptions): string => {
    return addNotification(NOTIFICATION_TYPES.SUCCESS, options)
  }

  /**
   * Показывает уведомление об ошибке
   */
  const error = (options: NotificationOptions): string => {
    return addNotification(NOTIFICATION_TYPES.ERROR, {
      ...options,
      persistent: options.persistent ?? true, // Ошибки показываем постоянно по умолчанию
    })
  }

  /**
   * Показывает предупреждение
   */
  const warning = (options: NotificationOptions): string => {
    return addNotification(NOTIFICATION_TYPES.WARNING, options)
  }

  /**
   * Показывает информационное уведомление
   */
  const info = (options: NotificationOptions): string => {
    return addNotification(NOTIFICATION_TYPES.INFO, options)
  }

  return {
    // State
    notifications: computed(() => notifications.value),
    
    // Actions
    addNotification,
    removeNotification,
    clearNotifications,
    success,
    error,
    warning,
    info,
  }
} 