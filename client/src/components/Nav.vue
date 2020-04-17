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
                    <i class="fas fa-vial menu_icon"></i>
                    Samples
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


            <li>
                <router-link to="/rack" class="context-menu__link">
                    <i class="fas fa-box menu_icon"></i>
                    Rack
                </router-link>
            </li>

            <li>
                <router-link to="/tray" class="context-menu__link">
                    <i class="fas fa-th menu_icon"></i>
                    Tray
                </router-link>
            </li>

            <li>
                <router-link to="/box" class="context-menu__link">
                    <i class="fas fa-briefcase menu_icon"></i>
                    Box
                </router-link>
            </li>

            <li>
                <router-link to="/publication" class="context-menu__link">
                    <i class="fas fa-brain menu_icon"></i>
                    Publication
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
