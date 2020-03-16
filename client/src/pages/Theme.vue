<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <!--                <h1> {{page_title}} </h1>-->
                <!--                <hr>-->
                <!--                <br> <br>-->
                <b-button class="float_btn" v-b-modal.modal-theme variant="primary"> Add Theme</b-button>
                <br> <br>
                <table class=" table table-hover">
                    <thead>
                    <tr>
                        <th scope="col"> Name</th>
                        <th scope="col"> Code</th>
                        <th scope="col"> Update</th>
                        <th scope="col"> Delete</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="theme.id" v-for="theme in response.message">
                        <td> {{ theme.name }}</td>
                        <td> {{ theme.code }}</td>

                        <td>
                            <button @click="formSubmit" class="btn btn-warning btn-sm" type="button"> Update</button>
                            <!--                            <p><span class="glyphicon glyphicon-pencil"></span></p>-->
                            <!--                                        <button type="button" class="btn btn-default btn-sm">-->
                            <!--          <span class="glyphicon glyphicon-pencil"></span> Pencil-->
                            <!--        </button>-->
                            <!--                        </td>-->
                        <td>
                            <button @click="deleteTheme(name)" class="btn btn-danger btn-sm" type="button"> Delete
                            </button>
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

            deleteTheme: function(name) {
    axios.delete('localhost:5000/theme'/+name)
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
};
</script>
