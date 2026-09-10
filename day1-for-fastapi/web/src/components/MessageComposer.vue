<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ disabled?: boolean }>()
const emit = defineEmits<{ send: [content: string] }>()
const draft = ref('')

function send() {
  const content = draft.value.trim()
  if (!content) return
  emit('send', content)
  draft.value = ''
}
</script>

<template>
  <form class="composer" @submit.prevent="send">
    <textarea
      v-model="draft"
      rows="1"
      placeholder="&#36755;&#20837;&#20320;&#30340;&#38382;&#39064;..."
      :disabled="disabled"
      @keydown.enter.exact.prevent="send"
    />
    <div class="composer__bottom">
      <span>Enter &#21457;&#36865; &#183; Shift + Enter &#25442;&#34892;</span>
      <button class="send-button" type="submit" :disabled="disabled || !draft.trim()" title="&#21457;&#36865;&#38382;&#39064;">&#21457;&#36865; <span>&#8599;</span></button>
    </div>
  </form>
</template>
