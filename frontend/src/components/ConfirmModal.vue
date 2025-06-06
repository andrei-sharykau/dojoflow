<template>
  <div class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header border-0 pb-0">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="btn-close" @click="$emit('cancel')"></button>
        </div>
        
        <div class="modal-body">
          <div class="text-center mb-4">
            <div class="mb-3">
              <i 
                class="bi fs-1"
                :class="iconClass"
              ></i>
            </div>
            <p class="mb-0">{{ message }}</p>
          </div>
        </div>
        
        <div class="modal-footer border-0 pt-0">
          <button 
            type="button" 
            class="btn btn-outline-secondary"
            @click="$emit('cancel')"
            :disabled="loading"
          >
            {{ cancelText }}
          </button>
          <button 
            type="button" 
            :class="confirmClass"
            @click="handleConfirm"
            :disabled="loading"
          >
            <span 
              v-if="loading" 
              class="spinner-border spinner-border-sm me-2"
              role="status"
              aria-hidden="true"
            ></span>
            {{ loading ? 'Подождите...' : confirmText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  title: string
  message: string
  confirmText?: string
  cancelText?: string
  confirmClass?: string
  icon?: string
}

const props = withDefaults(defineProps<Props>(), {
  confirmText: 'Подтвердить',
  cancelText: 'Отмена',
  confirmClass: 'btn btn-primary',
  icon: 'bi-question-circle-fill text-warning'
})

const emit = defineEmits<{
  confirm: []
  cancel: []
}>()

const loading = ref(false)

const iconClass = computed(() => {
  if (props.confirmClass.includes('btn-danger')) {
    return 'bi-exclamation-triangle-fill text-danger'
  }
  if (props.confirmClass.includes('btn-warning')) {
    return 'bi-exclamation-circle-fill text-warning'
  }
  return props.icon
})

const handleConfirm = async () => {
  loading.value = true
  try {
    emit('confirm')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal {
  backdrop-filter: blur(4px);
}

.modal-content {
  border: none;
  border-radius: 0.75rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-header {
  padding: 1.5rem 1.5rem 0;
}

.modal-body {
  padding: 1rem 1.5rem;
}

.modal-footer {
  padding: 0 1.5rem 1.5rem;
}
</style> 