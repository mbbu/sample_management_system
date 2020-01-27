<template>
  <b-container>
    <form-wizard>
      <template v-slot="{formData}">
        <tab name="Step 1" info="Project Information" :selected="true" :formData="formData">
              <div id="form-step-1" >
            
                   <span> Please select a Theme </span>
                    <b-form-select v-model="theme" class="mb-3" id="theme-dropdown">
                    <option :value="null">Please select a Theme</option>
                    <option value="1"> Plant Health</option>
                    <option value="2" > Animal Health </option>
                    <option value="3" > Environmental Health </option>
                    <option value="4" > Human Health </option>
                    </b-form-select>

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
                      label="Enter Project Owner"
                    > </b-form-input>
                  </b-form-group>


                    <b-form-group id="form-sampleType-group" label="Sample Type:" label-for="form-sampleType-input">
                    <b-form-input
                      id="form-sampleType-input"
                      type="text"
                      v-model="sampleType"
                      label="Enter Sample Type"
                    > </b-form-input>
                  </b-form-group>

                  <b-form-group id="form-species-group" label="Sample Species:" label-for="form-species-input">
                    <b-form-input
                      id="form-species-input"
                      type="text"
                      v-model="species"
                      label="Enter Species"
                    > </b-form-input>
                  </b-form-group>

                    <b-form-group id="form-description-group" label="Sample description:" label-for="form-description-input">
                    <b-form-input
                      id="form-description-input"
                      type="text"
                      v-model="description"
                      label="Enter description"
                    > </b-form-input>
                  </b-form-group>

              </div>
         </tab>

         <tab name="Step 2" info="Sample Location in Institution" data-vv-scope="step2">
              <div id="form-step-2">

                    <b-form-group id="form-locationCollected-group" label="Location collected:" label-for="form-locationCollected-input">
                    <b-form-input
                      id="form-locationCollected-input"
                      type="text"
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
                                </b-form-group>  </b-col>

                        <b-col>
                                        <span> Please select the chamber </span>
                                <b-form-select v-model="chamber" class="mb-3" id="form-quantity-dropdown">
                                <option :value="null">Chamber</option>
                                <option value="Middle"> Middle</option>
                                <option value="Top" > Top </option>
                                <option value="Bottom" > Bottom </option>
                                </b-form-select> </b-col>
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

                </div>
          </tab>

          <tab name="Step 3" info="Finishing Up" >
              <div id="form-step-3">

                   <span> Add Security Level Needed </span>
                    <b-form-select v-model="securityLevel" class="mb-3" id="form-securityLevel-dropdown">
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

                   <div class="btn-group" role="group">
                     <b-button type="submit" variant="primary"> Submit </b-button>
                     <b-button type="reset" variant="danger"> Reset </b-button>
                    </div>

            
                   
             </div>
        </tab>

          </template>
          </form-wizard>

  </b-container>
</template>

<script>
import Vue from 'vue';
import  * as VeeValidate from 'vee-validate';
import FormWizard from '../components/FormWizard.vue';
import Tab from '../components/Tab.vue';
import 'bulma/css/bulma.css';

Vue.use(VeeValidate);
export default {
  name: 'app',
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