<template>
  <div id="sampleForm">
  <b-container>
    <form-wizard title="Sample Data Form" subtitle="Kindly input the correct information" @submit.prevent="handleSubmit" >
        <tab-content title="Sample Details">

                   <label for="theme"> Please select a Theme </label>
                   <div class="form">
                     <select v-model="sample.theme" id="theme" name="theme" class="form-control" :class="{ 'is-invlaid' : submitted && $v.sample.theme.$error }" >
                    <option value="1"> Plant Health</option>
                    <option value="2" > Animal Health </option>
                    <option value="3" > Environmental Health </option>
                    <option value="4" > Human Health </option>
                     </select>
                     <span v-if="!$v.sample.theme.required"> Theme is required </span>
                     <span v-if="!$v.sample.theme.theme"> Select one </span>
                   </div>
                    
                    <div class="form-group">
                      <div class="form">
                        <label for="projectOwner"> Project Owner</label>
                        <input type="text" v-model="sample.projectOwner" id="projectOwner" class="form-control" :class="{ 'is-invalid': submitted && $sample.projectOwner.$error}" />
                        <div v-if="submitted && !v.sample.projectOwner.required" class="invalid-feedback"> Project owner is required </div> 
                      </div>
                    </div>

                    <div class="form-group">
                      <div class="form">
                        <label for="sampleType"> Sample Type</label>
                        <input type="text" v-model="sample.sampleType" id="sampleType" class="form-control" :class="{ 'is-invalid': submitted && $sample.sampleType.$error}" />
                        <div v-if="submitted && !v.sample.sampleType.required" class="invalid-feedback"> Sample Type is required </div> 
                      </div>
                    </div>

                    <div class="form-group">
                      <div class="form">
                        <label for="species"> Species</label>
                        <input type="text" v-model="sample.species" id="species" class="form-control" :class="{ 'is-invalid': submitted && $sample.species.$error}" />
                        <div v-if="submitted && !v.sample.species.required" class="invalid-feedback"> Species is required </div> 
                      </div>
                    </div>

                    <div class="form-group">
                      <div class="form">
                        <label for="description"> Description</label>
                        <input type="text" v-model="sample.description" id="description" class="form-control" :class="{ 'is-invalid': submitted && $sample.description.$error}" />
                        <div v-if="submitted && !v.sample.description.required" class="invalid-feedback"> Description is required </div> 
                        <span v-if="!$sample.description.required"> Description is required </span>
                        <span v-if="!$sample.description.minLength"> Description must be at least 25 words </span>
                      </div>
                    </div>
                      
        </tab-content>

         <tab-content title="Sample Location in Institution" >



                  <b-form-group id="form-locationCollected-group" label="Location collected:" label-for="form-locationCollected-input">
                    <b-form-input
                      id="form-locationCollected-input"
                      type="text" required 
                      v-model="locationCollected" 
                      label="Enter Location Collected"
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-lab-group" label="Lab:" label-for="form-lab-input">
                        <b-form-input
                            id="form-lab-input"
                            type="text"
                            v-model="lab" 
                            label="Enter Laboratory"
                         > </b-form-input>
                    </b-form-group>

                  <b-row>
                       <b-col>
                               <b-form-group id="form-freezer-group" label="Freezer:" label-for="form-freezer-input">
                                <b-form-input
                                id="form-freezer-input"
                                type="text"
                                v-model="freezer" 
                                label="Enter Freezer"
                                > </b-form-input>
                                </b-form-group>
                       </b-col>

                        <b-col>
                                <span> Please select the chamber </span>
                                <b-form-select data-vv-scope="step2" class="field" id="chamber">
                                <option :value="null">Chamber</option>
                                <option value="Middle"> Middle</option>
                                <option value="Top" > Top </option>
                                <option value="Bottom" > Bottom </option>
                                </b-form-select> 
                        </b-col>
                    </b-row>

                     <b-row>
                          <b-col>
                            <b-form-group id="form-rack-group" label="Rack:" label-for="form-rack-input">
                            <b-form-input
                            id="form-rack-input"
                            type="number" min="0"
                            v-model="rack" 
                            label="Enter Rack"
                            > </b-form-input>
                           </b-form-group>
                        </b-col>

                        <b-col>
                            <b-form-group id="form-tray-group" label="Tray:" label-for="form-tray-input">
                            <b-form-input
                            id="form-tray-input"
                            type="number" min="0"
                            v-model="tray" 
                            label="Enter Rack"
                            > </b-form-input>
                         </b-form-group>
                        </b-col>

                        <b-col>
                            <b-form-group id="form-box-group" label="Box:" label-for="form-box-input">
                            <b-form-input
                            id="form-box-input"
                            type="number" min="0"
                            v-model="box" 
                            label="Enter Box"
                            > </b-form-input>
                            </b-form-group>
                      </b-col>

                    </b-row>

                   <b-row>
                        <b-col> 
                            <b-form-group id="form-temperature-group" label="Temperature:" label-for="form-temperature-input">
                            <b-form-input
                            id="form-temperature-input"
                            type="number"
                            v-model="temperature" 
                            label="Enter temperature "
                            > </b-form-input>
                          </b-form-group>
                        </b-col>

                        <b-col>
                            <b-form-group id="form-amount-group" label="Amount:" label-for="form-amount-input">
                            <b-form-input
                            id="form-amount-input"
                            type="number" min="0"
                            v-model="amount" 
                            label="Enter amount of sample "
                            > </b-form-input>
                          </b-form-group>
                        </b-col>

                        <b-col>
                             <span> Please select the quantity type </span>
                            <b-form-select v-model="quantity_type" class="mb-3" id="form-quantity-dropdown">
                            <option :value="null">Please select the quantity type</option>
                            <option value="ML"> ML</option>
                            <option value="Meters" > Meters </option>
                            <option value="Kilograms" > Kilograms </option>
                            <option value="Actual Number" > Actual Number</option>
                            </b-form-select>
                        </b-col>
                    </b-row>
         </tab-content>


          <tab-content title="Finishing Up" >
            
                   <span> Add Security Level Needed </span>
                    <b-form-select v-model="securityLevel"  class="mb-3" id="form-securityLevel-dropdown">
                    <option :value="null">Please select the security level</option>
                    <option value="High"> High </option>
                    <option value="Medium" > Medium </option>
                    <option value="Low" > Low </option>
                    </b-form-select>

                    <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
                    <b-form-input
                      id="form-code-input"
                      type="number" min="0"
                      v-model="code" 
                      label="Enter code "
                    > </b-form-input>
                  </b-form-group>

                  <b-form-group id="form-barcode-group" label="Barcode:" label-for="form-barcode-input">
                    <b-form-input
                      id="form-barcode-input"
                      type="text"
                      v-model="barcode" 
                      label="Enter barcode number "
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-analysis-group" label="Analysis:" label-for="form-analysis-input">
                    <b-form-input
                      id="form-analysis-input"
                      type="text"
                      v-model="analysis" 
                      label="Enter analysis carried out "
                    > </b-form-input>
                  </b-form-group>
             

                    <b-form-group id="form-retention-group" label="Retention:" label-for="form-retention-input">
                    <b-form-input
                      id="form-retention-input"
                      type="number" min="0"
                      v-model="retention" 
                      label="Enter retention period in months "
                    > </b-form-input>
                  </b-form-group>

          </tab-content>

           <template slot="footer" scope="props">
            <div class=wizard-footer-left>
                <wizard-button  v-if="props.activeTabIndex > 0 && !props.isLastStep" :style="props.fillButtonStyle">Previous</wizard-button>
            </div>
            
              <div class="wizard-footer-right">
                <wizard-button v-if="!props.isLastStep" @click.native="props.nextTab()" class="wizard-footer-right" :style="props.fillButtonStyle">Next</wizard-button>
                
                <wizard-button v-else @click.native="formSubmit" class="wizard-footer-right finish-button" :style="props.fillButtonStyle">{{props.isLastStep ? 'Done' : 'Next'}}</wizard-button>
              </div>
          </template> 
          </form-wizard>
  </b-container>
  </div>
</template>

<script>
import Vue from 'vue';
import VueFormWizard, { TabContent } from 'vue-form-wizard';
import 'vue-form-wizard/dist/vue-form-wizard.min.css'
import { required, minLength } from "vuelidate/lib/validators";
import axios from 'axios';

Vue.use(VueFormWizard)
Vue.use(TabContent)

export default {
  name: "sampleForm",
     
  data() {
    return {
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
            terms: "",
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
        lab: { required } ,
        freezer: { required } ,


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
};


</script>
