<script setup lang="ts">
const lotteryConfig = defineModel<any>({ required: true })
const emit = defineEmits(['onSubmit'])

const accordionItems = [
    {
        label: 'Statistique',
        value: 'loto',
        component: defineAsyncComponent(() => import('~/components/loto/forms/FormsStats.vue'))
    },
    {
        label: 'Technique',
        value: 'grand',
        component: defineAsyncComponent(() => import('~/components/loto/forms/FormsTech.vue'))
    },
    {
        label: 'Tirage',
        value: 'super',
        component: defineAsyncComponent(() => import('~/components/loto/forms/FormsDraw.vue'))
    }
]
</script>
<template>
    <UForm
        :state="lotteryConfig"
        class="h-full gap-2 flex flex-col justify-between"
        @submit="emit('onSubmit')"
    >
        <div>
            <UAccordion default-value="loto" :unmount-on-hide="true" :items="accordionItems">
                <template #content="{ item }">
                    <component :is="item.component" v-if="item.component" v-model="lotteryConfig" />
                </template>
            </UAccordion>
        </div>
        <Teleport to="#modals">
            <UButton label="Générer" type="submit" block size="xl" />
        </Teleport>
    </UForm>
</template>
