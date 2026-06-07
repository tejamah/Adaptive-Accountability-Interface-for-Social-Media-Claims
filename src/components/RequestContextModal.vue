<script setup>
import { computed, ref, watch } from 'vue'
import { AlertTriangle, Check, FileQuestion, Link, MessageSquareText, Scale, X } from 'lucide-vue-next'

const props = defineProps({
  post: { type: Object, default: null },
  open: { type: Boolean, default: false },
})

const emit = defineEmits(['close', 'submit'])

const requestTypes = [
  { id: 'source', label: 'Ask for source', icon: Link },
  { id: 'clarification', label: 'Ask for clarification', icon: MessageSquareText },
  { id: 'evidence', label: 'Ask for evidence', icon: FileQuestion },
  { id: 'classification', label: 'Opinion, rumor, or confirmed?', icon: Scale },
]

const selected = ref('source')
const question = ref('')
const submitted = ref(false)

const isSerious = computed(() => props.post?.serious)

watch(() => props.open, (open) => {
  if (open) {
    selected.value = 'source'
    question.value = ''
    submitted.value = false
  }
})

function submit() {
  emit('submit', { type: selected.value, question: question.value.trim() })
  submitted.value = true
  setTimeout(() => emit('close'), 850)
}
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="open" class="fixed inset-0 z-50 flex items-end justify-center bg-black/70 backdrop-blur-sm sm:items-center" @click.self="emit('close')">
        <Transition name="sheet" appear>
          <section class="safe-bottom w-full max-w-[580px] rounded-t-[28px] border border-line bg-[#11141b] p-5 shadow-2xl sm:rounded-[28px]">
            <div class="mx-auto mb-4 h-1 w-10 rounded-full bg-white/20 sm:hidden" />
            <div v-if="submitted" class="grid min-h-[360px] place-items-center text-center">
              <div>
                <div class="mx-auto grid h-14 w-14 place-items-center rounded-full bg-signal/10 text-signal">
                  <Check :size="26" />
                </div>
                <h2 class="mt-4 text-xl font-semibold">Request recorded</h2>
                <p class="mt-2 max-w-xs text-sm leading-5 text-mist">
                  It stays private until enough people independently request context.
                </p>
              </div>
            </div>

            <template v-else>
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-xs font-semibold uppercase tracking-[.15em] text-violet">Accountability</p>
                  <h2 class="mt-1 text-xl font-semibold">Request context</h2>
                </div>
                <button class="rounded-full bg-white/5 p-2 text-mist hover:text-white" @click="emit('close')">
                  <X :size="19" />
                </button>
              </div>

              <blockquote class="mt-4 line-clamp-2 border-l-2 border-violet/60 pl-3 text-sm leading-5 text-mist">
                {{ post?.text }}
              </blockquote>

              <div v-if="isSerious" class="mt-4 flex gap-2.5 rounded-xl border border-amber-400/20 bg-amber-400/[.06] p-3 text-amber-200">
                <AlertTriangle class="mt-0.5 shrink-0" :size="17" />
                <p class="text-xs leading-5">This request may involve a personal or legal allegation. Ask for context without repeating an unverified accusation.</p>
              </div>

              <div class="mt-5 grid grid-cols-2 gap-2">
                <button
                  v-for="type in requestTypes"
                  :key="type.id"
                  class="flex min-h-16 items-center gap-2.5 rounded-xl border px-3 text-left text-xs font-medium transition"
                  :class="selected === type.id ? 'border-violet bg-violet/10 text-white' : 'border-line text-mist hover:border-white/20'"
                  @click="selected = type.id"
                >
                  <component :is="type.icon" :size="17" class="shrink-0" />
                  {{ type.label }}
                </button>
              </div>

              <label class="mt-5 block text-xs font-medium text-mist" for="clarification">
                What should the creator clarify?
              </label>
              <textarea
                id="clarification"
                v-model="question"
                rows="3"
                maxlength="240"
                placeholder="Add a specific, respectful question…"
                class="mt-2 w-full resize-none rounded-xl border border-line bg-ink/60 px-3.5 py-3 text-sm outline-none transition placeholder:text-mist/50 focus:border-violet"
              />
              <div class="mt-1 flex justify-between text-[10px] text-mist/60">
                <span>Visible to the creator</span>
                <span>{{ question.length }}/240</span>
              </div>

              <button
                class="mt-5 w-full rounded-xl bg-white py-3 text-sm font-semibold text-ink transition hover:bg-signal disabled:cursor-not-allowed disabled:opacity-40"
                :disabled="!question.trim()"
                @click="submit"
              >
                Submit context request
              </button>
              <p class="mt-3 text-center text-[11px] leading-4 text-mist/70">
                Requests are not votes on whether a claim is true or false.
              </p>
            </template>
          </section>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>
