import type { ChatResponse } from '../types/chat'
import { request } from './client'

export const chatApi = {
  sendMessage(message: string) {
    const params = new URLSearchParams({ message: message.trim() })
    return request<ChatResponse>(`/chat?${params.toString()}`, {
      method: 'POST',
    })
  },
}
