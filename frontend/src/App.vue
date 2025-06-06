<script setup lang="ts">
import { useAuthStore } from './stores/auth'
import AppHeader from './components/layout/AppHeader.vue'

const authStore = useAuthStore()
</script>

<template>
  <div id="app" class="min-vh-100 bg-gray-50">
    <!-- Индикатор загрузки при инициализации -->
    <div v-if="!authStore.initialized && authStore.loading" class="d-flex justify-content-center align-items-center min-vh-100">
      <div class="text-center">
        <div class="spinner-border text-primary mb-3" role="status">
          <span class="visually-hidden">Загрузка...</span>
        </div>
        <p class="text-gray-600">Инициализация приложения...</p>
      </div>
    </div>

    <!-- Основное приложение -->
    <div v-else>
      <!-- Хедер -->
      <AppHeader v-if="authStore.isAuthenticated" />

      <!-- Основной контент -->
      <main class="flex-grow-1">
        <router-view />
      </main>
    </div>

    <!-- Глобальные уведомления -->
    <div v-if="authStore.error" class="position-fixed top-0 end-0 p-3" style="z-index: 1050;">
      <div class="alert alert-danger alert-dismissible d-flex align-items-center" role="alert">
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        <div>{{ authStore.error }}</div>
        <button 
          type="button" 
          class="btn-close" 
          @click="authStore.clearError()"
        ></button>
      </div>
    </div>
  </div>
</template>

<style>
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
