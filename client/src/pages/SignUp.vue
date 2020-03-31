<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title"></top-nav>
                <section class="form-gradient" style="margin-top: 2%">
                    <mdb-row>
                        <mdb-col md="12">
                            <mdb-card>
                                <div class="header pt-3 blue-gradient">
                                    <mdb-row class="d-flex justify-content-center">
                                        <h3 class="white-text mb-3 pt-3"><i class="fa fa-user"></i> {{ page_title }} :
                                        </h3>
                                    </mdb-row>
                                </div>

                                <mdb-card-body class="mx-4 mt-4">
                                    <form @submit.prevent="submit">
                                        <div class="grey-text">

                                            <b-form-group :class="{ 'form-group--error': $v.user.firstName.$error }">
                                                <mdb-input id="fName" v-model.trim="$v.user.firstName.$model"
                                                           label="First name" icon="user" type="text"/>
                                                <div v-if="$v.user.firstName.$dirty">
                                                    <div class="error" v-if="!$v.user.firstName.required">Field is
                                                        required
                                                    </div>
                                                    <div class="error" v-if="!$v.user.firstName.minLength">Name must
                                                        have at least {{$v.user.firstName.$params.minLength.min}}
                                                        letters.
                                                    </div>
                                                </div>
                                            </b-form-group>

                                            <b-form-group :class="{ 'form-group--error': $v.user.lastName.$error }">
                                                <mdb-input id="lName" v-model.trim="$v.user.lastName.$model"
                                                           label="Last name" icon="user" type="text"/>
                                                <div v-if="$v.user.lastName.$dirty">
                                                    <div class="error" v-if="!$v.user.lastName.required">Field is
                                                        required
                                                    </div>
                                                    <div class="error" v-if="!$v.user.lastName.minLength">Name must have
                                                        at least {{$v.user.lastName.$params.minLength.min}} letters.
                                                    </div>
                                                </div>
                                            </b-form-group>

                                            <b-form-group :class="{ 'form-group--error': $v.user.email.$error }">
                                                <mdb-input id="email" v-model.trim="$v.user.email.$model"
                                                           label="Your email" icon="envelope" type="email"/>
                                                <div v-if="$v.user.email.$dirty">
                                                    <div class="error" v-if="!$v.user.email.required">Field is
                                                        required
                                                    </div>
                                                    <div class="error" v-if="!$v.user.email.email">Email mismatch.
                                                        Example johndoe123@icipe.org
                                                    </div>
                                                </div>
                                            </b-form-group>

                                            <b-form-group :class="{ 'form-group--error': $v.user.password.$error }">
                                                <mdb-input id="password" v-model.trim="$v.user.password.$model"
                                                           label="Your password" icon="lock" type="password"/>
                                                <div v-if="$v.user.password.$dirty">
                                                    <div class="error" v-if="!$v.user.password.required">Field is
                                                        required
                                                    </div>
                                                    <div class="error" v-if="!$v.user.password.minLength">Password must
                                                        have at least {{$v.user.password.$params.minLength.min}}.
                                                    </div>
                                                </div>
                                            </b-form-group>

                                            <b-form-group
                                                    :class="{ 'form-group--error': $v.user.confirmPassword.$error }">
                                                <mdb-input id="pwd-confirm"
                                                           v-model.trim="$v.user.confirmPassword.$model"
                                                           label="Confirm your confirmPassword"
                                                           icon="exclamation-triangle"
                                                           type="password"/>
                                                <div v-if="$v.user.confirmPassword.$dirty">
                                                    <div class="error" v-if="!$v.user.confirmPassword.required">Field is
                                                        required
                                                    </div>
                                                    <div class="error" v-if="!$v.user.confirmPassword.sameAsPassword">
                                                        Passwords must be
                                                        identical!{{$v.user.confirmPassword.$params.minLength.min}}.
                                                    </div>
                                                </div>
                                            </b-form-group>

                                        </div>
                                        <!--                                    </form>-->

                                    <mdb-row class="d-flex align-items-center mb-4 mt-5">
                                        <mdb-col md="5" class="d-flex align-items-start">
                                            <div class="text-center">
                                                <mdb-btn rounded type="submit" class="z-depth-1a">Register</mdb-btn>
                                            </div>
                                        </mdb-col>
                                        <mdb-col md="7" class="d-flex justify-content-end">
                                            <p class="font-small grey-text mt-3">Have an account already? <a
                                                    href="/login"
                                                    class="dark-grey-text ml-1 font-weight-bold">
                                                Log In</a></p>
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
    import {mdbBtn, mdbCard, mdbCardBody, mdbCol, mdbInput, mdbRow} from "mdbvue";
    import TopNav from "../components/TopNav";
    import {email, minLength, required, sameAs} from "vuelidate/lib/validators"

    export default {
        name: "SignUp",
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
                page_title: 'Sign Up',
                errors: [],
                user: {
                    firstName: '',
                    lastName: '',
                    email: '',
                    password: '',
                    confirmPassword: ''
                }
            }
        },

        validations: {
            user: {
                firstName: {required, minLength: minLength(3)},
                lastName: {required, minLength: minLength(3)},
                email: {required, email},
                password: {required, minLength: minLength(6)},
                confirmPassword: {required, sameAsPassword: sameAs('password')}
            }
        },

        methods: {
            submit() {
                // stop here if form is invalid
                this.$v.$touch();
                if (this.$v.$invalid) {
                    return;
                }

                alert("SUCCESS!! :-)\n\n" + JSON.stringify(this.user));

                // this.$v.form.$touch();
                // // if its still pending or an error is returned do not submit
                // if (this.$v.form.$pending || this.$v.form.$error) return;
                // // to form submit after this
                // alert("Form submitted");
            }
        }

    }
</script>