import { computed, ref } from 'vue'
import type { ChatStore, Conversation, ConversationMode, Message, SearchResult } from '../types/chat'

const STORAGE_KEY = 'day1-chat-store'

function emptyStore(): ChatStore {
  return { activeConversationId: null, conversations: [] }
}

function readStoredState(): ChatStore {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return emptyStore()
    const parsed = JSON.parse(stored) as ChatStore
    if (!Array.isArray(parsed.conversations)) return emptyStore()
    return {
      activeConversationId: parsed.activeConversationId ?? null,
      conversations: parsed.conversations.map((conversation) => ({
        ...conversation,
        mode: conversation.mode === 'search' ? 'search' : 'chat',
        messages: Array.isArray(conversation.messages)
          ? conversation.messages.map((message) => ({
              ...message,
              kind: message.kind === 'search' ? 'search' : message.kind,
              searchResults: Array.isArray(message.searchResults)
                ? (message.searchResults as SearchResult[])
                : undefined,
            }))
          : [],
      })),
    }
  } catch {
    return emptyStore()
  }
}

function makeId() {
  return typeof crypto.randomUUID === 'function'
    ? crypto.randomUUID()
    : `${Date.now()}-${Math.random().toString(16).slice(2)}`
}

function makeConversation(mode: ConversationMode = 'chat'): Conversation {
  const timestamp = new Date().toISOString()
  return {
    id: makeId(),
    title: '\u65b0\u5bf9\u8bdd',
    createdAt: timestamp,
    updatedAt: timestamp,
    mode,
    messages: [],
  }
}

export function useChatStore() {
  const state = ref<ChatStore>(readStoredState())
  const conversations = computed(() =>
    [...state.value.conversations].sort((a, b) => b.updatedAt.localeCompare(a.updatedAt)),
  )
  const activeConversationId = computed(() => state.value.activeConversationId)
  const activeConversation = computed(() =>
    state.value.conversations.find(({ id }) => id === state.value.activeConversationId),
  )

  const save = () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state.value))
  }

  const createConversation = (mode: ConversationMode = 'chat') => {
    const conversation = makeConversation(mode)
    state.value.conversations.push(conversation)
    state.value.activeConversationId = conversation.id
    save()
    return conversation
  }

  const setConversationMode = (mode: ConversationMode) => {
    const conversation = activeConversation.value
    if (!conversation || conversation.messages.length > 0) return false
    conversation.mode = mode
    save()
    return true
  }

  const selectConversation = (id: string) => {
    if (state.value.conversations.some((conversation) => conversation.id === id)) {
      state.value.activeConversationId = id
      save()
    }
  }

  const deleteConversation = (id: string) => {
    const index = state.value.conversations.findIndex((conversation) => conversation.id === id)
    if (index === -1) return
    state.value.conversations.splice(index, 1)
    if (state.value.activeConversationId === id) {
      state.value.activeConversationId = conversations.value[0]?.id ?? null
    }
    save()
  }

  const addUserMessage = (content: string) => {
    const trimmed = content.trim()
    if (!trimmed || !activeConversation.value) return
    const now = new Date().toISOString()
    const message: Message = {
      id: makeId(),
      role: 'user',
      content: trimmed,
      createdAt: now,
    }
    activeConversation.value.messages.push(message)
    activeConversation.value.updatedAt = now
    if (activeConversation.value.messages.length === 1) {
      activeConversation.value.title = trimmed.slice(0, 24)
    }
    save()
  }

  const addAssistantMessage = (
    content: string,
    conversationId = activeConversationId.value,
    options: { kind?: 'text' | 'search'; searchResults?: SearchResult[] } = {},
  ) => {
    const trimmed = content.trim()
    const conversation = state.value.conversations.find(({ id }) => id === conversationId)
    if (!trimmed || !conversation) return
    const now = new Date().toISOString()
    const message: Message = {
      id: makeId(),
      role: 'assistant',
      content: trimmed,
      createdAt: now,
    }
    if (options.kind) message.kind = options.kind
    if (options.searchResults) message.searchResults = options.searchResults
    conversation.messages.push(message)
    conversation.updatedAt = now
    save()
  }

  return {
    conversations,
    activeConversationId,
    activeConversation,
    createConversation,
    setConversationMode,
    selectConversation,
    deleteConversation,
    addUserMessage,
    addAssistantMessage,
  }
}
