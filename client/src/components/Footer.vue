<template>
    <div class="footer text-white text-center">
        <p>
            <em>Copyright &copy; {{ getThisYear() }}
                <br>All rights reserved to I.C.I.P.E.</em>
        </p>
    </div>
</template>

<script>
    import {getThisYear} from "@/utils/util_functions";

    export default {
        name: "FooterScript",
        data() {
            return {
                year: null
            }
        },
        methods: {getThisYear},
    }
</script>
