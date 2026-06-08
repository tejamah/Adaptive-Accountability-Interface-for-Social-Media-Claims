<script setup>
import { computed, reactive, ref } from 'vue'
import {
  CheckCircle2,
  Clock3,
  FilePlus2,
  FileUp,
  Link,
  MessageSquareMore,
  Plus,
  Send,
  Trash2,
  X,
} from 'lucide-vue-next'

const props = defineProps({
  posts: { type: Array, required: true },
  creatorId: { type: String, default: 'c1' },
})

const emit = defineEmits(['respond'])
const activePost = ref(null)
const responseTypes = ['Personal Experience', 'Opinion', 'Official Source', 'Supporting Evidence', 'Correction']
const form = reactive({
  responseType: 'Official Source',
  explanation: '',
  sources: [{ title: '', url: '' }],
  documents: [],
  documentName: '',
  evidenceNote: '',
})

const creatorPosts = computed(() => props.posts.filter((post) => post.creatorId === props.creatorId))
const pending = computed(() => creatorPosts.value.filter((post) => post.requests.length && !post.response))
const responded = computed(() => creatorPosts.value.filter((post) => post.response))

function typeBreakdown(post) {
  const counts = post.requests.reduce((acc, request) => {
    acc[request.type] = (acc[request.type] || 0) + 1
    return acc
  }, {})
  return Object.entries(counts).sort((a, b) => b[1] - a[1])
}

function commonQuestion(post) {
  return post.requests.find((request) => request.question)?.question || 'No written clarification question.'
}

function openResponse(post) {
  activePost.value = post
  form.responseType = 'Official Source'
  form.explanation = ''
  form.sources = [{ title: '', url: '' }]
  form.documents = []
  form.documentName = ''
  form.evidenceNote = ''
}

function addSource() {
  form.sources.push({ title: '', url: '' })
}

function removeSource(index) {
  form.sources.splice(index, 1)
}

function addDocument() {
  const name = form.documentName.trim()
  if (!name) return
  form.documents.push({ name, type: 'Supporting document' })
  form.documentName = ''
}

function publish() {
  const sources = form.sources.filter((source) => source.url.trim())
  emit('respond', activePost.value.id, {
    responseType: form.responseType,
    explanation: form.explanation,
    sources,
    documents: [...form.documents],
    sourceLink: sources[0]?.url || '',
    evidenceNote: form.evidenceNote,
    label: form.responseType,
  })
  activePost.value = null
}
</script>

