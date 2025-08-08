<script setup lang="ts">
import { h, resolveComponent } from 'vue'
import type { TableColumn } from '@nuxt/ui'

const config = useRuntimeConfig()

const start_date = ref('2019-07-14')
const end_date = ref('2025-08-01')
const items = ref(['loto', 'super', 'grand'])
const value = ref(['loto', 'super', 'grand'])

const queries = computed(() => ({
    sources: value.value.join(','),
    start_date: start_date.value,
    end_date: end_date.value
}))

const { data: weights } = useFetch('api/draws/weights', {
    key: 'get-draws-weights',
    method: 'GET',
    immediate: true,
    watch: [start_date, end_date, value],
    query: queries,
    baseURL: config.public.BASE_URL
})

const UButton = resolveComponent('UButton')

type Weight = {
    count: number
    number: number
    weight: number
}

const columns: TableColumn<Weight>[] = [
    {
        accessorKey: 'number',
        header: ({ column }) => {
            const isSorted = column.getIsSorted()

            return h(UButton, {
                color: 'neutral',
                variant: 'ghost',
                label: 'Numéros',
                icon: isSorted
                    ? isSorted === 'asc'
                        ? 'i-lucide-arrow-up-narrow-wide'
                        : 'i-lucide-arrow-down-wide-narrow'
                    : 'i-lucide-arrow-up-down',
                class: '-mx-2.5',
                onClick: () => column.toggleSorting(column.getIsSorted() === 'asc')
            })
        },
        cell: ({ row }) => h('div', { class: 'lowercase' }, row.getValue('number'))
    },
    {
        accessorKey: 'count',
        header: ({ column }) => {
            const isSorted = column.getIsSorted()

            return h(UButton, {
                color: 'neutral',
                variant: 'ghost',
                label: 'Nombre de sorties',
                icon: isSorted
                    ? isSorted === 'asc'
                        ? 'i-lucide-arrow-up-narrow-wide'
                        : 'i-lucide-arrow-down-wide-narrow'
                    : 'i-lucide-arrow-up-down',
                class: '-mx-2.5',
                onClick: () => column.toggleSorting(column.getIsSorted() === 'asc')
            })
        },
        cell: ({ row }) => h('div', { class: 'lowercase' }, row.getValue('count'))
    },
     {
        accessorKey: 'percentage',
        header: ({ column }) => {
            const isSorted = column.getIsSorted()

            return h(UButton, {
                color: 'neutral',
                variant: 'ghost',
                label: '% de sorties',
                icon: isSorted
                    ? isSorted === 'asc'
                        ? 'i-lucide-arrow-up-narrow-wide'
                        : 'i-lucide-arrow-down-wide-narrow'
                    : 'i-lucide-arrow-up-down',
                class: '-mx-2.5',
                onClick: () => column.toggleSorting(column.getIsSorted() === 'asc')
            })
        },
        cell: ({ row }) => h('div', { class: 'lowercase' }, row.getValue('percentage'))
    },
    {
        accessorKey: 'weight',
        header: ({ column }) => {
            const isSorted = column.getIsSorted()

            return h(UButton, {
                color: 'neutral',
                variant: 'ghost',
                label: 'Pondérés *',
                icon: isSorted
                    ? isSorted === 'asc'
                        ? 'i-lucide-arrow-up-narrow-wide'
                        : 'i-lucide-arrow-down-wide-narrow'
                    : 'i-lucide-arrow-up-down',
                class: '-mx-2.5',
                onClick: () => column.toggleSorting(column.getIsSorted() === 'asc')
            })
        },
        cell: ({ row }) => h('div', { class: 'lowercase' }, row.getValue('weight'))
    }
]
</script>

<template>
    <div class="flex-1 divide-y divide-accented w-full mt-60">
        <div class="flex flex-col items-center gap-2 px-4 py-3.5 overflow-x-auto">
            <h2 class="text-xl">Palmarès des numéros</h2>
            <p class="mb-4 text-sm">Tout tirage confondu</p>
        </div>
        <div class="flex justify-between space-x-2 gap-4 bg-white text-black rounded-xl p-3">
            <CommonsFieldDate v-model="start_date" label="Debut" />
            <CommonsFieldDate v-model="end_date" label="Fin" />
            <UFormField
                label="Type de tirage"
                :ui="{ container: 'w-full', root: 'w-full', label: 'text-black-600' }"
            >
                <USelect v-model="value" multiple :items="items" size="lg" class="w-full py-2.5 font-semibold capitalize" />
            </UFormField>
        </div>
        <UTable :data="weights?.numbers ?? []" :columns="columns" sticky class="h-96">
            <template #expanded="{ row }">
                <pre>{{ row.original }}</pre>
            </template>
        </UTable>
        <p class="px-4 py-3.5 text-sm text-muted">
            * Calcul du pondéré : weight(7) = (38 - 10) / (38 - 10) = 28 / 28 = 1.0
            <br />
            1.0 (le plus fréquent)
            <br />
            0.5 (moyen)
            <br />
            0.0 (le moins fréquent)
        </p>
    </div>
    <div class="flex-1 divide-y divide-accented w-full">
        <div class="flex flex-col items-center gap-2 px-4 py-3.5 overflow-x-auto">
            <h2 class="text-xl">Palmarès des numéros chance</h2>
            <p class="mb-4 text-sm">Tout tirage confondu</p>
        </div>
        <UTable :data="weights?.lucky_numbers ?? []" :columns="columns" sticky class="h-96">
            <template #expanded="{ row }">
                <pre>{{ row.original }}</pre>
            </template>
        </UTable>

        <p class="px-4 py-3.5 text-sm text-muted">
            * Calcul du pondéré : weight(7) = (38 - 10) / (38 - 10) = 28 / 28 = 1.0
            <br />
            1.0 (le plus fréquent)
            <br />
            0.5 (moyen)
            <br />
            0.0 (le moins fréquent)
        </p>
    </div>
</template>
