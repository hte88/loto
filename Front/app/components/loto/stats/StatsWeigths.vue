<script setup lang="ts">
import { h, resolveComponent } from 'vue'
import type { TableColumn } from '@nuxt/ui'

const config = useRuntimeConfig()

const { data: weights } = useFetch('api/draws/weights', {
    key: 'get-draws-weights',
    method: 'GET',
    query: { sources: 'loto,super', start_date: '2025-07-01', end_date: '2025-08-01' },
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
    <div class="flex-1 divide-y divide-accented w-full">
        <div class="flex flex-col items-center gap-2 px-4 py-3.5 overflow-x-auto">
            <h2 class="text-xl">Palmarès des numéros</h2>
            <p class="mb-4 text-sm">Tout tirage confondu</p>
        </div>
        <UTable :data="[...weights?.numbers] ?? []" :columns="columns" sticky class="h-96">
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
        <UTable :data="[...weights?.lucky_numbers] ?? []" :columns="columns" sticky class="h-96">
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
