<script setup lang="ts">
//import state from '../stats.json'
import type { CheckboxGroupItem } from '@nuxt/ui'

const config = useRuntimeConfig()

const isDrawerOpen = ref(false)

/* const { data } = useFetch('api/draws/', {
     key:'get-draws',
  method: 'GET',
    baseURL: config.public.BASE_URL
}) */

/* const { execute } = useFetch('api/draws/bulk', {
    key:'post-draws',
    method: 'POST',
    baseURL: config.public.BASE_URL,
    body: state
}) */
/* const { execute } = useFetch('api/draws/generate', {
    key:'post-draws-generate',
    method: 'POST',
    baseURL: config.public.BASE_URL,
    body: {}
}) */

/*
const { data: weights, execute: execWeights } = useFetch('api/draws/weights', {
    key: 'get-draws-weights',
    method: 'GET',
    baseURL: config.public.BASE_URL
}) */
type generationMode = 'score' | 'weight' | 'percentage' | 'random'

const lotteryConfig = ref({
    start_date: '1976-01-01',
    end_date: '2025-09-01',
    shouldBalanceEvenOdd: true,
    favorEven: 60, // 60–40%

    shouldBalanceHighLow: true,
    favorHigh: 50, // 50%

    shouldAvoidLogicalSequences: true,
    sequenceTolerance: 2, // 2 consecutive numbers are acceptable

    shouldAvoidRoundNumbers: true,
    roundNumberTolerance: 2, // Max 2 round numbers per grid

    includeNumbers: [],
    excludeNumbers: [],
    shouldCheckExistence: true,
    shouldEvaluateScore: true,
    shouldEvaluatePercentage: false,
    shouldEvaluateWeight: false,
    shouldGenerateLucky: true, // weighted selection by past frequency
    favorLucky: 1,
    excludeLucky: [],
    gridsToGenerate: 1,
    numbersToGenerate: 5,
    includedSources: ['loto', 'super', 'grand']
})

const { data: dgenerate, execute: execGenerate } = useFetch('api/draws/generate', {
    key: 'post-draws-generate',
    baseURL: config.public.BASE_URL,
    method: 'POST',
    immediate: false,
    watch: false,
    body: lotteryConfig
    /* transform: (dgenerate) =>
        dgenerate.map((it) => ({
            ...it,
            numbers: Array.isArray(it.numbers) ? it.numbers.join('-') : it.numbers
        })) */
})

function execute() {
    isDrawerOpen.value = false
    execGenerate()
}

onMounted(() => {
    /*  execFrequency()
    execWeights()
    execGenerate() */
    // execute()
})

const numbers = ref<CheckboxGroupItem[]>(Array.from({ length: 49 }, (_, i) => i + 1))
const luckNumbers = ref<CheckboxGroupItem[]>(Array.from({ length: 10 }, (_, i) => i + 1))

const result = computed(() => dgenerate.value ?? [])
/* const first = computed(() => result.value?.[0]?.numbers.split('-') ?? [])
const firstLucky = computed(() => result.value?.[0]?.lucky_number.toString() ?? '') */
const visibleItems = ref(new Set())

const animateResults = async () => {
    visibleItems.value.clear()

    for (let lineIndex = 0; lineIndex < result.value.length; lineIndex++) {
        // Animer les numéros de la ligne
        for (let numIndex = 0; numIndex < result.value[lineIndex].numbers.length; numIndex++) {
            await new Promise((resolve) => setTimeout(resolve, 50))
            visibleItems.value.add(`${lineIndex}-${numIndex}`)
        }

        // Animer le numéro chance
        await new Promise((resolve) => setTimeout(resolve, 50))
        visibleItems.value.add(`${lineIndex}-lucky`)

        await new Promise((resolve) => setTimeout(resolve, 100))
        visibleItems.value.add(`${lineIndex}-info`)

        // Pause avant la ligne suivante
        if (lineIndex < result.value.length - 1) {
            await new Promise((resolve) => setTimeout(resolve, 100))
        }
    }
}