<template>
  <div class="min-h-full bg-ink">
    <header class="border-b border-line bg-panel px-5 pb-5 pt-6">
      <p class="text-xs font-semibold uppercase tracking-[.16em] text-signal">Creator view</p>
      <h1 class="mt-1 text-2xl font-semibold">Response center</h1>
      <p class="mt-2 text-sm text-mist">Context requests for posts by Avery Rao.</p>
      <div class="mt-5 grid grid-cols-3 gap-2">
        <div class="rounded-xl border border-line bg-ink/40 p-3">
          <p class="text-xl font-semibold">{{ creatorPosts.length }}</p>
          <p class="mt-1 text-[10px] uppercase tracking-wide text-mist">Claims</p>
        </div>
        <div class="rounded-xl border border-violet/20 bg-violet/[.05] p-3">
          <p class="text-xl font-semibold text-violet">{{ pending.length }}</p>
          <p class="mt-1 text-[10px] uppercase tracking-wide text-mist">Pending</p>
        </div>
        <div class="rounded-xl border border-signal/20 bg-signal/[.05] p-3">
          <p class="text-xl font-semibold text-signal">{{ responded.length }}</p>
          <p class="mt-1 text-[10px] uppercase tracking-wide text-mist">Answered</p>
        </div>
      </div>
    </header>

    <div class="space-y-3 p-4">
      <div v-if="!pending.length" class="rounded-2xl border border-line bg-panel p-8 text-center">
        <CheckCircle2 class="mx-auto text-signal" :size="30" />
        <p class="mt-3 font-semibold">All caught up</p>
        <p class="mt-1 text-sm text-mist">There are no pending context requests.</p>
      </div>

      <article v-for="post in pending" :key="post.id" class="rounded-2xl border border-line bg-panel p-4">
        <div class="flex items-start justify-between gap-3">
          <div>
            <span class="rounded-full bg-violet/10 px-2 py-1 text-[10px] font-semibold uppercase tracking-wide text-violet">
              {{ post.classification }}
            </span>
            <p class="mt-3 text-[15px] leading-6">{{ post.text }}</p>
          </div>
          <span class="shrink-0 rounded-lg bg-white/5 px-2.5 py-1.5 text-sm font-semibold">{{ post.requests.length }}</span>
        </div>

        <div class="mt-4 flex flex-wrap gap-1.5">
          <span v-for="[type, count] in typeBreakdown(post)" :key="type" class="rounded-full border border-line px-2 py-1 text-[10px] capitalize text-mist">
            {{ type }} · {{ count }}
          </span>
        </div>

        <div class="mt-4 rounded-xl bg-ink/50 p-3">
          <p class="flex items-center gap-1.5 text-[10px] font-semibold uppercase tracking-[.12em] text-mist">
            <MessageSquareMore :size="13" /> Common clarification
          </p>
          <p class="mt-2 text-xs leading-5 text-[#d7dae0]">“{{ commonQuestion(post) }}”</p>
        </div>

        <button class="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-white py-2.5 text-sm font-semibold text-ink hover:bg-signal" @click="openResponse(post)">
          Respond with context <Send :size="15" />
        </button>
      </article>

      <section v-if="responded.length" class="pt-4">
        <h2 class="px-1 text-sm font-semibold">Published responses</h2>
        <div v-for="post in responded" :key="post.id" class="mt-3 rounded-xl border border-line bg-panel p-4">
          <div class="flex gap-3">
            <CheckCircle2 class="mt-0.5 shrink-0 text-signal" :size="18" />
            <div class="min-w-0 flex-1">
              <p class="line-clamp-2 text-sm leading-5">{{ post.text }}</p>
              <p class="mt-2 text-xs text-mist">{{ post.response.responseType || post.response.label }} · {{ post.requests.length }} requests</p>
              <div class="mt-3 flex flex-wrap gap-2 text-[10px] text-mist">
                <span class="rounded-full border border-line px-2 py-1">Sources attached: {{ post.response.sources?.length || (post.response.sourceLink ? 1 : 0) }}</span>
                <span class="rounded-full border border-line px-2 py-1">Evidence attached: {{ post.response.documents?.length || (post.response.evidenceNote ? 1 : 0) }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <Teleport to="body">
      <Transition name="fade">
        <div v-if="activePost" class="fixed inset-0 z-50 flex items-end justify-center bg-black/70 backdrop-blur-sm sm:items-center" @click.self="activePost = null">
          <Transition name="sheet" appear>
            <form class="safe-bottom max-h-[92vh] w-full max-w-[580px] overflow-y-auto rounded-t-[28px] border border-line bg-panel p-5 sm:rounded-[28px]" @submit.prevent="publish">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-xs font-semibold uppercase tracking-[.15em] text-signal">Add context</p>
                  <h2 class="mt-1 text-xl font-semibold">Creator response</h2>
                </div>
                <button type="button" class="rounded-full bg-white/5 p-2 text-mist" @click="activePost = null"><X :size="19" /></button>
              </div>
              <p class="mt-4 rounded-xl bg-ink/50 p-3 text-sm leading-5 text-mist">{{ activePost.text }}</p>

              <fieldset class="mt-5">
                <legend class="text-xs font-medium text-mist">Response type</legend>
                <div class="mt-2 grid grid-cols-2 gap-2">
                  <label
                    v-for="type in responseTypes"
                    :key="type"
                    class="flex cursor-pointer items-center gap-2 rounded-xl border p-3 text-xs transition"
                    :class="form.responseType === type ? 'border-signal/50 bg-signal/[.06] text-white' : 'border-line text-mist'"
                  >
                    <input v-model="form.responseType" type="radio" :value="type" class="accent-[#b7f36b]" />
                    {{ type }}
                  </label>
                </div>
              </fieldset>

              <label class="mt-5 block text-xs font-medium text-mist">Creator response</label>
              <textarea v-model="form.explanation" required rows="4" placeholder="Clarify what you meant and what is known…" class="mt-2 w-full resize-none rounded-xl border border-line bg-ink/60 p-3 text-sm outline-none focus:border-signal" />

              <div class="mt-5 flex items-center justify-between">
                <label class="text-xs font-medium text-mist"><Link class="mr-1 inline" :size="13" /> Source section</label>
                <button type="button" class="flex items-center gap-1 text-[11px] font-semibold text-signal" @click="addSource"><Plus :size="13" /> Add source</button>
              </div>
              <div v-for="(source, index) in form.sources" :key="index" class="mt-2 rounded-xl border border-line bg-ink/40 p-3">
                <div class="flex gap-2">
                  <input v-model="source.title" type="text" placeholder="Source title" class="min-w-0 flex-1 rounded-lg border border-line bg-ink/60 px-3 py-2 text-xs outline-none focus:border-signal" />
                  <button v-if="form.sources.length > 1" type="button" class="text-mist hover:text-rose-300" @click="removeSource(index)"><Trash2 :size="15" /></button>
                </div>
                <input v-model="source.url" type="url" placeholder="Source URL" class="mt-2 w-full rounded-lg border border-line bg-ink/60 px-3 py-2 text-xs outline-none focus:border-signal" />
              </div>

              <label class="mt-5 block text-xs font-medium text-mist"><FileUp class="mr-1 inline" :size="13" /> Supporting document</label>
              <div class="mt-2 flex gap-2">
                <input v-model="form.documentName" type="text" placeholder="Document name (demo)" class="min-w-0 flex-1 rounded-xl border border-line bg-ink/60 p-3 text-xs outline-none focus:border-signal" @keyup.enter.prevent="addDocument" />
                <button type="button" class="rounded-xl border border-line px-3 text-mist hover:text-white" @click="addDocument"><FilePlus2 :size="17" /></button>
              </div>
              <div v-if="form.documents.length" class="mt-2 space-y-2">
                <div v-for="(document, index) in form.documents" :key="document.name" class="flex items-center justify-between rounded-lg bg-ink/50 px-3 py-2 text-xs">
                  <span class="truncate">{{ document.name }}</span>
                  <button type="button" class="text-mist hover:text-rose-300" @click="form.documents.splice(index, 1)"><X :size="14" /></button>
                </div>
              </div>

              <label class="mt-5 block text-xs font-medium text-mist">Additional notes</label>
              <textarea v-model="form.evidenceNote" rows="3" placeholder="Describe supporting evidence, limitations, or corrections…" class="mt-2 w-full resize-none rounded-xl border border-line bg-ink/60 p-3 text-sm outline-none focus:border-signal" />

              <button class="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-signal py-3 text-sm font-semibold text-ink disabled:opacity-40" :disabled="!form.explanation.trim()">
                Publish response <Send :size="15" />
              </button>
              <p class="mt-3 flex items-center justify-center gap-1 text-[11px] text-mist"><Clock3 :size="12" /> Response time is recorded for research metrics.</p>
            </form>
          </Transition>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>
