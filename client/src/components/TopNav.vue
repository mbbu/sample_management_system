<template>
<div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
        <b-navbar-nav class="item_title"><h1>{{ page_title }}</h1></b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">

            <b-nav-form>
                <b-form-input size="sm" class="mr-sm-2"></b-form-input>
                <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
            </b-nav-form>

            <b-nav-item-dropdown right>
                <!-- Using 'button-content' slot -->
                <template v-slot:button-content>
                    <i class="fas fa-user fa-2x"></i> <em>User</em>
                </template>
                <b-dropdown-item>
                    <i class="far fa-id-badge fa-lg"></i>
                    <router-link to="/user"> Profile</router-link>
                </b-dropdown-item>
                <b-dropdown-item>
                    <i class="fas fa-sign-out-alt fa-lg"></i>
                    <router-link to="/home"> Sign Out</router-link>
                </b-dropdown-item>
            </b-nav-item-dropdown>
        </b-navbar-nav>

    </b-navbar>
</div>
</template>

<script>
    export default {
        name: 'top-nav',
        props: {
            page_title: {
                type: String,
                required: true,
            }
        },
    }
</script>