// Déclencher après le fetch
watch(
    () => result.value,
    () => {
        if (result.value.length > 0) {
            animateResults()
        }
    },
    { immediate: true }
)
</script>

<template>
    <div class="inline-flex">
        <div class="border-t-2 flex flex-row h-auto">
            <aside class="bg-slate-50 h-full w-96 border-slate-200 border-r">
                <LotoForm v-model="lotteryConfig" @on-submit="execute()" />
            </aside>
            <div class="size-full mx-auto p-4 sm:p-6 lg:p-8 flex flex-col flex-1">
                <div
                    class="relative size-full flex flex-col flex-1 border-slate-200 border rounded-lg gap-4 p-4"
                >
                    <div class="flex justify-center items-center flex-col gap-4">
                        <p>
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam adipisci
                            quaerat ut!
                        </p>
                        <UPopover>
                            <UButton
                                label="Récapitulatif"
                                color="neutral"
                                variant="subtle"
                                :ui="{ base: 'w-fit' }"
                            />
                            <template #content>
                                <LotoConfigTable :lottery-config="lotteryConfig" />
                            </template>
                        </UPopover>
                        <UButton
                            size="xl"
                            label="GENERER"
                            :ui="{ base: 'w-fit' }"
                            @click="execute()"
                        />
                    </div>
                    <h3
                        v-if="result?.length > 0"
                        class="text-pretty tracking-tight font-bold text-2xl mb-2 bg-gradient-to-r from-cyan-600 to-error bg-clip-text text-transparent"
                    >
                        Résultat(s)
                    </h3>
                    <div
                        v-for="(
                            { numbers, lucky_number, score, total_draws_used }, lineIndex
                        ) in result"
                        :key="lineIndex"
                        class="flex flex-row gap-4"
                    >
                        <UCheckbox
                            v-for="(num, numIndex) in numbers"
                            :key="`${lineIndex}-${num}`"
                            v-show="visibleItems.has(`${lineIndex}-${numIndex}`)"
                            class="fade-in"
                            indicator="hidden"
                            variant="card"
                            :label="String(num)"
                            :ui="{
                                root: 'size-14 bg-primary-600 rounded-full',
                                base: 'justify-center flex bg-black-200',
                                wrapper: 'h-full',
                                label: 'justify-center items-center h-full flex text-white text-xl'
                            }"
                        />

                        <UCheckbox
                            v-show="visibleItems.has(`${lineIndex}-lucky`)"
                            class="fade-in"
                            indicator="hidden"
                            variant="card"
                            :label="String(lucky_number)"
                            :ui="{
                                root: 'size-14 bg-error rounded-full',
                                base: 'justify-center flex bg-black-200',
                                wrapper: 'h-full',
                                label: 'justify-center items-center h-full flex text-white text-xl'
                            }"
                        />
                        <ul
                            v-show="visibleItems.has(`${lineIndex}-info`)"
                            class="text-xs flex flex-col justify-center text-black-600"
                        >
                            <li><b>Tirage :</b> {{ numbers.join(' ') }} {{ lucky_number }}</li>
                            <li><b>Score:</b> {{ score }}</li>
                            <li>
                                Calculé sur <b>{{ total_draws_used }}</b> tirages
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!--   <div class="h-screen pt-20">
        <div
            class="w-full max-w-(--ui-container) mx-auto px-4 sm:px-6 lg:px-8 flex flex-col lg:grid gap-16 sm:gap-y-24 lg:items-center !pb-20 py-24 sm:py-32 lg:py-40"
        >

            <div class="flex flex-col gap-4 w-4xl mx-auto">
                <section class="justify-center flex flex-col items-center gap-4">
                    <h2 class="text-xl text-black-700">1. Premiere etape</h2>
                    <UDrawer
                        v-model:open="isDrawerOpen"
                        direction="right"
                        title="don't delete me"
                        description="don't delete me"
                        :handle="false"
                        :dismissible="false"
                        :ui="{ container: 'bg-black-200 w-lg' }"
                    >
                        <UButton
                            label="Configuration"
                            variant="solid"
                            trailing-icon="i-lucide-cog"
                            :ui="{
                                base: 'h-16 text-2xl w-fit',
                                trailingIcon: 'text-white size-10'
                            }"
                        />
                        <template #title />
                        <template #description />
                        <template #header>
                            <div class="flex flex-row justify-between items-center">
                                <h2 class="text-xl font-semibold text-black">Configuration</h2>
                                <UButton
                                    color="neutral"
                                    variant="ghost"
                                    icon="i-lucide-x"
                                    :ui="{ leadingIcon: 'text-black' }"
                                    @click="isDrawerOpen = false"
                                />
                            </div>
                        </template>
                        <template #body>
                            <LotoForm v-model="lotteryConfig" @on-submit="execute()" />
                        </template>
                    </UDrawer>
                </section>
                <h2 class="text-xl text-black-700 mx-auto">2. Resultat(s)</h2>

                <div
                    v-for="(
                        { numbers, lucky_number, score, total_draws_used }, lineIndex
                    ) in result"
                    :key="lineIndex"
                    class="flex flex-row gap-4 mx-auto w-fit"
                >

                    <UCheckbox
                        v-for="(num, numIndex) in numbers"
                        :key="`${lineIndex}-${num}`"
                        v-show="visibleItems.has(`${lineIndex}-${numIndex}`)"
                        class="fade-in"
                        indicator="hidden"
                        variant="card"
                        :label="String(num)"
                        :ui="{
                            root: 'size-14 bg-primary-600 rounded-full',
                            base: 'justify-center flex bg-black-200',
                            wrapper: 'h-full',
                            label: 'justify-center items-center h-full flex text-white text-xl'
                        }"
                    />

                    <UCheckbox
                        v-show="visibleItems.has(`${lineIndex}-lucky`)"
                        class="fade-in"
                        indicator="hidden"
                        variant="card"
                        :label="String(lucky_number)"
                        :ui="{
                            root: 'size-14 bg-error rounded-full',
                            base: 'justify-center flex bg-black-200',
                            wrapper: 'h-full',
                            label: 'justify-center items-center h-full flex text-white text-xl'
                        }"
                    />
                    <ul
                        v-show="visibleItems.has(`${lineIndex}-info`)"
                        class="text-xs flex flex-col justify-center text-black-600"
                    >
                        <li><b>Tirage :</b> {{ numbers.join(' ') }} {{ lucky_number }}</li>
                        <li><b>Score:</b> {{ score }}</li>
                        <li>
                            Calculé sur <b>{{ total_draws_used }}</b> tirages
                        </li>
                    </ul>
                </div>

                 <section class="flex justify-between gap-4">
                    <div class="flex-1">
                        <UCheckboxGroup
                            v-model="first"
                            indicator="hidden"
                            variant="card"
                            :default-value="first"
                            :items="numbers"
                            :ui="{
                                fieldset: 'flex flex-wrap flex-row',
                                item: 'size-14 content-center'
                            }"
                        />
                    </div>
                    <div class="w-32">
                        <URadioGroup
                            v-model="firstLucky"
                            indicator="hidden"
                            variant="card"
                            :default-value="firstLucky"
                            :items="luckNumbers"
                            :ui="{
                                fieldset: 'flex flex-wrap flex-row',
                                item: 'size-14 content-center'
                            }"
                        />
                    </div>
                </section>

                 <section v-if="result.length > 0">
                    <CommonsTableStat :data="result" />
                </section>
            </div>
        </div>
    </div> -->
</template>
<style scoped>
.fade-in {
    animation: fadeInUp 0.4s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px) scale(0.8);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}
</style>
