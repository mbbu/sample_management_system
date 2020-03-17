<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title"></top-nav>

                <FlashMessage></FlashMessage>
                <b-button class="float_btn" v-b-modal.modal-theme variant="primary">Add Theme</b-button>

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
                                    v-b-tooltip.hover :title="`Update ${theme.name}`"
                                    v-b-modal.modal-theme

                            ></b-icon>
                            <!--                            @click="fillFormForUpdate(theme.name, theme.code)"-->
                            <!--                            @click="updateTheme(theme.code)"-->
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

            <b-modal @ok="createTheme"
                     @submit="showModal = false"
                     id="modal-theme"
                     ok-title="Save"
                     cancel-variant="danger"
                     title="Add Theme"
                     v-if="showModal"
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
    </div>
</template>

<script>
    import axios from 'axios';
    import theme_resource from '../../src/utils/api_paths'
    import TopNav from "@/components/TopNav";

    export default {
        name: 'Theme',
        page_title: "Themes",
        data() {
            return {
                page_title: "Themes",
                response: [],
                name: null,
                code: null,
                showModal: true,
            };
        },
        methods: {
            clearForm() {
                this.name = null;
                this.code = null
            },

            fillFormForUpdate(name, code) {
                this.name = name;
                this.code = code;
                this.showModal = true;
            },

            getTheme() {
                const path = theme_resource;
                axios.get(path)
                    .then((res) => {
                        this.response = res.data;
                        console.log(res.data);
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
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
                    .catch((error, response) => {
                        console.log(error);
                        this.flashMessage.show({
                            status: 'error',
                            title: error, message: response.data['message']
                        });
                    });
            },

            updateTheme: function (code) {
                this.fillFormForUpdate(this.name, this.code);
                axios.put(theme_resource, {
                    headers: {
                        code: code
                    },
                    name: this.name,
                    code: this.code,
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
        },

        components: {TopNav}
    };
</script>
