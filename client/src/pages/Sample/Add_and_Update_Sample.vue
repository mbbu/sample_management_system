<template>
  <div id="jumbotron">
    <div class="container">
      <top-nav :page_title="page_title"></top-nav>

      <form-wizard ref="formContainer" subtitle="Kindly input the correct information"
                   title="Sample Data Form" @submit.prevent="formSubmit">
        <!-- FLASH MESSAGES -->
        <FlashMessage :position="'right bottom'"></FlashMessage>

        <tab-content :before-change="handleSubmit"
                     title="Sample Details">
          <!--THEME-->
          <div class="form-group">
            <b-form-group id="form-theme" label="Select a Theme:" label-for="form-theme-input">
              <ejs-dropdownlist
                  id="theme-dropdownlist"
                  :dataSource='themeDataList'
                  :fields="fields"
                  :v-model="sample.theme"
                  :value="selectDropDownItemForUpdate('theme-dropdownlist', sample.theme, themeDataList)"
                  placeholder='Select a theme'
                  @change="setTheme"
              ></ejs-dropdownlist>
            </b-form-group>
          </div>

          <!-- PROJECT -->
          <div class="form-group">
            <b-form-group id="form-project" label="Select a project:" label-for="form-theme-input">
              <ejs-dropdownlist
                  id="project-dropdownlist"
                  :dataSource='projectDataList'
                  :fields="fields"
                  :v-model="sample.project"
                  :value="selectDropDownItemForUpdate('project-dropdownlist', sample.project, projectDataList)"
                  placeholder='Select a project'
                  @change="setProject"
              ></ejs-dropdownlist>
            </b-form-group>
          </div>

          <!--PROJECT HEAD-->
          <div class="form-group">
            <label for="projectHead"> Project Head(P.I)</label>
            <input id="projectHead" v-model="sample.projectHead" class="form-control" disabled
                   type="text"/>
          </div>

          <!--SAMPLE OWNER-->
          <div class="form-group" hidden>
            <label for="sampleOwner"> Sample Owner</label>
            <input id="sampleOwner" v-model="sample.sampleOwner" class="form-control" disabled
                   type="text"/>
          </div>

          <!--SAMPLE TYPE-->
          <div class="form-group">
            <label for="sampleType"> Sample Type</label>
            <input id="sampleType" v-model="sample.sampleType" class="form-control" required type="text"/>
          </div>

          <!--SPECIES-->
          <div class="form-group">
            <label for="species"> Species</label>
            <input id="species" v-model="sample.species" class="form-control" required type="text"/>
          </div>

          <!--DESC-->
          <div class="form-group">
            <label for="description"> Description</label>
            <textarea id="description" v-model="sample.description" class="form-control" name="description"
                      type="text"/>
          </div>
          <errors-display :errors="errors"></errors-display>
        </tab-content>

        <!-- TAB 2 -->
        <tab-content :before-change="handleSubmit" title="Sample Location in Institution">
          <!-- LOCATION -->
          <div class="form-group">
            <b-form-group id="form-locationCollected" label="Select Location:" label-for="form-loc-input">
              <ejs-dropdownlist
                  id="locationCollected-dropdownlist"
                  :dataSource='locDataList'
                  :fields="fields"
                  :v-model="sample.locationCollected"
                  :value="selectDropDownItemForUpdate('locationCollected-dropdownlist', sample.locationCollected, locDataList)"
                  placeholder='Select location sample(s) was collected from'
                  @change="setLocation"
              ></ejs-dropdownlist>
            </b-form-group>
          </div>

