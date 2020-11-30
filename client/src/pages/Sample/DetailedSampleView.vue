<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-12">
        <top-nav :page_title="page_title"></top-nav>

        <!-- FLASH MESSAGES -->
        <FlashMessage :position="'right bottom'"></FlashMessage>
        <br> <br>
        <em class="table-header-style">About Sample</em>
        <br> <br>
        <table class="table table-hover">
          <thead class="blue-gradient white-text">
          <tr>
            <th scope="col"><em><b>THEME</b></em></th>
            <th scope="col"><em><b>PROJECT</b></em></th>
            <th scope="col"><em><b>PROJECT HEAD</b></em></th>
            <th scope="col"><em><b>SAMPLE HANDLER</b></em></th>
          </tr>
          </thead>
          <tbody>
          <tr>
            <td v-if="sample.theme"> {{ sample.theme}}</td>
            <td v-else>N/A</td>
            <td v-if="sample.project"> {{ sample.project}}</td>
            <td v-else>N/A</td>
            <td v-if="sample.projectHead">{{sample.projectHead}}</td>
            <td v-else>N/A</td>
            <td v-if="sample.user">{{ sample.user}} &nbsp;

              <a :href="`mailto:${ sample.userEmail }`" target="_blank">
                <i class="far fa-envelope fa-lg"
                   title="Email sample handler? But if you want the sample, request at bottom of the page.">
                </i>
              </a>
            </td>
            <td v-else-if="!sample.user">N/A</td>

          </tr>
          </tbody>
        </table>

        <hr>
        <hr>
        <em class="table-header-style">Sample Details</em>
        <br> <br>
        <table class="table table-hover">
          <thead class="blue-gradient white-text">
          <tr>
            <th id="blank">&nbsp;</th>
            <th id="co1" headers="blank" scope="col"><em><b>SAMPLE TYPE</b></em></th>
            <th id="co3" headers="blank" scope="col"><em><b>SPECIES</b></em></th>
            <th id="co4" headers="blank" scope="col"><em><b>LOCATION COLLECTED</b></em></th>
            <th id="co5" headers="blank" scope="col"><em><b>ANALYSIS</b></em></th>
          </tr>
          </thead>
          <tr>
            <th id="c1" headers="blank"></th>
            <td v-if="sample.sampleType" headers="co1 c1">{{ sample.sampleType}}</td>
            <td v-else-if="!sample.sampleType">N/A</td>
            <td v-if="sample.species" headers="co3 c1">{{ sample.species}}</td>
            <td v-else-if="!sample.species">N/A</td>
            <td v-if="sample.locationCollected" headers="co4 c1">{{ sample.locationCollected}}</td>
            <td v-else-if="!sample.locationCollected">N/A</td>
            <td v-if="sample.analysis" headers="co5 c1">{{ sample.analysis}}</td>
            <td v-else-if="!sample.analysis">N/A</td>
          </tr>
          <thead class="blue-gradient white-text">
          <tr>
            <th>&nbsp;</th>
            <th id="co6" headers="blank" scope="col"><em><b>PUBLICATIONS</b></em></th>
            <th id="co7" headers="blank" scope="col"><em><b>SURVEYS</b></em></th>
            <th id="co8" headers="blank" scope="col"><em><b>DESCRIPTION</b></em></th>
            <th id="co8." headers="blank" scope="col"><em><b></b></em></th>
          </tr>
          </thead>
          <tr>
            <th id="c2" headers="blank"></th>
            <td v-if="sample.publication" headers="co6 c2">{{ sample.publication}}</td>
            <td v-else-if="!sample.publication">N/A</td>
            <td v-if="sample.survey" headers="co7 c2">{{ sample.survey}}</td>
            <td v-else-if="!sample.survey">N/A</td>
            <td v-if="sample.description" headers="co8 c2">{{ sample.description}}</td>
            <td v-else-if="!sample.description">N/A</td>
            <td headers="co8. c2"></td>
          </tr>
        </table>

        <hr>
        <hr>
        <em class="table-header-style">Sample Location at I.C.I.P.E</em>
        <br> <br>
        <table class="table table-hover">
          <thead class="blue-gradient white-text">
          <tr>
            <th id="loc_blank">&nbsp;</th>
            <th id="loc_co1" headers="loc_blank" scope="col"><em><b>LAB NAME</b></em></th>
            <th id="loc_co2" headers="loc_blank" scope="col"><em><b>ROOM NUM</b></em></th>
            <th id="loc_co3" headers="loc_blank" scope="col"><em><b>FREEZER NUM</b></em></th>
            <th id="loc_co4" headers="loc_blank" scope="col"><em><b>CHAMBER TYPE</b></em></th>
            <th id="loc_co44" headers="loc_blank" scope="col"><em><b></b></em></th>
          </tr>
          </thead>
          <tr>
            <th id="loc_c1" headers="loc_blank"></th>
            <td v-if="sample.lab" headers="loc_co1 loc_c1">{{ sample.lab }}</td>
            <td v-else-if="!sample.lab">N/A</td>
            <td v-if="sample.room" headers="loc_co2 loc_c1">{{ sample.room }}</td>
            <td v-else-if="!sample.room">N/A</td>
            <td v-if="sample.freezer" headers="loc_co3 loc_c1">{{ sample.freezer }}</td>
            <td v-else-if="!sample.freezer">N/A</td>
            <td v-if="sample.chamber" headers="loc_co4 loc_c1">{{ sample.chamber }}</td>
            <td v-else-if="!sample.chamber">N/A</td>
          </tr>
          <thead class="blue-gradient white-text">
          <tr>
            <th>&nbsp;</th>
            <th id="loc_co5" headers="loc_blank" scope="col"><em><b>RACK NUM</b></em></th>
            <th id="loc_co6" headers="loc_blank" scope="col"><em><b>TRAY NUM</b></em></th>
            <th id="loc_co7" headers="loc_blank" scope="col"><em><b>BOX LABEL</b></em></th>
            <th id="loc_co8" headers="loc_blank" scope="col"><em><b>SLOT</b></em></th>
            <th id="loc_co9" headers="loc_blank" scope="col"><em><b>RETENTION PERIOD (Sample will be stored
              until)</b></em></th>
          </tr>
          </thead>
          <tr>
            <th id="loc_c2" headers="loc_blank"></th>
            <td v-if="sample.rack" headers="loc_co5 loc_c2">{{ sample.rack }}</td>
            <td v-else>N/A</td>
            <td v-if="sample.tray" headers="loc_co6 loc_c2">{{ sample.tray }}</td>
            <td v-else-if="!sample.tray">N/A</td>
            <td v-if="sample.box" headers="loc_co7 loc_c2">{{ sample.box }}</td>
            <td v-else-if="!sample.box">N/A</td>
            <td v-if="sample.slot" headers="loc_co8 loc_c2">{{ sample.slot }}</td>
            <td v-else>N/A</td>
            <td v-if="sample.retention && isRetentionPeriodValid(sample.retention)"
                headers="loc_co9 loc_c2"> {{sample.retention }}
              <i class="fas fa-check fa-icon-checked" title="Sample available"></i>
            </td>
            <td v-if="sample.retention && !isRetentionPeriodValid(sample.retention)" class="text-danger font-weight-bold"
                headers="loc_co9 loc_c2">
              {{sample.retention }} - Sample is overdue by {{overDueRetentionPeriod(sample.retention)}}.
              <i class="fas fa-exclamation-triangle fa-icon-exclamation"
                 title="Sample not available"></i>
            </td>
            <td v-else-if="!sample.retention">N/A</td>
          </tr>
        </table>

        <em class="table-header-style">Other Important Details</em>
        <br> <br>
        <table class="table table-hover">
          <thead class="blue-gradient white-text">
          <tr>
            <th scope="col"><em><b>AMOUNT</b></em></th>
            <th scope="col"><em><b>STORAGE TEMP (Degree Celsius)</b></em><i
                class="fas fa-temperature-low"></i></th>
            <th scope="col"><em><b>BioHazard LEVEL</b></em></th>
          </tr>
          </thead>
          <tbody>
          <tr>
            <td v-if="sample.amount">{{ sample.amount }} {{ sample.quantity_type }} available on
              {{ sample.date }}
            </td>
            <td v-else-if="!sample.amount">N/A</td>
            <td v-if="sample.temperature">{{ sample.temperature}}</td>
            <td v-else-if="!sample.temperature">N/A</td>
            <td v-if="sample.securityLevel">{{ sample.securityLevel}}</td>
            <td v-else-if="!sample.securityLevel">N/A</td>
          </tr>
          </tbody>
        </table>

        <!-- SAMPLE REQUEST FORM -->
        <b-modal
            id="modal-sample-request"
            cancel-variant="danger"
            ok-title="Request"
            title="Request Sample"
            @hidden="clearForm"
            @ok="requestSample(sample.code)"
        >
          <form>

            <b-form-group id="form-amount-group"
                          label="Amount:" label-for="form-amount-input">
              <b-form-input
                  id="form-amount-input"
                  v-model="sampleRequest.amount"
                  :max="sample.amount"
                  min=1
                  placeholder="Enter Amount"
                  required
                  type="number"
              ></b-form-input>
            </b-form-group>

            <label title="Specify the date you would like to start using the sample">
              Date (Specify the date you would like to start using the sample):
            </label>
            <functional-calendar
                v-model="sampleRequest.date" :change-month-function='true'
                :change-year-function='true' :is-dark="true"
                :is-date-picker='true'
                :is-layout-expandable="true"
                :is-typeable="true"
                :limits='{min: sampleRequest.today, max:getMaxRequestDate}'
            ></functional-calendar>
          </form>
        </b-modal>

        <!--  PAGE FOOTER BUTTONS  -->
        <mdb-row class="d-flex align-items-center mb-4 mt-5">
          <mdb-col class="d-flex align-items-start" md="5">
            <a href="/sample">
              <button class="btn btn-outline-info btn-rounded" type="button">
                <i class="fas fa-arrow-left"></i>
                Back
              </button>
            </a>
          </mdb-col>
          <mdb-col class="d-flex justify-content-end" md="7">
            <div class="text-center">
              <div v-if="!isRetentionPeriodValid(sample.retention) || !isAuth">
                <button :disabled="!isRetentionPeriodValid(sample.retention) || !isAuth"
                        class="btn btn-outline-info btn-rounded"
                        type="button"> Request Sample
                  <i aria-hidden="true" class="fa fa-inbox menu_icon"> </i>
                </button>
              </div>
              <div v-else>
                <button v-b-modal.modal-sample-request
                        class="btn btn-outline-info btn-rounded"
                        type="button"> Request Sample
                  <i aria-hidden="true" class="fa fa-inbox menu_icon"> </i>
                </button>
              </div>
            </div>
            <div v-if="isSampleOwner(sample.userEmail)" class="text-center">
              <button class="btn btn-outline-info btn-rounded" type="button"
                      @click="requestUpdateSample"> Update Sample
                <i class="fas fa-pencil-alt"></i></button>
            </div>
            <div v-if="isSampleOwner(sample.userEmail)" class="text-center">
              <button class="btn btn-outline-danger btn-rounded" type="button"
                      @click="deleteSample(sample.code)"> Delete Sample
                <i class="far fa-trash-alt"></i></button>
            </div>
          </mdb-col>
        </mdb-row>
      </div>
    </div>
  </div>
