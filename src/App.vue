<script setup>
import { computed, ref } from 'vue'
import {
  Bell,
  BarChart3,
  FlaskConical,
  Home,
  RotateCcw,
  Search,
  Shield,
  UserRound,
} from 'lucide-vue-next'
import AccountabilityHistory from './components/AccountabilityHistory.vue'
import ContextDrawer from './components/ContextDrawer.vue'
import CreatorDashboard from './components/CreatorDashboard.vue'
import ExperimentStudy from './components/ExperimentStudy.vue'
import PostCard from './components/PostCard.vue'
import ResearchDashboard from './components/ResearchDashboard.vue'
import RequestContextModal from './components/RequestContextModal.vue'
import { demoUser } from './data/mockPosts'
import {
  loadPosts,
  loadReviews,
  loadStudyResponses,
  resetDemo,
  savePosts,
  saveReviews,
  saveStudyResponses,
} from './services/storage'

const posts = ref(loadPosts())
const reviews = ref(loadReviews())
const studyResponses = ref(loadStudyResponses())
const activeView = ref('feed')
const selectedPost = ref(null)
const requestOpen = ref(false)
const contextOpen = ref(false)
const toast = ref('')

const views = [
  { id: 'feed', label: 'Feed', icon: Home },
  { id: 'study', label: 'Study', icon: FlaskConical },
  { id: 'creator', label: 'Creator', icon: UserRound },
  { id: 'history', label: 'History', icon: Shield },
  { id: 'lab', label: 'Lab', icon: BarChart3 },
]

const viewTitle = computed(() => views.find((view) => view.id === activeView.value)?.label)

function showToast(message) {
  toast.value = message
  setTimeout(() => {
    if (toast.value === message) toast.value = ''
  }, 2600)
}

function openRequest(post) {
  selectedPost.value = post
  requestOpen.value = true
}

function openContext(post) {
  selectedPost.value = post
  contextOpen.value = true
}

function submitRequest(payload) {
  const post = posts.value.find((item) => item.id === selectedPost.value.id)
  if (!post || post.requests.some((request) => request.userId === demoUser.id)) return
  post.requests.push({
    userId: demoUser.id,
    type: payload.type,
    question: payload.question,
    createdAt: new Date().toISOString(),
  })
  savePosts(posts.value)
}

function publishResponse(postId, response) {
  const post = posts.value.find((item) => item.id === postId)
  if (!post) return
  post.response = { ...response, createdAt: new Date().toISOString() }
  savePosts(posts.value)
  showToast('Context response published')
}

function submitStudyResponse(response) {
  studyResponses.value = [...studyResponses.value, response]
  saveStudyResponses(studyResponses.value)
  showToast('Study judgment recorded')
}

function reportMisuse(post) {
  post.reports ||= []
  if (!post.reports.some((report) => report.userId === demoUser.id)) {
    post.reports.push({
      userId: demoUser.id,
      type: 'misuse',
      note: 'Submitted by an audience participant for observer review.',
      reviewed: false,
    })
    savePosts(posts.value)
    showToast('Sent to the research observer queue')
  } else {
    showToast('You already reported this request')
  }
}

function markReviewed(postId) {
  reviews.value = { ...reviews.value, [postId]: new Date().toISOString() }
  saveReviews(reviews.value)
  showToast('Marked as reviewed')
}

function reset() {
  resetDemo()
  posts.value = loadPosts()
  reviews.value = loadReviews()
  studyResponses.value = loadStudyResponses()
  activeView.value = 'feed'
  showToast('Demo data reset')
}
</script>

<template>
  <div class="min-h-screen sm:px-6 sm:py-8">
    <main class="relative mx-auto min-h-screen max-w-[580px] overflow-hidden bg-ink shadow-phone sm:min-h-[calc(100vh-4rem)] sm:rounded-[32px] sm:border sm:border-line">
      <div class="h-[100dvh] overflow-y-auto pb-[76px] sm:h-[calc(100vh-4rem)]">
        <template v-if="activeView === 'feed'">
          <header class="sticky top-0 z-20 border-b border-line bg-ink/90 px-4 pb-3 pt-4 backdrop-blur-xl">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2.5">
                <div class="grid h-9 w-9 place-items-center rounded-xl bg-signal text-sm font-black text-ink">C</div>
                <div>
                  <p class="text-base font-semibold leading-none">Context</p>
                  <p class="mt-1 text-[10px] uppercase tracking-[.14em] text-mist">Social research space</p>
                </div>
              </div>
              <div class="flex items-center gap-1">
                <button class="rounded-full p-2 text-mist hover:bg-white/5 hover:text-white" aria-label="Search"><Search :size="20" /></button>
                <button class="relative rounded-full p-2 text-mist hover:bg-white/5 hover:text-white" aria-label="Notifications">
                  <Bell :size="20" />
                  <span class="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-signal" />
                </button>
              </div>
            </div>
            <div class="mt-4 flex items-center justify-between">
              <h1 class="text-xl font-semibold">For you</h1>
              <button class="flex items-center gap-1.5 text-[11px] text-mist hover:text-white" @click="reset">
                <RotateCcw :size="12" /> Reset demo
              </button>
            </div>
          </header>

          <section>
            <PostCard
              v-for="post in posts"
              :key="post.id"
              :post="post"
              :current-user-id="demoUser.id"
              @request="openRequest"
              @context="openContext"
              @report="reportMisuse"
            />
          </section>
        </template>

        <ExperimentStudy v-else-if="activeView === 'study'" :posts="posts" :responses="studyResponses" @submit="submitStudyResponse" />
        <CreatorDashboard v-else-if="activeView === 'creator'" :posts="posts" @respond="publishResponse" />
        <AccountabilityHistory v-else-if="activeView === 'history'" :posts="posts" />
        <ResearchDashboard v-else-if="activeView === 'lab'" :posts="posts" :study-responses="studyResponses" :reviews="reviews" @review="markReviewed" />
      </div>

      <nav class="safe-bottom absolute bottom-0 left-0 right-0 z-30 grid grid-cols-5 border-t border-line bg-[#0b0e13]/95 px-1 pt-2 backdrop-blur-xl">
        <button
          v-for="view in views"
          :key="view.id"
          class="flex flex-col items-center gap-1 py-1 text-[9px] font-medium transition"
          :class="activeView === view.id ? 'text-signal' : 'text-mist hover:text-white'"
          :aria-label="view.label"
          @click="activeView = view.id"
        >
          <component :is="view.icon" :size="19" :stroke-width="activeView === view.id ? 2.4 : 1.8" />
          {{ view.label }}
        </button>
      </nav>

      <Transition name="fade">
        <div v-if="toast" class="absolute bottom-24 left-1/2 z-40 -translate-x-1/2 whitespace-nowrap rounded-full border border-white/10 bg-[#242935] px-4 py-2 text-xs font-medium shadow-xl">
          {{ toast }}
        </div>
      </Transition>
    </main>

    <RequestContextModal
      :post="selectedPost"
      :open="requestOpen"
      @close="requestOpen = false"
      @submit="submitRequest"
    />
    <ContextDrawer
      :post="selectedPost"
      :open="contextOpen"
      @close="contextOpen = false"
    />
  </div>
</template>
