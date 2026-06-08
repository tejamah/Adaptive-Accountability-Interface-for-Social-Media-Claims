<script setup>
import { BrainCircuit, Gauge, Scale, Share2, Sparkles, Users, WandSparkles } from 'lucide-vue-next'

const metrics = [
  { label: 'Perceived credibility', icon: Sparkles },
  { label: 'Trust judgment', icon: Scale },
  { label: 'Sharing intention', icon: Share2 },
  { label: 'Perceived fairness', icon: Users },
  { label: 'Cognitive load', icon: BrainCircuit },
  { label: 'Creator burden', icon: Gauge },
  { label: 'Willingness to use', icon: WandSparkles },
]

const classifications = ['Personal', 'Opinion', 'Public claim', 'High-impact claim', 'Rumor/news', 'Health / finance / political / AI claim']
</script>

<template>
  <div class="min-h-full bg-ink">
    <header class="relative overflow-hidden border-b border-line bg-panel px-5 py-8">
      <div class="absolute -right-12 -top-16 h-48 w-48 rounded-full bg-violet/10 blur-3xl" />
      <p class="relative text-xs font-semibold uppercase tracking-[.17em] text-violet">Research prototype</p>
      <h1 class="relative mt-2 max-w-sm text-3xl font-semibold leading-tight">Accountability, only when it becomes socially necessary.</h1>
      <p class="relative mt-4 text-sm leading-6 text-mist">
        This prototype explores how accountability mechanisms can be introduced into social media without disrupting normal user behavior. The system does not decide whether a post is true or false. Instead, it makes creator responsiveness, evidence submission, and unresolved context requests visible to audiences.
      </p>
    </header>

    <div class="space-y-4 p-4">
      <section class="rounded-2xl border border-violet/20 bg-violet/[.05] p-5">
        <p class="text-[10px] font-semibold uppercase tracking-[.15em] text-violet">Research question</p>
        <p class="mt-3 text-lg font-medium leading-7">How can adaptive accountability mechanisms help audiences assess social media credibility while minimizing disruption to normal user behavior?</p>
      </section>

      <section class="rounded-2xl border border-signal/20 bg-signal/[.04] p-5">
        <p class="text-[10px] font-semibold uppercase tracking-[.15em] text-signal">HCI positioning</p>
        <h2 class="mt-2 text-lg font-semibold">Participatory accountability</h2>
        <p class="mt-2 text-sm leading-6 text-mist">The interface does not fact-check for audiences. It gives audiences a structured way to ask for context and gives creators a visible way to respond, making accountability a shared social process.</p>
      </section>

      <section class="rounded-2xl border border-line bg-panel p-5">
        <h2 class="font-semibold">Evaluation metrics</h2>
        <div class="mt-4 grid grid-cols-2 gap-2">
          <div v-for="metric in metrics" :key="metric.label" class="flex min-h-20 flex-col justify-between rounded-xl bg-ink/60 p-3">
            <component :is="metric.icon" :size="17" class="text-signal" />
            <span class="mt-3 text-xs text-mist">{{ metric.label }}</span>
          </div>
        </div>
      </section>

      <section class="rounded-2xl border border-line bg-panel p-5">
        <div class="flex items-center gap-2">
          <BrainCircuit :size="19" class="text-violet" />
          <h2 class="font-semibold">AI-assisted content classification suggestion</h2>
        </div>
        <p class="mt-2 text-xs leading-5 text-mist">Non-functional placeholder. Suggestions determine whether accountability controls may be relevant.</p>
        <div class="mt-4 flex flex-wrap gap-2">
          <span v-for="classification in classifications" :key="classification" class="rounded-full border border-line px-2.5 py-1.5 text-[11px] text-mist">
            {{ classification }}
          </span>
        </div>
        <p class="mt-4 border-t border-line pt-3 text-[11px] leading-4 text-mist/70">The classifier must never label content as true, false, fake, or misleading.</p>
      </section>

      <section class="rounded-2xl border border-line p-5 text-sm leading-6 text-mist">
        <h2 class="font-semibold text-white">Prototype limitations</h2>
        <p class="mt-2">Uses mock data, simulated roles, fixed thresholds, and local browser storage. It does not provide authentication, automated classification, source validation, or production moderation.</p>
      </section>
    </div>
  </div>
</template>
