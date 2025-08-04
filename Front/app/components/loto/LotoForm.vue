<script setup lang="ts">
import { z } from 'zod'

const lotteryConfig = defineModel<any>({ required: true })
const emit = defineEmits(['onSubmit'])

const schema = z.object({
    list: z.array(z.number()).max(9).optional()
})
</script>
<template>
    <UForm
        :state="lotteryConfig"
        :schema
        class="h-full gap-4 flex flex-col justify-between"
        @submit="emit('onSubmit')"
    >
        <div class="gap-4 grid">
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

            <div class="flex flex-col gap-4 bg-gray-600 rounded-xl p-3">
                <div class="flex flex-row justify-between items-center">
                    <p class="text-sm font-medium">Exclure si la combinaison existe deja</p>
                    <USwitch v-model="lotteryConfig.shouldCheckExistence" size="xl" />
                </div>
            </div>

            <div class="flex flex-col gap-4 bg-gray-600 rounded-xl p-3">
                <div class="flex flex-row justify-between items-center">
                    <p class="text-sm font-medium">
                        Favoriser ceux qui ont un score de probabilité élevé
                    </p>
                    <USwitch v-model="lotteryConfig.shouldEvaluateScore" size="xl" />
                </div>
            </div>

            <div class="flex flex-col gap-4 bg-gray-600 rounded-xl p-3">
                <div class="flex flex-row justify-between items-center">
                    <p class="text-sm font-medium">
                        Generer un numero chance avec un score de probabilité élevé
                    </p>
                    <USwitch v-model="lotteryConfig.shouldGenerateLucky" size="xl" />
                </div>
            </div>

            <CommonsFieldInputNumberTag
                v-model="lotteryConfig.excludeLucky"
                title="Numéros à exclure du numéro chance"
                placeholder="Ex: 1, 5, ..."
                :max="5"
            />

            <div class="flex flex-col gap-4 bg-gray-600 rounded-xl p-3">
                <UFormField
                    label="Combien de grille voulez-vous"
                    name="gridsToGenerate"
                    class="block w-full"
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
        </div>
        <UButton label="Générer" type="submit" block size="xl" />
    </UForm>
</template>
