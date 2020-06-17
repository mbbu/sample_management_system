<template>
    <div class="sidebar">
        <router-link to="/sample">
            <a> <i class="fas fa-vials menu_icon"></i>
                Samples</a>
        </router-link>

        <hr>
        <hr>

        <router-link to="/themes">
            <a> <i aria-hidden="true" class="fa fa-trophy menu_icon"> </i>
                Themes</a>
        </router-link>

        <router-link to="/projects">
            <a> <i aria-hidden="true" class="fas fa-project-diagram menu_icon"></i>
                Projects</a>
        </router-link>

        <router-link to="/bio-hazard-level">
            <a> <i aria-hidden="true" class="fas fa-biohazard menu_icon"> </i>
                Bio Hazard Level</a>
        </router-link>

        <router-link to="/quantity-type">
            <a> <i aria-hidden="true" class="fas fa-balance-scale menu_icon"></i>
                Quantity Type</a>
        </router-link>

        <router-link to="/lab">
            <a> <i aria-hidden="true" class="fa fa-building menu_icon"></i>
                Labs</a>
        </router-link>

        <router-link to="/freezer">
            <a> <i class="fas fa-snowflake menu_icon"></i>
                Freezers</a>
        </router-link>

        <router-link to="/chamber">
            <a> <i class="fas fa-box menu_icon"></i>
                Chambers</a>
        </router-link>

        <router-link to="/rack">
            <a><i class="fas fa-bars menu_icon"></i>
                Racks</a>
        </router-link>

        <router-link to="/tray">
            <a> <i class="fas fa-th menu_icon"></i>
                Trays</a>
        </router-link>


        <router-link to="/box">
            <a> <i class="fas fa-briefcase menu_icon"></i>
                Boxes</a>
        </router-link>

        <router-link to="/publication">
            <a> <i class="fas fa-brain menu_icon"></i>
                Publications</a>
        </router-link>

        <hr>
        <hr>

        <footer-script></footer-script>
    </div>
</template>

<script>
    import FooterScript from "./../components/Footer";

    export default {
        name: 'side-menu',
        components: {FooterScript}
    };
</script>
