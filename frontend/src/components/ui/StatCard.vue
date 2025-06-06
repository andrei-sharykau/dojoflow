<script setup lang="ts">
interface Props {
  title: string
  value: string | number
  icon: string
  iconColor?: 'primary' | 'success' | 'warning' | 'danger' | 'info'
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  iconColor: 'primary',
  loading: false
})
</script>

<template>
  <div class="card border-0 shadow-sm h-100">
    <div class="card-body">
      <div class="d-flex align-items-center">
        <div class="flex-shrink-0">
          <div 
            class="rounded-3 p-3"
            :class="`bg-${iconColor} bg-opacity-10`"
          >
            <i 
              :class="`bi ${icon} text-${iconColor} fs-4`"
            ></i>
          </div>
        </div>
        <div class="ms-3">
          <h6 class="text-gray-600 mb-1">{{ title }}</h6>
          <div v-if="loading" class="placeholder-glow">
            <span class="placeholder col-4"></span>
          </div>
          <h3 v-else class="fw-bold text-gray-900 mb-0">{{ value }}</h3>
        </div>
      </div>
    </div>
  </div>
</template> 