<template>
  <form @submit.prevent="onSubmit">
    <!-- STATUS -->
    <b-form-group class="form_input_margin">
      <i class="fas fa-question"></i> Status: <br/>
      <ejs-dropdownlist
          :dataSource='statusDataList'
          :fields="fields"
          v-model.trim="$v.sampleResponse.status.$model"
          id='dropdownlist'
          placeholder='Select a response'
      ></ejs-dropdownlist>
      <div v-if="$v.sampleResponse.status.$dirty">
        <div class="error" v-if="!$v.sampleResponse.status.required">Status is required!</div>
      </div>
    </b-form-group>


    <!-- APPROVED AMOUNT -->
    <b-form-group>
      <mdb-input class="form_input_margin" icon="fas fa-balance-scale-right"
                 id="amount" label="Amount Approved"
                 :min=sampleResponse.amount type="number"
                 v-model.number.trim="$v.sampleResponse.amount.$model"/>

      <div v-if="$v.sampleResponse.amount.$dirty">
        <div class="error" v-if="!$v.sampleResponse.amount.required">Amount is
          required
        </div>
      </div>
    </b-form-group>

    <!--Notes-->
    <div class="form-group">
      <label for="description">Notes: (Quick response to the requester)</label>
      <textarea class="form-control" id="description" name="description"
                type="text"
                v-model="sampleResponse.notes"/>
    </div>

    <mdb-row class="d-flex align-items-center mb-4 mt-5">
      <mdb-col class="d-flex justify-content-end" md="12">
        <div class="text-center">
          <mdb-btn class="z-depth-1a" rounded type="submit">Respond</mdb-btn>
        </div>
      </mdb-col>
    </mdb-row>
  </form>
</template>

<script>
import {mdbBtn, mdbCol, mdbInput, mdbRow} from "mdbvue";
import {required} from "vuelidate/lib/validators";
import {APPROVED_STATUS, DECLINED_STATUS} from "@/utils/constants";
import {sample_response_resource} from "@/utils/api_paths";
import {
  getSelectedItemCode,
  redirectAfterCountDown,
  respondTo401,
  secureStoreGetAuthString,
  showFlashMessage,
  startLoader
} from "@/utils/util_functions";
import axios from "axios";
import EventBus from "@/components/EventBus";

export default {
  name: "SampleResponseForm",
  data() {
    return {
      statusDataList: [
        {'Code': APPROVED_STATUS, 'Name': 'Approved'},
        {'Code': DECLINED_STATUS, 'Name': 'Declined'},
      ],
      fields: {
        text: 'Name',
        value: 'Code'
      },
      sampleResponse: {
        status: null,
        amount: 0,
        notes: "",
        code: "",
      }
    }
  },
  validations: {
    sampleResponse: {
      status: {required},
      amount: {required}
    }
  },

  mounted() {
    EventBus.$on('request-code', payload => {
      console.log("request code is: " + payload)
      this.sampleResponse.code = payload
    })
  },

  methods: {
    onSubmit() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }

      // component is called in diff. places. Close component where it's rendered in a modal box
      EventBus.$emit('close-modal', false)
      this.responsePath = sample_response_resource.concat(this.$router.currentRoute.params.pathMatch)
      this.makeResponse(this.responsePath)
    },

    makeResponse: function (path) {
      let self = this;
      let loader = startLoader(this)
      this.sampleResponse.status = getSelectedItemCode('dropdownlist', this.statusDataList);

      axios.put(path, {
        status: this.sampleResponse.status,
        approved_amount: this.sampleResponse.amount,
        notes: this.sampleResponse.notes
      }, {
        headers: {
          code: this.sampleResponse.code,
          Authorization: secureStoreGetAuthString()
        }
      })
          .then((response) => {
            setTimeout(() => {
              loader.hide()
              if (response.status === 200) {
                showFlashMessage(self, 'success', response.data['message'], '')
                redirectAfterCountDown(self, '/user')
              }
            }, 1000)
          })
          .catch((error) => {
            loader.hide()
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
    }
  },
  components: {
    mdbInput,
    mdbBtn,
    mdbCol,
    mdbRow,
  },
}
</script>

<style scoped>

</style>