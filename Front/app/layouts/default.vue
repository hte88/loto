<template>
    <div class="min-h-screen inline-flex flex-col">
        <UApp>
            <AppHeader />
            <div class="text-center mt-40">
                <h1
                    class="text-pretty w-fit mx-auto tracking-tight font-bold text-5xl sm:text-7xl bg-gradient-to-r from-cyan-600 to-error bg-clip-text text-transparent"
                >
                    Loto Cheat
                </h1>
                <p class="text-lg sm:text-xl/8 text-muted text-pretty mt-6">
                    commodo. Elit sunt amet fugiat veniam occaecat.
                </p>
            </div>
            <slot />
        </UApp>
    </div>
</template>
