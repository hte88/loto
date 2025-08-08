<script setup lang="ts">
import type { ColumnDef } from '@tanstack/vue-table'

const { lotteryConfig } = defineProps<{
    lotteryConfig: {
        shouldEvaluateScore: boolean
        shouldCheckExistence: boolean
        shouldGenerateLucky: boolean
        favorEven: number
        favorHigh: number
        sequenceTolerance: number
        roundNumberTolerance: number
        includeNumbers: number[] | string
        excludeNumbers: number[] | string
        favorLucky: number[] | string
        excludeLucky: number[] | string
        gridsToGenerate: number
        numbersToGenerate: number
        includedSources: string[]
        start_date: string
        end_date: string
    }
}>()

interface ConfigRow {
    parameter: string
    value: string | number
}

const columns: ColumnDef<ConfigRow>[] = [
    {
        accessorKey: 'parameter',
        header: 'Récapitulatif'
    },
    {
        accessorKey: 'value',
        header: ''
    }
]

const configRows = computed((): ConfigRow[] => {
    const draw = [
        {
            parameter: 'Grilles à générer',
            value: `${lotteryConfig.gridsToGenerate} grille(s)`
        },
        {
            parameter: 'Numéros par grille',
            value: `${lotteryConfig.numbersToGenerate} numéros`
        },
        {
            parameter: 'Sources incluses',
            value: Array.isArray(lotteryConfig.includedSources)
                ? lotteryConfig.includedSources.join(', ')
                : 'Aucune'
        },
        {
            parameter: 'Période des tirages',
            value: `Du ${lotteryConfig.start_date}`
        },
        {
            parameter: '',
            value: `Au ${lotteryConfig.end_date}`
        }
    ]
    const stats = [
        {
            parameter: 'Favoriser les nombres pairs',
            value: `${lotteryConfig.favorEven}%`
        },
        {
            parameter: 'Favoriser les nombres impairs',
            value: `${100 - lotteryConfig.favorEven}%`
        },
        {
            parameter: 'Favoriser les nombres hauts',
            value: `${lotteryConfig.favorHigh}%`
        },
        {
            parameter: 'Favoriser les nombres bas',
            value: `${100 - lotteryConfig.favorHigh}%`
        },
        {
            parameter: 'Nombre de suites tolérées',
            value: lotteryConfig.sequenceTolerance
        },
        {
            parameter: 'Nombres ronds tolérés',
            value: lotteryConfig.roundNumberTolerance
        },
        {
            parameter: 'Favoriser les nombres',
            value: Array.isArray(lotteryConfig.includeNumbers)
                ? lotteryConfig.includeNumbers.join(', ')
                : lotteryConfig.includeNumbers || 'Aucun'
        },
        {
            parameter: 'Exclure les nombres',
            value: Array.isArray(lotteryConfig.excludeNumbers)
                ? lotteryConfig.excludeNumbers.join(', ')
                : lotteryConfig.excludeNumbers || 'Aucun'
        },
        {
            parameter: 'Favoriser les nombres - Numéro chance',
            value: Array.isArray(lotteryConfig.favorLucky)
                ? lotteryConfig.favorLucky.join(', ')
                : lotteryConfig.favorLucky || 'Aucun'
        },
        {
            parameter: 'Exclure les nombres - Numéro chance',
            value: Array.isArray(lotteryConfig.excludeLucky)
                ? lotteryConfig.excludeLucky.join(', ')
                : lotteryConfig.excludeLucky || 'Aucun'
        }
    ]
    const tech = [
        {
            parameter: 'Tirage',
        },
        {
            parameter: 'Prendre en compte le score',
            value: lotteryConfig.shouldEvaluateScore ? 'Oui' : 'Non'
        },
        {
            parameter: 'Éviter une grille déjà sortie',
            value: lotteryConfig.shouldCheckExistence ? 'Oui' : 'Non'
        },
        {
            parameter: 'Prendre en compte le score pour le numéro chance',
            value: lotteryConfig.shouldGenerateLucky ? 'Oui' : 'Non'
        }
    ]

    return [...stats, ...tech, ...draw]
})
</script>

<template>
    <div
        class="flex flex-col gap-2 rounded-xl p-3 transition-colors ease-linear duration-300 bg-white text-black mt-4"
    >
        <UTable
            :data="configRows"
            :columns="columns"
            class="w-full"
            :ui="{ td: 'p-1 whitespace-normal text-xs' }"
        >
            <template #empty-state>
                <div class="flex flex-col items-center justify-center py-6 gap-3">
                    <span class="italic text-sm">Aucune configuration trouvée</span>
                </div>
            </template>
        </UTable>
    </div>
</template>
