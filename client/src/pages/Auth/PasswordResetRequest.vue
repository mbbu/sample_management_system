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
                                        <h3 class="white-text mb-3 pt-3"><i class="fas fa-inbox"></i> Request
                                            Password Reset</h3>
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
                                        </div>

                                        <br>
                                        <mdb-row class="d-flex align-items-center mb-4 mt-5">
                                            <mdb-col class="d-flex align-items-start" md="12">
                                                <div class="text-center">
                                                    <mdb-btn class="z-depth-1a" rounded type="submit">Request</mdb-btn>
                                                </div>
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
    import {email, required} from "vuelidate/lib/validators";
    import axios from "axios";
    import {request_password_reset_resource} from "../../utils/api_paths";
    import {countDownTimer, showFlashMessage, startLoader} from "../../utils/util_functions";
    import {mdbBtn, mdbCard, mdbCardBody, mdbCol, mdbInput, mdbRow} from "mdbvue";
    import TopNav from "../../components/TopNav";

    export default {
        name: "PasswordResetRequest",
        data() {
            return {
                page_title: "Password Reset",
                user: {
                    email: ''
                }
            }
        },
        validations: {
            user: {
                email: {required, email},
            }
        },
        methods: {
            onSubmit() {
                this.$v.$touch();
                if (this.$v.$invalid) {
                    return;
                }
                this.sendResetEmail(this.user);
            },
            sendResetEmail(user) {
                let loader = startLoader(this)
                let self = this;
                axios.post(request_password_reset_resource, {email: user.email})
                    .then((response) => {
                        setTimeout(() => {
                            loader.hide()
                            if (response.status === 200) {
                                showFlashMessage(self, 'success', 'Email sent', 'Check your email');
                                countDownTimer(self, 5, '/home')
                            }
                        }, 3000)
                    })
                    .catch((error) => {
                        loader.hide()
                        this.$log.error(error);
                        this.$log.error("error: ", error.response.status);
                        if (error.response) {
                            showFlashMessage(self, 'error', error.response.data['message'], 'Email not sent');
                        }
                    })
            }
        },
        components: {
            mdbBtn, mdbCard, mdbCardBody, mdbCol, mdbInput, mdbRow, TopNav
        }
    }
</script>

<style scoped>

</style>