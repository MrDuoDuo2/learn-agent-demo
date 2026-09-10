<script setup lang="ts">
import type { Conversation } from '../types/chat'

defineProps<{
  conversations: Conversation[]
  activeConversationId: string | null
  mobileOpen: boolean
}>()

const emit = defineEmits<{
  create: []
  select: [id: string]
  delete: [id: string]
  close: []
}>()

function formatDate(value: string) {
  return new Intl.DateTimeFormat('zh-CN', { month: 'short', day: 'numeric' }).format(new Date(value))
}
</script>

<template>
  <aside class="sidebar" :class="{ 'sidebar--open': mobileOpen }">
    <div class="sidebar__brand">
      <div class="brand-mark">D1</div>
      <div>
        <strong>Day1</strong>
        <span>&#38382;&#31572;&#24037;&#20316;&#21488;</span>
      </div>
    </div>

    <button class="new-chat-button" type="button" @click="emit('create'); emit('close')">
      <span class="button-icon">+</span>
      &#24320;&#22987;&#26032;&#23545;&#35805;
    </button>

    <div class="sidebar__section-title">
      <span>&#21382;&#21490;&#35760;&#24405;</span>
      <span class="conversation-count">{{ conversations.length }}</span>
    </div>

    <div v-if="conversations.length" class="conversation-list">
      <div
        v-for="conversation in conversations"
        :key="conversation.id"
        class="conversation-item"
        :class="{ 'conversation-item--active': conversation.id === activeConversationId }"
      >
        <button class="conversation-select" type="button" @click="emit('select', conversation.id); emit('close')">
          <span class="conversation-dot" />
          <span class="conversation-copy">
            <strong>{{ conversation.title }}</strong>
            <small>{{ formatDate(conversation.updatedAt) }} &#183; {{ conversation.messages.length }} &#26465;&#28040;&#24687;</small>
          </span>
        </button>
        <button class="icon-button icon-button--danger" type="button" title="&#21024;&#38500;&#23545;&#35805;" @click="emit('delete', conversation.id)">
          &#215;
        </button>
      </div>
    </div>
    <div v-else class="sidebar__empty">
      <span class="empty-symbol">&#9675;</span>
      &#36824;&#27809;&#26377;&#21382;&#21490;&#23545;&#35805;
    </div>

    <div class="sidebar__footer">
      <span class="status-dot" />
      &#26412;&#22320;&#21382;&#21490;&#24050;&#21551;&#29992;
    </div>
  </aside>
</template>
