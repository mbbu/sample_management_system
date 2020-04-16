<template>
    <p v-if="errors.length">
        <b>Please correct the following error(s):</b>
    <ul>
        <em>
            <li class="text-danger" :key="index" v-for="(error, index) in errors">* {{ error }}</li>
        </em>
    </ul>
    </p>
</template>

<script>
    // import {showFlashMessage} from "../utils/util_functions";

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