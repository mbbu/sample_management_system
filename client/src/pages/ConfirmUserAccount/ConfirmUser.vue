<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-12">
        <top-nav :page_title="page_title"></top-nav>
        <mdb-row>
          <mdb-col md="12">
            <mdb-card>
              <!-- FLASH MESSAGES -->
              <FlashMessage :position="'right bottom'"></FlashMessage>
              <div class="header pt-3 blue-gradient">
                <mdb-row class="d-flex justify-content-center">
                  <h3 class="white-text mb-3 pt-3"><i class="fas fa-question"></i> Confirmation Status
                  </h3>
                </mdb-row>
              </div>

              <mdb-card-body class="mx-4 mt-4">
                <div v-if="success">
                  <h2><i class="fas fa-check menu_icon_large_success"></i> {{ success }}
                    <i class="fas fa-smile-wink menu_icon_large"></i></h2>
                </div>
                <div v-else-if="fail">
                  <h2><i class="fas fa-times menu_icon_large_danger"></i> {{ fail }}
                    <i class="fas fa-sad-tear menu_icon_large"></i></h2>
                </div>

              </mdb-card-body>
            </mdb-card>
          </mdb-col>
        </mdb-row>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import TopNav from "../../components/TopNav";
import {mdbCard, mdbCardBody, mdbCol, mdbRow} from "mdbvue";
import {email_confirm_resource} from "@/utils/api_paths";
import {
  handleError,
  redirectAfterCountDown,
  secureStoreSetUserInfo,
  showFlashMessage,
  startLoader
} from "@/utils/util_functions";

export default {
  name: "ConfirmUser",
  data() {
    return {
      page_title: "Confirm Account",
      response: null,
      success: '',
      fail: '',
      confirmationPath: ''
    }
  },

  methods: {
    checkAccount(path) {
      let loader = startLoader(this)

      axios.get(path)
          .then((response) => {
            setTimeout(() => {
              loader.hide()
              // redirect after successful login
              if (response.status === 200) {
                this.success = response.data.message.response
                showFlashMessage(this, 'success', response.data.message.response, 'Redirecting you to home page in ' +
                    redirectAfterCountDown(this, '/home') + " seconds");

                // set jwt token required across requests
                secureStoreSetUserInfo(response.data.message.token, response.data.message.email, response.data.message.first_name,
                    response.data.message.last_name, response.data.message['role.code']);
              }
            }, 3000)
          })
          .catch((error) => {
            this.fail = handleError(this, error, loader)
          });
    }
  },
  components: {TopNav, mdbCard, mdbCardBody, mdbCol, mdbRow},
  created() {
    this.confirmationPath = email_confirm_resource.concat(this.$router.currentRoute.params.pathMatch)
    this.checkAccount(this.confirmationPath)
  }
}
</script>

<style scoped>

</style>