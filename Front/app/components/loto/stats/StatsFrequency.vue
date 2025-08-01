<script setup lang="ts">
const config = useRuntimeConfig()

const { data: frequency, execute: execFrequency } = useFetch('api/draws/frequency', {
    key: 'get-draws-frequency',
    method: 'GET',
    baseURL: config.public.BASE_URL
})

const RevenueCategories = computed(() => ({
    count: {
        name: 'Nombre de sorties',
        color: '#22c55e'
    }
}))

const xFormatter = (i: number): string => `${frequency.value?.global_frequency[i]?.number}`
const yFormatter = (i: number) => i.toString()

onMounted(() => {
    execFrequency()
})
</script>
<template>
    <div class="chart-wrapper">
        <h2 class="text-xl">Palmarès des numéros</h2>
        <p class="mb-4  text-sm">Tout tirage confondu</p>
        <BarChart
            :data="frequency?.global_frequency ?? []"
            :height="500"
            :categories="RevenueCategories"
            :y-axis="['count']"
            :x-num-ticks="49"
            :y-grid-line="true"
            :radius="4"
            :x-formatter="xFormatter"
            :y-formatter="yFormatter"
            :hide-legend="true"
            yLabel="Nombre de sorties"
            xLabel="Numéros"
        />
    </div>
</template>
