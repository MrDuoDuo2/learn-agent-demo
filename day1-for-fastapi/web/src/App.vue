<script setup lang="ts">
import { ref } from 'vue'
import { chatApi } from './api/chat'
import ConversationSidebar from './components/ConversationSidebar.vue'
import ChatPanel from './components/ChatPanel.vue'
import MessageComposer from './components/MessageComposer.vue'
import { useChatStore } from './composables/useChatStore'

const mobileOpen = ref(false)
const loading = ref(false)
const notice = ref('')
const {
  conversations,
  activeConversationId,
  activeConversation,
  createConversation,
  selectConversation,
  deleteConversation,
  addUserMessage,
  addAssistantMessage,
} = useChatStore()

async function sendMessage(content: string) {
  let conversation = activeConversation.value
  if (!conversation) {
    conversation = createConversation()
  }

  addUserMessage(content)
  loading.value = true
  notice.value = ''

  try {
    const result = await chatApi.sendMessage(content)
    addAssistantMessage(result.answer, conversation.id)
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
      <ChatPanel :conversation="activeConversation" :loading="loading" @create="createConversation" />
      <p v-if="notice" class="notice">{{ notice }}</p>
      <MessageComposer :disabled="loading" @send="sendMessage" />
    </main>
  </div>
</template>
