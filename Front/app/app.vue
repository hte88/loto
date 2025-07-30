<script setup lang="ts">

const config = useRuntimeConfig()

 const {data} = useFetch('api/draws/', {
  method: 'GET',
  baseURL: config.public.BASE_URL
 })
console.log(config.public.BASE_URL);

const {execute} = useFetch('api/draws/', {
  method: 'POST',
  baseURL: config.public.BASE_URL,
  body: {
  number_1: 123,
  number_2: 2,
  number_3: 3,
  number_4: 4,
  number_5: 5,
  lucky_number: 6
  }
 })

 onMounted(() => {
  execute()
 })

</script>

<template>
  <div>
{{data}}    <NuxtRouteAnnouncer />
    <NuxtWelcome />
  </div>
</template>
