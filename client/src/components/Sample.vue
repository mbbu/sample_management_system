<template>
    <div class="container-fluid">
     <div class="row">
     <div class="col-sm-12">

         <h1> Samples </h1>
         <hr>  <br> <br>

         {{ sample }}
         <button type="button" class="btn btn-success btn-sm" v-b-modal.sample-modal> Add Sample </button>
     <br> <br>
     <table class="table table-hover">
         <thead>
             <tr >
             <th scope="col"> Species </th>
             <th scope="col"> Description </th>
             <th scope="col"> Theme </th>
             <th scope="col"> PI </th>
             </tr>
         </thead>

         <tbody>
             <tr v-for="(sample, index) in samples" :key="index">
                 <td> {{ sample.animal_species }} </td>
                 <td> {{ sample.sample_description }} </td>
                 <td> {{ sample.theme.name }} </td>
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


     <b-modal ref="addSampleModal" id="sample-modal" title="Add new Sample">

         <b-form @submit="onSubmit" @reset="onReset" class="w-100">
    
        <b-form-group id="form-theme-group" label="Theme:" label-for="form-theme-input">
        <b-form-input
          id="form-theme-input"
          type ="text"
          v-model="addSampleForm.theme"
          required
          placeholder="Enter Theme"
        > </b-form-input>
      </b-form-group>

       <b-form-group id="form-lab-group" label="Lab:" label-for="form-lab-input">
        <b-form-input
          id="form-lab-input"
          type="text"
          v-model="addSampleForm.lab"
          required
          placeholder="Enter Laboratory"
        > </b-form-input>
      </b-form-group>

        <b-form-group id="form-freezer-group" label="Freezer:" label-for="form-freezer-input">
        <b-form-input
          id="form-freezer-input"
          type="text"
          v-model="addSampleForm.freezer"
          required
          placeholder="Enter Freezer"
        > </b-form-input>
      </b-form-group>

        <span> Please select the chamber </span>
        <b-form-select v-model="selected" class="mb-3" id="form-quantity-dropdown">
        <option :value="null">Chamber</option>
        <option value="a"> Middle</option>
        <option value="b" > Top </option>
        <option value="b" > Bottom </option>
        </b-form-select>

        <b-form-group id="form-rack-group" label="Rack:" label-for="form-rack-input">
        <b-form-input
          id="form-rack-input"
          type="number"
          v-model="addSampleForm.rack"
          required
          placeholder="Enter Rack"
        > </b-form-input>
      </b-form-group>

        <b-form-group id="form-tray-group" label="Tray:" label-for="form-tray-input">
        <b-form-input
          id="form-tray-input"
          type="number"
          v-model="addSampleForm.tray"
          required
          placeholder="Enter Rack"
        > </b-form-input>
      </b-form-group>

        <b-form-group id="form-box-group" label="Box:" label-for="form-box-input">
        <b-form-input
          id="form-box-input"
          type="number"
          v-model="addSampleForm.box"
          required
          placeholder="Enter Box"
        > </b-form-input>
      </b-form-group>

        <b-form-group id="form-species-group" label="Sample Species:" label-for="form-species-input">
        <b-form-input
          id="form-species-input"
          type="text"
          v-model="addSampleForm.species"
          required
          placeholder="Enter Species"
        > </b-form-input>
      </b-form-group>


        <b-form-group id="form-sampleType-group" label="Sample Type:" label-for="form-sampleType-input">
        <b-form-input
          id="form-sampleType-input"
          type="text"
          v-model="addSampleForm.sampleType"
          required
          placeholder="Enter Sample Type"
        > </b-form-input>
      </b-form-group>

        <b-form-group id="form-description-group" label="Sample description:" label-for="form-description-input">
        <b-form-input
          id="form-description-input"
          type="text"
          v-model="addSampleForm.description"
          required
          placeholder="Enter description"
        > </b-form-input>
      </b-form-group>

        <b-form-group id="form-locationCollected-group" label="Location collected:" label-for="form-locationCollected-input">
        <b-form-input
          id="form-locationCollected-input"
          type="text"
          v-model="addSampleForm.locationcollected"
          required
          placeholder="Enter Location Collected"
        > </b-form-input>
      </b-form-group>

        <span> Enter Project Name </span>
        <b-form-select v-model="selected" class="mb-3" id="form-project-dropdown" label="Enter Project Name">
        <option :value="null">Please select your project</option>
        <option value="a"> H3Bionet</option>
        <option value="b" >IENBit</option>
        <option value="b" >Tsetse Launch</option>
        <option value="b" >Africa Now </option>
        </b-form-select>

        <b-form-group id="form-projectOwner-group" label="Project Owner:" label-for="form-projectOwner-input">
        <b-form-input
          id="form-projectOwner-input"
          type="text"
          v-model="addSampleForm.projectOwner"
          required
          placeholder="Enter Project Owner"
        > </b-form-input>
      </b-form-group>

        <b-form-group id="form-retention-group" label="Retention:" label-for="form-retention-input">
        <b-form-input
          id="form-retention-input"
          type="number"
          v-model="addSampleForm.retention"
          required
          placeholder="Enter retention period in months "
        > </b-form-input>
      </b-form-group>

        <b-form-group id="form-barcode-group" label="Barcode:" label-for="form-barcode-input">
        <b-form-input
          id="form-barcode-input"
          type="text"
          v-model="addSampleForm.barcode"
          required
          placeholder="Enter barcode number "
        > </b-form-input>
      </b-form-group>

        <b-form-group id="form-analysis-group" label="Analysis:" label-for="form-analysis-input">
        <b-form-input
          id="form-analysis-input"
          type="text"
          v-model="addSampleForm.analysis"
          required
          placeholder="Enter analysis carried out "
        > </b-form-input>
      </b-form-group>

        <b-form-group id="form-temperature-group" label="Temperature:" label-for="form-temperature-input">
        <b-form-input
          id="form-temperature-input"
          type="number"
          v-model="addSampleForm.temperature"
          required
          placeholder="Enter temperature "
        > </b-form-input>
      </b-form-group>


        <b-form-group id="form-amount-group" label="Amount:" label-for="form-amount-input">
        <b-form-input
          id="form-amount-input"
          type="number"
          v-model="addSampleForm.amount"
          required
          placeholder="Enter amount of sample "
        > </b-form-input>
      </b-form-group>


        <span> Please select the quantity type </span>
        <b-form-select v-model="selected" class="mb-3" id="form-quantity-dropdown">
        <option :value="null">Please select the quantity type</option>
        <option value="a"> ML</option>
        <option value="b" > Meters </option>
        <option value="b" > Kilograms </option>
        <option value="b" > Actual  Number</option>
        </b-form-select>

        <span> Add Security Level Needed </span>
        <b-form-select v-model="selected" class="mb-3" id="form-securityLevel-dropdown">
        <option :value="null">Please select the security level</option>
        <option value="a"> High </option>
        <option value="b" > Medium </option>
        <option value="b" > Low </option>
        </b-form-select>

        <b-button type="submit" variant="primary"> Submit </b-button>
        <b-button type="submit" variant="danger"> Reset </b-button>

    </b-form>
     </b-modal>
    </div>
