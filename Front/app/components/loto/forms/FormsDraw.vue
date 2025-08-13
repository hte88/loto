<script setup lang="ts">
const lotteryConfig = defineModel<any>({ required: true })
</script>
<template>
    <div class="gap-2 grid mt-2">
        <CommonsFieldSwitch
            v-model:should="lotteryConfig.shouldCheckExistence"
            title="Exclure si la combinaison existe deja"
        />
        <CommonsFieldSwitch
            v-model:should="lotteryConfig.shouldEvaluateScore"
            title="Favoriser ceux qui ont un score de probabilité élevé"
        />
        <CommonsFieldSwitch
            v-model:should="lotteryConfig.shouldEvaluatePercentage"
            title="Favoriser ceux qui ont un score de sortie élevée"
        />
        <CommonsFieldSwitch
            v-model:should="lotteryConfig.shouldEvaluateWeight"
            title="Favoriser ceux qui ont un score pondéré élevé"
        />
        <CommonsFieldSwitch
            v-model:should="lotteryConfig.shouldGenerateLucky"
            title="Generer un numero chance avec un score de probabilité élevé"
        />
    </div>
</template>
