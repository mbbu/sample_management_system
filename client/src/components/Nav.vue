<template>
    <div class="menu-container">
        <ul class="menu">
            <li class="menu__top">
                <router-link to="/" class="menu__logo">
                    <i class="fas fa-user"> </i>
                </router-link>
            </li>

            <li>
            <a href="#"
                @click.prevent="updateMenu('home')"
                :class="highlightSection('home')"
                >
            <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
                Home </a>
            </li>

            <li>
            <a href="#"
                @click.prevent="updateMenu('search_samples')"
                :class="highlightSection('search_samples')"
                >
            <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
                Search Samples </a>
            </li>

            <li>
            <a href="#"
                @click.prevent="updateMenu('sample_requests')"
                :class="highlightSection('sample_requests')"
                >
            <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
                Sample Requests </a>
            </li>

            <li>
            <a href="#"
                @click.prevent="updateMenu('add_sample')"
                :class="highlightSection('add_sample')"
                >
            <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
               Add New Sample </a>
            </li>

            <li>
            <a href="#"
                @click.prevent="updateMenu('update_profile')"
                :class="highlightSection('update_profile')"
                >
            <i class="fa fa-home menu__icon" aria-hidden="true"> </i>
               Update Profile </a>
            </li>


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
