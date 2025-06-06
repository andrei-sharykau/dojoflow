<template>
  <DeleteModal
    :visible="visible"
    :loading="loading"
    title="Удаление студента"
    entity-type="этого студента"
    :item="studentItem"
    :related-data="relatedData"
    @close="handleClose"
    @confirm="handleConfirm"
    @cancel="handleCancel"
  >
    <template #additional-info>
      <div v-if="student?.years_of_practice" class="mb-3">
        <small class="text-gray-600">
          <i class="bi bi-calendar me-1"></i>
          Занимается с {{ formatDate(student.start_date) }}
          ({{ student.years_of_practice }} {{ getYearsText(student.years_of_practice) }})
        </small>
      </div>
    </template>
  </DeleteModal>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import DeleteModal from '@/components/ui/Modal/DeleteModal.vue'
import type { StudentDetail } from '@/types'
import type { DeleteModalItem, DeleteModalRelatedData } from '@/components/ui/Modal/DeleteModal.vue'

interface Props {
  visible: boolean
  student: StudentDetail | null
  loading?: boolean
}

interface Emits {
  (e: 'close'): void
  (e: 'confirm'): void
  (e: 'cancel'): void
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const emit = defineEmits<Emits>()

// Computed
const studentItem = computed((): DeleteModalItem | null => {
  if (!props.student) return null
  
  return {
    name: props.student.full_name,
    description: `${props.student.club_name} • ${props.student.city}`,
    icon: 'bi bi-person-fill'
  }
})

const relatedData = computed((): DeleteModalRelatedData[] => {
  if (!props.student) return []
  
  const attestationsCount = props.student.attestations?.length || 0
  
  return [
    {
      title: 'История аттестаций',
      description: `${attestationsCount} записей`,
      count: attestationsCount,
      icon: 'bi bi-award text-success',
      iconBg: 'bg-success'
    },
    {
      title: 'Участие в аттестациях',
      description: 'Связи с проведенными аттестациями',
      count: 1, // Всегда есть связи
      icon: 'bi bi-calendar-event text-info',
      iconBg: 'bg-info'
    },
    {
      title: 'Персональные данные',
      description: 'Контакты, адрес, место работы',
      count: 1, // Всегда есть данные
      icon: 'bi bi-person-lines-fill text-primary',
      iconBg: 'bg-primary'
    }
  ]
})

// Methods
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ru-RU')
}

const getYearsText = (years: number) => {
  if (years === 1) return 'год'
  if (years >= 2 && years <= 4) return 'года'
  return 'лет'
}

const handleClose = () => {
  emit('close')
}

const handleConfirm = () => {
  emit('confirm')
}

const handleCancel = () => {
  emit('cancel')
}
</script> 