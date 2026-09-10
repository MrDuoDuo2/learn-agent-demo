# Local Chat UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Vue chat page that stores user-only messages and conversation history in browser local storage.

**Architecture:** A Vite-hosted Vue 3 application will keep the chat domain logic in a small composable and persist one `ChatStore` object under a namespaced `localStorage` key. Stateless sidebar, panel, and composer components will receive data via props and emit user actions to `App.vue`.

**Tech Stack:** Vue 3, Vite, TypeScript, Vitest, Vue Test Utils, CSS.

**Spec:** `day1-for-fastapi/doc/chat-ui-design.md`

## Global Constraints

- Create all frontend files under `day1-for-fastapi/web/`.
- Do not call or modify `day1-for-fastapi/backend/`.
- Persist only messages with `role: 'user'`; do not generate assistant responses.
- Use browser `localStorage` only; no external state library or remote API.
- Support desktop and narrow-screen layouts without obscuring the message composer.

---

## File Structure

- `web/package.json`: Vite commands and frontend dependencies.
- `web/index.html`: application HTML entry point.
- `web/src/main.ts`: mounts Vue application.
- `web/src/App.vue`: connects chat state to presentational components.
- `web/src/types/chat.ts`: `Message`, `Conversation`, and `ChatStore` interfaces.
- `web/src/composables/useChatStore.ts`: state creation, validation, persistence, and conversation operations.
- `web/src/components/ConversationSidebar.vue`: session list and controls.
- `web/src/components/ChatPanel.vue`: header, messages, and empty state.
- `web/src/components/MessageComposer.vue`: keyboard-aware message input.
- `web/src/styles.css`: responsive application styles.
- `web/src/composables/useChatStore.spec.ts`: domain and persistence unit tests.
- `web/src/components/MessageComposer.spec.ts`: composer interaction test.

### Task 1: Scaffold the Vue application and define chat types

**Files:**
- Create: `day1-for-fastapi/web/package.json`
- Create: `day1-for-fastapi/web/index.html`
- Create: `day1-for-fastapi/web/tsconfig.json`
- Create: `day1-for-fastapi/web/vite.config.ts`
- Create: `day1-for-fastapi/web/src/main.ts`
- Create: `day1-for-fastapi/web/src/types/chat.ts`

**Interfaces:**
- Produces: `Message`, `Conversation`, and `ChatStore` types for all UI and state modules.

- [ ] **Step 1: Write the type definitions**

```ts
export type Message = {
  id: string
  role: 'user'
  content: string
  createdAt: string
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
```

- [ ] **Step 2: Add Vite, Vue, TypeScript, Vitest, and Vue Test Utils configuration**

```json
{
  "dependencies": {
    "vue": "^3.5.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.2.0",
    "@vue/test-utils": "^2.4.6",
    "typescript": "^5.7.0",
    "vite": "^6.0.0",
    "vitest": "^2.1.0",
    "vue-tsc": "^2.2.0"
  },
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc --noEmit && vite build",
    "test": "vitest run"
  }
}
```

- [ ] **Step 3: Run the type-checking build**

Run: `npm run build`

Expected: the empty application compiles with exit code 0.

### Task 2: Implement and test persistent conversation state

**Files:**
- Create: `day1-for-fastapi/web/src/composables/useChatStore.ts`
- Create: `day1-for-fastapi/web/src/composables/useChatStore.spec.ts`

**Interfaces:**
- Consumes: `Message`, `Conversation`, `ChatStore` from `src/types/chat.ts`.
- Produces: `useChatStore()` with `conversations`, `activeConversationId`, `activeConversation`, `createConversation()`, `selectConversation(id)`, `deleteConversation(id)`, and `addUserMessage(content)`.

- [ ] **Step 1: Write failing state tests**

