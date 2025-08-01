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

const { data: frequency, execute: execFrequency } = useFetch('api/draws/frequency', {
    key: 'get-draws-frequency',
    method: 'GET',
    baseURL: config.public.BASE_URL
})
/*
const { data: weights, execute: execWeights } = useFetch('api/draws/weights', {
    key: 'get-draws-weights',
    method: 'GET',
    baseURL: config.public.BASE_URL
}) */

const lotteryConfig = ref({
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
    shouldGenerateLucky: true, // weighted selection by past frequency
    favorLucky: 6,
    excludeLucky: [1, 10],
    gridsToGenerate: 1
})

const { data: dgenerate, execute: execGenerate } = useFetch('api/draws/generate', {
    key: 'post-draws-generate',
    baseURL: config.public.BASE_URL,
    method: 'POST',
    immediate: false,
    watch: false,
    body: lotteryConfig
})

function execute() {
    isDrawerOpen.value = false
    execGenerate()
}

onMounted(() => {
    execFrequency()
    /*  execFrequency()
    execWeights()
    execGenerate() */
    // execute()
})

const numbers = ref<CheckboxGroupItem[]>(Array.from({ length: 49 }, (_, i) => i + 1))
const luckNumbers = ref<CheckboxGroupItem[]>(Array.from({ length: 10 }, (_, i) => i + 1))

const numbersSelected = ref(dgenerate.value?.numbers ?? [])
const luckyNumberSelected = ref([])
const result = computed(() => `${numbersSelected.value} ${luckyNumberSelected.value}`)

const first = computed(() => dgenerate.value?.[0]?.numbers.map(String) ?? [])
const firstLucky = computed(() => dgenerate.value?.[0]?.lucky_number.toString() ?? '')
</script>

<template>
    <div>
        <div class="text-center">
            <h1 class="text-5xl font-semibold text-balance text-white">Loto Cheat</h1>
            <p class="mt-8 text-lg font-medium text-gray-500">
                commodo. Elit sunt amet fugiat veniam occaecat.
            </p>
        </div>
        <div class="flex flex-col gap-4 w-4xl mx-auto">
            <section>
                <UDrawer
                    v-model:open="isDrawerOpen"
                    direction="right"
                    :handle="false"
                    :dismissible="false"
                >
                    <UButton
                        label="Configuration"
                        color="neutral"
                        variant="subtle"
                        trailing-icon="i-lucide-cog"
                    />
                    <template #header>
                        <div class="flex flex-row justify-between items-center">
                            <h2 class="text-xl font-semibold">Configuration</h2>
                            <UButton
                                color="neutral"
                                variant="ghost"
                                icon="i-lucide-x"
                                @click="isDrawerOpen = false"
                            />
                        </div>
                    </template>
                    <template #body>
                        <LotoForm v-model="lotteryConfig" @on-submit="execute()" />
                    </template>
                </UDrawer>
            </section>

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

            <div>
                <ul>
                    <li v-for="number in dgenerate" :key="number.number">
                        {{ number.numbers }} - {{ number.lucky_number }} - {{ number.score }}
                    </li>
                </ul>
            </div>

            <div>
            <ul>
                <li v-for="number in frequency.global_frequency" :key="number.number">
                    {{ number.number }} - {{ number.count }} - {{ number.weight }}
                </li>
            </ul>
        </div>
       <!--  <div>
            <ul>
                <li v-for="number in dgenerate" :key="number.number">
                    {{ number.numbers }} - {{ number.lucky_number }} - {{ number.score }}
                </li>
            </ul>
        </div>  -->
        </div>
    </div>
</template>
