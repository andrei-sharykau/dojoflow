import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Student, StudentCreateUpdate, AttestationLevel } from '../types'
import { studentsService, attestationLevelsAPI } from '../services/api'

export const useStudentsStore = defineStore('students', () => {
  const students = ref<Student[]>([])
  const currentStudent = ref<Student | null>(null)
  const attestationLevels = ref<AttestationLevel[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const pagination = ref({
    count: 0,
    next: null as string | null,
    previous: null as string | null,
  })

  async function fetchStudents(params?: { club?: number; search?: string; page?: number }) {
    try {
      loading.value = true
      error.value = null

      const response = await studentsService.getStudents(params)
      
      students.value = response.results
      pagination.value = {
        count: response.count,
        next: response.next,
        previous: response.previous,
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Ошибка загрузки студентов'
      students.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchStudent(id: number) {
    try {
      loading.value = true
      error.value = null

      const student = await studentsService.getDetail(id)
      currentStudent.value = student
      
      return student
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Ошибка загрузки студента'
      return null
    } finally {
      loading.value = false
    }
  }

  async function createStudent(studentData: StudentCreateUpdate) {
    try {
      loading.value = true
      error.value = null

      const newStudent = await studentsService.createStudent(studentData)
      students.value.unshift(newStudent as Student)
      
      return newStudent
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Ошибка создания студента'
      return null
    } finally {
      loading.value = false
    }
  }

  async function updateStudent(id: number, studentData: Partial<StudentCreateUpdate>) {
    try {
      loading.value = true
      error.value = null

      const updatedStudent = await studentsService.updateStudent(id, studentData)
      
      const index = students.value.findIndex(s => s.id === id)
      if (index !== -1) {
        students.value[index] = updatedStudent as Student
      }
      
      if (currentStudent.value?.id === id) {
        currentStudent.value = updatedStudent as Student
      }
      
      return updatedStudent
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Ошибка обновления студента'
      return null
    } finally {
      loading.value = false
    }
  }

  async function deleteStudent(id: number) {
    try {
      loading.value = true
      error.value = null

      await studentsService.deleteStudent(id)
      
      students.value = students.value.filter(s => s.id !== id)
      
      if (currentStudent.value?.id === id) {
        currentStudent.value = null
      }
      
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Ошибка удаления студента'
      return false
    } finally {
      loading.value = false
    }
  }

  async function fetchAttestationLevels() {
    try {
      if (attestationLevels.value.length > 0) {
        return attestationLevels.value
      }

      const levels = await attestationLevelsAPI.getAll()
      attestationLevels.value = levels.results || levels
      
      return levels
    } catch (err: any) {
      console.error('Ошибка загрузки уровней аттестации:', err)
      return []
    }
  }

  function clearCurrentStudent() {
    currentStudent.value = null
  }

  function clearError() {
    error.value = null
  }

  return {
    students,
    currentStudent,
    attestationLevels,
    loading,
    error,
    pagination,
    fetchStudents,
    fetchStudent,
    createStudent,
    updateStudent,
    deleteStudent,
    fetchAttestationLevels,
    clearCurrentStudent,
    clearError,
  }
}) 