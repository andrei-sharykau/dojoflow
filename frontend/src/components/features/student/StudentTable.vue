<script setup lang="ts">
import { computed } from 'vue'
import type { Student } from '@/types'

interface Props {
  students: Student[]
  loading?: boolean
  error?: string | null
}

interface Emits {
  (e: 'student-click', student: Student): void
  (e: 'phone-click', phone: string): void
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  error: null
})

const emit = defineEmits<Emits>()

function onStudentClick(student: Student) {
  emit('student-click', student)
}

function onPhoneClick(event: Event, phone: string) {
  event.stopPropagation()
  emit('phone-click', phone)
}

const formatDate = (dateString: string | null) => {
  if (!dateString) return 'Нет данных'
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch {
    return 'Некорректная дата'
  }
}

const getBadgeColor = (level: string | null) => {
  if (!level) return 'bg-gray-500'
  
  const colors: Record<string, string> = {
    'белый': 'bg-secondary',
    'жёлтый': 'bg-warning',
    'оранжевый': 'bg-warning',
    'зелёный': 'bg-success',
    'синий': 'bg-primary',
    'коричневый': 'bg-dark',
    'чёрный': 'bg-dark'
  }
  
  return colors[level.toLowerCase()] || 'bg-gray-500'
}
</script>

<template>
  <div class="table-responsive">
    <!-- Загрузка -->
    <div v-if="loading" class="d-flex justify-content-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="alert alert-danger" role="alert">
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ error }}
    </div>

    <!-- Пустое состояние -->
    <div v-else-if="students.length === 0" class="text-center py-5">
      <div class="mb-4">
        <i class="bi bi-people text-gray-400" style="font-size: 4rem;"></i>
      </div>
      <h5 class="text-gray-900 mb-2">Студенты не найдены</h5>
      <p class="text-gray-600 mb-0">
        Попробуйте изменить критерии поиска или добавить новых студентов
      </p>
    </div>

    <!-- Таблица -->
    <table v-else class="table table-hover mb-0">
      <thead class="table-light">
        <tr>
          <th class="border-0">Студент</th>
          <th class="border-0">Возраст</th>
          <th class="border-0">Телефон</th>
          <th class="border-0">Уровень</th>
          <th class="border-0">Начало занятий</th>
          <th class="border-0">Последняя аттестация</th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="student in students" 
          :key="student.id" 
          class="cursor-pointer" 
          @click="onStudentClick(student)"
        >
          <td class="border-0">
            <div class="d-flex align-items-center">
              <div class="bg-primary rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px;">
                <i class="bi bi-person-fill text-white"></i>
              </div>
              <div>
                <div class="fw-medium text-gray-900">{{ student.full_name }}</div>
                <small class="text-gray-600">{{ student.city }}</small>
              </div>
            </div>
          </td>
          <td class="border-0">
            <span class="badge bg-light text-gray-700">{{ student.age }} лет</span>
          </td>
          <td class="border-0">
            <a 
              :href="`tel:${student.phone}`" 
              class="text-decoration-none" 
              @click="onPhoneClick($event, student.phone)"
            >
              {{ student.phone }}
            </a>
          </td>
          <td class="border-0">
            <span 
              v-if="student.current_level"
              class="badge text-white"
              :class="getBadgeColor(student.current_level)"
            >
              {{ student.current_level }}
            </span>
            <span v-else class="text-gray-500">Не указан</span>
          </td>
          <td class="border-0">
            <span class="text-gray-600">{{ formatDate(student.start_date) }}</span>
          </td>
          <td class="border-0">
            <span class="text-gray-600">{{ formatDate(student.last_attestation_date) }}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}

.cursor-pointer:hover {
  background-color: var(--bs-gray-50);
}
</style> 