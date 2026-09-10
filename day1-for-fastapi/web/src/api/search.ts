import type { SearchResponse } from '../types/chat'
import { request } from './client'

export const searchApi = {
  search(message: string) {
    const params = new URLSearchParams({ message: message.trim() })
    return request<SearchResponse>(`/search?${params.toString()}`, {
      method: 'POST',
    })
  },
}
