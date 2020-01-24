<template>
    <div class="container-fluid">
     <div class="row">
     <div class="col-sm-12">

         <h1> Themes </h1>
         <hr>  <br> <br>
         <b-button v-b-modal.modal-theme.lg variant="primary"> Add Theme </b-button>
     <br> <br>
  <table class=" table table-hover">
   <thead>
     <tr>
         <th scope="col"> Name </th>
         <th scope="col"> Code </th>
         <th scope="col"> Update </th>
         <th scope="col"> Delete </th>
       </tr>
   </thead>
   <tbody>
     <tr v-for="theme in response.message" :key="theme.id">
<!--        <p> {{ value }} </p>-->
        <td> {{ theme.name }} </td>
        <td> {{ theme.code }} </td>

         <td><button type="button" class="btn btn-warning btn-sm"> Update </button></td>
         <td ><button @click="deleteTheme(name)" type="button" class="btn btn-danger btn-sm" > Delete </button> </td>
     </tr>
   </tbody>

 </table>
     </div>
    <b-modal
        id="modal-theme"
        ref="modal">

             <form @submit="formSubmit">

                   <b-form-group id="form-name-group" label="Name:" label-for="form-name-input">
                    <b-form-input
                      id="form-name-input"
                      type="text"
                      v-model="name"
                      placeholder="Enter Name"
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
                    <b-form-input
                      id="form-code-input"
                      type="text"
                      v-model="code"
                      placeholder="Enter Code"
                    > </b-form-input>
                  </b-form-group>

         <div class="btn-group" role="group">
                     <b-button type="submit" variant="primary"> Submit </b-button> <br>
                     <b-button type="reset" variant="danger"> Reset </b-button>
                    </div>
        </form>
    </b-modal>
    </div>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Theme',
  data() {
    return {
      response: [],
      name: '',
      code: '',
    };
  },
  methods: {
    getTheme() {
      const path = 'http://localhost:5000/theme';
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
            axios.post('http://localhost:5000/sample' || 'http://localhost:5000/samples', {
            name: this.name,
            code: this.code,
       })
            .then(function (response) {
            currentObj.output = response.data;
            })
            .catch(function (error) {
            currentObj.output = error;
            });
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
