<script setup>
import { computed } from 'vue'
import {
  Check,
  CircleHelp,
  Clock3,
  ExternalLink,
  FileCheck2,
  FileText,
  MessageSquareQuote,
  Users,
  X,
} from 'lucide-vue-next'

const props = defineProps({
  post: { type: Object, default: null },
  open: { type: Boolean, default: false },
})

defineEmits(['close'])

const summary = computed(() => {
  if (!props.post?.requests?.length) return ''
  const counts = props.post.requests.reduce((result, request) => {
    result[request.type] = (result[request.type] || 0) + 1
    return result
  }, {})
  const top = Object.entries(counts).sort((a, b) => b[1] - a[1])[0]?.[0]
  const labels = {
    source: 'Community members most often asked for the original source.',
    clarification: 'Community members most often asked for clarification and scope.',
    evidence: 'Community members most often asked for supporting evidence.',
    classification: 'Community members most often asked whether this was opinion, rumor, or confirmed.',
  }
  return labels[top]
})

const timestamp = computed(() => {
  if (!props.post?.response?.createdAt) return null
  return new Intl.DateTimeFormat('en', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(props.post.response.createdAt))
})

const lastUpdated = computed(() => {
  if (!props.post?.response?.createdAt) return null
  const hours = Math.max(1, Math.round((Date.now() - new Date(props.post.response.createdAt).getTime()) / 36e5))
  return hours < 24 ? `${hours}h ago` : `${Math.round(hours / 24)}d ago`
})

const sources = computed(() => {
  const attached = props.post?.response?.sources || []
  if (attached.length) return attached
  return props.post?.response?.sourceLink ? [{ title: 'Creator source', url: props.post.response.sourceLink }] : []
})

const documents = computed(() => props.post?.response?.documents || [])
const evidenceCount = computed(() => documents.value.length || (props.post?.response?.evidenceNote ? 1 : 0))

const classificationReason = computed(() => {
  if (props.post?.classificationReason) return props.post.classificationReason
  const reasons = {
    'AI claim': 'Makes a claim about an AI system that audiences may want supported with technical or documentary context.',
    'political claim': 'States a public-affairs claim that audiences may want to trace to an official record.',
    'rumor/news': 'Contains a report that is not presented as officially confirmed in the post.',
    'health claim': 'Makes a health-related claim that may influence personal decisions.',
    'high-impact claim': 'Contains a serious claim that may create legal, safety, or reputational harm.',
  }
  return reasons[props.post?.classification] || 'The post makes a public claim for which additional context may help audiences interpret it.'
})

