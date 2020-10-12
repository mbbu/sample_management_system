<template>
    <p v-if="errors.length">
      <b>Please correct the following error(s):</b>
      <ul>
        <li class="text-danger" :key="index" v-for="(error, index) in errors"><em>* {{ error }}</em></li>
      </ul>
    </p>
</template>

<script>
    export default {
        name: "ErrorsDisplay",
        props: {
            errors: {
                type: Array,
                required: false,
            }
        },
    }
</script>