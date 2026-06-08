<script setup>
import { computed } from 'vue'
import { CheckCircle2, Clock3, ExternalLink, FileCheck2, History, MessageSquareWarning, Reply } from 'lucide-vue-next'

const props = defineProps({
  posts: { type: Array, required: true },
  creatorId: { type: String, default: 'c1' },
})

const creatorPosts = computed(() => props.posts.filter((post) => post.creatorId === props.creatorId))
const requestTotal = computed(() => creatorPosts.value.reduce((sum, post) => sum + post.requests.length, 0))
const responses = computed(() => creatorPosts.value.filter((post) => post.response).length)
const requestedPosts = computed(() => creatorPosts.value.filter((post) => post.requests.length))
const responseRate = computed(() => requestedPosts.value.length ? Math.round((responses.value / requestedPosts.value.length) * 100) : 0)
const unresolved = computed(() => requestedPosts.value.length - responses.value)
const evidenceCount = computed(() => creatorPosts.value.filter((post) => post.response?.sourceLink || post.response?.evidenceNote).length)
const claimsClarified = computed(() => creatorPosts.value.filter((post) => post.response).length)
const sourcesProvided = computed(() => creatorPosts.value.reduce((sum, post) => sum + (post.response?.sources?.length || (post.response?.sourceLink ? 1 : 0)), 0))
const evidenceSubmitted = computed(() => creatorPosts.value.reduce((sum, post) => sum + (post.response?.documents?.length || (post.response?.evidenceNote ? 1 : 0)), 0))

const metrics = computed(() => [
  { label: 'Requests received', value: requestTotal.value, icon: MessageSquareWarning, tone: 'text-violet' },
  { label: 'Responses provided', value: responses.value, icon: Reply, tone: 'text-signal' },
  { label: 'Response rate', value: `${responseRate.value}%`, icon: CheckCircle2, tone: 'text-signal' },
  { label: 'Avg. response time', value: '5h 26m', icon: Clock3, tone: 'text-sky-400' },
  { label: 'Open requests', value: unresolved.value, icon: History, tone: 'text-amber-300' },
  { label: 'Claims clarified', value: claimsClarified.value, icon: CheckCircle2, tone: 'text-signal' },
  { label: 'Evidence submitted', value: evidenceSubmitted.value, icon: FileCheck2, tone: 'text-cyan-300' },
  { label: 'Sources provided', value: sourcesProvided.value, icon: ExternalLink, tone: 'text-sky-300' },
])
</script>

<template>
  <div class="min-h-full bg-ink">
    <header class="border-b border-line bg-panel px-5 py-6">
      <p class="text-xs font-semibold uppercase tracking-[.16em] text-violet">Public profile</p>
      <div class="mt-4 flex items-center gap-4">
        <div class="grid h-16 w-16 place-items-center rounded-full bg-gradient-to-br from-violet-400 to-indigo-600 text-lg font-bold">AR</div>
        <div>
          <h1 class="text-xl font-semibold">Avery Rao</h1>
          <p class="text-sm text-mist">@averyreports</p>
          <span class="mt-2 inline-block rounded-full border border-line px-2 py-1 text-[10px] text-mist">Public affairs writer</span>
        </div>
      </div>
    </header>

    <section class="p-4">
      <div class="rounded-2xl border border-line bg-panel p-4">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="font-semibold">Accountability history</h2>
            <p class="mt-1 text-xs text-mist">Behavior over the last 90 days</p>
          </div>
          <History class="text-mist" :size="21" />
        </div>
        <div class="mt-4 grid grid-cols-2 gap-2.5">
          <div v-for="metric in metrics" :key="metric.label" class="rounded-xl border border-line bg-ink/50 p-3">
            <component :is="metric.icon" :size="17" :class="metric.tone" />
            <p class="mt-3 text-xl font-semibold">{{ metric.value }}</p>
            <p class="mt-1 text-[11px] text-mist">{{ metric.label }}</p>
          </div>
        </div>
      </div>

      <div class="mt-4 rounded-2xl border border-line bg-panel p-4">
        <h2 class="text-sm font-semibold">Recent accountability activity</h2>
        <div v-for="post in requestedPosts" :key="post.id" class="mt-4 border-l pl-3" :class="post.response ? 'border-signal' : 'border-violet'">
          <div class="flex items-center gap-2">
            <span class="text-xs font-semibold" :class="post.response ? 'text-signal' : 'text-violet'">
              {{ post.response ? 'Responded' : 'Creator invited' }}
            </span>
            <span class="text-[10px] text-mist">· {{ post.requests.length }} requests</span>
          </div>
          <p class="mt-1 line-clamp-2 text-xs leading-5 text-mist">{{ post.text }}</p>
        </div>
      </div>

      <div class="mt-4 rounded-2xl border border-signal/20 bg-signal/[.04] p-4">
        <p class="text-[10px] font-semibold uppercase tracking-[.14em] text-signal">Behavioral accountability</p>
        <div class="mt-3 flex items-end justify-between">
          <div>
            <p class="text-2xl font-semibold">{{ responses }} / {{ requestedPosts.length }}</p>
            <p class="text-xs text-mist">Context requests resolved</p>
          </div>
          <div class="text-right">
            <p class="text-2xl font-semibold">{{ responseRate }}%</p>
            <p class="text-xs text-mist">Response consistency</p>
          </div>
        </div>
        <div class="mt-4 h-1.5 overflow-hidden rounded-full bg-line">
          <div class="h-full rounded-full bg-signal" :style="{ width: `${responseRate}%` }" />
        </div>
      </div>

      <p class="px-3 py-5 text-center text-[11px] leading-4 text-mist/70">
        This history reflects responsiveness and evidence sharing. It is not a truth or trust score.
      </p>
    </section>
  </div>
</template>
