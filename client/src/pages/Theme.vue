<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title" v-bind:search_query="search"></top-nav>

                <FlashMessage :position="'center bottom'"></FlashMessage>
                <br> <br>
                <table class=" table table-hover">
                    <thead>
                    <tr>
                        <th scope="col"> Id</th>
                        <th scope="col"> Name</th>
                        <th scope="col"> Code</th>
                        <th scope="col"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="theme.id" v-for="(theme, index) in filteredList">
                        <td> {{ index + 1 }}</td>
                        <td> {{ theme.name }}</td>
                        <td> {{ theme.code }}</td>

                        <td>
                            <b-icon
                                    :title="`Update ${ theme.name }`"
                                    @mouseover="fillFormForUpdate(theme.name, theme.code)"
                                    class="border border-info rounded" font-scale="2.0"
                                    icon="pencil" v-b-modal.modal-theme-edit
                                    v-b-tooltip.hover
                                    variant="info"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    :title="`Delete ${theme.name}!`" @click="deleteTheme(theme.code)"
                                    class="border rounded bg-danger p-1" font-scale="1.85"
                                    icon="trash" v-b-tooltip.hover
                                    variant="light"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>

            <div v-if="!isEditing">
                <b-modal
                        @hidden="clearForm"
                        @ok="createTheme"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-theme"
                        ok-title="Save"
                        title="Add Theme"
                >
                    <form @submit.prevent="createTheme">

                        <b-form-group id="form-name-group" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Name"
                                    required="true"
                                    type="text"
                                    v-model="name"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required="true"
                                    type="text"
                                    v-model="code"></b-form-input>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>

            <div v-else-if="isEditing">
                <b-modal
                        @hidden="clearForm"
                        @ok="updateTheme(old_code)"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-theme-edit"
                        ok-title="Update"
                        title="Edit Theme"
                >
                    <form>

                        <b-form-group id="form-name-group-edit" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Name"
                                    required="true"
                                    type="text"
                                    v-model="name"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required="true"
                                    type="text"
                                    v-model="code"></b-form-input>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
            <b-button class="float_btn"
                      v-b-modal.modal-theme variant="primary"
            >Add Theme
            </b-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import {theme_resource} from '../utils/api_paths'
    import TopNav from "../components/TopNav";
    import {respondTo401, secureStoreGetString, showFlashMessage} from '../utils/util_functions'
    import EventBus from '../components/EventBus';

    export default {
        name: 'Theme',
        data() {
            return {
                page_title: "Themes",
                response: [],
                name: null,
                code: null,
                search: '',
                themeList: [],

                // values for data modification
                old_code: null,
                showModal: true,
                isEditing: false,
            };
        },

        mounted() {
            EventBus.$on('searchQuery', (payload) => {
                this.search = payload
                this.filteredList()
            })
        },

        computed: {
            filteredList() {
                return this.themeList.filter(theme => {
                    console.log("SEARCH: " + this.search);
                    return theme.name.toLowerCase().includes(this.search.toLowerCase())
                })
            }
        },

        methods: {
            clearForm() {
                this.name = null;
                this.code = null;
                this.isEditing = false;
            },

            fillFormForUpdate(name, code) {
                this.name = name;
                this.code = code;
                this.old_code = code;
                this.isEditing = true;
                this.showModal = true;
            },

            getTheme() {
                axios.get(theme_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " " + res.data['message']);
                        this.response = res.data;
                        this.themeList = this.response.message
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        this.$log.error(error);
                    });
            },

            createTheme: function () {
                let self = this;
                axios.post(theme_resource, {
                    name: this.name,
                    code: this.code,
                }, {
                    headers: {
                        Authorization: secureStoreGetString()
                    }
                })
                    .then((response) => {
                        this.getTheme();
                        this.clearForm();
                        showFlashMessage(self, 'success', response.data['message'], '')
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 409) {
                                showFlashMessage(self, 'error', 'Error', error.response.data['message'])
                            } else if (error.response.status === 401) {
                                respondTo401(self);
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', 'Error', error.response.data['message'])
                            }
                        }
                    });
                this.clearForm();
            },

            updateTheme: function (code) {
                let self = this;
                axios.put(theme_resource, {
                    name: this.name,
                    code: this.code,
                }, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getTheme();
                        showFlashMessage(self, 'success', response.data['message'], '')
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 304) {
                                showFlashMessage(self, 'info', 'Info', 'Record not modified!')
                            } else if (error.response.status === 401) {
                                respondTo401(self);
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', 'Error', error.response.data['message'])
                            }
                        }
                    });
                this.clearForm();
            },

            deleteTheme: function (code) {
                let self = this;
                axios.delete(theme_resource, {
                    headers: {
                        code: code,
                        Authorization: secureStoreGetString()
                    }
                })
                    .then((response) => {
                        this.getTheme();
                        showFlashMessage(self, 'success', response.data['message'], '')
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 401) {
                                respondTo401(self);
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', 'Error', error.response.data['message'])
                            }
                        }
                    });
            },
        },
        created() {
            this.getTheme();
        },
        components: {TopNav}
    };
</script>
