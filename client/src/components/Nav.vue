<template>
    <div class="menu-container">
        <ul class="menu">
            <li class="menu__top">
                <router-link to="/index" class="menu__logo">
                    <img :src="require('../assets/logo.png')" />
                </router-link>
            </li>

            <li>
            <router-link to="/home" class="context-menu__link"> 
            <i class="fa fa-home menu__icon" aria-hidden="true"> </i>  
            Home </router-link> 
            </li>

            <li>
            <router-link to="/sample" class="context-menu__link"> 
            <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
             Search Samples </router-link>
            </li>

            <li>
            <a href="https://redcap.icipe.org/surveys/?s=W7A7TFJ89J" class="context-menu__link"> 
            <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
             Sample Requests </a>
            </li>

            <li>
            <router-link to="/addsample" class="context-menu__link"> 
            <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
             Add New Sample </router-link></li>

            <li>
             <router-link to="/updateprofile" class="context-menu__link"> 
            <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
            Update Profile </router-link></li>


        </ul>
    </div>
</template>

<script>

export default {
        contentSection: '',
        name: 'Menu',
        

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
