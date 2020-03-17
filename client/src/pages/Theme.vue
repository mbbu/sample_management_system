<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title"></top-nav>

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
                                    v-b-tooltip.hover title="Update Item"
                                    @click="formSubmit"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    icon="trash" font-scale="1.85"
                                    class="border rounded bg-danger p-1" variant="light"
                                    v-b-tooltip.hover title="Delete Item!"
                                    @click="deleteTheme(code)"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>

            <b-modal @ok="formSubmit"
                     @submit="showModal = false"
                     id="modal-theme"
                     ok-title="Save"
                     cancel-variant="danger"
                     title="Add Theme"
                     v-if="showModal">

                <form @submit.prevent="formSubmit">

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

            formSubmit(e) {
                e.preventDefault();
                let currentObj = this;
                axios.post(theme_resource, {
                    name: this.name,
                    code: this.code,
                })
                    .then(function (response) {
                        currentObj.output = response.data;
                    })
                    .catch(function (error) {
                        currentObj.output = error;
                    });
                this.clearForm();
                this.showModal = false;
                this.getTheme();
            },

            deleteTheme: function (code) {
                axios.delete('localhost:5000/theme' / +code)
                    .then((response) => {
                        this.getTheme();
                        console.log(response)
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            },
        },
        created() {
            this.getTheme();
        },

        components: {TopNav}
    };
</script>
