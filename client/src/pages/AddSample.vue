<template>
  <div id="jumbotron">
  <div class="container">
    <form-wizard title="Sample Data Form" subtitle="Kindly input the correct information" @submit.prevent="handleSubmit" >
        <tab-content title="Sample Details" @click.native="handleSubmit" >

                   <label for="theme"> Please select a Theme </label>
                   <div class="form-group">
                     <select v-model="sample.theme" id="theme" name="theme" class="form-control" :class="{ 'is-invlaid' : submitted && $v.sample.theme.$error }" >
                    <option value="1"> Plant Health</option>
                    <option value="2" > Animal Health </option>
                    <option value="3" > Environmental Health </option>
                    <option value="4" > Human Health </option>
                     </select>
                    <div v-if="submitted && $v.sample.theme.$error" class="invaid-feedback">
                     <span v-if="!$v.sample.theme.required"> Theme is required </span>
                     <span v-if="!$v.sample.theme.theme"> Select one </span>
                   </div> </div>
                    
                    <div class="form-group">
                        <label for="projectOwner"> Project Owner</label>
                        <input type="text" v-model="sample.projectOwner" id="projectOwner" class="form-control" :class="{ 'is-invalid': submitted && $sample.projectOwner.$error}" />
                        <div v-if="submitted && !$v.sample.projectOwner.required" class="invalid-feedback"> Project owner is required </div> 
                      </div>

                    <div class="form-group">
                        <label for="sampleType"> Sample Type</label>
                        <input type="text" v-model="sample.sampleType" id="sampleType" class="form-control" :class="{ 'is-invalid': submitted && $sample.sampleType.$error}" />
                        <div v-if="submitted && !$v.sample.sampleType.required" class="invalid-feedback"> Sample Type is required </div> 
                      </div>

                    <div class="form-group">
                        <label for="species"> Species</label>
                        <input type="text" v-model="sample.species" id="species" class="form-control" :class="{ 'is-invalid': submitted && $sample.species.$error}" />
                        <div v-if="submitted && !$v.sample.species.required" class="invalid-feedback"> Species is required </div> 
                      </div>

                    <div class="form-group">
                          <label for="description"> Description</label>
                        <input type="text" v-model="sample.description" id="description" name="description" class="form-control" :class="{ 'is-invalid': submitted && $sample.description.$error}" />
                        <div v-if="submitted && $v.sample.description.$error" class="invalid-feedback"> 
                        <span v-if="!$v.sample.description.required"> Description is required </span>
                        <span v-if="!$v.sample.description.minLength"> Description must be at least 25 words </span>
                    </div> </div> 
                      
        </tab-content>

         <tab-content title="Sample Location in Institution" @click.native="handleSubmit"  >

                  <div class="form-group">
                        <label for="locationCollected">Location Collected</label>
                        <input type="text" v-model="sample.locationCollected" id="locationCollected" class="form-control" :class="{ 'is-invalid': submitted && $sample.locationCollected.$error}" />
                        <div v-if="submitted && !$v.sample.locationCollected" class="invalid-feedback"> 
                        <span v-if="!$v.sample.locationCollected.required"> Location Collected is required </span>
                        <span v-if="!$v.sample.locationCollected.minLength"> Location Collected must be at least 25 words </span>
                      </div> </div>

                  <div class="form-group">
                        <label for="lab">Lab</label>
                        <input type="number" v-model="sample.lab" id="lab" class="form-control" :class="{ 'is-invalid': submitted && $sample.lab.$error}" />
                        <div v-if="submitted && !$v.sample.lab" class="invalid-feedback">  
                        <span v-if="!$v.sample.lab.required"> Lab is required </span>
                        <span v-if="!$v.sample.lab.minValue"> Lab Should be more than zero </span>
                      </div> </div>

                <!-- Start row -->
                  <div class="row">
                    <div class="col">
                  <div class="form-group">
                        <label for="freezer"> Freezer</label>
                        <input type="number" v-model="sample.freezer" id="freezer" class="form-control" :class="{ 'is-invalid': submitted && $sample.freezer.$error}" />
                        <div v-if="submitted && !$v.sample.freezer" class="invalid-feedback"> 
                        <span v-if="!$v.sample.freezer.required"> Freezer is required </span>
                        <span v-if="!$v.sample.freezer.minValue"> Freezer Should be more than zero </span>
                      </div> </div>
                    </div>

                  <div class="col">
                    <label for="chamber"> Please select a Chamber </label>
                   <div class="form">
                     <select v-model="sample.chamber" id="chamber" name="chamber" class="form-control" :class="{ 'is-invlaid' : submitted && $v.sample.chamber.$error }" >
                    <option value="1"> Top</option>
                    <option value="2" > Middle </option>
                    <option value="3" > Bottom </option>
                     </select>
                  <div v-if="submitted && $v.sample.chamber.$error" class="invaid-feedback">
                     <span v-if="!$v.sample.chamber.required"> Chamber is required </span>
                     <span v-if="!$v.sample.chamber.chamber"> Select one </span>
                   </div> </div>

                  </div>
                  
                  </div>
                  
                  <!-- End row -->


                  <!-- Start Row -->
                  <div class="row">
                    <div class="col">
                       <div class="form-group">
                        <label for="freezer"> Rack</label>
                        <input type="number" v-model="sample.rack" id="rack" class="form-control" :class="{ 'is-invalid': submitted && $sample.rack.$error}" />
                        <div v-if="submitted && !$v.sample.rack" class="invalid-feedback">
                        <span v-if="!$v.sample.rack.required"> Rack Collected is required </span>
                        <span v-if="!$v.sample.rack.minValue"> Rack Should be more than zero </span>
                      </div> </div>
                    </div>

                    <div class="col">
                       <div class="form-group">
                        <label for="tray"> Tray</label>
                        <input type="number" v-model="sample.tray" id="tray" class="form-control" :class="{ 'is-invalid': submitted && $sample.tray.$error}" />
                        <div v-if="submitted && !$v.sample.tray" class="invalid-feedback"> 
                        <span v-if="!$v.sample.tray.required"> Tray Collected is required </span>
                        <span v-if="!$v.sample.tray.minValue"> Tray Should be more than zero </span>
                      </div> </div>
                    </div>

                    <div class="col">
                       <div class="form-group">
                        <label for="box"> Box</label>
                        <input type="number" v-model="sample.box" id="box" class="form-control" :class="{ 'is-invalid': submitted && $sample.box.$error}" />
                        <div v-if="submitted && !$v.sample.box" class="invalid-feedback">  
                        <span v-if="!$v.sample.box.required"> Box Collected is required </span>
                        <span v-if="!$v.sample.box.minValue"> Box Should be more than zero </span>
                      </div> </div> 
                    </div>
                  </div>

                  <!-- Start Row -->


                  <!-- Start row -->
                  <div class="row">
                    <div class="col">
                      <div class="form-group">
                        <label for="temperature">Temperature</label>
                        <input type="number" v-model="sample.temperature" id="temperature" class="form-control" :class="{ 'is-invalid': submitted && $sample.temperature.$error}" />
                        <div v-if="submitted && !$v.sample.temperature" class="invalid-feedback"> Temperature Collected is required </div> 
                        </div>

                  </div>

                    <div class="col">
                         <div class="form-group">
                        <label for="amount"> amount</label>
                        <input type="number" v-model="sample.amount" id="amount" class="form-control" :class="{ 'is-invalid': submitted && $sample.amount.$error}" />
                        <div v-if="submitted && !$v.sample.amount" class="invalid-feedback"> 
                        <span v-if="!$v.sample.amount.required"> Amount is required </span>
                        <span v-if="!$v.sample.amount.minValue"> Amount Should be more than zero </span>
                      </div> </div>

                  </div>
                    <div class="col">
                      <label for="theme"> Please select a Quantity Type </label>
                   <div class="form-group">
                     <select v-model="sample.quantity_type" id="quantity_type" name="quantity_type" class="form-control" :class="{ 'is-invlaid' : submitted && $v.sample.quantity_type.$error }" >
                    <option value="1"> MILLILITRES</option>
                    <option value="2" > LITRES </option>
                    <option value="3" > CENTIMETRES </option>
                    <option value="4" > MILIMETER MERCURY </option>
                     </select>
                     <div v-if="submitted && $v.sample.quantity_type.$error" class="invaid-feedback">
                     <span v-if="!$v.sample.quantity_type.required"> Quantity Type is required </span>
                     <span v-if="!$v.sample.quantity_type.quantity_type"> Select one </span>
                   </div> </div>

                  </div>
                  </div>

                  <!-- End Row -->

         </tab-content>


          <tab-content title="Finishing Up" @click.native="handleSubmit" >

                <label for="securityLevel"> Security Level Needed </label>
                  <div class="form-group">
                     <select v-model="sample.securityLevel" id="securityLevel" name="securityLevel" class="form-control" :class="{ 'is-invlaid' : submitted && $v.sample.securityLevel.$error }" >
                    <option value="1"> Low</option>
                    <option value="2" > Meduim </option>
                    <option value="3" > High </option>
                     </select>
                    <div v-if="submitted && $v.sample.securityLevel.$error" class="invaid-feedback">
                     <span v-if="!$v.sample.securityLevel.required"> Security Level is required </span>
                     <span v-if="!$v.sample.securityLevel.securityLevel"> Select one </span>
                   </div> </div>

                    <div class="form-group">
                      <label for="code"> Code</label>
                      <input type="text" v-model="sample.code" id="code" class="form-control" :class="{ 'is-invalid': submitted && $sample.code.$error}" />
                      <div v-if="submitted && !$v.sample.code" class="invalid-feedback"> Code is required </div> 
                    </div>

                    <div class="form-group">
                      <label for="barcode"> Barcode</label>
                      <input type="text" v-model="sample.barcode" id="barcode" class="form-control" :class="{ 'is-invalid': submitted && $sample.barcode.$error}" />
                      <div v-if="submitted && !$v.sample.barcode" class="invalid-feedback"> Barcode is required </div> 
                    </div>

                    <div class="form-group">
                      <label for="analysis"> Analysis</label>
                      <input type="text" v-model="sample.analysis" id="analysis" class="form-control" :class="{ 'is-invalid': submitted && $sample.analysis.$error}" />
                      <div v-if="submitted && !v.sample.analysis" class="invalid-feedback"> Analysis is required </div> 
                    </div>

                    <div class="form-group">
                        <label for="retention"> Retention</label>
                        <input type="number" v-model="sample.retention" id="retention" class="form-control" :class="{ 'is-invalid': submitted && $sample.retention.$error}" />
                        <div v-if="submitted && !$v.sample.retention" class="invalid-feedback">
                        <span v-if="!$v.sample.retention.required"> Retention is required </span>
                        <span v-if="!$v.sample.retention.minValue"> Retention Should be more than zero </span>
                      </div> </div>

          </tab-content>

           <template slot="footer" scope="props">
            <div class=wizard-footer-left>
                <wizard-button  v-if="props.activeTabIndex > 0 && !props.isLastStep" :style="props.fillButtonStyle">Previous</wizard-button>
            </div>
            
              <div class="wizard-footer-right">
                <wizard-button v-if="!props.isLastStep"  @click.native="props.nextTab()" class="wizard-footer-right" :style="props.fillButtonStyle">Next</wizard-button>
                
                <wizard-button v-else @click.native="formSubmit" class="wizard-footer-right finish-button" :style="props.fillButtonStyle">{{props.isLastStep ? 'Done' : 'Next'}}</wizard-button>
              </div>
          </template> 
          </form-wizard>
  </div>
  </div>
