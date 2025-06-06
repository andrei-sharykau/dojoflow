<template>
  <Teleport to="body">
    <Transition name="modal" appear>
      <div
        v-if="visible"
        class="modal-overlay"
        @click="handleOverlayClick"
      >
        <div
          class="modal-container"
          :class="containerClass"
          @click.stop
        >
          <div class="modal-content">
            <!-- Header -->
            <header v-if="!hideHeader" class="modal-header">
              <div class="modal-header__content">
                <slot name="header">
                  <div class="modal-header__icon" v-if="icon">
                    <div 
                      class="modal-header__icon-wrapper"
                      :class="iconClass"
                    >
                      <i :class="icon"></i>
                    </div>
                  </div>
                  <div>
                    <h3 v-if="title" class="modal-header__title">{{ title }}</h3>
                    <p v-if="subtitle" class="modal-header__subtitle">{{ subtitle }}</p>
                  </div>
                </slot>
              </div>
              <button
                v-if="!hideCloseButton"
                type="button"
                class="modal-header__close"
                @click="handleClose"
                :disabled="loading"
                aria-label="Закрыть"
              >
                <i class="bi bi-x"></i>
              </button>
            </header>

            <!-- Body -->
            <main class="modal-body" :class="{ 'modal-body--padded': padded }">
              <slot />
            </main>

            <!-- Footer -->
            <footer v-if="!hideFooter" class="modal-footer">
              <slot name="footer">
                <div class="modal-footer__actions">
                  <button
                    v-if="!hideCancelButton"
                    type="button"
                    class="btn btn-outline-secondary"
                    @click="handleCancel"
                    :disabled="loading"
                  >
                    {{ cancelText }}
                  </button>
                  <button
                    v-if="!hideConfirmButton"
                    type="button"
                    class="btn"
                    :class="confirmButtonClass"
                    @click="handleConfirm"
                    :disabled="loading || confirmDisabled"
                  >
                    <span 
                      v-if="loading" 
                      class="spinner-border spinner-border-sm me-2"
                      role="status"
                      aria-hidden="true"
                    ></span>
                    {{ loading ? loadingText : confirmText }}
                  </button>
                </div>
              </slot>
            </footer>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue'

export interface BaseModalProps {
  visible: boolean
  title?: string
  subtitle?: string
  icon?: string
  iconVariant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info'
  size?: 'sm' | 'md' | 'lg' | 'xl'
  closeOnOverlay?: boolean
  closeOnEscape?: boolean
  hideHeader?: boolean
  hideFooter?: boolean
  hideCloseButton?: boolean
  hideCancelButton?: boolean
  hideConfirmButton?: boolean
  padded?: boolean
  loading?: boolean
  confirmDisabled?: boolean
  cancelText?: string
  confirmText?: string
  loadingText?: string
  confirmVariant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info'
}

const props = withDefaults(defineProps<BaseModalProps>(), {
  size: 'md',
  closeOnOverlay: true,
  closeOnEscape: true,
  hideHeader: false,
  hideFooter: false,
  hideCloseButton: false,
  hideCancelButton: false,
  hideConfirmButton: true,
  padded: true,
  loading: false,
  confirmDisabled: false,
  cancelText: 'Отмена',
  confirmText: 'Подтвердить',
  loadingText: 'Загрузка...',
  confirmVariant: 'primary',
  iconVariant: 'primary'
})

const emit = defineEmits<{
  close: []
  confirm: []
  cancel: []
}>()

// Computed
const containerClass = computed(() => [
  `modal-container--${props.size}`
])

const iconClass = computed(() => {
  if (!props.icon) return ''
  
  const variantClasses = {
    primary: 'bg-primary bg-opacity-10 text-primary',
    secondary: 'bg-secondary bg-opacity-10 text-secondary', 
    success: 'bg-success bg-opacity-10 text-success',
    danger: 'bg-danger bg-opacity-10 text-danger',
    warning: 'bg-warning bg-opacity-10 text-warning',
    info: 'bg-info bg-opacity-10 text-info'
  }
  
  return variantClasses[props.iconVariant]
})

const confirmButtonClass = computed(() => {
  const variantClasses = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    success: 'btn-success', 
    danger: 'btn-danger',
    warning: 'btn-warning',
    info: 'btn-info'
  }
  
  return variantClasses[props.confirmVariant]
})

// Methods
const handleClose = () => {
  if (!props.loading) {
    emit('close')
  }
}

const handleCancel = () => {
  if (!props.loading) {
    emit('cancel')
    emit('close')
  }
}

const handleConfirm = () => {
  if (!props.loading && !props.confirmDisabled) {
    emit('confirm')
  }
}

const handleOverlayClick = () => {
  if (props.closeOnOverlay && !props.loading) {
    emit('close')
  }
}

const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && props.closeOnEscape && !props.loading) {
    emit('close')
  }
}

// Lifecycle
onMounted(() => {
  if (props.closeOnEscape) {
    document.addEventListener('keydown', handleKeyDown)
  }
})

onUnmounted(() => {
  if (props.closeOnEscape) {
    document.removeEventListener('keydown', handleKeyDown)
  }
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
  padding: 1rem;
  overflow-y: auto;
}

.modal-container {
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  margin: auto;
}

.modal-container--sm {
  max-width: 400px;
}

.modal-container--md {
  max-width: 500px;
}

.modal-container--lg {
  max-width: 800px;
}

.modal-container--xl {
  max-width: 1140px;
}

.modal-content {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.175);
  display: flex;
  flex-direction: column;
  max-height: 100%;
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid var(--bs-border-color);
  flex-shrink: 0;
}

.modal-header__content {
  display: flex;
  align-items: flex-start;
  flex: 1;
}

.modal-header__icon {
  margin-right: 1rem;
  flex-shrink: 0;
}

.modal-header__icon-wrapper {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.modal-header__title {
  margin: 0 0 0.25rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--bs-gray-900);
}

.modal-header__subtitle {
  margin: 0;
  font-size: 0.875rem;
  color: var(--bs-gray-600);
}

.modal-header__close {
  background: none;
  border: none;
  font-size: 1.25rem;
  line-height: 1;
  color: var(--bs-gray-500);
  padding: 0.25rem;
  margin: -0.25rem -0.25rem -0.25rem 1rem;
  cursor: pointer;
  flex-shrink: 0;
}

.modal-header__close:hover:not(:disabled) {
  color: var(--bs-gray-700);
}

.modal-header__close:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
}

.modal-body--padded {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--bs-border-color);
  flex-shrink: 0;
}

.modal-footer__actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

/* Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.25s ease;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.25s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.9) translateY(-2rem);
}
</style> 