```ts
it('adds only a user message and persists it', () => {
  const chat = useChatStore()
  chat.createConversation()
  chat.addUserMessage('hello')

  expect(chat.activeConversation.value?.messages).toMatchObject([
    { role: 'user', content: 'hello' },
  ])
  expect(localStorage.getItem('day1-chat-store')).toContain('hello')
})

it('loads an empty store when local storage is invalid', () => {
  localStorage.setItem('day1-chat-store', '{bad json')
  expect(useChatStore().conversations.value).toEqual([])
})
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `npm test -- useChatStore.spec.ts`

Expected: FAIL because `useChatStore` does not exist.

- [ ] **Step 3: Implement the composable**

```ts
export function useChatStore() {
  const state = ref<ChatStore>(readStoredState())
  const save = () => localStorage.setItem(STORAGE_KEY, JSON.stringify(state.value))

  const addUserMessage = (content: string) => {
    const trimmed = content.trim()
    if (!trimmed || !activeConversation.value) return
    const now = new Date().toISOString()
    const message: Message = {
      id: crypto.randomUUID(),
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

  return { conversations, activeConversationId, activeConversation, createConversation, selectConversation, deleteConversation, addUserMessage }
}
```

- [ ] **Step 4: Run the state tests**

Run: `npm test -- useChatStore.spec.ts`

Expected: PASS; invalid storage falls back to an empty store, and only user messages are saved.

### Task 3: Build the presentational conversation components

**Files:**
- Create: `day1-for-fastapi/web/src/components/ConversationSidebar.vue`
- Create: `day1-for-fastapi/web/src/components/ChatPanel.vue`
- Create: `day1-for-fastapi/web/src/components/MessageComposer.vue`
- Create: `day1-for-fastapi/web/src/components/MessageComposer.spec.ts`

**Interfaces:**
- Consumes: `Conversation` and `Message` types from `src/types/chat.ts`.
- Produces: sidebar events `create`, `select(id)`, `delete(id)` and composer event `send(content)`.

- [ ] **Step 1: Write a failing composer test**

```ts
it('emits trimmed content for Enter and leaves Shift+Enter for a newline', async () => {
  const wrapper = mount(MessageComposer)
  const textarea = wrapper.get('textarea')
  await textarea.setValue(' hello ')
  await textarea.trigger('keydown', { key: 'Enter' })

  expect(wrapper.emitted('send')).toEqual([['hello']])
})
```

- [ ] **Step 2: Run the composer test to confirm it fails**

Run: `npm test -- MessageComposer.spec.ts`

Expected: FAIL because `MessageComposer.vue` does not exist.

- [ ] **Step 3: Implement the three components**

```vue
<textarea
  v-model="draft"
  @keydown.enter.exact.prevent="send"
  @keydown.enter.shift.stop
/>
```

`ConversationSidebar` renders conversations ordered by `updatedAt` and uses button controls for new and delete actions. `ChatPanel` shows a distinct empty state when no conversation is selected or when its message list is empty. `MessageComposer` trims and emits non-empty drafts only.

- [ ] **Step 4: Run the component test**

Run: `npm test -- MessageComposer.spec.ts`

Expected: PASS; Enter emits trimmed content and Shift+Enter does not emit.

### Task 4: Compose the page, make it responsive, and verify it

**Files:**
- Create: `day1-for-fastapi/web/src/App.vue`
- Create: `day1-for-fastapi/web/src/styles.css`
- Modify: `day1-for-fastapi/web/src/main.ts`

**Interfaces:**
- Consumes: the store composable and the three component event contracts.
- Produces: a single responsive chat application mounted at `#app`.

- [ ] **Step 1: Connect state to the UI**

```vue
<ConversationSidebar
  :conversations="conversations"
  :active-conversation-id="activeConversationId"
  @create="createConversation"
  @select="selectConversation"
  @delete="deleteConversation"
/>
<ChatPanel :conversation="activeConversation" />
<MessageComposer @send="addUserMessage" />
```

- [ ] **Step 2: Add stable responsive layout rules**

```css
.app-shell { min-height: 100dvh; display: grid; grid-template-columns: 17rem minmax(0, 1fr); }
.chat-panel { min-height: 0; display: grid; grid-template-rows: auto minmax(0, 1fr) auto; }
@media (max-width: 720px) { .app-shell { grid-template-columns: 1fr; } }
```

- [ ] **Step 3: Run the full automated suite and build**

Run: `npm test && npm run build`

Expected: all tests pass and Vite writes a production bundle to `web/dist/`.

- [ ] **Step 4: Manually verify the browser workflow**

Run: `npm run dev -- --host 127.0.0.1`

Expected: creating a conversation, sending one message, refreshing the browser, switching conversations, and deleting the current conversation all work without an assistant response.
