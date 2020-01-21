<template>
    <div class="container-fluid">
     <div class="row">
     <div class="col-sm-12">

         <h1> Samples </h1>
         <hr>  <br> <br>
         <b-button v-b-modal.modal-sample.lg variant="primary"> Add Sample </b-button>
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
    <b-modal
        id="modal-sample"
        ref="modal">

             <form @submit="formSubmit">
                   <span> Please select a Theme </span>
                    <b-form-select v-model="theme" class="mb-3" id="theme-dropdown">
                    <option :value="null">Please select a Theme</option>
                    <option value="Plant Health"> Plant Health</option>
                    <option value="Animal Health" > Animal Health </option>
                    <option value="Environmental Health" > Environmental Health </option>
                    <option value="Human Health" > Human Health </option>
                    </b-form-select>

                   <b-form-group id="form-lab-group" label="Lab:" label-for="form-lab-input">
                    <b-form-input
                      id="form-lab-input"
                      type="text"
                      v-model="lab"
                      placeholder="Enter Laboratory"
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-freezer-group" label="Freezer:" label-for="form-freezer-input">
                    <b-form-input
                      id="form-freezer-input"
                      type="text"
                      v-model="freezer"
                      placeholder="Enter Freezer"
                    > </b-form-input>
                  </b-form-group>

                    <span> Please select the chamber </span>
                    <b-form-select v-model="chamber" class="mb-3" id="form-quantity-dropdown">
                    <option :value="null">Chamber</option>
                    <option value="Middle"> Middle</option>
                    <option value="Top" > Top </option>
                    <option value="Bottom" > Bottom </option>
                    </b-form-select>

                    <b-form-group id="form-rack-group" label="Rack:" label-for="form-rack-input">
                    <b-form-input
                      id="form-rack-input"
                      type="number" min="0"
                      v-model="rack"
                      placeholder="Enter Rack"
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-tray-group" label="Tray:" label-for="form-tray-input">
                    <b-form-input
                      id="form-tray-input"
                      type="number" min="0"
                      v-model="tray"
                      placeholder="Enter Rack"
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-box-group" label="Box:" label-for="form-box-input">
                    <b-form-input
                      id="form-box-input"
                      type="number" min="0"
                      v-model="box"
                      placeholder="Enter Box"
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-species-group" label="Sample Species:" label-for="form-species-input">
                    <b-form-input
                      id="form-species-input"
                      type="text"
                      v-model="species"
                      placeholder="Enter Species"
                    > </b-form-input>
                  </b-form-group>


                    <b-form-group id="form-sampleType-group" label="Sample Type:" label-for="form-sampleType-input">
                    <b-form-input
                      id="form-sampleType-input"
                      type="text"
                      v-model="sampleType"
                      placeholder="Enter Sample Type"
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-description-group" label="Sample description:" label-for="form-description-input">
                    <b-form-input
                      id="form-description-input"
                      type="text"
                      v-model="description"
                      placeholder="Enter description"
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-locationCollected-group" label="Location collected:" label-for="form-locationCollected-input">
                    <b-form-input
                      id="form-locationCollected-input"
                      type="text"
                      v-model="locationCollected"
                      placeholder="Enter Location Collected"
                    > </b-form-input>
                  </b-form-group>

                    <span> Enter Project Name </span>
                    <b-form-select v-model="project" class="mb-3" id="form-project-name" label="Enter Project Name">
                    <option :value="null">Please select your project</option>
                    <option value="H3Bionet"> H3Bionet</option>
                    <option value="IENBit" >IENBit</option>
                    <option value="Tsetse Launch" >Tsetse Launch</option>
                    <option value="Africa Now" >Africa Now </option>
                    </b-form-select>

                    <b-form-group id="form-projectOwner-group" label="Project Owner:" label-for="form-projectOwner-input">
                    <b-form-input
                      id="form-projectOwner-input"
                      type="text"
                      v-model="projectOwner"
                      placeholder="Enter Project Owner"
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-retention-group" label="Retention:" label-for="form-retention-input">
                    <b-form-input
                      id="form-retention-input"
                      type="number" min="0"
                      v-model="retention"
                      placeholder="Enter retention period in months "
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-barcode-group" label="Barcode:" label-for="form-barcode-input">
                    <b-form-input
                      id="form-barcode-input"
                      type="text"
                      v-model="barcode"
                      placeholder="Enter barcode number "
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-analysis-group" label="Analysis:" label-for="form-analysis-input">
                    <b-form-input
                      id="form-analysis-input"
                      type="text"
                      v-model="analysis"
                      placeholder="Enter analysis carried out "
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-temperature-group" label="Temperature:" label-for="form-temperature-input">
                    <b-form-input
                      id="form-temperature-input"
                      type="number"
                      v-model="temperature"
                      placeholder="Enter temperature "
                    > </b-form-input>
                  </b-form-group>


                    <b-form-group id="form-amount-group" label="Amount:" label-for="form-amount-input">
                    <b-form-input
                      id="form-amount-input"
                      type="number" min="0"
                      v-model="amount"
                      placeholder="Enter amount of sample "
                    > </b-form-input>
                  </b-form-group>


                    <span> Please select the quantity type </span>
                    <b-form-select v-model="quantity" class="mb-3" id="form-quantity-dropdown">
                    <option :value="null">Please select the quantity type</option>
                    <option value="ML"> ML</option>
                    <option value="Meters" > Meters </option>
                    <option value="Kilograms" > Kilograms </option>
                    <option value="Actual Number" > Actual Number</option>
                    </b-form-select>

                    <span> Add Security Level Needed </span>
                    <b-form-select v-model="securityLevel" class="mb-3" id="form-securityLevel-dropdown">
                    <option :value="null">Please select the security level</option>
                    <option value="High"> High </option>
                    <option value="Medium" > Medium </option>
                    <option value="Low" > Low </option>
                    </b-form-select>

                    <div class="btn-group" role="group">
                     <b-button type="submit" variant="primary"> Submit </b-button>
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
    data() {
        return {
            response: [],
            theme: '',
            lab: '',
            freezer:'',
            chamber:'',
            rack: '',
            tray: '',
            box: '',
            species: '',
            sampleType: '',
            description: '',
            locationCollected: '',
            project: '',
            projectOwner: '',
            retention: '',
            barcode: '',
            analysis: '',
            temperature: '',
            amount: '',
            quantity: '',
            securityLevel: '',
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
            quantity: this.quantity,
            security_level: this.securityLevel,

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
