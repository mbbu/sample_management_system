<template>
    <div class="container">
     <div class="row">
     <div class="col-sm-12">

         <h2 style="text-align: center"> Samples </h2>
     <br> <br>
     <table class="table table-hover">
         <thead>
             <tr >
             <th scope="col"> Species </th>
             <th scope="col"> Project </th>
             <th scope="col"> Theme </th>
             <th scope="col"> PI </th>
             </tr>
         </thead>

         <tbody>
             <tr v-for="sample in response.message" :key="sample.id">
                 <td> {{ sample.animal_species }} </td>
                 <td> {{ sample.project }} </td>
                 <td> {{ sample['theme.name'] }} </td>
                 <td> {{ sample.project_owner }} </td>
                     
                 <td>
                     <div class="btn-group" role="group">
                        <button type="button" class="btn btn-warning btn-sm"> Update </button>
                        <button type="button" class="btn btn-danger btn-sm"> Delete </button>
                     </div>
                 </td>
             </tr>

         </tbody>
     </table>
     </div>
            <a href="/addsample">
                <b-button class="float_btn" variant="primary">Add Sample</b-button>
            </a>
     </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        data() {
            return {
                response: [],
            };
        },
        methods: {
            getSamples() {
                const path = 'http://localhost:5000/sample';
                axios.get(path)
                    .then((res) => {
                        this.response = res.data;
                        console.info("Response: ", this.response)
            })
             .catch((error) => {
                 console.error(error);
             });
        },
     created() {
    this.getSamples ();
},
    },
};
</script>
