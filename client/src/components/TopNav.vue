<template>
    <div>
        <mdb-navbar class="top-nav" dark position="top" scrolling>
            <mdb-navbar-brand href="#">
                <router-link to="/index">
                    <img :src="getCompanyLogo()" alt="Logo" class="menu_logo"/>
                </router-link>
            </mdb-navbar-brand>
            <mdb-navbar-nav>
                <mdb-nav-item class="item_title" href="#" waves-fixed><h2> {{ page_title }} </h2></mdb-nav-item>
            </mdb-navbar-nav>
            <mdb-navbar-toggler>
                <mdb-navbar-nav></mdb-navbar-nav>
                <mdb-form-inline>
                    <mdb-input @change="getSearchQuery()" aria-label="Search" class="mr-sm-2" id="search"
                               placeholder="Search"
                               type="text" v-model="search_query"/>
                    <mdb-btn class="my-0" outline="white" size="sm" type="submit">Search
                        <i aria-hidden="true" class="fas fa-search"></i></mdb-btn>
                </mdb-form-inline>

                <div v-if="isAuth === true">
                    <mdb-dropdown class="nav-item item_title" tag="li">
                        <mdb-dropdown-toggle
                                navLink
                                slot="toggle"
                                tag="a"
                                waves-fixed
                        ><i class="fas fa-user fa-2x"></i> {{this.userName}}
                        </mdb-dropdown-toggle
                        >
                        <mdb-dropdown-menu>
                            <mdb-dropdown-item>
                                <i class="far fa-id-badge fa-lg"></i>
                                <router-link to="/user"> Profile</router-link>
                            </mdb-dropdown-item>
                            <mdb-dropdown-item>
                                <i class="fas fa-sign-out-alt fa-lg"></i>
                                <router-link @click.native="signOut" to="#"> Sign Out</router-link>
                            </mdb-dropdown-item>
                        </mdb-dropdown-menu>
                    </mdb-dropdown>
                </div>
                <div v-else-if="isAuth === false">
                    <mdb-dropdown class="nav-item item_title" disabled="true" tag="li">
                        <mdb-dropdown-toggle
                                navLink
                                slot="toggle"
                                tag="a"
                                waves-fixed
                        ><i class="fas fa-user fa-2x"></i>User
                        </mdb-dropdown-toggle>
                        <mdb-dropdown-menu>
                            <mdb-dropdown-item>
                                <router-link to="/login">Login</router-link>
                            </mdb-dropdown-item>
                            <mdb-dropdown-item>
                                <router-link to="/register">Sign Up</router-link>
                            </mdb-dropdown-item>
                        </mdb-dropdown-menu>
                    </mdb-dropdown>
                </div>
            </mdb-navbar-toggler>
        </mdb-navbar>
        <div style="height: 18vh">
            <div class="view intro-2">
                <div class="full-bg-img">
                    <div class="mask rgba-white-strong">
                        <div class="container flex-center">
                            <div class="dark-grey-text">
                                <h2 class="font-weight-bold">

                                </h2>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {getStoredUserDetails, isUserLoggedIn, logOutUser,} from '../utils/util_functions';
    import {
        mdbBtn,
        mdbDropdown,
        mdbDropdownItem,
        mdbDropdownMenu,
        mdbDropdownToggle,
        mdbFormInline,
        mdbInput,
        mdbNavbar,
        mdbNavbarBrand,
        mdbNavbarNav,
        mdbNavbarToggler,
        mdbNavItem
    } from 'mdbvue'
    import EventBus from '../components/EventBus';

    export default {
        name: 'top-nav',
        props: {
            page_title: {
                type: String,
                required: true,
            },
            search_query: {
                type: String,
                required: false,
            }
        },
        data() {
            return {
                userName: null,
                isAuth: null,
            }
        },
        methods: {
            getCompanyLogo() {
                return require('../assets/logo.png')
            },
            getUser() {
                this.isAuth = isUserLoggedIn()
                if (this.isAuth === true) {
                    let user = getStoredUserDetails()
                    this.userName = user['first_name']
                } else {
                    this.userName = null
                }
            },

            getSearchQuery() {
                let query = document.getElementById('search').value;
                EventBus.$emit('searchQuery', query);
            },

            signOut() {
                return logOutUser(this)
            }
        },
        components: {
            mdbInput, mdbNavbar, mdbNavbarBrand, mdbNavbarToggler, mdbNavbarNav, mdbNavItem,
            mdbDropdown, mdbDropdownMenu, mdbDropdownItem, mdbDropdownToggle, mdbFormInline,
            mdbBtn
        },
        created() {
            this.getUser()
        }
    }
</script>
