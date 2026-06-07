<script setup>
import { computed } from 'vue'
import { AlertCircle, Check, Eye, Flag, ShieldCheck } from 'lucide-vue-next'

const props = defineProps({
  posts: { type: Array, required: true },
  reviews: { type: Object, required: true },
})

defineEmits(['review'])

const queue = computed(() => props.posts
  .filter((post) => post.serious || post.reports?.length || (post.accountable && post.requests.length >= 5 && !post.response))
  .map((post) => ({
    ...post,
    reason: post.reports?.length
      ? 'Misuse report'
      : post.serious
        ? 'High-impact claim'
        : 'Unresolved request',
  })))

const reviewedCount = computed(() => queue.value.filter((item) => props.reviews[item.id]).length)
</script>

<template>
  <div class="min-h-full bg-ink">
    <header class="border-b border-line bg-panel px-5 py-6">
      <p class="text-xs font-semibold uppercase tracking-[.16em] text-sky-400">Research observer</p>
      <h1 class="mt-1 text-2xl font-semibold">Review queue</h1>
      <p class="mt-2 text-sm leading-5 text-mist">Observe edge cases and potential misuse. Review does not remove or suppress content.</p>
      <div class="mt-5 flex gap-2">
        <span class="rounded-full bg-amber-400/10 px-3 py-1.5 text-xs font-medium text-amber-200">{{ queue.length - reviewedCount }} open</span>
        <span class="rounded-full bg-signal/10 px-3 py-1.5 text-xs font-medium text-signal">{{ reviewedCount }} reviewed</span>
      </div>
    </header>

    <div class="space-y-3 p-4">
      <article v-for="item in queue" :key="item.id" class="rounded-2xl border bg-panel p-4" :class="reviews[item.id] ? 'border-signal/20 opacity-70' : 'border-line'">
        <div class="flex items-center justify-between">
          <span class="flex items-center gap-1.5 rounded-full px-2 py-1 text-[10px] font-semibold uppercase tracking-wide"
            :class="item.reason === 'Misuse report' ? 'bg-rose-400/10 text-rose-300' : 'bg-amber-400/10 text-amber-200'">
            <Flag v-if="item.reason === 'Misuse report'" :size="11" />
            <AlertCircle v-else :size="11" />
            {{ item.reason }}
          </span>
          <span class="text-[10px] text-mist">{{ item.classification }}</span>
        </div>
        <p class="mt-3 text-sm leading-5">{{ item.text }}</p>
        <div class="mt-3 flex gap-4 text-[11px] text-mist">
          <span>{{ item.requests.length }} requests</span>
          <span>{{ item.reports?.length || 0 }} reports</span>
          <span>{{ item.response ? 'Responded' : 'Unresolved' }}</span>
        </div>
        <div v-if="item.reports?.[0]?.note" class="mt-3 rounded-lg bg-rose-400/[.05] p-2.5 text-xs text-rose-200/80">
          Report note: {{ item.reports[0].note }}
        </div>
        <button
          class="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border py-2.5 text-xs font-semibold transition"
          :class="reviews[item.id] ? 'border-signal/20 text-signal' : 'border-line text-mist hover:border-white/20 hover:text-white'"
          :disabled="reviews[item.id]"
          @click="$emit('review', item.id)"
        >
          <Check v-if="reviews[item.id]" :size="14" />
          <Eye v-else :size="14" />
          {{ reviews[item.id] ? 'Reviewed' : 'Mark as reviewed' }}
        </button>
      </article>

      <div class="flex gap-3 rounded-xl border border-sky-400/15 bg-sky-400/[.04] p-4 text-sky-100/80">
        <ShieldCheck class="shrink-0" :size="19" />
        <p class="text-xs leading-5">This queue supports research observation and abuse prevention. It is not a censorship or content-ranking tool.</p>
      </div>
    </div>
  </div>
</template>
