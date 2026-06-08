<script setup>
import { computed, reactive, ref } from 'vue'
import { Check, ChevronRight, FlaskConical, Info, RotateCcw } from 'lucide-vue-next'

const props = defineProps({
  posts: { type: Array, required: true },
  responses: { type: Array, required: true },
})

const emit = defineEmits(['submit'])
const condition = ref('control')
const claimIndex = ref(0)
const submitted = ref(false)
const ratings = reactive({ credibility: 4, sharing: 4, confidence: 4 })

const studyClaims = computed(() => props.posts.filter((post) => post.accountable).slice(0, 5))
const claim = computed(() => studyClaims.value[claimIndex.value] || props.posts[0])
const labels = {
  credibility: ['Not credible', 'Highly credible'],
  sharing: ['Would not share', 'Would share'],
  confidence: ['Not confident', 'Very confident'],
}

function submitTrial() {
  emit('submit', {
    condition: condition.value,
    postId: claim.value.id,
    claimCategory: claim.value.classification,
    ...ratings,
    createdAt: new Date().toISOString(),
  })
  submitted.value = true
}

function nextTrial() {
  submitted.value = false
  claimIndex.value = (claimIndex.value + 1) % studyClaims.value.length
  condition.value = condition.value === 'control' ? 'experimental' : 'control'
  ratings.credibility = 4
  ratings.sharing = 4
  ratings.confidence = 4
}
</script>

<template>
  <div class="min-h-full bg-ink">
    <header class="border-b border-line bg-panel px-5 py-6">
      <p class="flex items-center gap-2 text-xs font-semibold uppercase tracking-[.16em] text-violet">
        <FlaskConical :size="15" /> Audience study
      </p>
      <h1 class="mt-2 text-2xl font-semibold">Credibility judgment task</h1>
      <p class="mt-2 text-sm leading-5 text-mist">Compare judgments in a normal feed and an adaptive-accountability feed.</p>
      <div class="mt-5 grid grid-cols-2 rounded-xl bg-ink/60 p-1">
        <button class="rounded-lg px-3 py-2 text-xs font-semibold transition" :class="condition === 'control' ? 'bg-white text-ink' : 'text-mist'" @click="condition = 'control'; submitted = false">
          Control condition
        </button>
        <button class="rounded-lg px-3 py-2 text-xs font-semibold transition" :class="condition === 'experimental' ? 'bg-signal text-ink' : 'text-mist'" @click="condition = 'experimental'; submitted = false">
          Experimental
        </button>
      </div>
    </header>

    <div class="p-4">
      <div class="mb-3 flex items-center justify-between text-[11px] text-mist">
        <span>{{ condition === 'control' ? 'Normal social media feed' : 'Adaptive accountability feed' }}</span>
        <span>Trial {{ claimIndex + 1 }} / {{ studyClaims.length }}</span>
      </div>

      <article class="overflow-hidden rounded-2xl border border-line bg-panel">
        <div class="p-4">
          <div class="flex items-center gap-3">
            <div class="grid h-10 w-10 place-items-center rounded-full bg-gradient-to-br text-xs font-bold" :class="claim.avatarTone">{{ claim.initials }}</div>
            <div>
              <p class="text-sm font-semibold">{{ claim.creator }}</p>
              <p class="text-xs text-mist">{{ claim.handle }} · {{ claim.time }}</p>
            </div>
          </div>
          <p class="mt-4 text-[15px] leading-6">{{ claim.text }}</p>
          <div v-if="claim.image" class="mt-4 aspect-[16/8] rounded-xl bg-gradient-to-br" :class="claim.image.tone" />
        </div>

        <div v-if="condition === 'experimental'" class="border-t border-violet/20 bg-violet/[.05] p-4">
          <div class="flex items-start gap-3">
            <Info class="mt-0.5 shrink-0 text-violet" :size="17" />
            <div>
              <div class="flex flex-wrap items-center gap-2">
                <span class="text-xs font-semibold text-violet">{{ claim.classification }}</span>
                <span class="rounded-full border border-violet/20 px-2 py-0.5 text-[9px] text-mist">{{ claim.requests.length }} requests</span>
              </div>
              <p class="mt-2 text-xs leading-5 text-mist">{{ claim.classificationReason }}</p>
              <p v-if="claim.response" class="mt-2 text-xs font-semibold text-signal">Creator responded · Sources attached</p>
              <p v-else class="mt-2 text-xs font-semibold text-violet">Creator invited to provide context</p>
            </div>
          </div>
        </div>
      </article>

      <div v-if="!submitted" class="mt-4 space-y-3">
        <div v-for="key in ['credibility', 'sharing', 'confidence']" :key="key" class="rounded-2xl border border-line bg-panel p-4">
          <div class="flex items-center justify-between">
            <label class="text-sm font-semibold" :for="key">
              {{ key === 'credibility' ? 'How credible is this claim?' : key === 'sharing' ? 'Would you share this?' : 'How confident are you?' }}
            </label>
            <span class="grid h-8 w-8 place-items-center rounded-lg bg-white/5 text-sm font-semibold text-signal">{{ ratings[key] }}</span>
          </div>
          <input :id="key" v-model.number="ratings[key]" type="range" min="1" max="7" step="1" class="mt-4 w-full accent-[#b7f36b]" />
          <div class="mt-1 flex justify-between text-[10px] text-mist">
            <span>{{ labels[key][0] }}</span><span>{{ labels[key][1] }}</span>
          </div>
        </div>

        <button class="w-full rounded-xl bg-white py-3 text-sm font-semibold text-ink hover:bg-signal" @click="submitTrial">
          Submit judgment
        </button>
      </div>

      <div v-else class="mt-4 rounded-2xl border border-signal/20 bg-signal/[.05] p-6 text-center">
        <div class="mx-auto grid h-12 w-12 place-items-center rounded-full bg-signal/10 text-signal"><Check :size="22" /></div>
        <h2 class="mt-3 font-semibold">Trial recorded</h2>
        <p class="mt-1 text-xs text-mist">{{ responses.length }} study responses stored in this browser.</p>
        <button class="mt-5 inline-flex items-center gap-2 rounded-xl bg-signal px-4 py-2.5 text-xs font-semibold text-ink" @click="nextTrial">
          Next condition <ChevronRight :size="15" />
        </button>
      </div>

      <button class="mx-auto mt-5 flex items-center gap-1.5 text-[11px] text-mist hover:text-white" @click="claimIndex = 0; submitted = false">
        <RotateCcw :size="12" /> Restart task
      </button>
    </div>
  </div>
</template>
