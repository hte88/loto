<script setup lang="ts">
import { z } from 'zod'

const lotteryConfig = defineModel<any>({ required: true })
const emit = defineEmits(['onSubmit'])

const schema = z.object({
    list: z.array(z.number()).max(9).optional()
})

const items = [
    { label: 'Loto', value: 'loto' },
    { label: 'Grand Loto', value: 'grand' },
    { label: 'Super Loto', value: 'super' }
]
</script>
<template>
    <UForm
        :state="lotteryConfig"
        :schema
        class="h-full gap-2 flex flex-col justify-between"
        @submit="emit('onSubmit')"
    >
        <div class="gap-2 grid">
            <CommonsFieldSwitch
                v-model:should="lotteryConfig.shouldBalanceEvenOdd"
                v-model:tolerance="lotteryConfig.favorEven"
                title="Favoiser les nombres pair"
                :min-tolerance="40"
                :max-tolerance="60"
            />
            <CommonsFieldSwitch
                v-model:should="lotteryConfig.shouldBalanceHighLow"
                v-model:tolerance="lotteryConfig.favorHigh"
                title="Favoiser les nombres supperieur a 25"
                :min-tolerance="40"
                :max-tolerance="60"
            />
            <CommonsFieldSwitch
                v-model:should="lotteryConfig.shouldAvoidLogicalSequences"
                v-model:tolerance="lotteryConfig.sequenceTolerance"
                title="Suite consecutive tolerée"
                :min-tolerance="0"
                :max-tolerance="2"
                :slider="{ min: 0, max: 9, step: 1 }"
                label="Combien de suite consecutive tolerez vous dans votre grille"
                :error="`Information, les probabilités que ${lotteryConfig.sequenceTolerance} nombres consecutive sortent reste mince`"
            />
            <CommonsFieldSwitch
                v-model:should="lotteryConfig.shouldAvoidRoundNumbers"
                v-model:tolerance="lotteryConfig.roundNumberTolerance"
                title="Favoiser les nombres rond"
                :min-tolerance="0"
                :max-tolerance="2"
                :slider="{ min: 0, max: 5, step: 1 }"
                label="Combien de nombre rond tolerez vous dans votre grille"
                :error="`Information, les probabilités que ${lotteryConfig.roundNumberTolerance} nombres ronds sortent reste mince`"
            />
            <CommonsFieldInputNumberTag
                v-model="lotteryConfig.includeNumbers"
                title="Numéros à inclure"
                placeholder="Ex: 3, 7, 12..."
            />
            <CommonsFieldInputNumberTag
                v-model="lotteryConfig.excludeNumbers"
                title="Numéros à exclure"
                placeholder="Ex: 3, 7, 12..."
            />
            <CommonsFieldSwitch
                v-model:should="lotteryConfig.shouldCheckExistence"
                title="Exclure si la combinaison existe deja"
            />
            <CommonsFieldSwitch
                v-model:should="lotteryConfig.shouldEvaluateScore"
                title="Favoriser ceux qui ont un score de probabilité élevé"
            />
            <CommonsFieldSwitch
                v-model:should="lotteryConfig.shouldGenerateLucky"
                title="Generer un numero chance avec un score de probabilité élevé"
            />
            <CommonsFieldInputNumberTag
                v-model="lotteryConfig.excludeLucky"
                title="Numéros à exclure du numéro chance"
                placeholder="Ex: 1, 5, ..."
                :max="5"
            />

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
        <UButton label="Générer" type="submit" block size="xl" />
    </UForm>
</template>
