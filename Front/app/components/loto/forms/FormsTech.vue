<script setup lang="ts">
const lotteryConfig = defineModel<any>({ required: true })

const items = [
    { label: 'Loto', value: 'loto' },
    { label: 'Grand Loto', value: 'grand' },
    { label: 'Super Loto', value: 'super' }
]
</script>
<template>
    <div class="gap-2 grid mt-2">
        <div class="flex flex-col gap-4 rounded-xl p-3">
            <UFormField
                label="Combien de grille voulez-vous"
                name="gridsToGenerate"
                class="block w-full"
                :ui="{ label: 'text-black-600' }"
            >
                <UInput
                    v-model="lotteryConfig.gridsToGenerate"
                    type="number"
                    min="1"
                    max="10"
                    size="xl"
                    :ui="{ root: 'w-full' }"
                />
            </UFormField>
        </div>

        <div class="flex flex-col gap-4 bg-white text-black rounded-xl p-3">
            <UFormField
                label="Combien de grille voulez-vous"
                name="numbersToGenerate"
                class="block w-full"
                :ui="{ label: 'text-black-600' }"
            >
                <UInput
                    v-model="lotteryConfig.numbersToGenerate"
                    type="number"
                    min="5"
                    max="9"
                    size="xl"
                    :ui="{ root: 'w-full' }"
                />
                <p v-if="lotteryConfig.numbersToGenerate > 5">
                    ⚠️ Cela impactera le prix de votre grille de loto
                </p>
            </UFormField>
        </div>
        <div class="bg-white text-black rounded-xl p-3">
            <UFormField label="Inclure les tirages du" :ui="{ label: 'text-black-600' }">
                <UCheckboxGroup
                    v-model="lotteryConfig.includedSources"
                    indicator="end"
                    orientation="horizontal"
                    variant="card"
                    :default-value="['loto', 'super', 'grand']"
                    :items="items"
                    :ui="{ fieldset: 'justify-between', item: 'w-full' }"
                />
            </UFormField>
        </div>
        <div class="flex justify-between space-x-2 gap-4 bg-white text-black rounded-xl p-3">
            <CommonsFieldDate v-model="lotteryConfig.start_date" label="Debut" />
            <CommonsFieldDate v-model="lotteryConfig.end_date" label="Fin" />
        </div>
    </div>
</template>
