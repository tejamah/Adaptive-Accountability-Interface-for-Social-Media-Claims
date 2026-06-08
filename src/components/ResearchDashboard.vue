<script setup>
import { computed } from 'vue'
import {
  BarChart3,
  Clock3,
  FileCheck2,
  FlaskConical,
  MessageSquareText,
  Paperclip,
  Reply,
  Share2,
} from 'lucide-vue-next'
import ModeratorQueue from './ModeratorQueue.vue'
import communityNotesMetrics from '../data/communityNotesMetrics.json'

const props = defineProps({
  posts: { type: Array, required: true },
  studyResponses: { type: Array, required: true },
  reviews: { type: Object, required: true },
})

defineEmits(['review'])

const allRequests = computed(() => props.posts.flatMap((post) => post.requests || []))
const respondedPosts = computed(() => props.posts.filter((post) => post.response))
const attachmentCount = computed(() => respondedPosts.value.reduce((sum, post) => {
  const sources = post.response.sources?.length || (post.response.sourceLink ? 1 : 0)
  const evidence = post.response.documents?.length || (post.response.evidenceNote ? 1 : 0)
  return sum + sources + evidence
}, 0))
const claimsStudied = computed(() => new Set(props.studyResponses.map((response) => response.postId)).size)
const averageSharing = computed(() => {
  if (!props.studyResponses.length) return '—'
  const average = props.studyResponses.reduce((sum, response) => sum + response.sharing, 0) / props.studyResponses.length
  return average.toFixed(1)
})

const metrics = computed(() => [
  { label: 'Claims studied', value: claimsStudied.value, icon: FlaskConical, tone: 'text-violet' },
  { label: 'Requests submitted', value: allRequests.value.length, icon: MessageSquareText, tone: 'text-sky-300' },
  { label: 'Responses received', value: respondedPosts.value.length, icon: Reply, tone: 'text-signal' },
  { label: 'Avg. response time', value: '5h 26m', icon: Clock3, tone: 'text-amber-200' },
  { label: 'Evidence attachments', value: attachmentCount.value, icon: Paperclip, tone: 'text-cyan-300' },
  { label: 'Sharing intention', value: `${averageSharing.value}/7`, icon: Share2, tone: 'text-rose-300' },
])

const requestReasons = computed(() => {
  const groups = [
    { key: 'source', label: 'Source request', color: 'bg-violet' },
    { key: 'evidence', label: 'Evidence request', color: 'bg-sky-400' },
    { key: 'clarification', label: 'Clarification request', color: 'bg-signal' },
    { key: 'classification', label: 'Claim-status request', color: 'bg-amber-300' },
  ]
  return groups.map((group) => {
    const count = allRequests.value.filter((request) => request.type === group.key).length
    return { ...group, count, percent: allRequests.value.length ? Math.round((count / allRequests.value.length) * 100) : 0 }
  })
})

const conditionSummary = computed(() => ['control', 'experimental'].map((condition) => {
  const rows = props.studyResponses.filter((response) => response.condition === condition)
  const average = (key) => rows.length ? (rows.reduce((sum, row) => sum + row[key], 0) / rows.length).toFixed(1) : '—'
  return {
    condition,
    count: rows.length,
    credibility: average('credibility'),
    sharing: average('sharing'),
    confidence: average('confidence'),
  }
}))

const communityNotes = communityNotesMetrics
const statusTotal = communityNotes.statusHistory.totalStatusRecords
const pendingCount = communityNotes.statusHistory.currentStatusCounts.NEEDS_MORE_RATINGS
const pendingPercent = Math.round((pendingCount / statusTotal) * 1000) / 10
const topNoteReasons = Object.entries(communityNotes.notes.reasonCounts).slice(0, 5)
const ratings = communityNotes.ratings
const enrollment = communityNotes.userEnrollment
const helpfulPercent = Math.round((ratings.helpfulnessCounts.HELPFUL / ratings.totalRatings) * 1000) / 10
const notHelpfulPercent = Math.round((ratings.helpfulnessCounts.NOT_HELPFUL / ratings.totalRatings) * 1000) / 10
const earnedInPercent = Math.round((enrollment.enrollmentStateCounts.earnedIn / enrollment.totalParticipants) * 1000) / 10
const topHelpfulReasons = Object.entries(ratings.helpfulReasonCounts).slice(0, 4)
const topNotHelpfulReasons = Object.entries(ratings.notHelpfulReasonCounts).slice(0, 4)
const formatLargeNumber = (value) => new Intl.NumberFormat('en', { notation: 'compact', maximumFractionDigits: 1 }).format(value)
</script>