</template>

<script>
import Vue from 'vue';
import VueFormWizard, { TabContent } from 'vue-form-wizard';
import 'vue-form-wizard/dist/vue-form-wizard.min.css';
import { required, minLength, minValue } from "vuelidate/lib/validators";
import axios from 'axios';

Vue.use(VueFormWizard)
Vue.use(TabContent)

export default {
  name: "jumbotron",
     
  data() {
    return {
        response: [],
        sample: {
            theme: "",
            project: "",
            projectOwner: "",
            sampleType: "",
            species: "",
            description: "",
            lab: "",
            freezer: "",
            chamber: "",
            rack: "",
            tray: "",
            box: "",   
            locationCollected: "",
            retention: "",
            barcode: "",
            analysis: "",
            temperature: "",
            amount: "",
            quantity_type: "",
            securityLevel: "",
            code: "",
            
      },
      submitted: false     
     };
    },

    validations: {
      sample: {
        theme: { required } ,
        projectOwner: { required } ,
        project: { required } ,
        sampleType: { required } ,
        species: { required } ,
        description: { required, minLength: minLength(25) } ,
        lab: { required, minValue: minValue(0) } ,
        freezer: { required, minValue: minValue(0) } ,
        chamber: {required, minValue: minValue(0)},
        rack: { required, minValue: minValue(0)},
        tray: { required, minValue: minValue(0)},
        box: { required, minValue: minValue(0)},
        locationCollected: {required},
        retention: {required},
        barcode: { required},
        analysis: { required},
        temperature: {required},
        amount: {required, minValue: minValue(0)},
        quantity_type: { required},
        securityLevel: {required},
        code: {required},
      },
    },

  methods : {

        handleSubmit(e) {
          this.submitted = true;

          this.$v.$touch(e);
          if (this.$v.$invalid) {
            return;
          }
        alert ("Sucsess! :-)\n\n" + JSON.stringify(this.sample));

          }
    }, 

         formSubmit(e) {
            e.preventDefault();
            let currentObj = this;
            axios.post('http://localhost:5000/sample' || 'http://localhost:5000/samples', {
            theme: this.sample.theme,
            lab: this.sample.lab,
            freezer: this.sample.freezer,
            chamber: this.sample.chamber,
            rack: this.sample.rack,
            tray: this.sample.tray,
            box: this.sample.box,
            animal_species: this.sample.species,
            sample_type: this.sample.sampleType,
            sample_description: this.sample.description,
            project: this.sample.project,
            project_owner: this.sample.projectOwner,
            retention_period: this.sample.retention,
            barcode: this.sample.barcode,
            analysis: this.sample.analysis,
            temperature: this.sample.temperature,
            amount: this.sample.amount,
            quantity_type: this.sample.quantity_type,
            security_level: this.sample.securityLevel,
            code: this.sample.code,
            })
            .then(function (response) {
            currentObj.output = response.data;
            })
            .catch(function (error) {
            currentObj.output = error;
            });
        },
};


</script>