</template>

<script>
import {mdbCol, mdbRow} from "mdbvue";
import TopNav from "@/components/TopNav";
import {sample_request_resource, sample_resource} from "@/utils/api_paths";
import {FunctionalCalendar} from 'vue-functional-calendar';
import axios from 'axios';
import {
  getSampleCode,
  isRetentionPeriodValid,
  isSampleOwner,
  isUserLoggedIn,
  overDueRetentionPeriod,
  redirectAfterCountDown,
  respondTo401,
  secureStoreGetAuthString,
  setSampleDetailsForEditing,
  setUpdateSample,
  showFlashMessage,
  startLoader
} from "@/utils/util_functions";

export default {
  name: "DetailedSampleView",
  data() {
    return {
      page_title: "Sample MetaData",
      response: [],

      // variable to check user status and role
      isAuth: null,

      sample: {
        theme: "",
        user: "",
        userEmail: "",
        project: "",
        projectHead: "",
        sampleType: "",
        species: "",
        description: "",
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
        slot: "",

        // extra fields
        publication: "",
        survey: "",
        lab: "",
        room: "",
        freezer: "",
        chamber: "",
        rack: "",
        tray: "",
        date: "",
      },

      sampleRequest: {
        amount: null,
        date: null,
        /* dates are limited to make sure a request is not made for a date that has already passed or
           when the sample is no longer in retention. The maximum date is placed under compute to avoid
            onLoad errors since sample by then is not set. */
        today: new Date().toLocaleDateString('en-GB'),
      },
    }
  },

  computed: {
    getMaxRequestDate: function () {
      return new Date(this.sample.retention).toLocaleDateString('en-GB')
    },
  },

  methods: {
    isRetentionPeriodValid, overDueRetentionPeriod, isSampleOwner,
    setSampleData(res) {
      this.sample.theme = res['theme.name'];
      this.sample.user = res['user.first_name'] + " " + res['user.last_name'];
      this.sample.userEmail = res['user.email'];
      this.sample.project = res['project'];
      this.sample.projectOwner = res['project_owner'];
      this.sample.sampleType = res['sample_type'];
      this.sample.species = res['animal_species'];
      this.sample.description = res['sample_description'];
      this.sample.locationCollected = res['location_collected'];
      this.sample.retention = res['retention_date'];
      this.sample.barcode = res['barcode'];
      this.sample.analysis = res['analysis'];
      this.sample.temperature = res['temperature'];
      this.sample.amount = res['amount'];
      this.sample.quantity_type = res['quantity.id'];
      this.sample.securityLevel = res['bioHazardLevel.name'];
      this.sample.code = res['code'];
      this.sample.date = this.dateNow();
      this.sample.lab = res['slot.box.tray.rack.chamber.freezer.lab.name'];
      this.sample.room = res['slot.box.tray.rack.chamber.freezer.lab.room'];
      this.sample.freezer = res['slot.box.tray.rack.chamber.freezer.number'];
      this.sample.chamber = res['slot.box.tray.rack.chamber.type'];
      this.sample.rack = res['slot.box.tray.rack.number'];
      this.sample.tray = res['slot.box.tray.number'];
      this.sample.box = res['slot.box.label'];
      this.sample.slot = res['slot.position'];
      this.sample.project = res['project.name'];
      this.sample.projectHead = res['project.lead.first_name'] + " " + res['project.lead.last_name'];
    },

    dateNow() {
      let now = Date();
      return now.toString();
    },

    getSampleByCode(code) {
      this.isAuth = isUserLoggedIn()

      let self = this;
      let loader = startLoader(this)

      axios.get(sample_resource, {
        headers:
            {
              code: code,
            }
      })
          .then((res) => {
            setTimeout(() => {
              loader.hide()
              this.response = res.data.message;
              this.setSampleData(this.response)
              this.$log.info("Response: " + res.status + " " + res.data +
                  " this.response has", this.response);
            }, 2500)
          })
          .catch((error) => {
            // eslint-disable-next-line
            loader.hide()
            this.$log.error(error);
            if (error.response) {
              if (error.response.status === 401) {
                respondTo401(self);
              } else if (error.response.status === 404) {
                showFlashMessage(self, 'error', 'Connection Error', 'Request was timed out');

              }
            }
          });
    },

    requestUpdateSample() {
      let self = this;
      let loader = startLoader(this)

      setTimeout(() => {
        loader.hide()
        setSampleDetailsForEditing(this.response)
        setUpdateSample(true)
        redirectAfterCountDown(self, '/addsample')
      }, 1000)
    },

    requestSample: function (code) {
      let self = this;
      let loader = startLoader(this)

      axios.post(sample_request_resource, {
        sample: code,
        amount: this.sampleRequest.amount,
        date: this.sampleRequest.date.selectedDate
      }, {
        headers: {
          Authorization: secureStoreGetAuthString()
        }
      })
          .then((response) => {
            setTimeout(() => {
              loader.hide()
              if (response.status === 201) {
                showFlashMessage(self, 'success', response.data['message'], '')
              }
            }, 1000)
          })
          .catch((error) => {
            this.$log.error(error);
            if (error.response) {
              if (error.response.status === 409) {
                showFlashMessage(self, 'error', 'Error', error.response.data['message'])
              } else if (error.response.status === 401) {
                respondTo401(self);
              } else if (error.response.status === 403) {
                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
              } else {
                showFlashMessage(self, 'error', 'Error', error.response.data['message'])
              }
            }
          })
    },

    clearForm() {
      this.sampleRequest.date = null
      this.sampleRequest.amount = null
    },

    deleteSample: function (code) {
      let self = this;
      let loader = startLoader(this)

      axios.delete(sample_resource, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      })
          .then((response) => {
            setTimeout(() => {
              loader.hide()
              showFlashMessage(self, 'success', response.data['message'], '');
              redirectAfterCountDown(self, '/sample')
            }, 1500)
          })
          .catch((error) => {
            this.$log.error(error);
            if (error.response) {
              if (error.response.status === 401) {
                respondTo401(self);
              } else if (error.response.status === 403) {
                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
              } else {
                showFlashMessage(self, 'error', error.response.data['message'], '');
              }
            }
          });
    },
  },
  components: {TopNav, mdbCol, mdbRow, FunctionalCalendar},
  created() {
    let code = getSampleCode()
    this.getSampleByCode(code)
  }
}
</script>

<style scoped>

</style>