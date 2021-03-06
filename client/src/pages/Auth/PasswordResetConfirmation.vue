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
                  <h3 class="white-text mb-3 pt-3"> Password Reset</h3>
                </mdb-row>
              </div>

              <mdb-card-body class="mx-4 mt-4">
                <div id="form">
                  <form @submit.prevent="onSubmit">
                    <div class="grey-text">
                      <!--PASSWORD-->
                      <b-form-group :class="{ 'form-group--error': $v.user.password.$error }">
                        <div class="row">
                          <mdb-input id="password" v-model.trim="$v.user.password.$model"
                                     class="form_input_margin" icon="lock"
                                     label="Your password" type="password"/>
                          <span id="view-pwd" v-b-tooltip.hover
                                :title="'see raw password'"
                                aria-hidden="true" class="fa fa-fw fa-eye"
                                @click="viewPassword()"/>
                        </div>
                        <div v-if="$v.user.password.$dirty">
                          <div v-if="!$v.user.password.required" class="error">Field is
                            required
                          </div>
                          <div v-if="!$v.user.password.strongPassword" class="error">
                            Strong passwords need to have a letter, a number, a special
                            character, and be more than 8 characters long..
                          </div>
                        </div>
                      </b-form-group>

                      <!--REPEAT PASSWORD-->
                      <b-form-group
                          :class="{ 'form-group--error': $v.user.confirmPassword.$error }">
                        <mdb-input id="confirmPassword"
                                   v-model.trim="$v.user.confirmPassword.$model"
                                   icon="exclamation-triangle"
                                   label="Confirm your password"
                                   type="password"/>
                        <div v-if="$v.user.confirmPassword.$dirty">
                          <div v-if="!$v.user.confirmPassword.required" class="error">Field is
                            required
                          </div>
                          <div v-if="!$v.user.confirmPassword.sameAsPassword" class="error">
                            Passwords must be identical!
                          </div>
                        </div>
                      </b-form-group>
                    </div>

                    <br>
                    <mdb-row class="d-flex align-items-center mb-4 mt-5">
                      <mdb-col class="d-flex align-items-start" md="12">
                        <div class="text-center">
                          <mdb-btn class="z-depth-1a" rounded type="submit">Reset</mdb-btn>
                        </div>
                      </mdb-col>
                    </mdb-row>
                  </form>
                </div>

                <div id="response">
                  <div v-if="success">
                    <h2><i class="fas fa-check menu_icon_large_success"></i> {{ success }}
                      <i class="fas fa-smile-wink menu_icon_large"></i></h2>
                  </div>
                  <div v-else-if="fail">
                    <h2><i class="fas fa-times menu_icon_large_danger"></i> {{ fail }}
                      <i class="fas fa-sad-tear menu_icon_large"></i></h2>
                  </div>
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
import axios from "axios";
import TopNav from "../../components/TopNav";
import {password_reset_resource} from "@/utils/api_paths";
import {
  handleError,
  redirectAfterCountDown,
  showFlashMessage,
  startLoader,
  strongPassword,
  viewPassword
} from "@/utils/util_functions";
import {mdbBtn, mdbCard, mdbCardBody, mdbCol, mdbInput, mdbRow} from "mdbvue";
import {required, sameAs} from "vuelidate/lib/validators";

export default {
  name: "PasswordResetConfirmation",
  data() {
    return {
      page_title: "Password Reset",
      response: null,
      success: '',
      fail: '',
      resetPath: '',
      user: {
        password: '',
        confirmPassword: ''
      }
    }
  },

  validations: {
    user: {
      password: {required, strongPassword},
      confirmPassword: {required, sameAsPassword: sameAs('password')}
    }
  },

  methods: {
    viewPassword,
    onSubmit() {
      // stop here if form is invalid
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      this.resetPath = password_reset_resource.concat(this.$router.currentRoute.params.pathMatch)
      this.resetPassword(this.resetPath)
    },

    resetPassword(path) {
      let loader = startLoader(this)

      axios.post(path, {
        password: this.user.password
      })
          .then((response) => {
            setTimeout(() => {
              loader.hide()
              // redirect after successful login
              if (response.status === 200) {
                this.success = response.data.message.response
                this.showHideDiv()
                showFlashMessage(this, 'success', response.data.message, 'Redirecting you to login page in ' +
                    redirectAfterCountDown(this, '/login') + " seconds");
              }
            }, 3000)
          })
          .catch((error) => {
            this.fail = handleError(this, error, loader)
          });
    },

    showHideDiv() {
      let form = document.getElementById("form");
      let resBody = document.getElementById("response");

      if (this.response === null) {
        resBody.style.display = "none";
      } else if (this.response) {
        form.style.display = "none";
      }
    },
  },
  components: {TopNav, mdbCard, mdbCardBody, mdbCol, mdbRow, mdbBtn, mdbInput},
  created() {
    this.showHideDiv()
  }
}
</script>

<style scoped>

</style>