export type ConversationMode = 'chat' | 'search'

export type SearchResult = {
  title: string
  href: string
  body: string
}

export type Message = {
  id: string
  role: 'user' | 'assistant'
  content: string
  createdAt: string
  kind?: 'text' | 'search'
  searchResults?: SearchResult[]
}

export type ChatResponse = {
  answer: string
  confidence: number | null
}

export type SearchResponse = {
  query: string
  results: SearchResult[]
}

export type Conversation = {
  id: string
  title: string
  createdAt: string
  updatedAt: string
  mode: ConversationMode
  messages: Message[]
}

export type ChatStore = {
  activeConversationId: string | null
  conversations: Conversation[]
}
