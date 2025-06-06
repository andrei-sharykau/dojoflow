<template>
  <div class="attestation-level-select">
    <select 
      :id="inputId"
      :value="modelValue" 
      @input="updateValue"
      class="form-select"
      :class="selectClass"
      :required="required"
    >
      <option value="">{{ placeholder }}</option>
      
      <!-- Ученические степени (кю) -->
      <optgroup label="Ученические степени (кю)">
        <option 
          v-for="level in kyuLevels" 
          :key="level.id" 
          :value="level.id"
        >
          {{ level.display_name }} 
          <span v-if="showOrder">({{ level.order }})</span>
        </option>
      </optgroup>
      
      <!-- Мастерские степени (дан) -->
      <optgroup label="Мастерские степени (дан)">
        <option 
          v-for="level in danLevels" 
          :key="level.id" 
          :value="level.id"
        >
          {{ level.display_name }}
          <span v-if="showOrder">({{ level.order }})</span>
        </option>
      </optgroup>
    </select>
    
    <!-- Дополнительная информация о выбранном уровне -->
    <div v-if="selectedLevel && showLevelInfo" class="level-info mt-2 p-2 bg-light rounded">
      <small class="text-muted">
        <strong>{{ selectedLevel.display_name }}</strong>
        <span v-if="selectedLevel.level.includes('ky')"> - Ученическая степень</span>
        <span v-else> - Мастерская степень</span>
        (Порядок: {{ selectedLevel.order }})
      </small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, type PropType } from 'vue'
import type { AttestationLevel } from '@/composables/useAttestations'

interface Props {
  modelValue: number | string
  levels: AttestationLevel[]
  placeholder?: string
  inputId?: string
  selectClass?: string
  required?: boolean
  showOrder?: boolean
  showLevelInfo?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Выберите уровень',
  required: false,
  showOrder: false,
  showLevelInfo: false
})

const emit = defineEmits<{
  'update:modelValue': [value: number | string]
}>()

// Группировка уровней
const kyuLevels = computed(() => {
  return props.levels.filter(level => level.level.includes('ky'))
})

const danLevels = computed(() => {
  return props.levels.filter(level => level.level.includes('dan'))
})

// Выбранный уровень
const selectedLevel = computed(() => {
  const levelId = Number(props.modelValue)
  return props.levels.find(level => level.id === levelId)
})

// Обновление значения
const updateValue = (event: Event) => {
  const target = event.target as HTMLSelectElement
  const value = target.value ? Number(target.value) : ''
  emit('update:modelValue', value)
}
</script>

<style scoped>
.level-info {
  font-size: 0.875rem;
  border: 1px solid #e9ecef;
}

.form-select optgroup {
  font-weight: 600;
  color: #495057;
}

.form-select option {
  font-weight: normal;
  padding: 0.375rem 0.75rem;
}
</style> 