import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Student, StudentCreate, AttestationLevel } from '../types'
import { studentsAPI, attestationLevelsAPI } from '../services/api'

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

      const response = await studentsAPI.getAll(params)
      
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

      const student = await studentsAPI.getById(id)
      currentStudent.value = student
      
      return student
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Ошибка загрузки студента'
      return null
    } finally {
      loading.value = false
    }
  }

  async function createStudent(studentData: StudentCreate) {
    try {
      loading.value = true
      error.value = null

      const newStudent = await studentsAPI.create(studentData)
      students.value.unshift(newStudent)
      
      return newStudent
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Ошибка создания студента'
      return null
    } finally {
      loading.value = false
    }
  }

  async function updateStudent(id: number, studentData: Partial<StudentCreate>) {
    try {
      loading.value = true
      error.value = null

      const updatedStudent = await studentsAPI.update(id, studentData)
      
      const index = students.value.findIndex(s => s.id === id)
      if (index !== -1) {
        students.value[index] = updatedStudent
      }
      
      if (currentStudent.value?.id === id) {
        currentStudent.value = updatedStudent
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

      await studentsAPI.delete(id)
      
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
      attestationLevels.value = levels
      
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