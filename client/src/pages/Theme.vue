<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title"></top-nav>

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
                    <tr :key="theme.id" v-for="(theme, index) in response.message">
                        <td> {{ index + 1 }}</td>
                        <td> {{ theme.name }}</td>
                        <td> {{ theme.code }}</td>

                        <td>
                            <b-icon
                                    icon="pencil" font-scale="2.0"
                                    class="border border-info rounded" variant="info"
                                    v-b-tooltip.hover :title="`Update ${ theme.name }`"
                                    v-b-modal.modal-theme-edit
                                    @mouseover="fillFormForUpdate(theme.name, theme.code)"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    icon="trash" font-scale="1.85"
                                    class="border rounded bg-danger p-1" variant="light"
                                    v-b-tooltip.hover :title="`Delete ${theme.name}!`"
                                    @click="deleteTheme(theme.code)"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>

            <div v-if="!isEditing">
                <b-modal
                        title="Add Theme"
                        id="modal-theme"
                        ok-title="Save"
                        cancel-variant="danger"
                        @ok="createTheme"
                        @submit="showModal = false"
                        @hidden="clearForm"
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
                        title="Edit Theme"
                        @ok="updateTheme(old_code)"
                        @submit="showModal = false"
                        id="modal-theme-edit"
                        ok-title="Update"
                        cancel-variant="danger"
                        @hidden="clearForm"
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
    import theme_resource from '../../src/utils/api_paths'
    import TopNav from "@/components/TopNav";

    export default {
        name: 'Theme',
        data() {
            return {
                page_title: "Themes",
                response: [],
                name: null,
                code: null,

                // values for data modification
                old_code: null,
                showModal: true,
                isEditing: false,
            };
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
                const path = theme_resource;
                axios.get(path)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " " + res.data['message']);
                        this.response = res.data;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        this.$log.error(error);
                    });
            },

            createTheme: function () {
                axios.post(theme_resource, {
                    name: this.name,
                    code: this.code,
                })
                    .then((response) => {
                        this.getTheme();
                        this.clearForm();
                        this.flashMessage.show({
                            status: 'success',
                            title: response.data['message'], message: ""
                        });
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 409) {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Error",
                                    message: error.response.data['message']
                                });
                            } else {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Error",
                                    message: "Theme name already exists"
                                });
                            }
                        }
                    });
                this.clearForm();
            },

            updateTheme: function (code) {
                axios.put(theme_resource, {
                        name: this.name,
                        code: this.code,
                    }, {headers: {code: code}}
                )
                    .then((response) => {
                        this.getTheme();
                        this.flashMessage.show({
                            status: 'success',
                            title: response.data['message'], message: ""
                        });
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 304) {
                                this.flashMessage.show({
                                    status: 'info',
                                    title: "Info",
                                    message: "Record not modified"
                                });
                            } else {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Error",
                                    message: error.response.data['message']
                                });
                            }
                        }
                    });
                this.clearForm();
            },

            deleteTheme: function (code) {
                axios.delete(theme_resource, {
                    headers: {
                        code: code
                    }
                })
                    .then((response) => {
                        this.getTheme();
                        this.flashMessage.show({
                            status: 'success',
                            title: response.data['message'], message: ""
                        });
                    })
                    .catch((error) => {
                        console.log(error);
                        this.flashMessage.show({
                            status: 'error',
                            title: error, message: ""
                        });
                    });
            },
        },
        created() {
            this.getTheme();
            // this.$log.info('Test Logging')
        },
        components: {TopNav}
    };
</script>