const timeline = computed(() => [
  {
    label: `${props.post?.requests.length || 0} users requested context`,
    detail: 'Independent requests were recorded.',
    complete: true,
  },
  {
    label: 'Threshold reached',
    detail: 'The context request became publicly visible.',
    complete: true,
  },
  {
    label: 'Creator notified',
    detail: 'The creator was invited to add context.',
    complete: true,
  },
  {
    label: props.post?.response ? 'Creator response submitted' : 'Creator invited to provide context',
    detail: props.post?.response ? 'A response was published by the creator.' : 'No response has been published yet.',
    complete: Boolean(props.post?.response),
  },
  {
    label: props.post?.response ? 'Public context updated' : 'Public context not updated yet',
    detail: props.post?.response ? 'Audience members can now review the response, sources, and evidence notes.' : 'This step appears after a creator response is published.',
    complete: Boolean(props.post?.response),
  },
])
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="open" class="fixed inset-0 z-50 flex justify-end bg-black/70 backdrop-blur-sm" @click.self="$emit('close')">
        <Transition name="sheet" appear>
          <section class="safe-bottom h-full w-full max-w-[580px] overflow-y-auto border-l border-line bg-[#0d1016]">
            <header class="sticky top-0 z-10 flex items-center justify-between border-b border-line bg-[#0d1016]/95 px-5 py-4 backdrop-blur">
              <div>
                <p class="text-xs font-semibold uppercase tracking-[.15em] text-signal">Available context</p>
                <h2 class="mt-1 text-lg font-semibold">Accountability details</h2>
              </div>
              <button class="rounded-full bg-white/5 p-2 text-mist hover:text-white" @click="$emit('close')">
                <X :size="19" />
              </button>
            </header>

            <div class="p-5">
              <blockquote class="rounded-2xl border border-line bg-panel p-4 text-[15px] leading-6">
                "{{ post?.text }}"
                <footer class="mt-3 text-xs text-mist">{{ post?.creator }} · {{ post?.category }}</footer>
              </blockquote>

              <div class="mt-5 grid grid-cols-2 gap-3">
                <div class="rounded-xl border border-line bg-panel p-3">
                  <Users :size="18" class="text-violet" />
                  <p class="mt-3 text-xl font-semibold">{{ post?.requests.length }}</p>
                  <p class="text-xs text-mist">Context requests</p>
                </div>
                <div class="rounded-xl border border-line bg-panel p-3">
                  <FileText :size="18" class="text-violet" />
                  <p class="mt-3 text-sm font-semibold capitalize">{{ post?.classification }}</p>
                  <p class="text-xs text-mist">Claim type</p>
                </div>
              </div>

              <section class="mt-4 rounded-xl border border-line bg-panel p-4">
                <div class="flex items-center gap-2 text-xs font-semibold">
                  <CircleHelp :size="15" class="text-violet" />
                  Why this classification?
                </div>
                <p class="mt-2 text-xs leading-5 text-mist">{{ classificationReason }}</p>
                <p class="mt-2 text-[10px] leading-4 text-mist/60">This suggestion identifies the kind of context that may be useful. It is not a verdict on the claim.</p>
              </section>

              <section class="mt-6">
                <div class="flex items-center gap-2 text-sm font-semibold">
                  <MessageSquareQuote :size="17" class="text-violet" />
                  Community clarification summary
                </div>
                <p class="mt-2 text-sm leading-6 text-mist">{{ summary }}</p>
              </section>

              <section class="mt-6">
                <h3 class="text-sm font-semibold">Context timeline</h3>
                <div class="mt-4">
                  <div v-for="(event, index) in timeline" :key="event.label" class="relative flex gap-3 pb-5 last:pb-0">
                    <div v-if="index < timeline.length - 1" class="absolute left-[11px] top-6 h-[calc(100%-12px)] w-px" :class="event.complete ? 'bg-violet/40' : 'bg-line'" />
                    <span class="relative z-10 grid h-6 w-6 shrink-0 place-items-center rounded-full border" :class="event.complete ? 'border-violet/40 bg-violet/10 text-violet' : 'border-line bg-panel text-mist'">
                      <Check v-if="event.complete" :size="13" />
                      <Clock3 v-else :size="12" />
                    </span>
                    <div>
                      <p class="text-xs font-semibold" :class="event.complete ? 'text-white' : 'text-mist'">{{ event.label }}</p>
                      <p class="mt-1 text-[11px] leading-4 text-mist">{{ event.detail }}</p>
                    </div>
                  </div>
                </div>
              </section>

              <section v-if="post?.response" class="mt-6 overflow-hidden rounded-2xl border border-signal/20 bg-signal/[.04]">
                <div class="border-b border-signal/15 px-4 py-3">
                  <div class="flex items-center justify-between gap-3">
                    <p class="text-sm font-semibold text-signal">Creator Responded</p>
                    <span class="rounded-full bg-signal/10 px-2 py-1 text-[10px] font-semibold text-signal">
                      {{ post.response.responseType || post.response.label }}
                    </span>
                  </div>
                  <p class="mt-1 text-[11px] text-mist">Last updated: {{ lastUpdated }} · {{ timestamp }}</p>
                  <div class="mt-3 grid grid-cols-2 gap-2">
                    <div class="rounded-lg border border-signal/15 bg-ink/40 p-2">
                      <p class="text-lg font-semibold">{{ sources.length }}</p>
                      <p class="text-[10px] text-mist">Sources attached</p>
                    </div>
                    <div class="rounded-lg border border-signal/15 bg-ink/40 p-2">
                      <p class="text-lg font-semibold">{{ evidenceCount }}</p>
                      <p class="text-[10px] text-mist">Evidence attached</p>
                    </div>
                  </div>
                </div>
                <div class="space-y-4 p-4">
                  <p class="text-sm leading-6">{{ post.response.explanation }}</p>

                  <div v-if="sources.length">
                    <p class="text-[10px] font-semibold uppercase tracking-[.14em] text-mist">Sources</p>
                    <div class="mt-2 space-y-2">
                      <a v-for="source in sources" :key="source.url" :href="source.url" target="_blank" rel="noopener" class="flex items-center justify-between rounded-xl border border-line bg-ink/40 px-3 py-2 text-xs text-signal hover:border-signal/30">
                        <span class="truncate">{{ source.title || source.url }}</span>
                        <ExternalLink class="shrink-0" :size="13" />
                      </a>
                    </div>
                  </div>

                  <div v-if="documents.length">
                    <p class="text-[10px] font-semibold uppercase tracking-[.14em] text-mist">Supporting documents</p>
                    <div class="mt-2 space-y-2">
                      <div v-for="document in documents" :key="document.name" class="flex items-center gap-2 rounded-xl border border-line bg-ink/40 px-3 py-2 text-xs">
                        <FileCheck2 :size="14" class="text-signal" />
                        <span class="truncate">{{ document.name }}</span>
                      </div>
                    </div>
                  </div>

                  <div v-if="post.response.evidenceNote">
                    <p class="text-[10px] font-semibold uppercase tracking-[.14em] text-mist">Additional notes</p>
                    <p class="mt-1 text-sm leading-5 text-mist">{{ post.response.evidenceNote }}</p>
                  </div>
                </div>
              </section>

              <section v-else class="mt-6 rounded-2xl border border-violet/20 bg-violet/[.04] p-4">
                <p class="text-sm font-semibold text-violet">Creator invited to provide context</p>
                <p class="mt-1 text-sm leading-5 text-mist">The request threshold has been reached and the creator has been invited to add context.</p>
              </section>

              <div class="mt-7 rounded-xl border border-line p-4 text-xs leading-5 text-mist">
                This system does not determine whether the claim is true or false. It shows accountability behavior and available context.
              </div>
            </div>
          </section>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>
