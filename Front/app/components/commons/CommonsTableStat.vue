<script setup lang="ts">
import { h, resolveComponent } from 'vue'
import type { TableColumn } from '@nuxt/ui'

const props = defineProps<{ data: [] }>()

const UButton = resolveComponent('UButton')

type Weight = {
    count: number
    number: number
    weight: number
}

const columns: TableColumn<Weight>[] = [
    {
        accessorKey: 'numbers',
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
        cell: ({ row }) => h('div', { class: 'lowercase' }, row.getValue('numbers'))
    },
    {
        accessorKey: 'lucky_number',
        header: ({ column }) => {
            const isSorted = column.getIsSorted()

            return h(UButton, {
                color: 'neutral',
                variant: 'ghost',
                label: 'Numéro chance',
                icon: isSorted
                    ? isSorted === 'asc'
                        ? 'i-lucide-arrow-up-narrow-wide'
                        : 'i-lucide-arrow-down-wide-narrow'
                    : 'i-lucide-arrow-up-down',
                class: '-mx-2.5',
                onClick: () => column.toggleSorting(column.getIsSorted() === 'asc')
            })
        },
        cell: ({ row }) => h('div', { class: 'lowercase' }, row.getValue('lucky_number'))
    },
    {
        accessorKey: 'score',
        header: ({ column }) => {
            const isSorted = column.getIsSorted()

            return h(UButton, {
                color: 'neutral',
                variant: 'ghost',
                label: 'Score *',
                icon: isSorted
                    ? isSorted === 'asc'
                        ? 'i-lucide-arrow-up-narrow-wide'
                        : 'i-lucide-arrow-down-wide-narrow'
                    : 'i-lucide-arrow-up-down',
                class: '-mx-2.5',
                onClick: () => column.toggleSorting(column.getIsSorted() === 'asc')
            })
        },
        cell: ({ row }) => h('div', { class: 'lowercase' }, row.getValue('score'))
    }
]
</script>

<template>
    <div class="flex-1 divide-y divide-accented w-full">
        <div class="flex flex-col items-center gap-2 px-4 py-3.5 overflow-x-auto">
            <h2 class="text-xl">Résultats</h2>
            <p class="mb-4 text-sm"></p>
        </div>
        <UTable :data="data ?? []" :columns="columns" sticky class="h-96">
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