<template>
  <div class="min-h-full bg-ink">
    <header class="border-b border-line bg-panel px-5 py-6">
      <p class="flex items-center gap-2 text-xs font-semibold uppercase tracking-[.16em] text-sky-400">
        <BarChart3 :size="15" /> Accountability Lab
      </p>
      <h1 class="mt-2 text-2xl font-semibold">Research analytics</h1>
      <p class="mt-2 text-sm leading-5 text-mist">Behavioral and study measures from this local prototype session.</p>
    </header>

    <div class="space-y-4 p-4">
      <section class="grid grid-cols-2 gap-2.5">
        <div v-for="metric in metrics" :key="metric.label" class="rounded-xl border border-line bg-panel p-3">
          <component :is="metric.icon" :size="17" :class="metric.tone" />
          <p class="mt-3 text-xl font-semibold">{{ metric.value }}</p>
          <p class="mt-1 text-[11px] text-mist">{{ metric.label }}</p>
        </div>
      </section>

      <section class="rounded-2xl border border-line bg-panel p-4">
        <h2 class="font-semibold">Why audiences requested context</h2>
        <p class="mt-1 text-xs text-mist">Distribution of request behavior across claim posts.</p>
        <div class="mt-5 space-y-4">
          <div v-for="reason in requestReasons" :key="reason.key">
            <div class="flex justify-between text-xs">
              <span>{{ reason.label }}</span>
              <span class="font-semibold">{{ reason.percent }}%</span>
            </div>
            <div class="mt-2 h-2 overflow-hidden rounded-full bg-ink">
              <div class="h-full rounded-full" :class="reason.color" :style="{ width: `${reason.percent}%` }" />
            </div>
          </div>
        </div>
      </section>

      <section class="overflow-hidden rounded-2xl border border-sky-400/20 bg-sky-400/[.04]">
        <div class="border-b border-sky-400/15 p-4">
          <p class="text-[10px] font-semibold uppercase tracking-[.15em] text-sky-300">Community Notes data snapshot</p>
          <h2 class="mt-2 font-semibold">Real-world participation context</h2>
          <p class="mt-1 text-xs leading-5 text-mist">{{ communityNotes.notes.createdDateRange.start }} to {{ communityNotes.notes.createdDateRange.end }} · aggregate, de-identified data</p>
        </div>
        <div class="grid grid-cols-2 gap-px bg-line/70">
          <div class="bg-panel p-4">
            <p class="text-xl font-semibold">{{ formatLargeNumber(communityNotes.notes.totalNotes) }}</p>
            <p class="mt-1 text-[11px] text-mist">Authored notes</p>
          </div>
          <div class="bg-panel p-4">
            <p class="text-xl font-semibold">{{ formatLargeNumber(statusTotal) }}</p>
            <p class="mt-1 text-[11px] text-mist">Status records</p>
          </div>
          <div class="bg-panel p-4">
            <p class="text-xl font-semibold text-amber-200">{{ pendingPercent }}%</p>
            <p class="mt-1 text-[11px] text-mist">Need more ratings</p>
          </div>
          <div class="bg-panel p-4">
            <p class="text-xl font-semibold text-signal">{{ communityNotes.statusHistory.medianHoursToFirstNonPendingStatus }}h</p>
            <p class="mt-1 text-[11px] text-mist">Median to first non-pending status</p>
          </div>
        </div>
        <div class="p-4">
          <h3 class="text-xs font-semibold">Most frequent authored note reasons</h3>
          <div class="mt-3 space-y-2">
            <div v-for="[reason, count] in topNoteReasons" :key="reason" class="flex items-center justify-between text-xs">
              <span class="text-mist">{{ reason }}</span>
              <span class="font-semibold">{{ formatLargeNumber(count) }}</span>
            </div>
          </div>
          <p class="mt-4 text-[10px] leading-4 text-mist/70">
            Reason flags can overlap. Note classifications and helpfulness statuses describe participant and rating behavior; they are not truth labels for posts.
          </p>
        </div>
      </section>

      <section class="overflow-hidden rounded-2xl border border-violet/20 bg-violet/[.04]">
        <div class="border-b border-violet/15 p-4">
          <p class="text-[10px] font-semibold uppercase tracking-[.15em] text-violet">Rating behavior</p>
          <h2 class="mt-2 font-semibold">{{ formatLargeNumber(ratings.totalRatings) }} note ratings</h2>
          <p class="mt-1 text-xs text-mist">{{ ratings.createdDateRange.start }} to {{ ratings.createdDateRange.end }}</p>
        </div>
        <div class="grid grid-cols-2 gap-px bg-line/70">
          <div class="bg-panel p-4">
            <p class="text-xl font-semibold text-signal">{{ helpfulPercent }}%</p>
            <p class="mt-1 text-[11px] text-mist">Rated helpful</p>
          </div>
          <div class="bg-panel p-4">
            <p class="text-xl font-semibold text-amber-200">{{ notHelpfulPercent }}%</p>
            <p class="mt-1 text-[11px] text-mist">Rated not helpful</p>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-3 p-4">
          <div>
            <h3 class="text-[11px] font-semibold text-signal">Helpful because</h3>
            <div class="mt-3 space-y-2">
              <div v-for="[reason, count] in topHelpfulReasons" :key="reason" class="text-[11px]">
                <p class="text-mist">{{ reason }}</p>
                <p class="font-semibold">{{ formatLargeNumber(count) }}</p>
              </div>
            </div>
          </div>
          <div>
            <h3 class="text-[11px] font-semibold text-amber-200">Not helpful because</h3>
            <div class="mt-3 space-y-2">
              <div v-for="[reason, count] in topNotHelpfulReasons" :key="reason" class="text-[11px]">
                <p class="text-mist">{{ reason }}</p>
                <p class="font-semibold">{{ formatLargeNumber(count) }}</p>
              </div>
            </div>
          </div>
        </div>
        <p class="px-4 pb-4 text-[10px] leading-4 text-mist/70">Reason flags can overlap. Helpfulness measures the note contribution, not the truth of the underlying post.</p>
      </section>

      <section class="rounded-2xl border border-line bg-panel p-4">
        <p class="text-[10px] font-semibold uppercase tracking-[.15em] text-sky-300">Contributor participation</p>
        <div class="mt-3 grid grid-cols-2 gap-2">
          <div class="rounded-xl bg-ink/60 p-3">
            <p class="text-xl font-semibold">{{ formatLargeNumber(enrollment.totalParticipants) }}</p>
            <p class="text-[11px] text-mist">Enrollment records</p>
          </div>
          <div class="rounded-xl bg-ink/60 p-3">
            <p class="text-xl font-semibold text-signal">{{ earnedInPercent }}%</p>
            <p class="text-[11px] text-mist">Currently earned in</p>
          </div>
        </div>
        <div class="mt-4 space-y-2">
          <div v-for="(count, state) in enrollment.enrollmentStateCounts" :key="state" class="flex items-center justify-between text-xs">
            <span class="capitalize text-mist">{{ state.replace(/([A-Z])/g, ' $1') }}</span>
            <span class="font-semibold">{{ formatLargeNumber(count) }}</span>
          </div>
        </div>
        <p class="mt-4 text-[10px] leading-4 text-mist/70">Enrollment states describe contribution eligibility and lifecycle, not participant credibility or reputation.</p>
      </section>

      <section class="rounded-2xl border border-line bg-panel p-4">
        <h2 class="font-semibold">Condition summary</h2>
        <p class="mt-1 text-xs text-mist">Descriptive means from submitted 1–7 judgments.</p>
        <div class="mt-4 grid grid-cols-2 gap-2">
          <div v-for="condition in conditionSummary" :key="condition.condition" class="rounded-xl bg-ink/60 p-3">
            <p class="text-xs font-semibold capitalize" :class="condition.condition === 'experimental' ? 'text-signal' : 'text-white'">{{ condition.condition }}</p>
            <p class="mt-1 text-[10px] text-mist">n = {{ condition.count }}</p>
            <dl class="mt-3 space-y-2 text-xs">
              <div class="flex justify-between"><dt class="text-mist">Credibility</dt><dd>{{ condition.credibility }}</dd></div>
              <div class="flex justify-between"><dt class="text-mist">Sharing</dt><dd>{{ condition.sharing }}</dd></div>
              <div class="flex justify-between"><dt class="text-mist">Confidence</dt><dd>{{ condition.confidence }}</dd></div>
            </dl>
          </div>
        </div>
      </section>

      <section class="rounded-2xl border border-line bg-panel p-4">
        <div class="flex items-center gap-2">
          <FileCheck2 :size="17" class="text-signal" />
          <h2 class="font-semibold">Interpretation boundary</h2>
        </div>
        <p class="mt-2 text-xs leading-5 text-mist">These analytics describe interaction and response behavior. They are not truth, trust, reputation, or credibility scores.</p>
      </section>
    </div>

    <ModeratorQueue :posts="posts" :reviews="reviews" @review="$emit('review', $event)" />
  </div>
</template>
