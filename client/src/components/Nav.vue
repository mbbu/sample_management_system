<template>
    <nav class="menu-container">
        <ul class="menu">
            <li class="menu_top">
                <router-link to="/index">
                    <img :src="require('../assets/logo.png')" class="menu_logo"/>
                </router-link>
            </li>

            <li>
                <router-link to="/home" class="context-menu__link">
                    <i class="fa fa-home menu_icon" aria-hidden="true"> </i>
                    Home
                </router-link>
            </li>

            <li>
                <router-link to="/sample" class="context-menu__link">
                    <i class="fa fa-search menu_icon" aria-hidden="true"> </i>
                    Search Samples
                </router-link>
            </li>

            <li>
                <a href="https://redcap.icipe.org/surveys/?s=W7A7TFJ89J" class="context-menu__link">
                    <i class="fa fa-inbox menu_icon" aria-hidden="true"> </i>
                    Request Sample </a>
            </li>

            <li>
                <router-link to="/addsample" class="context-menu__link">
                    <i class="fa fa-plus menu_icon" aria-hidden="true"> </i>
                    Add New Sample
                </router-link>
            </li>

            <hr>
            <hr>

            <li>
                <router-link to="/themes" class="context-menu__link">
                    <i class="fa fa-trophy menu_icon" aria-hidden="true"> </i>
                    Themes
                </router-link>
            </li>

            <li>
                <router-link to="/security-level" class="context-menu__link">
                    <i class="fa fa-exclamation-triangle menu_icon" aria-hidden="true"> </i>
                    Security Level
                </router-link>
            </li>

            <li>
                <router-link to="/quantity-type" class="context-menu__link">
                    <i class="fas fa-balance-scale menu_icon" aria-hidden="true"></i>
                    Quantity Type
                </router-link>
            </li>

            <li>
                <router-link to="/lab" class="context-menu__link">
                    <i class="fa fa-building menu_icon" aria-hidden="true"></i>
                    Labs
                </router-link>
            </li>

            <li>
                <router-link to="/freezer" class="context-menu__link">
                    <i class="fas fa-snowflake menu_icon"></i>
                    Freezer
                </router-link>
            </li>


            <li>
                <router-link to="/chamber" class="context-menu__link">
                    <i class="fas fa-bars menu_icon"></i>
                    Chamber
                </router-link>
            </li>


        </ul>
    </nav>
</template>

<script>

export default {
    name: 'side-menu',
    contentSection: '',

    methods: {
        openProjectLink() {
            alert('You need to log in');
        },

        highlightSection(section) {
            return {
                'menu__link': true,
                'menu__link--active': section === this.contentSection,
            };
        },
    },
};
</script>
