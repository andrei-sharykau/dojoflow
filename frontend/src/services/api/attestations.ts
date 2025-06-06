/**
 * API сервис для аттестаций
 */

import { BaseApiService } from './base'
import { API_ENDPOINTS } from '@/constants/api'
import type { 
  Attestation, 
  AttestationDetail, 
  AttestationCreateUpdate,
  AttestationFilters,
  AttestationHistory,
  PaginatedResponse
} from '@/types'

export class AttestationsApiService extends BaseApiService {
  constructor() {
    super(API_ENDPOINTS.ATTESTATIONS)
  }

  async getAttestations(filters?: AttestationFilters): Promise<PaginatedResponse<Attestation>> {
    return await super.getAll<Attestation>(filters)
  }

  async getDetail(id: number): Promise<AttestationDetail> {
    return await this.getById<AttestationDetail>(id)
  }

  async createAttestation(data: AttestationCreateUpdate): Promise<Attestation> {
    return await this.create<Attestation, AttestationCreateUpdate>(data)
  }

  async updateAttestation(id: number, data: Partial<AttestationCreateUpdate>): Promise<Attestation> {
    return await this.update<Attestation, AttestationCreateUpdate>(id, data)
  }

  async deleteAttestation(id: number): Promise<void> {
    await this.delete(id)
  }

  async getStudentHistory(studentId: number): Promise<AttestationHistory[]> {
    const api = this.getApi()
    return await api.get<AttestationHistory[]>(`/api/students/${studentId}/attestation_history/`)
  }
}

export const attestationsAPI = new AttestationsApiService() 