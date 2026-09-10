import { beforeEach, describe, expect, it } from 'vitest'
import { useChatStore } from './useChatStore'

describe('useChatStore conversation modes', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('creates a selectable mode and locks it after the first message', () => {
    const store = useChatStore()
    store.createConversation('search')

    expect(store.activeConversation.value?.mode).toBe('search')
    expect(store.setConversationMode('chat')).toBe(true)
    expect(store.activeConversation.value?.mode).toBe('chat')

    store.addUserMessage('FastAPI')

    expect(store.setConversationMode('search')).toBe(false)
    expect(store.activeConversation.value?.mode).toBe('chat')
  })

  it('persists structured search results as an assistant message', () => {
    const store = useChatStore()
    store.createConversation('search')
    store.addAssistantMessage('找到 1 条结果', undefined, {
      kind: 'search',
      searchResults: [
        {
          title: 'FastAPI',
          href: 'https://fastapi.tiangolo.com',
          body: '现代 Python Web 框架。',
        },
      ],
    })

    expect(store.activeConversation.value?.messages[0]).toMatchObject({
      role: 'assistant',
      kind: 'search',
      searchResults: [{ title: 'FastAPI' }],
    })
  })

  it('migrates old conversations to chat mode', () => {
    localStorage.setItem(
      'day1-chat-store',
      JSON.stringify({
        activeConversationId: 'old',
        conversations: [
          {
            id: 'old',
            title: '旧对话',
            createdAt: '2026-09-11T00:00:00.000Z',
            updatedAt: '2026-09-11T00:00:00.000Z',
            messages: [],
          },
        ],
      }),
    )

    expect(useChatStore().activeConversation.value?.mode).toBe('chat')
  })
})
