/**
 * API сервис для уровней аттестации
 */

import { BaseApiService } from './base'
import { API_ENDPOINTS } from '@/constants/api'
import type { AttestationLevel } from '@/types'

export class AttestationLevelsApiService extends BaseApiService {
  constructor() {
    super(API_ENDPOINTS.ATTESTATION_LEVELS)
  }

  async getAllLevels(): Promise<AttestationLevel[]> {
    const response = await super.getAll<AttestationLevel>()
    return response.results || []
  }

  async getLevel(id: number): Promise<AttestationLevel> {
    return await this.getById<AttestationLevel>(id)
  }
}

export const attestationLevelsAPI = new AttestationLevelsApiService() 