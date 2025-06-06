/**
 * API сервис для студентов
 */

import { BaseApiService } from './base'
import { API_ENDPOINTS } from '@/constants/api'
import type { 
  Student, 
  StudentDetail, 
  StudentCreateUpdate,
  StudentFilters,
  StudentStatistics,
  PaginatedResponse,
  Attestation
} from '@/types'

export class StudentsApiService extends BaseApiService {
  constructor() {
    super(API_ENDPOINTS.STUDENTS)
  }

  async getStudents(filters?: StudentFilters): Promise<PaginatedResponse<Student>> {
    return await super.getAll<Student>(filters)
  }

  async getDetail(id: number): Promise<StudentDetail> {
    return await this.getById<StudentDetail>(id)
  }

  async createStudent(data: StudentCreateUpdate): Promise<Student> {
    return await this.create<Student, StudentCreateUpdate>(data)
  }

  async updateStudent(id: number, data: Partial<StudentCreateUpdate>): Promise<Student> {
    return await this.update<Student, StudentCreateUpdate>(id, data)
  }

  async deleteStudent(id: number): Promise<void> {
    await this.delete(id)
  }

  async getAttestations(id: number): Promise<Attestation[]> {
    const api = this.getApi()
    return await api.get<Attestation[]>(`${this.endpoint}${id}/attestations/`)
  }

  async getStatistics(filters?: StudentFilters): Promise<StudentStatistics> {
    const api = this.getApi()
    return await api.get<StudentStatistics>(`${this.endpoint}statistics/`, filters)
  }

  async getEligibleForAttestation(clubId?: number): Promise<Student[]> {
    const api = this.getApi()
    const params = clubId ? { club: clubId } : {}
    return await api.get<Student[]>(`${this.endpoint}eligible_for_attestation/`, params)
  }

  async transferStudent(id: number, newClubId: number): Promise<Student> {
    const api = this.getApi()
    return await api.post<Student>(`${this.endpoint}${id}/transfer/`, {
      new_club: newClubId
    })
  }
}

export const studentsAPI = new StudentsApiService() 