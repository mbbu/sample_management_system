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
         const path= 'http://localhost:5000/sample'  ;
         axios.get(path)
            .then((res) => {
                this.response = res.data;
            })
             .catch((error) => {
                 console.error(error);
             });
        },
        formSubmit(e) {
            e.preventDefault();
            let currentObj = this;
            axios.post('http://localhost:5000/sample' || 'http://localhost:5000/samples', {
            theme: this.theme,
            lab: this.lab,
            freezer: this.freezer,
            chamber: this.chamber,
            rack: this.rack,
            tray: this.tray,
            box: this.box,
            animal_species: this.species,
            sample_type: this.sampleType,
            sample_description: this.description,
            project: this.project,
            project_owner: this.projectOwner,
            retention_period: this.retention,
            barcode: this.barcode,
            analysis: this.analysis,
            temperature: this.temperature,
            amount: this.amount,
            quantity_type: this.quantity_type,
            security_level: this.securityLevel,
            code: this.code,
            })
            .then(function (response) {
            currentObj.output = response.data;
            })
            .catch(function (error) {
            currentObj.output = error;
            });
        },
},
    created() {
    this.getSamples ();
},
};
</script>
