export type Message = {
  id: string
  role: 'user' | 'assistant'
  content: string
  createdAt: string
}

export type ChatResponse = {
  answer: string
  confidence: number | null
}

export type Conversation = {
  id: string
  title: string
  createdAt: string
  updatedAt: string
  messages: Message[]
}

export type ChatStore = {
  activeConversationId: string | null
  conversations: Conversation[]
}
