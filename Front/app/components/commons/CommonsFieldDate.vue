<script setup lang="ts">
const { label } = defineProps<{ label: string }>()
const modelValue = defineModel()

const currentYear = ref(new Date().getFullYear())
const selectedMonth = ref(null)
const selectedYear = ref(null)
const view = ref('year') // 'year' ou 'month'
const isOpen = ref(false)

// Limites d'années
const MIN_YEAR = 1976
const MAX_YEAR = new Date().getFullYear()

const months = [
    'Janvier',
    'Février',
    'Mars',
    'Avril',
    'Mai',
    'Juin',
    'Juillet',
    'Août',
    'Septembre',
    'Octobre',
    'Novembre',
    'Décembre'
]

// Génération des années avec limites
const years = computed(() => {
    const startYear = Math.max(currentYear.value, MIN_YEAR)
    const endYear = Math.min(currentYear.value + 11, MAX_YEAR)
    const yearCount = endYear - startYear + 1

    return Array.from({ length: yearCount }, (_, i) => startYear + i)
})

const handleYearSelect = (year) => {
    selectedYear.value = year
    view.value = 'month'
}

const handleMonthSelect = (monthIndex) => {
    isOpen.value = false
    selectedMonth.value = monthIndex
    // Format : YYYY-MM (mois avec padding)
    const monthStr = String(monthIndex + 1).padStart(2, '0')
    const formattedDate = new Date(`${selectedYear.value}-${monthStr}-01T00:00:00Z`)
        .toISOString()
        .slice(0, 10)
    modelValue.value = formattedDate

    emit('dateSelected', {
        year: selectedYear.value,
        month: monthIndex + 1, // Mois de 1 à 12
        monthName: months[monthIndex]
    })
}

const goToPreviousYear = () => {
    if (view.value === 'year') {
        // Limiter la navigation vers le passé
        const newYear = currentYear.value - 12
        if (newYear >= MIN_YEAR) {
            currentYear.value = newYear
        } else {
            // Ajuster pour afficher depuis 1976
            currentYear.value = MIN_YEAR
        }
    } else {
        // Navigation année par année en vue mois
        if (selectedYear.value > MIN_YEAR) {
            selectedYear.value -= 1
        }
    }
}

const goToNextYear = () => {
    if (view.value === 'year') {
        // Limiter la navigation vers le futur
        const newEndYear = currentYear.value + 12 + 11 // +11 car on affiche 12 années
        if (newEndYear <= MAX_YEAR) {
            currentYear.value += 12
        }
    } else {
        // Navigation année par année en vue mois
        if (selectedYear.value < MAX_YEAR) {
            selectedYear.value += 1
        }
    }
}

// Initialiser currentYear pour commencer dans une plage valide
onMounted(() => {
    // Si l'année actuelle dépasse notre plage d'affichage de 12 ans, ajuster
    if (currentYear.value + 11 > MAX_YEAR) {
        currentYear.value = Math.max(MAX_YEAR - 11, MIN_YEAR)
    }
})

const emit = defineEmits(['dateSelected'])
</script>

<template>
    <UPopover v-model:open="isOpen">
        <UFormField :label :ui="{ container: 'w-full', root: 'w-full', label: 'text-black-600' }">
            <UButton color="neutral" variant="outline" size="xl" block icon="i-lucide-calendar">
                {{
                    modelValue
                        ? new Date(modelValue).toLocaleDateString('fr-FR', {
                              year: 'numeric',
                              month: 'long',
                              day: 'numeric'
                          })
                        : 'Sélectionner une date'
                }}
            </UButton>
        </UFormField>

        <template #content>
            <div class="max-w-md mx-auto bg-white border border-gray-200 rounded-lg shadow-lg">
                <!-- Vue Année -->
                <div v-if="view === 'year'" class="p-6">
                    <div class="flex items-center justify-between mb-6">
                        <UButton
                            icon="i-lucide-chevron-left"
                            variant="ghost"
                            :disabled="currentYear <= MIN_YEAR"
                            @click="goToPreviousYear"
                        />
                        <h2 class="text-xl font-semibold">
                            {{
                                Math.min(currentYear + 11, MAX_YEAR) === currentYear + 11
                                    ? `${currentYear} - ${currentYear + 11}`
                                    : `${currentYear} - ${MAX_YEAR}`
                            }}
                        </h2>
                        <UButton
                            icon="i-lucide-chevron-right"
                            variant="ghost"
                            :disabled="currentYear + 11 >= MAX_YEAR"
                            @click="goToNextYear"
                        />
                    </div>

                    <div class="grid grid-cols-3 gap-4">
                        <UButton
                            v-for="year in years"
                            :key="year"
                            :variant="selectedYear === year ? 'solid' : 'outline'"
                            :color="selectedYear === year ? 'primary' : 'gray'"
                            class="p-4 h-12"
                            @click="handleYearSelect(year)"
                        >
                            {{ year }}
                        </UButton>
                    </div>
                </div>

                <!-- Vue Mois -->
                <div v-else class="p-6">
                    <div class="flex items-center justify-between mb-6">
                        <UButton
                            icon="i-lucide-chevron-left"
                            variant="ghost"
                            :disabled="selectedYear <= MIN_YEAR"
                            @click="goToPreviousYear"
                        />
                        <UButton
                            :label="String(selectedYear)"
                            variant="ghost"
                            @click="view = 'year'"
                            class="text-xl font-semibold"
                        />
                        <UButton
                            icon="i-lucide-chevron-right"
                            variant="ghost"
                            :disabled="selectedYear >= MAX_YEAR"
                            @click="goToNextYear"
                        />
                    </div>

                    <div class="grid grid-cols-3 gap-4">
                        <UButton
                            v-for="(month, index) in months"
                            :key="index"
                            :variant="selectedMonth === index ? 'solid' : 'outline'"
                            :color="selectedMonth === index ? 'green' : 'gray'"
                            class="p-4 h-12"
                            @click="handleMonthSelect(index)"
                        >
                            {{ month }}
                        </UButton>
                    </div>
                </div>
            </div>
        </template>
    </UPopover>
</template>
