<script setup>
import {
  Activity,
  Bookmark,
  Camera,
  Clapperboard,
  Heart,
  Landmark,
  MessageCircle,
  MoreHorizontal,
  Repeat2,
  Send,
  Sparkles,
} from 'lucide-vue-next'
import { REQUEST_THRESHOLD } from '../data/mockPosts'

const props = defineProps({
  post: { type: Object, required: true },
  currentUserId: { type: String, required: true },
})

defineEmits(['request', 'context', 'report'])

const imageIcons = { activity: Activity, camera: Camera, clapperboard: Clapperboard, landmark: Landmark, sparkles: Sparkles }

const formatCount = (count) => count >= 1000 ? `${(count / 1000).toFixed(count >= 10000 ? 0 : 1)}k` : count
const hasRequested = () => props.post.requests.some((request) => request.userId === props.currentUserId)
const isPublic = () => props.post.requests.length >= REQUEST_THRESHOLD
</script>

<template>
  <article class="border-b border-line bg-panel px-4 py-5">
    <header class="flex items-start gap-3">
      <div
        class="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-gradient-to-br text-xs font-bold text-white"
        :class="post.avatarTone"
      >
        {{ post.initials }}
      </div>
      <div class="min-w-0 flex-1">
        <div class="flex items-center gap-1.5">
          <span class="truncate text-[15px] font-semibold">{{ post.creator }}</span>
          <span class="truncate text-sm text-mist">{{ post.handle }}</span>
          <span class="text-mist">·</span>
          <span class="shrink-0 text-sm text-mist">{{ post.time }}</span>
        </div>
        <div class="mt-0.5 flex items-center gap-2">
          <span class="text-[11px] font-medium uppercase tracking-[.13em] text-mist">{{ post.category }}</span>
          <span v-if="post.opinion" class="rounded-full bg-violet/10 px-2 py-0.5 text-[10px] font-semibold text-violet">
            Opinion
          </span>
        </div>
      </div>
      <button class="rounded-full p-1 text-mist transition hover:bg-white/5 hover:text-white" aria-label="More options">
        <MoreHorizontal :size="20" />
      </button>
    </header>

    <p class="mt-3 text-[15px] leading-6 text-[#f0f1f3]">{{ post.text }}</p>

    <div
      v-if="post.image"
      class="relative mt-4 flex aspect-[16/9] items-end overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br p-4"
      :class="post.image.tone"
    >
      <div class="absolute inset-0 opacity-30" style="background-image: radial-gradient(circle at 75% 25%, white 0, transparent 1px); background-size: 22px 22px" />
      <component :is="imageIcons[post.image.icon]" class="absolute right-5 top-5 text-white/40" :size="42" :stroke-width="1.2" />
      <span class="relative rounded-full border border-white/15 bg-black/30 px-3 py-1 text-xs font-medium backdrop-blur">
        {{ post.image.label }}
      </span>
    </div>

    <div
      v-if="post.accountable && (isPublic() || post.response)"
      class="mt-4 flex items-center justify-between rounded-xl border px-3 py-2.5"
      :class="post.response ? 'border-signal/20 bg-signal/[.06]' : 'border-violet/20 bg-violet/[.06]'"
    >
      <div class="flex items-center gap-2.5">
        <span class="relative flex h-2.5 w-2.5">
          <span class="absolute inline-flex h-full w-full animate-ping rounded-full opacity-30" :class="post.response ? 'bg-signal' : 'bg-violet'" />
          <span class="relative inline-flex h-2.5 w-2.5 rounded-full" :class="post.response ? 'bg-signal' : 'bg-violet'" />
        </span>
        <div>
          <p class="text-xs font-semibold" :class="post.response ? 'text-signal' : 'text-violet'">
            {{ post.response ? 'Creator responded' : 'Context requested' }}
          </p>
          <p class="text-[11px] text-mist">{{ post.requests.length }} community requests</p>
        </div>
      </div>
      <button class="text-xs font-semibold text-white hover:underline" @click="$emit('context', post)">
        View context
      </button>
    </div>

    <div class="mt-4 flex items-center justify-between text-mist">
      <div class="flex items-center gap-5">
        <button class="flex items-center gap-1.5 transition hover:text-rose-400" aria-label="Like">
          <Heart :size="19" /> <span class="text-xs">{{ formatCount(post.likes) }}</span>
        </button>
        <button class="flex items-center gap-1.5 transition hover:text-sky-400" aria-label="Comment">
          <MessageCircle :size="19" /> <span class="text-xs">{{ formatCount(post.comments) }}</span>
        </button>
        <button class="flex items-center gap-1.5 transition hover:text-signal" aria-label="Repost">
          <Repeat2 :size="19" /> <span class="text-xs">{{ formatCount(post.shares) }}</span>
        </button>
        <button class="transition hover:text-white" aria-label="Share"><Send :size="18" /></button>
      </div>
      <button class="transition hover:text-white" aria-label="Bookmark"><Bookmark :size="18" /></button>
    </div>

    <div v-if="post.accountable && !post.response" class="mt-4 flex items-center justify-between border-t border-line/70 pt-3">
      <button
        class="text-xs font-semibold transition"
        :class="hasRequested() ? 'cursor-default text-signal' : 'text-mist hover:text-white'"
        :disabled="hasRequested()"
        @click="$emit('request', post)"
      >
        {{ hasRequested() ? 'Context request sent' : 'Request context' }}
      </button>
      <button class="text-[11px] text-mist/70 transition hover:text-mist" @click="$emit('report', post)">
        Report misuse
      </button>
    </div>
  </article>
</template>