<!--          <div v-if="isUpdate" class="form-group">-->
<!--            <label for="locationCollected">Location Collected</label>-->
<!--            <input id="locationCollected" v-model="sample.locationCollected" class="form-control" required-->
<!--                   type="text"/>-->
<!--          </div>-->

          <!-- CASCADING DROPDOWNS TO DETERMINE A PLACE FOR THE SAMPLE -->
          <div>
            <sample-location-finder></sample-location-finder>
          </div>

          <!-- Start row -->
          <div class="row">
            <div class="col">
              <div class="form-group">
                <label for="temperature">Temperature (Default in Celsius)</label>
                <input id="temperature" v-model="sample.temperature" class="form-control" required
                       type="number"/>
              </div>

            </div>

            <div class="col">
              <div class="form-group">
                <label for="amount">Amount</label>
                <input id="amount" v-model="sample.amount" class="form-control" min="1" required
                       type="number"/>
              </div>

            </div>
            <div class="col">
              <div class="form-group">
                <b-form-group id="form-QT" label="Select a Quantity Type:"
                              label-for="form-user-input">
                  <ejs-dropdownlist
                      id="QT-dropdownlist"
                      :dataSource='QTDataList'
                      :fields="fields"
                      :v-model="sample.quantity_type"
                      :value="selectDropDownItemForUpdate('QT-dropdownlist', sample.quantity_type, QTDataList)"
                      placeholder='Select a quantity type(e.g. ML, L, G ...)'
                      @change="setQuantityType"
                  ></ejs-dropdownlist>
                </b-form-group>
              </div>
            </div>
          </div>
          <!-- End Row -->
          <errors-display :errors="errors"></errors-display>
        </tab-content>

        <tab-content :before-change="handleSubmit" title="Finishing Up">
          <div class="form-group">
            <b-form-group id="form-securityLevel" label="BioHazard Level Needed:"
                          label-for="form-securityLevel-input">
              <ejs-dropdownlist
                  id="securityLevel-dropdownlist"
                  :dataSource='secLevelDataList'
                  :fields="fields"
                  :v-model="sample.securityLevel"
                  :value="selectDropDownItemForUpdate('securityLevel-dropdownlist', sample.securityLevel, secLevelDataList)"
                  placeholder='Select BioHazard Level Needed'
                  @change="setSecurityLevel"
              ></ejs-dropdownlist>
            </b-form-group>
          </div>

          <div v-if="isUpdate" class="form-group">
            <label for="code"> Code</label>
            <input id="code" v-model="sample.code" class="form-control"
                   required
                   type="text"/>
            <div v-if="submitted && error in errors" class="invalid-feedback">
              <span> Code is required + {{ error }} </span>
            </div>
          </div>

          <div v-if="isUpdate" class="form-group">
            <label for="barcode"> Barcode</label>
            <input id="barcode" v-model="sample.barcode" class="form-control" required type="text"/>
          </div>

          <div class="form-group">
            <label for="analysis"> Analysis</label>
            <input id="analysis" v-model="sample.analysis" class="form-control" required type="text"/>
          </div>

          <div class="row">
            <div class="col">
              <div class="form-group">
                <label for="retention"> Retention</label>
                <input id="retention" v-model="sample.retention" class="form-control" min="1" required
                       type="number"/>
              </div>
            </div>

            <div class="col">
              <div class="form-group">
                <label for="period">Select Retention Length:</label>
                <select id="period" class="custom-select" required @change="setRetentionPeriod">
                  <option selected>Select period(Days, Weeks ...)</option>
                  <option value="1">Days</option>
                  <option value="2">Weeks</option>
                  <option value="3">Months</option>
                  <option value="4">Years</option>
                </select>
              </div>
            </div>
          </div>
          <errors-display :errors="errors"></errors-display>
        </tab-content>

        <template slot="footer" scope="props">
          <div class=wizard-footer-left>
            <wizard-button v-if="props.activeTabIndex > 0 && !props.isLastStep" :style="props.fillButtonStyle"
                           @click.native="props.prevTab()">Previous
            </wizard-button>
          </div>

          <div class="wizard-footer-right">
            <wizard-button v-if="!props.isLastStep" :style="props.fillButtonStyle"
                           class="wizard-footer-right" @click.native="props.nextTab()">Next
            </wizard-button>

            <wizard-button v-else :style="props.fillButtonStyle"
                           class="wizard-footer-right finish-button"
                           @click.native="formSubmit">{{ props.isLastStep ? 'Done' : 'Next' }}
            </wizard-button>
          </div>
        </template>
      </form-wizard>
    </div>
  </div>
</template>

<script>
import Vue from 'vue';
import VueFormWizard, {TabContent} from 'vue-form-wizard';
import 'vue-form-wizard/dist/vue-form-wizard.min.css';
import axios from 'axios';
import {
  extractApiData, extractQTData,
  getItemDataList, getSampleDetailsForEditing, getSelectedItemCode,
  handleError, isUpdate, redirectAfterCountDown, secureStoreGetAuthString,
  selectDropDownItemForUpdate, showFlashMessage
} from "@/utils/util_functions";
import {
  bio_hazard_level_resource, project_resource,
  quantity_type_resource, sample_resource, study_block_resource, theme_resource
} from "@/utils/api_paths";
import TopNav from "@/components/TopNav";
import ErrorsDisplay from "@/components/ErrorsDisplay";
import SampleLocationFinder from "@/components/SampleLocationFinder";
import EventBus from "@/components/EventBus";

