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
                    <b-icon icon="house-fill" font-scale="1.8"></b-icon>
                    Home
                </router-link>
            </li>

            <li>
                <router-link to="/sample" class="context-menu__link">
                    <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
                    <b-icon icon="search" font-scale="1.5"></b-icon>
                    Search Samples
                </router-link>
            </li>

            <li>
                <a href="https://redcap.icipe.org/surveys/?s=W7A7TFJ89J" class="context-menu__link">
                    <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
                    <b-icon icon="inbox" font-scale="1.5"></b-icon>
                    Request Sample </a>
            </li>

            <li>
                <router-link to="/addsample" class="context-menu__link">
                    <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
                    <b-icon icon="plus" font-scale="1.5"></b-icon>
                    Add New Sample
                </router-link>
            </li>

            <hr>
            <hr>

            <li>
                <router-link to="/themes" class="context-menu__link">
                    <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
                    <b-icon icon="trophy" font-scale="1.5"></b-icon>
                    Themes
                </router-link>
            </li>

            <li>
                <router-link to="/security-level" class="context-menu__link">
                    <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
                    <b-icon icon="exclamation-triangle" font-scale="1.5"></b-icon>
                    Security Level
                </router-link>
            </li>

            <li>
                <router-link to="/quantity-type" class="context-menu__link">
                    <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
                    <b-icon icon="bucket" font-scale="1.5"></b-icon>
                    Quantity Type
                </router-link>
            </li>

            <li>
                <router-link to="/lab" class="context-menu__link">
                    <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
                    <b-icon icon="house-door" font-scale="1.5"></b-icon>
                    Labs
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
