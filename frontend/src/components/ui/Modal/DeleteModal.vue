<template>
  <BaseModal
    :visible="visible"
    :title="title"
    :subtitle="subtitle"
    icon="bi bi-exclamation-triangle"
    icon-variant="danger"
    :loading="loading"
    :confirm-disabled="!confirmChecked"
    confirm-text="Удалить"
    confirm-variant="danger"
    :loading-text="loadingText"
    :hide-confirm-button="false"
    @close="handleClose"
    @confirm="handleConfirm"
    @cancel="handleCancel"
  >
    <div class="delete-modal">
      <!-- Основная информация об объекте -->
      <div v-if="item" class="delete-modal__item">
        <div class="delete-modal__item-icon">
          <div class="delete-modal__item-icon-wrapper">
            <i :class="itemIcon || 'bi bi-file-text'"></i>
          </div>
        </div>
        <div class="delete-modal__item-info">
          <h6 class="delete-modal__item-name">{{ itemName }}</h6>
          <p v-if="itemDescription" class="delete-modal__item-description">
            {{ itemDescription }}
          </p>
        </div>
      </div>

      <!-- Предупреждение -->
      <div class="alert alert-warning border-0 mb-4">
        <div class="d-flex align-items-start">
          <i class="bi bi-exclamation-triangle text-warning me-2 mt-1 flex-shrink-0"></i>
          <div>
            <p class="fw-medium mb-2">
              {{ warningTitle || `Вы действительно хотите удалить ${entityType}?` }}
            </p>
            <p class="mb-0 small">
              {{ warningText || `Все связанные данные будут безвозвратно удалены:` }}
            </p>
          </div>
        </div>
      </div>

      <!-- Список данных для удаления -->
      <div v-if="relatedData && relatedData.length > 0" class="row g-3 mb-4">
        <div v-for="data in relatedData" :key="data.title" class="col-12">
          <div class="d-flex align-items-center p-3 bg-light rounded-3">
            <div class="bg-opacity-10 rounded-circle p-2 me-3" :class="data.iconBg">
              <i :class="data.icon"></i>
            </div>
            <div class="flex-grow-1">
              <div class="fw-medium text-gray-900">{{ data.title }}</div>
              <div class="text-gray-600 small">{{ data.description }}</div>
            </div>
            <div class="text-end">
              <span 
                class="badge"
                :class="data.count > 0 ? 'bg-warning' : 'bg-secondary'"
              >
                {{ data.count > 0 ? 'Будут удалены' : 'Нет данных' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Дополнительная информация -->
      <slot name="additional-info" />

      <!-- Подтверждение -->
      <div class="form-check">
        <input 
          id="confirmDelete" 
          v-model="confirmChecked" 
          class="form-check-input" 
          type="checkbox"
          :disabled="loading"
        >
        <label for="confirmDelete" class="form-check-label text-gray-700">
          {{ confirmText || 'Я понимаю, что это действие нельзя отменить' }}
        </label>
      </div>
    </div>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import BaseModal from './BaseModal.vue'

export interface DeleteModalItem {
  name: string
  description?: string
  icon?: string
}

export interface DeleteModalRelatedData {
  title: string
  description: string
  count: number
  icon: string
  iconBg: string
}

export interface DeleteModalProps {
  visible: boolean
  loading?: boolean
  item?: DeleteModalItem | null
  entityType?: string
  title?: string
  subtitle?: string
  itemName?: string
  itemDescription?: string
  itemIcon?: string
  warningTitle?: string
  warningText?: string
  confirmText?: string
  loadingText?: string
  relatedData?: DeleteModalRelatedData[]
}

const props = withDefaults(defineProps<DeleteModalProps>(), {
  loading: false,
  entityType: 'этот элемент',
  title: 'Удаление',
  subtitle: 'Это действие нельзя будет отменить',
  loadingText: 'Удаление...',
  confirmText: 'Я понимаю, что это действие нельзя отменить'
})

const emit = defineEmits<{
  close: []
  confirm: []
  cancel: []
}>()

// State
const confirmChecked = ref(false)

// Computed
const itemName = computed(() => {
  return props.itemName || props.item?.name || 'Элемент'
})

const itemDescription = computed(() => {
  return props.itemDescription || props.item?.description
})

const itemIcon = computed(() => {
  return props.itemIcon || props.item?.icon
})

// Methods
const handleClose = () => {
  resetModal()
  emit('close')
}

const handleConfirm = () => {
  if (confirmChecked.value && !props.loading) {
    emit('confirm')
  }
}

const handleCancel = () => {
  resetModal()
  emit('cancel')
}

const resetModal = () => {
  confirmChecked.value = false
}

// Expose reset method
defineExpose({
  resetModal
})
</script>

<style scoped>
.delete-modal__item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.delete-modal__item-icon {
  margin-right: 1rem;
  flex-shrink: 0;
}

.delete-modal__item-icon-wrapper {
  width: 3rem;
  height: 3rem;
  background: rgba(var(--bs-primary-rgb), 0.1);
  color: var(--bs-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.delete-modal__item-info {
  flex: 1;
}

.delete-modal__item-name {
  margin: 0 0 0.25rem 0;
  font-weight: 600;
  color: var(--bs-gray-900);
}

.delete-modal__item-description {
  margin: 0;
  font-size: 0.875rem;
  color: var(--bs-gray-600);
}
</style> 