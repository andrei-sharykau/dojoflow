<template>
  <div class="modal fade show d-block" id="studentDeleteModal" tabindex="-1" style="background: rgba(0,0,0,0.5);" @click="closeModal">
    <div class="modal-dialog modal-dialog-centered" @click.stop>
      <div class="modal-content border-0 shadow">
        <!-- Заголовок -->
        <div class="modal-header border-bottom-0 pb-2">
          <div class="d-flex align-items-center">
            <div class="bg-danger bg-opacity-10 rounded-circle p-2 me-3">
              <i class="bi bi-exclamation-triangle text-danger fs-4"></i>
            </div>
            <div>
              <h5 class="modal-title fw-bold text-gray-900 mb-0">
                Удаление студента
              </h5>
              <p class="text-gray-600 mb-0 small">
                Это действие нельзя будет отменить
              </p>
            </div>
          </div>
          <button 
            type="button" 
            class="btn-close" 
            @click="closeModal"
            aria-label="Закрыть"
            :disabled="deleting"
          ></button>
        </div>

        <!-- Содержимое -->
        <div class="modal-body py-4">
          <div v-if="student">
            <!-- Информация о студенте -->
            <div class="d-flex align-items-start mb-4">
              <div class="bg-primary bg-opacity-10 rounded-circle p-2 me-3 flex-shrink-0">
                <i class="bi bi-person-fill text-primary fs-5"></i>
              </div>
              <div class="flex-grow-1">
                <h6 class="fw-bold text-gray-900 mb-1">
                  {{ student.full_name }}
                </h6>
                <p class="text-gray-600 mb-0">
                  <i class="bi bi-building me-1"></i>
                  {{ student.club_name }} • {{ student.city }}
                </p>
                <p class="text-gray-600 mb-0 small">
                  <i class="bi bi-calendar me-1"></i>
                  Занимается с {{ formatDate(student.start_date) }}
                  <span v-if="student.years_of_practice">
                    ({{ student.years_of_practice }} {{ getYearsText(student.years_of_practice) }})
                  </span>
                </p>
              </div>
            </div>

            <!-- Предупреждение -->
            <div class="alert alert-warning border-0 mb-4">
              <div class="d-flex align-items-start">
                <i class="bi bi-exclamation-triangle text-warning me-2 mt-1 flex-shrink-0"></i>
                <div>
                  <p class="fw-medium mb-2">
                    Вы действительно хотите удалить этого студента?
                  </p>
                  <p class="mb-0 small">
                    Вместе со студентом будут <strong>безвозвратно удалены</strong> все связанные данные:
                  </p>
                </div>
              </div>
            </div>

            <!-- Список данных для удаления -->
            <div class="row g-3 mb-4">
              <!-- Аттестации -->
              <div class="col-12">
                <div class="d-flex align-items-center p-3 bg-light rounded-3">
                  <div class="bg-success bg-opacity-10 rounded-circle p-2 me-3">
                    <i class="bi bi-award text-success"></i>
                  </div>
                  <div class="flex-grow-1">
                    <div class="fw-medium text-gray-900">История аттестаций</div>
                    <div class="text-gray-600 small">
                      {{ attestationsCount }} записей
                    </div>
                  </div>
                  <div class="text-end">
                    <span 
                      class="badge"
                      :class="attestationsCount > 0 ? 'bg-warning' : 'bg-secondary'"
                    >
                      {{ attestationsCount > 0 ? 'Будут удалены' : 'Нет данных' }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Участие в аттестациях -->
              <div class="col-12">
                <div class="d-flex align-items-center p-3 bg-light rounded-3">
                  <div class="bg-info bg-opacity-10 rounded-circle p-2 me-3">
                    <i class="bi bi-calendar-event text-info"></i>
                  </div>
                  <div class="flex-grow-1">
                    <div class="fw-medium text-gray-900">Участие в аттестациях</div>
                    <div class="text-gray-600 small">
                      Связи с проведенными аттестациями
                    </div>
                  </div>
                  <div class="text-end">
                    <span class="badge bg-warning">Будут удалены</span>
                  </div>
                </div>
              </div>

              <!-- Персональные данные -->
              <div class="col-12">
                <div class="d-flex align-items-center p-3 bg-light rounded-3">
                  <div class="bg-primary bg-opacity-10 rounded-circle p-2 me-3">
                    <i class="bi bi-person-lines-fill text-primary"></i>
                  </div>
                  <div class="flex-grow-1">
                    <div class="fw-medium text-gray-900">Персональные данные</div>
                    <div class="text-gray-600 small">
                      Контакты, адрес, место работы
                    </div>
                  </div>
                  <div class="text-end">
                    <span class="badge bg-danger">Будут удалены</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Подтверждение -->
            <div class="form-check mb-3">
              <input 
                id="confirmDelete" 
                v-model="confirmChecked" 
                class="form-check-input" 
                type="checkbox"
                :disabled="deleting"
              >
              <label for="confirmDelete" class="form-check-label text-gray-700">
                Я понимаю, что это действие нельзя отменить
              </label>
            </div>
          </div>

          <!-- Загрузка -->
          <div v-if="deleting" class="text-center py-3">
            <div class="spinner-border text-danger me-2" role="status">
              <span class="visually-hidden">Удаление...</span>
            </div>
            <span class="text-gray-600">Удаление студента...</span>
          </div>
        </div>

        <!-- Кнопки -->
        <div class="modal-footer border-top-0 pt-0">
          <button 
            type="button" 
            class="btn btn-outline-secondary"
            @click="closeModal"
            :disabled="deleting"
          >
            Отмена
          </button>
          <button 
            type="button" 
            class="btn btn-danger"
            :disabled="!confirmChecked || deleting"
            @click="handleDelete"
          >
            <span 
              v-if="deleting" 
              class="spinner-border spinner-border-sm me-2"
              role="status"
              aria-hidden="true"
            ></span>
            {{ deleting ? 'Удаление...' : 'Удалить студента' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { StudentDetail } from '@/types'

interface Props {
  student: StudentDetail | null
}

interface Emits {
  (e: 'delete', studentId: number): void
  (e: 'success', message: string): void
  (e: 'error', message: string): void
  (e: 'close'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Состояние
const deleting = ref(false)
const confirmChecked = ref(false)

// Вычисляемые свойства
const attestationsCount = computed(() => {
  return props.student?.attestations?.length || 0
})

// Форматирование
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ru-RU')
}

const getYearsText = (years: number) => {
  if (years === 1) return 'год'
  if (years >= 2 && years <= 4) return 'года'
  return 'лет'
}

// Обработка удаления
const handleDelete = async () => {
  if (!props.student || !confirmChecked.value) return

  try {
    deleting.value = true
    emit('delete', props.student.id)
  } catch (error) {
    deleting.value = false
    // Ошибка будет обработана в родительском компоненте
  }
}

// Закрытие модального окна
const closeModal = () => {
  resetModal()
  emit('close')
}

// Сброс состояния при закрытии модального окна
const resetModal = () => {
  confirmChecked.value = false
  deleting.value = false
}

// Экспортируем функцию для сброса состояния
defineExpose({
  resetModal
})
</script>

<style scoped>
.modal-content {
  border-radius: 1rem;
}

.bg-opacity-10 {
  background-color: rgba(var(--bs-primary-rgb), 0.1) !important;
}
</style> 