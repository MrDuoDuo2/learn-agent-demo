<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import type { Conversation, ConversationMode } from '../types/chat'

const props = defineProps<{
  conversation?: Conversation
  loading?: boolean
}>()

const emit = defineEmits<{
  create: []
  'set-mode': [mode: ConversationMode]
}>()

const messageList = ref<HTMLElement>()

function scrollToBottom() {
  nextTick(() => {
    if (messageList.value) messageList.value.scrollTop = messageList.value.scrollHeight
  })
}

function formatTime(value: string) {
  return new Intl.DateTimeFormat('zh-CN', { hour: '2-digit', minute: '2-digit' }).format(new Date(value))
}

function avatarLabel(role: Conversation['messages'][number]['role']) {
  return role === 'user' ? '\u4f60' : 'D1'
}

function authorLabel(role: Conversation['messages'][number]['role']) {
  return role === 'user' ? '\u6211' : 'Day1'
}

function connectionLabel(mode?: ConversationMode) {
  return mode === 'search' ? '\u641c\u7d22 API' : 'API \u6a21\u5f0f'
}

watch(() => props.conversation?.messages.length, scrollToBottom)
</script>

<template>
  <section class="chat-panel">
    <header class="chat-header">
      <div>
        <span class="eyebrow">CONVERSATION</span>
        <h1>{{ conversation?.title || '\u5f00\u59cb\u4e00\u6b21\u65b0\u7684\u95ee\u7b54' }}</h1>
      </div>
      <div class="chat-header__actions">
        <div class="mode-switch" role="group" aria-label="&#23545;&#35805;&#27169;&#24335;">
          <button
            type="button"
            :class="{ 'mode-switch__button--active': conversation?.mode === 'chat' }"
            :disabled="!conversation || Boolean(conversation.messages.length)"
            @click="emit('set-mode', 'chat')"
          >
            &#38382;&#31572;
          </button>
          <button
            type="button"
            :class="{ 'mode-switch__button--active': conversation?.mode === 'search' }"
            :disabled="!conversation || Boolean(conversation.messages.length)"
            @click="emit('set-mode', 'search')"
          >
            &#25628;&#32034;
          </button>
        </div>
        <div class="connection-status"><span class="status-dot" /> {{ connectionLabel(conversation?.mode) }}</div>
      </div>
    </header>

    <div ref="messageList" class="message-list">
      <div v-if="!conversation" class="chat-empty">
        <div class="empty-orbit">?</div>
        <h2>&#20174;&#19968;&#20010;&#38382;&#39064;&#24320;&#22987;</h2>
        <p>&#21019;&#24314;&#26032;&#23545;&#35805;&#65292;&#35760;&#24405;&#20320;&#30340;&#24605;&#32771;&#19982;&#31572;&#26696;&#12290;</p>
        <button class="empty-action" type="button" @click="emit('create')">&#24320;&#22987;&#26032;&#23545;&#35805;</button>
      </div>
      <div v-else-if="!conversation.messages.length" class="chat-empty">
        <div class="empty-orbit empty-orbit--small">&#10022;</div>
        <h2>&#20934;&#22791;&#22909;&#20102;&#21527;&#65311;</h2>
        <p>&#22312;&#19979;&#26041;&#36755;&#20837;&#20320;&#30340;&#31532;&#19968;&#20010;&#38382;&#39064;&#12290;</p>
      </div>
      <div v-else class="messages">
        <div v-for="message in conversation.messages" :key="message.id" class="message-row" :class="`message-row--${message.role}`">
          <div class="message-avatar">{{ avatarLabel(message.role) }}</div>
          <div class="message-content">
            <div class="message-meta">
              <strong>{{ authorLabel(message.role) }}</strong>
              <time>{{ formatTime(message.createdAt) }}</time>
            </div>
            <div v-if="message.kind === 'search'" class="search-results">
              <a
                v-for="(result, index) in message.searchResults"
                :key="`${message.id}-${result.href}-${index}`"
                class="search-result"
                :href="result.href"
                target="_blank"
                rel="noreferrer"
              >
                <span class="search-result__index">{{ String(index + 1).padStart(2, '0') }}</span>
                <span class="search-result__body">
                  <strong>{{ result.title || result.href }}</strong>
                  <span v-if="result.body">{{ result.body }}</span>
                  <small>{{ result.href }}</small>
                </span>
                <span class="search-result__arrow">&#8599;</span>
              </a>
              <p v-if="!message.searchResults?.length" class="search-result__empty">{{ message.content }}</p>
            </div>
            <p v-else>{{ message.content }}</p>
          </div>
        </div>
      </div>
      <div v-if="loading" class="loading-row">
        <span /><span /><span /> &#27491;&#22312;&#25972;&#29702;&#22238;&#31572;...
      </div>
    </div>
  </section>
</template>
