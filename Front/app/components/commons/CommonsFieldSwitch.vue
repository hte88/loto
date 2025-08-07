<script setup lang="ts">
import { boolean, z } from 'zod'

const {
    maxTolerance = null,
    minTolerance = null,
    title,
    slider = { min: 0, max: 100, step: 1 },
    error,
    label
} = defineProps<{
    title: string
    maxTolerance?: number
    minTolerance?: number
    slider?: {
        min: number
        max: number
        step: number
    }
    error?: string
    label?: string
}>()

const should = defineModel<boolean>('should', { required: true })
const tolerance = defineModel<number>('tolerance')

const schema = z.object({
    should: z.boolean(),
    tolerance: z.number().min(0).max(100)
})

const isToleranceInvalid = computed(() => {
    if (!tolerance.value || !minTolerance || !maxTolerance) {
        return
    }
    return tolerance.value < minTolerance || tolerance.value > maxTolerance
})
const labelField = computed(() => {
    return label ? `${label} (${tolerance.value})` : `Favoriser a (${tolerance.value}%)`
})
</script>

<template>
    <UForm
        attach
        :state="{ should, tolerance }"
        :schema="schema"
        class="flex flex-col gap-2 rounded-xl p-3 transition-colors ease-linear duration-300"
        :class="should ? 'bg-white text-black' : 'bg-black-600 text-white'"
    >
        <div class="flex flex-row justify-between items-center">
            <p class="text-sm font-medium">{{ title }}</p>
            <USwitch v-model="should" size="xl" />
        </div>
        <template v-if="should && tolerance">
            <UFormField :label="labelField" name="tolerance" :ui="{ label: 'text-black-600' }">
                <USlider
                    v-model="tolerance"
                    :color="isToleranceInvalid ? 'warning' : 'primary'"
                    size="xl"
                    :min="slider.min"
                    :max="slider.max"
                    :step="slider.step"
                />
            </UFormField>

            <div v-if="isToleranceInvalid" class="text-sm">
                <p v-if="error">⚠️ {{ error }}</p>
                <p v-else>
                    ⚠️ La tolérance doit être entre {{ minTolerance }}% et {{ maxTolerance }}%.
                </p>
            </div>
        </template>
    </UForm>
</template>
