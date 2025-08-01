<script setup lang="ts">
import { boolean, z } from 'zod'

const { maxTolerance, minTolerance, title } = defineProps<{
    maxTolerance: number
    minTolerance: number
    title: string
}>()

const should = defineModel<boolean>('should', { required: true })
const tolerance = defineModel<number>('tolerance', { required: true })

const schema = z.object({
    should: z.boolean(),
    tolerance: z.number().min(0).max(100)
})

const isToleranceInvalid = computed(() => {
    return tolerance.value < minTolerance || tolerance.value > maxTolerance
})
</script>

<template>
    <UForm
        attach
        :state="{ should, tolerance }"
        :schema="schema"
        class="flex flex-col gap-4 bg-gray-600 rounded-xl p-3"
    >
        <div class="flex flex-row justify-between items-center">
            <p class="text-sm font-medium">{{ title }}</p>
            <USwitch v-model="should" size="xl" />
        </div>
        <template v-if="should">
            <UFormField :label="`Tolérance (${tolerance}%)`" name="tolerance">
                <USlider
                    v-model="tolerance"
                    :color="isToleranceInvalid ? 'warning' : 'primary'"
                    size="xl"
                    :min="0"
                    :max="100"
                    :step="1"
                />
            </UFormField>

            <p v-if="isToleranceInvalid" class="text-sm">
                ⚠️ La tolérance doit être entre {{ minTolerance }}% et {{ maxTolerance }}%.
            </p>
        </template>
    </UForm>
</template>
