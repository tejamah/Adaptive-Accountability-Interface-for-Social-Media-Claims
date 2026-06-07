<script setup>
import { computed } from 'vue'
import { ExternalLink, FileText, MessageSquareQuote, Users, X } from 'lucide-vue-next'

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
                “{{ post?.text }}”
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

              <section class="mt-6">
                <div class="flex items-center gap-2 text-sm font-semibold">
                  <MessageSquareQuote :size="17" class="text-violet" />
                  Community clarification summary
                </div>
                <p class="mt-2 text-sm leading-6 text-mist">{{ summary }}</p>
              </section>

              <section v-if="post?.response" class="mt-6 overflow-hidden rounded-2xl border border-signal/20 bg-signal/[.04]">
                <div class="border-b border-signal/15 px-4 py-3">
                  <div class="flex items-center justify-between">
                    <p class="text-sm font-semibold text-signal">Creator response</p>
                    <span class="rounded-full bg-signal/10 px-2 py-1 text-[10px] font-semibold text-signal">
                      {{ post.response.label }}
                    </span>
                  </div>
                  <p class="mt-1 text-[11px] text-mist">{{ timestamp }}</p>
                </div>
                <div class="space-y-4 p-4">
                  <p class="text-sm leading-6">{{ post.response.explanation }}</p>
                  <div v-if="post.response.evidenceNote">
                    <p class="text-[10px] font-semibold uppercase tracking-[.14em] text-mist">Evidence note</p>
                    <p class="mt-1 text-sm leading-5 text-mist">{{ post.response.evidenceNote }}</p>
                  </div>
                  <a
                    v-if="post.response.sourceLink"
                    :href="post.response.sourceLink"
                    target="_blank"
                    rel="noopener"
                    class="inline-flex items-center gap-1.5 text-xs font-semibold text-signal hover:underline"
                  >
                    Open source <ExternalLink :size="13" />
                  </a>
                </div>
              </section>

              <section v-else class="mt-6 rounded-2xl border border-violet/20 bg-violet/[.04] p-4">
                <p class="text-sm font-semibold text-violet">Awaiting creator response</p>
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
