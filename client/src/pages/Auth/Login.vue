<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title"></top-nav>

                <section class="form-gradient" style="margin-top: 2%">
                    <mdb-row>
                        <mdb-col md="12">
                            <mdb-card>
                                <!-- FLASH MESSAGES -->
                                <FlashMessage :position="'right bottom'"></FlashMessage>
                                <div class="header pt-3 blue-gradient">
                                    <mdb-row class="d-flex justify-content-center">
                                        <h3 class="white-text mb-3 pt-3"><i class="fa fa-lock"></i> Log In:</h3>
                                    </mdb-row>
                                </div>

                                <mdb-card-body class="mx-4 mt-4">
                                    <form @submit.prevent="onSubmit">
                                        <div class="grey-text">
                                            <!--EMAIL-->
                                            <b-form-group :class="{ 'form-group--error': $v.user.email.$error }">
                                                <mdb-input icon="envelope" id="email"
                                                           label="Your email" type="email"
                                                           v-model.trim="$v.user.email.$model"/>
                                                <div v-if="$v.user.email.$dirty">
                                                    <div class="error" v-if="!$v.user.email.required">Field is
                                                        required
                                                    </div>
                                                    <div class="error" v-if="!$v.user.email.email">Email mismatch.
                                                        Example johndoe123@icipe.org
                                                    </div>
                                                </div>
                                            </b-form-group>

                                            <!--PASSWORD-->
                                            <b-form-group :class="{ 'form-group--error': $v.user.password.$error }">
                                                <div class="row">
                                                    <mdb-input class="form_input_margin" icon="lock"
                                                               id="password" label="Your password"
                                                               type="password" v-model.trim="$v.user.password.$model"/>
                                                    <span :title="'see raw password'" @click="viewPassword()"
                                                          aria-hidden="true"
                                                          class="fa fa-fw fa-eye" id="view-pwd"
                                                          v-b-tooltip.hover/>
                                                </div>
                                                <div v-if="$v.user.password.$dirty">
                                                    <div class="error" v-if="!$v.user.password.required">Field is
                                                        required
                                                    </div>
                                                </div>
                                            </b-form-group>

                                            <!-- Remember Me -->
                                            <div class="form-check">
                                                <input class="form-check-input" id="materialUnchecked"
                                                       type="checkbox" v-model="$v.user.checked">
                                                <label class="form-check-label" for="materialUnchecked">Remember
                                                    Me?</label>
                                            </div>
                                        </div>

                                        <br>
                                        <p class="font-small grey-text d-flex justify-content-end">Forgot <a
                                                class="dark-grey-text ml-1 font-weight-bold"
                                                href="/forgot">
                                            Password?</a></p>
                                        <mdb-row class="d-flex align-items-center mb-4 mt-5">
                                            <mdb-col class="d-flex align-items-start" md="5">
                                                <div class="text-center">
                                                    <mdb-btn class="z-depth-1a" rounded type="submit">Login</mdb-btn>
                                                </div>
                                            </mdb-col>
                                            <mdb-col class="d-flex justify-content-end" md="7">
                                                <p class="font-small grey-text mt-3">Don't have an account? <a
                                                        class="dark-grey-text ml-1 font-weight-bold"
                                                        href="/register">
                                                    Sign up</a></p>
                                            </mdb-col>
                                        </mdb-row>
                                    </form>
                                </mdb-card-body>
                            </mdb-card>
                        </mdb-col>
                    </mdb-row>
                </section>

            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import 'es6-promise/auto';
import TopNav from "../../components/TopNav";
import {auth_resource} from "@/utils/api_paths";
import {email, required} from "vuelidate/lib/validators";
import {mdbBtn, mdbCard, mdbCardBody, mdbCol, mdbInput, mdbRow} from "mdbvue";
import {
  handleError,
  isUserLoggedIn,
  redirectAfterCountDown,
  secureStoreSetUserInfo,
  showFlashMessage,
  startLoader,
  viewPassword
} from "@/utils/util_functions";

export default {
  components: {
    mdbInput,
    mdbBtn,
    mdbCard,
    mdbCardBody,
    mdbCol,
    mdbRow,
    TopNav
  },

        data() {
            return {
                page_title: 'Log In',
                user: {
                    email: '',
                    password: '',
                    checked: []
                },
                show: true,
            }
        },

        validations: {
            user: {
                email: {required, email},
                password: {required},
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
                this.logInUser(this.user);
            },

            logInUser: function (user) {
                let loader = startLoader(this)

                axios.post(auth_resource, {
                    email: user.email,
                    password: user.password
                }).then((response) => {
                        setTimeout(() => {
                            loader.hide()
                            // redirect after successful login
                            if (response.status === 200) {
                              showFlashMessage(this, 'success', 'Logged In', 'Redirecting you to home page in ' +
                                  redirectAfterCountDown(this, '/home') + " seconds");
                              // set jwt token required across requests
                              secureStoreSetUserInfo(response.data.message.token, response.data.message.email, response.data.message.first_name,
                                  response.data.message.last_name, response.data.message['role.name']);
                            } else if (response.status === 203) {
                              showFlashMessage(this, 'error', response.data.message, 'You can request for reactivation email')
                              redirectAfterCountDown(this, '/requestConfirmation')
                            } else if (response.status === 204) {
                                showFlashMessage(this, 'error', 'User found but account is deactivated!', 'You can reactivate by signing up again')
                            }
                        }, 3000)
                }).catch((error) => { handleError( this, error, loader)})
            },
        },
  created() {
    if (isUserLoggedIn()) redirectAfterCountDown(this, '/user');
  }
}
</script>
