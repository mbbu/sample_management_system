<template>
  <div id="sampleform">
  <b-container>
    <form-wizard @submit="formSubmit" title="Sample Data Form" subtitle="Kindly input the correct information" >
        <tab-content title="Sample Details">
                   <span> Please select a Theme </span>
                    <b-form-select v-model="formData.theme" id="theme" >
                    <option :value="null">Please select a Theme</option>
                    <option value="1"> Plant Health</option>
                    <option value="2" > Animal Health </option>
                    <option value="3" > Environmental Health </option>
                    <option value="4" > Human Health </option>
                    </b-form-select>

                    
                    <b-form-group id="form-projectOwner-group" label="Project Owner:" label-for="form-projectOwner-input">
                    <b-form-input
                      id="form-projectOwner-input"
                      type="text"
                      v-model="formData.projectOwner"
                      label="Enter Project Owner"
                    > </b-form-input>
                  </b-form-group>


                    <b-form-group id="form-sampleType-group" label="Sample Type:" label-for="form-sampleType-input">
                    <b-form-input
                      id="form-sampleType-input"
                      type="text"
                      v-model="formData.sampleType"
                      label="Enter Sample Type"
                    > </b-form-input>
                  </b-form-group>

                  <b-form-group id="form-species-group" label="Sample Species:" label-for="form-species-input">
                    <b-form-input
                      id="form-species-input"
                      type="text"
                      v-model="formData.species"
                      label="Enter Species"
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-description-group" label="Sample description:" label-for="form-description-input">
                    <b-form-input
                      id="form-description-input"
                      type="text"
                      v-model="formData.description"
                      label="Enter description"
                    > </b-form-input>
                  </b-form-group>
        </tab-content>

         <tab-content title="Sample Location in Institution" >

                  <b-form-group id="form-locationCollected-group" label="Location collected:" label-for="form-locationCollected-input">
                    <b-form-input
                      id="form-locationCollected-input"
                      type="text" 
                      v-model="formData.locationCollected" 
                      label="Enter Location Collected"
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-lab-group" label="Lab:" label-for="form-lab-input">
                        <b-form-input
                            id="form-lab-input"
                            type="text"
                            v-model="formData.lab" 
                            label="Enter Laboratory"
                         > </b-form-input>
                    </b-form-group>

                  <b-row>
                       <b-col>
                               <b-form-group id="form-freezer-group" label="Freezer:" label-for="form-freezer-input">
                                <b-form-input
                                id="form-freezer-input"
                                type="text"
                                v-model="formData.freezer" 
                                label="Enter Freezer"
                                > </b-form-input>
                                </b-form-group>
                       </b-col>

                        <b-col>
                                <span> Please select the chamber </span>
                                <b-form-select data-vv-scope="step2" class="field" id="formData.chamber">
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
                            v-model="formData.rack" 
                            label="Enter Rack"
                            > </b-form-input>
                           </b-form-group>
                        </b-col>

                        <b-col>
                            <b-form-group id="form-tray-group" label="Tray:" label-for="form-tray-input">
                            <b-form-input
                            id="form-tray-input"
                            type="number" min="0"
                            v-model="formData.tray" 
                            label="Enter Rack"
                            > </b-form-input>
                         </b-form-group>
                        </b-col>

                        <b-col>
                            <b-form-group id="form-box-group" label="Box:" label-for="form-box-input">
                            <b-form-input
                            id="form-box-input"
                            type="number" min="0"
                            v-model="formData.box" 
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
                            v-model="formData.temperature" 
                            label="Enter temperature "
                            > </b-form-input>
                          </b-form-group>
                        </b-col>

                        <b-col>
                            <b-form-group id="form-amount-group" label="Amount:" label-for="form-amount-input">
                            <b-form-input
                            id="form-amount-input"
                            type="number" min="0"
                            v-model="formData.amount" 
                            label="Enter amount of sample "
                            > </b-form-input>
                          </b-form-group>
                        </b-col>

                        <b-col>
                             <span> Please select the quantity type </span>
                            <b-form-select v-model="formData.quantity_type" class="mb-3" id="form-quantity-dropdown">
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
                    <b-form-select v-model="formData.securityLevel"  class="mb-3" id="form-securityLevel-dropdown">
                    <option :value="null">Please select the security level</option>
                    <option value="High"> High </option>
                    <option value="Medium" > Medium </option>
                    <option value="Low" > Low </option>
                    </b-form-select>

                    <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
                    <b-form-input
                      id="form-code-input"
                      type="number" min="0"
                      v-model="formData.code" 
                      label="Enter code "
                    > </b-form-input>
                  </b-form-group>

                  <b-form-group id="form-barcode-group" label="Barcode:" label-for="form-barcode-input">
                    <b-form-input
                      id="form-barcode-input"
                      type="text"
                      v-model="formData.barcode" 
                      label="Enter barcode number "
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-analysis-group" label="Analysis:" label-for="form-analysis-input">
                    <b-form-input
                      id="form-analysis-input"
                      type="text"
                      v-model="formData.analysis" 
                      label="Enter analysis carried out "
                    > </b-form-input>
                  </b-form-group>
             

                    <b-form-group id="form-retention-group" label="Retention:" label-for="form-retention-input">
                    <b-form-input
                      id="form-retention-input"
                      type="number" min="0"
                      v-model="formData.retention" 
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
                
                <wizard-button v-else @click.native="alert('Done')" class="wizard-footer-right finish-button" :style="props.fillButtonStyle">{{props.isLastStep ? 'Done' : 'Next'}}</wizard-button>
              </div>
          </template>
          </form-wizard>
  </b-container>
  </div>
</template>

<script>
import Vue from 'vue';
import VueFormWizard, { TabContent } from 'vue-form-wizard'
import 'vue-form-wizard/dist/vue-form-wizard.min.css'

import axios from 'axios';

Vue.use(VueFormWizard)
Vue.use(TabContent)

export default {
  name: 'sampleform',
     
  data(){
    return{
        response: [],
        formData: {
            theme: '',
            project: '',
            projectOwner: '',
            sampleType: '',
            species: '',
            description: '',
            lab: '',
            freezer:'',
            chamber:'',
            rack: '',
            tray: '',
            box: '',   
            locationCollected: '',
            retention: '',
            barcode: '',
            analysis: '',
            temperature: '',
            amount: '',
            quantity_type: '',
            securityLevel: '',
            code: '',
            terms:'',
     }
        
    };
},
methods : {
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
}

</script>
