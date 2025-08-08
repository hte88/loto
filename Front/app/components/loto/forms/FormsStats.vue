<script setup lang="ts">
const lotteryConfig = defineModel<any>({ required: true })
</script>
<template>
    <div class="gap-2 grid mt-2">
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
        <CommonsFieldInputNumberTag
            v-model="lotteryConfig.excludeLucky"
            title="Numéros à exclure du numéro chance"
            placeholder="Ex: 1, 5, ..."
            :max="5"
        />
    </div>
</template>