</div>
</template>


<script>
import axios from 'axios';

export default {
    data() {
        return {
            samples: [],
            addSampleForm: {
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
            },
        };
    },
    methods: {
        getSamples() {
         const path= 'http://localhost:5000/sample'  ;
        axios.get(path)
            .then((res) => {
                this.samples = res.data.samples;
            })
             .catch((error) => {
                 console.error(error);
             });
        },
        addSample(payload) {
            const path = 'http://localhost:5000/sample' || 'http://localhost:5000/samples' ;
            axios.post(path, payload)
            .then(() => {
                this.getSamples();
            })
            .catch((error) => {
                console.log(error);
                this.getSamples();
            });
    },
    initForm() {
        this.addSampleForm.theme ='';
        this.addSampleForm.lab ='';
        this.addSampleForm.freezer ='';
        this.addSampleForm.chamber ='';
        this.addSampleForm.rack ='';
        this.addSampleForm.tray ='';
        this.addSampleForm.box ='';
        this.addSampleForm.species ='';
        this.addSampleForm.sampleType ='';
        this.addSampleForm.description ='';
        this.addSampleForm.locationCollected='';
        this.addSampleForm.project ='';
        this.addSampleForm.projectOwner ='';
        this.addSampleForm.retention ='';
        this.addSampleForm.barcode ='';
        this.addSampleForm.analysis ='';
        this.addSampleForm.temperature ='';
        this.addSampleForm.amount ='';
        this.addSampleForm.quantity ='';
        this.addSampleForm.securityLevel ='';
    },
    onsubmit(evt) {
        evt.preventDefault();
        this.$refs.addSampleModal.hide();
        this.initForm();   
    },
    onReset(evt) {
        evt.preventDefault();
        this.$refs.addSampleModal.hide();
        this.initForm();
    },
    },
    created() {
        this.getSamples();
    },   
};
</script>