Vue.use(VueFormWizard)
Vue.use(TabContent)

export default {
  name: "jumbotron",

  data() {
    return {
      response: [],
      sample: {
        theme: "", sampleOwner: "", project: "", projectHead: "", sampleType: "",
        species: "", description: "", box: "", locationCollected: "", retention: "",
        convertedRetentionPeriod: "", barcode: "", analysis: "", temperature: "",
        amount: "", quantity_type: "", securityLevel: "", code: "", slots: [],

        // extra fields
        tray: "", rack: "", chamber: "", freezer: "", lab: "",
      },
      submitted: false,
      isUpdate: false,

      tabNum: 0, tabOne: 0, tabTwo: 1, tabThree: 2,

      // lists
      errors: [], QTDataList: [], projectList: [], themeDataList: [], projectDataList: [], secLevelDataList: [],
      locDataList: [],
      fields: {text: '', value: ''},
      page_title: "Add Sample",
    };
  },

  mounted() {
    EventBus.$on('slotSelected', payload => {
      this.sample.slots = payload
    })
  },

  methods: {
    // util functions
    selectDropDownItemForUpdate,
    onLoadPage() {
      if (isUpdate()) {
        // call function to fill form
        this.fillSampleFormForUpdate()
        this.isUpdate = true;
      } else {
        this.getDataListItemsForForm()
      }
    },

    getDataListItemsForForm() {
      // GET THEME LIST
      getItemDataList(theme_resource).then(data => {
        let themeList = extractApiData(data);

        // update local variables with data from API
        this.fields = themeList['fields'];
        for (let i = 0; i < themeList.items.length; i++) {
          this.themeDataList.push({
            'Code': themeList.items[i].Code,
            'Name': themeList.items[i].Name,
          });
        }
      })

      // GET PROJECT LIST
      getItemDataList(project_resource).then(data => {
        // save this data for re-use
        this.projectList = data
        let projectList = extractApiData(data);

        // update local variables with data from API
        this.fields = projectList['fields'];
        for (let i = 0; i < projectList.items.length; i++) {
          this.projectDataList.push({
            'Code': projectList.items[i].Code,
            'Name': projectList.items[i].Name,
          });
        }
      })

      // GET StudyBlock LIST
      getItemDataList(study_block_resource).then(data => {
        let locationList = extractApiData(data);

        // update local variables with data from API
        this.fields = locationList['fields'];
        for (let i = 0; i < locationList.items.length; i++) {
          this.locDataList.push({
            'Code': locationList.items[i].Code,
            'Name': locationList.items[i].Name,
          });
        }
      })

      // GET QUANTITY TYPE LIST
      getItemDataList(quantity_type_resource).then(data => {
        let QTList = extractQTData(data);

        // update local variables with data from API
        this.fields = QTList['fields'];
        for (let i = 0; i < QTList.items.length; i++) {
          this.QTDataList.push({
            'Code': QTList.items[i].Code,
            'Name': QTList.items[i].Name,
          });
        }
      })

      // GET SECURITY LEVEL LIST
      getItemDataList(bio_hazard_level_resource).then(data => {
        let secLevelList = extractApiData(data);

        // update local variables with data from API
        this.fields = secLevelList['fields'];
        for (let i = 0; i < secLevelList.items.length; i++) {
          this.secLevelDataList.push({
            'Code': secLevelList.items[i].Code,
            'Name': secLevelList.items[i].Name,
          });
        }
      })
    },

    handleSubmit() {
      if (this.tabNum === 0) {
        this.errors = []
        return this.validateForm(this.tabOne)
      } else if (this.tabNum === 1) {
        this.errors = []
        return this.validateForm(this.tabTwo)
      } else if (this.tabNum === 2) {
        this.errors = []
        return this.validateForm(this.tabThree)
      }
    },

    validateForm(tabs) {

      switch (tabs) {
        case 0:
          if (!this.sample.theme) {
            this.errors.push("Theme is required");
          }
          if (!this.sample.project) {
            this.errors.push("Project is required");
          }
          if (!this.sample.sampleType) {
            this.errors.push("Sample Type is required");
          }
          if (!this.sample.species) {
            this.errors.push("Animal species is required");
          }
          if (!this.sample.description) {
            this.errors.push("Description is required.");
          }
          if (this.errors.length) {
            showFlashMessage(this, "error", "Check Form for Errors", "Correct errors to proceed!")
          }

          // no errors found in form
          if (!this.errors.length) {
            // emit event to trigger the fetching of lab data
            // required in the next page
            EventBus.$emit('locationFinder')
            this.tabNum++
            return true;
          }
          break;

        case 1:
          if (!this.sample.slots.length) {
            this.errors.push("Slot(s) is required");
          }
          if (!this.sample.temperature) {
            this.errors.push("Temperature is required");
          }
          if (!this.sample.amount) {
            this.errors.push("Amount is required");
          }
          if (!this.sample.quantity_type) {
            this.errors.push("Quantity Type is required");
          }
          if (this.errors.length) {
            showFlashMessage(this, "error", "Check Form for Errors", "Correct errors to proceed!")
          }
          if (!this.errors.length) {
            this.tabNum++
            return true;
          }
          break;

        case 2:
          if (!this.sample.securityLevel) {
            this.errors.push("Security level is required");
          }
          if (!this.sample.analysis) {
            this.errors.push("Analysis is required");
          }
          if (!this.sample.retention) {
            this.errors.push("Retention period is required");
          }
          if (this.errors.length) {
            showFlashMessage(this, "error", "Check Form for Errors", "Correct errors to proceed!")
          }
          if (!this.errors.length) {
            this.tabNum = 0
            return true;
          }
          break;

        default:
          this.errors = [];
          if (!this.errors.length) {
            return true;
          }
          break;
      }
    },

    setTheme() {
      this.sample.theme = getSelectedItemCode("theme-dropdownlist", this.themeDataList)
    },
    setProject() {
      let item = this.sample.project = getSelectedItemCode("project-dropdownlist", this.projectDataList)

      // fill details about the project head and sample owner/PI as well
      for (let i = 0; i < this.projectList.length; i++) {
        if (item === this.projectList[i].code) {
          this.sample.sampleOwner = this.projectList[i]['lead.email']
          this.sample.projectHead = this.projectList[i]['lead.first_name'] + " " + this.projectList[i]['lead.last_name']
        }
      }
    },
    setSecurityLevel() {
      this.sample.securityLevel = getSelectedItemCode("securityLevel-dropdownlist", this.secLevelDataList)
    },
    setQuantityType() {
      this.sample.quantity_type = getSelectedItemCode("QT-dropdownlist", this.QTDataList)
    },
    setRetentionPeriod() {
      let periodSelect = document.getElementById("period")
      let periodValue = parseInt(periodSelect.options[periodSelect.selectedIndex].value);

      if (periodValue === 1) {
        this.sample.convertedRetentionPeriod = this.sample.retention * 1
      } else if (periodValue === 2) {
        // convert week to days
        this.sample.convertedRetentionPeriod = this.sample.retention * 7
      } else if (periodValue === 3) {
        // convert months to days
        this.sample.convertedRetentionPeriod = this.sample.retention * 30
      } else if (periodValue === 4) {
        //  convert years to days
        this.sample.convertedRetentionPeriod = this.sample.retention * 365
      }
    },

    setLocation() {
      this.sample.locationCollected = getSelectedItemCode("locationCollected-dropdownlist", this.locDataList)
    },

    formSubmit() {
      if (isUpdate()) {
        this.updateSample()
      } else {
        let loader = this.$loading.show({
          isFullPage: true,
          canCancel: false,
          color: '#074880',
          loader: 'dots',
          width: 255,
          height: 255,
          backgroundColor: '#FAAB2C',
          opacity: 0.7,
          zIndex: 999,
        });

        axios.post(sample_resource, {
          theme: this.sample.theme,
          user: this.sample.sampleOwner,
          slots: JSON.stringify(this.sample.slots),
          animal_species: this.sample.species,
          sample_type: this.sample.sampleType,
          sample_description: this.sample.description,
          project: this.sample.project,
          project_owner: this.sample.projectHead,
          retention_period: this.sample.convertedRetentionPeriod,
          barcode: this.sample.barcode,
          analysis: this.sample.analysis,
          temperature: this.sample.temperature,
          amount: this.sample.amount,
          quantity_type: this.sample.quantity_type,
          bio_hazard_level: this.sample.securityLevel,
          location_collected: this.sample.locationCollected,
          code: this.sample.code,
        }, {
          headers:
              {
                Authorization: secureStoreGetAuthString()
              }
        })
            .then((response) => {
              setTimeout(() => {
                loader.hide()
                showFlashMessage(this, 'success', response.data['message'], '');
                // todo: redirect to sample view page
                redirectAfterCountDown(this, '/sample')
              }, 4000)
            })
            .catch((error) => {
              handleError(this, error, loader)
            });
      }
    },

    /* UPDATE FUNCTIONS */
    fillSampleFormForUpdate() {
      // 1st update the page title
      this.page_title = "Update Sample"

      // get data-lists for drop-downs
      this.getDataListItemsForForm()

      // set sample details
      let sampleForUpdate = getSampleDetailsForEditing()

      this.sample.project = sampleForUpdate['project'];
      this.sample.projectHead = sampleForUpdate['project_owner'];
      this.sample.sampleType = sampleForUpdate['sample_type'];
      this.sample.species = sampleForUpdate['animal_species'];
      this.sample.description = sampleForUpdate['sample_description'];
      this.sample.locationCollected = sampleForUpdate['location_collected'];
      this.sample.retention = sampleForUpdate['retention_period'];
      this.sample.barcode = sampleForUpdate['barcode'];
      this.sample.analysis = sampleForUpdate['analysis'];
      this.sample.temperature = sampleForUpdate['temperature'];
      this.sample.amount = sampleForUpdate['amount'];
      this.sample.code = sampleForUpdate['code'];
      this.sample.tray = sampleForUpdate['box.tray.number'];
      this.sample.rack = sampleForUpdate['box.tray.rack.number'];
      this.sample.chamber = sampleForUpdate['box.tray.rack.chamber.type'];
      this.sample.freezer = sampleForUpdate['box.tray.rack.chamber.freezer.number'];
      this.sample.lab = sampleForUpdate['box.tray.rack.chamber.freezer.lab.name']
          + " room " + sampleForUpdate['box.tray.rack.chamber.freezer.lab.room'];

      // drop-down data
      this.sample.theme = sampleForUpdate['theme.name'];
      this.sample.sampleOwner = sampleForUpdate['user.first_name'] + " " + sampleForUpdate['user.last_name'];
      this.sample.box = sampleForUpdate['box.label'];
      this.sample.quantity_type = sampleForUpdate['quantity.id'];
      this.sample.securityLevel = sampleForUpdate['bioHazardLevel.code'];
      this.sample.convertedRetentionPeriod = this.sample.retention;

      document.getElementById('period').selectedIndex = 1;

      let x = document.getElementById("period").selectedIndex;
      let y = document.getElementById("period").options;

      document.getElementById('period').value = y[x].text;
    },

    updateSample() {
      let loader = this.$loading.show({
        isFullPage: true,
        canCancel: false,
        color: '#074880',
        loader: 'dots',
        width: 255,
        height: 255,
        backgroundColor: '#FAAB2C',
        opacity: 0.7,
        zIndex: 999,
      })

      axios.put(sample_resource, {
        theme: this.sample.theme,
        user: this.sample.sampleOwner,
        slots: this.sample.slots,
        animal_species: this.sample.species,
        sample_type: this.sample.sampleType,
        sample_description: this.sample.description,
        project: this.sample.project,
        project_owner: this.sample.projectHead,
        retention_period: this.sample.convertedRetentionPeriod,
        barcode: this.sample.barcode,
        analysis: this.sample.analysis,
        temperature: this.sample.temperature,
        amount: this.sample.amount,
        quantity_type: this.sample.quantity_type,
        bio_hazard_level: this.sample.securityLevel,
        location_collected: this.sample.locationCollected,
        code: this.sample.code,
      }, {
        headers:
            {
              code: this.sample.code,
              Authorization: secureStoreGetAuthString()
            }
      })
          .then((response) => {
            setTimeout(() => {
              loader.hide()
              showFlashMessage(this, 'success', response.data['message'], '');
              // todo: redirect to sample view page
              redirectAfterCountDown(this, '/sample')
            }, 4000)
          })
          .catch((error) => {
            handleError(this, error, loader)
          });
    },
  },

  created() {
    this.onLoadPage();
  },

  components: {SampleLocationFinder, TopNav, ErrorsDisplay}
};
</script>
