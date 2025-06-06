<script setup lang="ts">
interface Props {
  modelValue: string
  placeholder?: string
  loading?: boolean
  disabled?: boolean
}

interface Emits {
  (e: 'update:modelValue', value: string): void
  (e: 'search', value: string): void
  (e: 'clear'): void
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Поиск...',
  loading: false,
  disabled: false
})

const emit = defineEmits<Emits>()

function onInput(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
  emit('search', target.value)
}

function clearSearch() {
  emit('update:modelValue', '')
  emit('clear')
}
</script>

<template>
  <div class="input-group">
    <span class="input-group-text">
      <i v-if="!loading" class="bi bi-search"></i>
      <div v-else class="spinner-border spinner-border-sm" role="status">
        <span class="visually-hidden">Поиск...</span>
      </div>
    </span>
    <input
      :value="modelValue"
      type="text"
      class="form-control"
      :placeholder="placeholder"
      :disabled="disabled || loading"
      @input="onInput"
    />
    <button 
      v-if="modelValue" 
      class="btn btn-outline-secondary" 
      type="button"
      :disabled="disabled || loading"
      @click="clearSearch"
    >
      <i class="bi bi-x"></i>
    </button>
  </div>
</template> 