<script setup lang="ts">
import { ref } from 'vue'
import { chatApi } from './api/chat'
import { searchApi } from './api/search'
import ConversationSidebar from './components/ConversationSidebar.vue'
import ChatPanel from './components/ChatPanel.vue'
import MessageComposer from './components/MessageComposer.vue'
import { useChatStore } from './composables/useChatStore'
import type { ConversationMode, SearchResponse } from './types/chat'

const mobileOpen = ref(false)
const loading = ref(false)
const notice = ref('')
const {
  conversations,
  activeConversationId,
  activeConversation,
  createConversation,
  setConversationMode,
  selectConversation,
  deleteConversation,
  addUserMessage,
  addAssistantMessage,
} = useChatStore()

function searchSummary(response: SearchResponse) {
  return response.results.length
    ? `\u627e\u5230 ${response.results.length} \u6761\u641c\u7d22\u7ed3\u679c`
    : `\u6ca1\u6709\u627e\u5230\u4e0e\u300c${response.query}\u300d\u76f8\u5173\u7684\u7ed3\u679c`
}

function changeMode(mode: ConversationMode) {
  setConversationMode(mode)
}

async function sendMessage(content: string) {
  let conversation = activeConversation.value
  if (!conversation) {
    conversation = createConversation()
  }

  addUserMessage(content)
  loading.value = true
  notice.value = ''

  try {
    if (conversation.mode === 'search') {
      const result = await searchApi.search(content)
      addAssistantMessage(searchSummary(result), conversation.id, {
        kind: 'search',
        searchResults: result.results,
      })
    } else {
      const result = await chatApi.sendMessage(content)
      addAssistantMessage(result.answer, conversation.id)
    }
  } catch {
    notice.value = '\u6682\u65f6\u65e0\u6cd5\u8fde\u63a5\u540e\u7aef\uff0c\u8bf7\u786e\u8ba4 FastAPI \u5df2\u8fd0\u884c\u5728 localhost:8000\u3002'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="app-shell">
    <div class="mobile-backdrop" :class="{ 'mobile-backdrop--visible': mobileOpen }" @click="mobileOpen = false" />
    <ConversationSidebar
      :conversations="conversations"
      :active-conversation-id="activeConversationId"
      :mobile-open="mobileOpen"
      @create="createConversation"
      @select="selectConversation"
      @delete="deleteConversation"
      @close="mobileOpen = false"
    />
    <main class="main-area">
      <button class="mobile-menu" type="button" title="&#25171;&#24320;&#21382;&#21490;&#35760;&#24405;" @click="mobileOpen = true">&#9776;</button>
      <ChatPanel
        :conversation="activeConversation"
        :loading="loading"
        @create="createConversation"
        @set-mode="changeMode"
      />
      <p v-if="notice" class="notice">{{ notice }}</p>
      <MessageComposer :disabled="loading" @send="sendMessage" />
    </main>
  </div>
</template>
