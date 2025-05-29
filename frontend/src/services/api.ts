import axios from 'axios'
import type {
  User,
  Club,
  Student,
  Attestation,
  AttestationLevel,
  LoginCredentials,
  TokenResponse,
  StudentCreate,
  AttestationCreate,
  ClubWithStudents
} from '../types'

const API_BASE_URL = 'http://localhost:8000/api'

// Создаем экземпляр axios с базовой конфигурацией
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Интерцептор для добавления токена авторизации
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Интерцептор для обработки ошибок авторизации
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
            refresh: refreshToken,
          })
          
          const { access } = response.data
          localStorage.setItem('access_token', access)
          
          // Повторяем оригинальный запрос с новым токеном
          originalRequest.headers.Authorization = `Bearer ${access}`
          return api(originalRequest)
        } catch (refreshError) {
          // Если обновление токена не удалось, очищаем localStorage и перенаправляем на логин
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      } else {
        // Нет refresh токена, перенаправляем на логин
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export const authAPI = {
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const response = await api.post('/auth/login/', credentials)
    return response.data
  },

  async logout(): Promise<void> {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get('/profile/me/')
    return response.data
  },

  async getUserClubs(): Promise<Club[]> {
    const response = await api.get('/profile/my_clubs/')
    return response.data
  },

  async getUserPermissions(): Promise<{ is_superuser: boolean; is_staff: boolean; clubs_count: number }> {
    const response = await api.get('/profile/permissions/')
    return response.data
  },
}

export const clubsAPI = {
  async getAll(): Promise<Club[]> {
    const response = await api.get('/clubs/')
    return response.data.results || response.data
  },

  async getById(id: number): Promise<Club> {
    const response = await api.get(`/clubs/${id}/`)
    return response.data
  },

  async getStudentsByClub(search?: string): Promise<ClubWithStudents[]> {
    const params = search ? { search } : {}
    const response = await api.get('/clubs/students_by_club/', { params })
    return response.data
  },
}

export const studentsAPI = {
  async getAll(params?: { club?: number; search?: string; page?: number }): Promise<{
    results: Student[]
    count: number
    next: string | null
    previous: string | null
  }> {
    const response = await api.get('/students/', { params })
    return response.data
  },

  async getById(id: number): Promise<Student> {
    const response = await api.get(`/students/${id}/`)
    return response.data
  },

  async create(student: StudentCreate): Promise<Student> {
    const response = await api.post('/students/', student)
    return response.data
  },

  async update(id: number, student: Partial<StudentCreate>): Promise<Student> {
    const response = await api.patch(`/students/${id}/`, student)
    return response.data
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/students/${id}/`)
  },

  async getAttestations(id: number): Promise<Attestation[]> {
    const response = await api.get(`/students/${id}/attestations/`)
    return response.data
  },
}

export const attestationsAPI = {
  async getAll(params?: { student?: number; club?: number; page?: number }): Promise<{
    results: Attestation[]
    count: number
    next: string | null
    previous: string | null
  }> {
    const response = await api.get('/attestations/', { params })
    return response.data
  },

  async getById(id: number): Promise<Attestation> {
    const response = await api.get(`/attestations/${id}/`)
    return response.data
  },

  async create(attestation: AttestationCreate): Promise<Attestation> {
    const response = await api.post('/attestations/', attestation)
    return response.data
  },

  async update(id: number, attestation: Partial<AttestationCreate>): Promise<Attestation> {
    const response = await api.patch(`/attestations/${id}/`, attestation)
    return response.data
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/attestations/${id}/`)
  },
}

export const attestationLevelsAPI = {
  async getAll(): Promise<AttestationLevel[]> {
    const response = await api.get('/attestation-levels/')
    return response.data.results || response.data
  },
}

export default api 