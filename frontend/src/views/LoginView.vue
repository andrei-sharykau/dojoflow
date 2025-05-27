<template>
  <div class="min-vh-100 bg-gray-50 d-flex align-items-center justify-content-center py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-4 col-sm-6">
          <!-- Логотип и заголовок -->
          <div class="text-center mb-4">
            <div class="d-inline-flex align-items-center justify-content-center bg-primary rounded-3 mb-3" style="width: 48px; height: 48px;">
              <div class="logo-icon"></div>
            </div>
            <h2 class="h4 fw-bold text-gray-900 mb-2">
              Войти в DojoFlow
            </h2>
            <p class="text-gray-600 small">
              Система учета занимающихся Айкидо
            </p>
          </div>
          
          <!-- Форма входа -->
          <div class="card shadow-sm border-0 mb-4">
            <div class="card-body p-4">
              <form @submit.prevent="handleSubmit">
                <!-- Поле имени пользователя -->
                <div class="mb-3">
                  <label for="username" class="form-label text-gray-700 fw-medium">
                    Имя пользователя
                  </label>
                  <input
                    id="username"
                    v-model="form.username"
                    name="username"
                    type="text"
                    required
                    class="form-control"
                    placeholder="Введите имя пользователя"
                  />
                </div>

                <!-- Поле пароля -->
                <div class="mb-3">
                  <label for="password" class="form-label text-gray-700 fw-medium">
                    Пароль
                  </label>
                  <input
                    id="password"
                    v-model="form.password"
                    name="password"
                    type="password"
                    required
                    class="form-control"
                    placeholder="Введите пароль"
                  />
                </div>

                <!-- Сообщение об ошибке -->
                <div v-if="authStore.error" class="alert alert-danger d-flex align-items-center" role="alert">
                  <i class="bi bi-exclamation-triangle-fill me-2"></i>
                  <div>{{ authStore.error }}</div>
                </div>

                <!-- Кнопка входа -->
                <button
                  type="submit"
                  :disabled="authStore.loading"
                  class="btn btn-primary w-100"
                >
                  <span v-if="authStore.loading" class="d-flex align-items-center justify-content-center">
                    <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Вход...
                  </span>
                  <span v-else>Войти</span>
                </button>
              </form>
            </div>
          </div>

          <!-- Тестовые аккаунты -->
          <div class="card shadow-sm border-0">
            <div class="card-body p-3">
              <h6 class="card-title text-gray-900 mb-2">Тестовые аккаунты</h6>
              <div class="small">
                <div class="d-flex justify-content-between mb-1">
                  <span class="text-gray-600">Москва:</span>
                  <code class="text-gray-900">club_admin_moscow / admin123</code>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-gray-600">СПб:</span>
                  <code class="text-gray-900">club_admin_spb / admin123</code>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import type { LoginCredentials } from '../types'

const authStore = useAuthStore()
const router = useRouter()

const form = ref<LoginCredentials>({
  username: '',
  password: '',
})

async function handleSubmit() {
  authStore.clearError()
  
  const success = await authStore.login(form.value)
  if (success) {
    // Ждем следующий тик для завершения всех реактивных обновлений
    await nextTick()
    // Принудительный редирект через window.location
    window.location.href = '/dashboard'
  }
}

onMounted(() => {
  // Очищаем ошибки при загрузке страницы логина
  authStore.clearError()
})
</script> 