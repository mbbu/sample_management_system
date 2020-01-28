<template>
  <div id="sampleform">
  <b-container>
    <form-wizard>
      <template v-slot="{formData}">

        <tab name="Step 1" info="Project Information" :selected="true" :formData="formData">
              <div id="form-step-1" >

                   <b-form-group id="theme-input-group-2" label="Theme" label-for="theme-input-2">
                      <b-form-select
                        id="theme-input-2"
                        name="theme-input-2"
                        v-model="formData.theme"
                        v-validate="{ required: true }"
                        :options="themes"
                        :state="validateState('theme-input-2')"
                        aria-describedby="theme-2-live-feedback"
                        data-vv-as="Theme"
                      ></b-form-select>

                      <b-form-invalid-feedback id="theme-2-live-feedback">{{ veeErrors.first('theme-input-2') }}</b-form-invalid-feedback>
                    </b-form-group>
            
                   <span> Please select a Theme </span>
                    <b-form-select v-model="formData.theme" id="theme" v-validate="{ required: true }" data-vv-scope="step1" class="input" >
                    <option :value="null">Please select a Theme</option>
                    <option value="1"> Plant Health</option>
                    <option value="2" > Animal Health </option>
                    <option value="3" > Environmental Health </option>
                    <option value="4" > Human Health </option>
                    </b-form-select>

                    <span> Enter Project Name </span>
                    <b-form-select v-model="formData.project" v-validate="{ required: true }" data-vv-scope="step1" class="input" id="project" label="Enter Project Name" >
                    <option :value="null">Please select your project</option>
                    <option value="H3Bionet"> H3Bionet</option>
                    <option value="IENBit" >IENBit</option>
                    <option value="Tsetse Launch" >Tsetse Launch</option>
                    <option value="Africa Now" >Africa Now </option>
                    </b-form-select>

                     <b-form-group id="projectOwner-input-group" label="Project Owner" label-for="projectOwner-input-1">
                      <b-form-input
                        id="projectOwner"
                        name="projectOwner-input-1"
                        v-model="formData.projectOwner"
                        v-validate="{ required: true, min: 3 }"
                        :state="validateState('projectOwner-input-1')"
                        aria-describedby="input-1-live-feedback"
                        data-vv-as="projectOwner"
                      ></b-form-input>
                      <b-form-invalid-feedback id="projectOwner-1-live-feedback">{{ veeErrors.first('projectOwner-input-1') }}</b-form-invalid-feedback>
                    </b-form-group>

                     <b-form-group id="sampleType-input-group" label="sample Type" label-for="sampleType-input-1">
                      <b-form-input
                        id="sampleType"
                        name="sampleType-input-1"
                        v-model="formData.sampleType"
                        v-validate="{ required: true, min: 3 }"
                        :state="validateState('sampleType-input-1')"
                        aria-describedby="input-1-live-feedback"
                        data-vv-as="sampleType"
                      ></b-form-input>
                      <b-form-invalid-feedback id="sampleType-1-live-feedback">{{ veeErrors.first('sampleType-input-1') }}</b-form-invalid-feedback>
                    </b-form-group>

                     <b-form-group id="species-input-group" label="species" label-for="species-input-1">
                      <b-form-input
                        id="species"
                        name="species-input-1"
                        v-model="formData.species"
                        v-validate="{ required: true, min: 3 }"
                        :state="validateState('species-input-1')"
                        aria-describedby="input-1-live-feedback"
                        data-vv-as="species"
                      ></b-form-input>
                      <b-form-invalid-feedback id="species-1-live-feedback">{{ veeErrors.first('species-input-1') }}</b-form-invalid-feedback>
                    </b-form-group>

                     <b-form-group id="description-input-group" label="description" label-for="description-input-1">
                      <b-form-input
                        id="description"
                        name="description-input-1"
                        v-model="formData.description"
                        v-validate="{ required: true, min: 10 }"
                        :state="validateState('description-input-1')"
                        aria-describedby="input-1-live-feedback"
                        data-vv-as="description"
                      ></b-form-input>
                      <b-form-invalid-feedback id="description-1-live-feedback">{{ veeErrors.first('description-input-1') }}</b-form-invalid-feedback>
                    </b-form-group>

              </div>
         </tab>

         <tab name="Step 2" info="Sample Location in Institution" data-vv-scope="step2">
              <div id="form-step-2">

                  <b-form-group id="form-locationCollected-group" label="Location collected:" label-for="form-locationCollected-input">
                    <b-form-input
                      id="form-locationCollected-input"
                      v-validate="{ required: true }"
                      type="text" 
                      v-model="formData.locationCollected" data-vv-scope="step2"
                      label="Enter Location Collected"
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-lab-group" label="Lab:" label-for="form-lab-input">
                        <b-form-input
                            id="form-lab-input"
                            type="text"
                            v-model="formData.lab" data-vv-scope="step2"
                            label="Enter Laboratory"
                         > </b-form-input>
                    </b-form-group>

                  <b-row>
                       <b-col>
                               <b-form-group id="form-freezer-group" label="Freezer:" label-for="form-freezer-input">
                                <b-form-input
                                id="form-freezer-input"
                                type="text"
                                v-model="formData.freezer" data-vv-scope="step2"
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
                            v-model="formData.rack" data-vv-scope="step2"
                            label="Enter Rack"
                            > </b-form-input>
                           </b-form-group>
                        </b-col>

                        <b-col>
                            <b-form-group id="form-tray-group" label="Tray:" label-for="form-tray-input">
                            <b-form-input
                            id="form-tray-input"
                            type="number" min="0"
                            v-model="formData.tray" data-vv-scope="step2"
                            label="Enter Rack"
                            > </b-form-input>
                         </b-form-group>
                        </b-col>

                        <b-col>
                            <b-form-group id="form-box-group" label="Box:" label-for="form-box-input">
                            <b-form-input
                            id="form-box-input"
                            type="number" min="0"
                            v-model="formData.box" data-vv-scope="step2"
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
                            v-model="formData.temperature" data-vv-scope="step2"
                            label="Enter temperature "
                            > </b-form-input>
                          </b-form-group>
                        </b-col>

                        <b-col>
                            <b-form-group id="form-amount-group" label="Amount:" label-for="form-amount-input">
                            <b-form-input
                            id="form-amount-input"
                            type="number" min="0"
                            v-model="formData.amount" data-vv-scope="step2"
                            label="Enter amount of sample "
                            > </b-form-input>
                          </b-form-group>
                        </b-col>

                        <b-col>
                             <span> Please select the quantity type </span>
                            <b-form-select v-model="formData.quantity_type" data-vv-scope="step2" class="mb-3" id="form-quantity-dropdown">
                            <option :value="null">Please select the quantity type</option>
                            <option value="ML"> ML</option>
                            <option value="Meters" > Meters </option>
                            <option value="Kilograms" > Kilograms </option>
                            <option value="Actual Number" > Actual Number</option>
                            </b-form-select>
                        </b-col>
                    </b-row>

                </div>
          </tab>

          <tab name="Step 3" info="Finishing Up" >
              <div id="form-step-3">

                   <span> Add Security Level Needed </span>
                    <b-form-select v-model="formData.securityLevel" data-vv-scope="step3" class="mb-3" id="form-securityLevel-dropdown">
                    <option :value="null">Please select the security level</option>
                    <option value="High"> High </option>
                    <option value="Medium" > Medium </option>
                    <option value="Low" > Low </option>
                    </b-form-select>

                    <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
                    <b-form-input
                      id="form-code-input"
                      type="number" min="0"
                      v-model="formData.code" data-vv-scope="step3"
                      label="Enter code "
                    > </b-form-input>
                  </b-form-group>

                  <b-form-group id="form-barcode-group" label="Barcode:" label-for="form-barcode-input">
                    <b-form-input
                      id="form-barcode-input"
                      type="text"
                      v-model="formData.barcode" data-vv-scope="step3"
                      label="Enter barcode number "
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-analysis-group" label="Analysis:" label-for="form-analysis-input">
                    <b-form-input
                      id="form-analysis-input"
                      type="text"
                      v-model="formData.analysis" data-vv-scope="step3"
                      label="Enter analysis carried out "
                    > </b-form-input>
                  </b-form-group>
             

                    <b-form-group id="form-retention-group" label="Retention:" label-for="form-retention-input">
                    <b-form-input
                      id="form-retention-input"
                      type="number" min="0"
                      v-model="formData.retention" data-vv-scope="step3"
                      label="Enter retention period in months "
                    > </b-form-input>
                  </b-form-group>

                   <div class="btn-group" role="group">
                     <b-button type="submit" variant="primary"> Submit </b-button>
                     <b-button type="reset" variant="danger"> Reset </b-button>
                    </div>
                  
             </div>
        </tab>
          </template>
          </form-wizard>
  </b-container>
  </div>
</template>

<script>
import Vue from 'vue';
import  VeeValidate from 'vee-validate';
import FormWizard from '../components/FormWizard.vue';
import Tab from '../components/Tab.vue';
import 'bulma/css/bulma.css';

Vue.use(VeeValidate, {
    // This is the default
  inject: true,
  // Important to name this something other than 'fields'
  fieldsBagName: 'veeFields',
  // This is not required but avoids possible naming conflicts
  errorBagName: 'veeErrors'
});

export default {
  name: 'sampleform',
  components: {
    FormWizard, Tab
  },
}
</script>

<style lang="scss">
@import "../../node_modules/bulma/bulma.sass";
@import "../../node_modules/bulma-steps-component/bulma-steps.sass";


[v-cloak] { display: none; }
</style>