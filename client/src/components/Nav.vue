<template>
    <div class="menu-container">
        <ul class="menu">
            <li class="menu_top">
                <router-link to="/index">
                    <img :src="require('../assets/logo.png')" class="menu_logo"/>
                </router-link>
            </li>

            <li>
                <router-link to="/home" class="context-menu__link">
                    <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
                    Home
                </router-link>
            </li>

            <li>
            <router-link to="/sample" class="context-menu__link"> 
            <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
             Search Samples </router-link>
            </li>

            <li>
            <a href="https://redcap.icipe.org/surveys/?s=W7A7TFJ89J" class="context-menu__link"> 
            <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
            Request Sample </a>
            </li>

            <li>
            <router-link to="/addsample" class="context-menu__link"> 
            <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
             Add New Sample </router-link></li>


        </ul>
    </div>
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
