<script setup lang="ts">
import { z } from 'zod'

const {
    placeholder,
    title,
    max = 20
} = defineProps<{
    placeholder: string
    title: string
    max?: number
}>()

const lotteryConfig = defineModel<number[]>({ required: true })

const error = ref<string | null>(null)

const schema = z.object({
    list: z.array(z.number()).max(9).optional()
})

const includeNumbersModel = computed<string[]>({
    get: () => lotteryConfig.value.map(String),
    set: (val: string[]) => {
        lotteryConfig.value = val
            .map((v) => parseInt(v, 10))
            .filter((v) => !isNaN(v) && v >= 1 && v <= 49)
    }
})

function validateTag(value: string): boolean {
    const num = parseInt(value, 10)

    if (isNaN(num) || num < 1 || num > 49) {
        error.value = `Veuillez entrer un nombre entre 1 et 49.`
        return false
    }

    if (lotteryConfig.value.includes(num)) {
        error.value = `Le nombre ${num} est déjà présent.`
        return false
    }

    if (lotteryConfig.value.length >= max) {
        error.value = `Vous ne pouvez ajouter que ${max} numéros maximum.`
        return false
    }

    error.value = null
    return true
}
</script>

<template>
    <UForm
        attach
        :state="{ list: lotteryConfig }"
        :schema="schema"
        class="flex flex-col gap-4 bg-gray-600 rounded-xl p-3"
    >
        <UFormField :label="title" name="list">
            <UInputTags
                v-model="includeNumbersModel"
                size="xl"
                :max
                :placeholder="placeholder"
                :ui="{ base: 'w-full' }"
                @add="
                    (e: any) => {
                        if (!validateTag(e)) e.preventDefault?.()
                    }
                "
            />
        </UFormField>

        <p v-if="error" class="text-red-500 text-sm">
            {{ error }}
        </p>
    </UForm>
</template>
