<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title"></top-nav>

                <section class="form-gradient" style="margin-top: 2%">
                    <mdb-row>
                        <mdb-col md="12">
                            <mdb-card>
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
                                                href="#">
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
    import {mdbBtn, mdbCard, mdbCardBody, mdbCol, mdbInput, mdbRow} from "mdbvue";
    import TopNav from "../components/TopNav";
    import {email, required} from "vuelidate/lib/validators";
    import {countDownTimer, secureStoreSetString, showFlashMessage, viewPassword} from "../utils/util_functions";
    import {auth_resource} from "../utils/api_paths";

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
                countDown: 3,
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
                    this.$log.info("FORM INVALID!");
                    return;
                }
                this.$log.info("FORM VALID!");
                // api call to authentication user.
                this.logInUser(this.user);
            },

            logInUser: function (user) {
                let self = this;

                axios.post(auth_resource, {
                    email: user.email,
                    password: user.password
                })
                    .then((response) => {
                        // redirect after successful login
                        if (response.status === 200) {
                            showFlashMessage(self, 'success', 'Logged In', 'Redirecting you to home page in ' +
                                countDownTimer(self, this.countDown, '/home') + " seconds");
                            // set jwt token required across requests
                            secureStoreSetString(response.data.message.token, response.data.message.email, response.data.message.first_name,
                                response.data.message.last_name, response.data.message['role.name']);
                        }
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        this.$log.error("error: ", error.response.status);
                        if (error.response) {
                            if (error.response.status === 403) {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            } else if (error.response.status === 404) {
                                showFlashMessage(self, 'error', error.response.data['message'], 'Try to SignUp instead');
                            } else if (error.response.status === 500) {
                                showFlashMessage(self, 'error', "Fatal Error", 'Admin has been contacted.');
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    })
            },
        }
    }
</script>
