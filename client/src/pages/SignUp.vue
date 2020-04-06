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
                                        <h3 class="white-text mb-3 pt-3"><i class="fa fa-user"></i> {{ page_title }} :
                                        </h3>
                                    </mdb-row>
                                </div>

                                <mdb-card-body class="mx-4 mt-4">
                                    <form @submit.prevent="onSubmit">
                                        <div>
                                            <!--FIRST NAME-->
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

                                            <!--LAST NAME-->
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

                                            <!-- ROLE -->
                                            <!-- LIST POPULATED FROM ROLE RESOURCE -->
                                            <b-form-group class="form_input_margin">
                                                <i class="fas fa-user-cog"></i> Role: <br/>
                                                <ejs-dropdownlist
                                                        id='dropdownlist'
                                                        :dataSource='roleDataList'
                                                        :fields="fields"
                                                        placeholder='Select a role'
                                                        :v-model="user.role"
                                                ></ejs-dropdownlist>
                                            </b-form-group>

                                            <!--EMAIL-->
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

                                            <!--PASSWORD-->
                                            <b-form-group :class="{ 'form-group--error': $v.user.password.$error }">
                                                <div class="row">
                                                    <mdb-input id="password" v-model.trim="$v.user.password.$model"
                                                               class="form_input_margin" label="Your password"
                                                               icon="lock" type="password"/>
                                                    <span id="view-pwd" class="fa fa-fw fa-eye" aria-hidden="true"
                                                          v-b-tooltip.hover :title="'see raw password'"
                                                          @click="viewPassword()"/>
                                                </div>
                                                <div v-if="$v.user.password.$dirty">
                                                    <div class="error" v-if="!$v.user.password.required">Field is
                                                        required
                                                    </div>
                                                    <div class="error" v-if="!$v.user.password.strongPassword">
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
                                                           label="Confirm your password"
                                                           icon="exclamation-triangle"
                                                           type="password"/>
                                                <div v-if="$v.user.confirmPassword.$dirty">
                                                    <div class="error" v-if="!$v.user.confirmPassword.required">Field is
                                                        required
                                                    </div>
                                                    <div class="error" v-if="!$v.user.confirmPassword.sameAsPassword">
                                                        Passwords must be
                                                        identical!
                                                    </div>
                                                </div>
                                            </b-form-group>
                                        </div>

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
    import axios from 'axios';
    import {mdbBtn, mdbCard, mdbCardBody, mdbCol, mdbInput, mdbRow} from "mdbvue";
    import TopNav from "../components/TopNav";
    import {email, minLength, required, sameAs} from "vuelidate/lib/validators"
    import {role_resource, user_resource} from "../utils/api_paths";
    import {
        countDownTimer,
        extractApiData,
        getItemDataList,
        getSelectedItem,
        showFlashMessage
    } from "../utils/util_functions"

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
                roleDataList: [],
                fields: {text: '', value: ''},
                user: {
                    firstName: '',
                    lastName: '',
                    role: '',
                    email: '',
                    password: '',
                    confirmPassword: ''
                },
                countDown: 5,
            };
        },

        validations: {
            user: {
                firstName: {required, minLength: minLength(3)},
                lastName: {required, minLength: minLength(3)},
                // role: {required},
                email: {required, email},
                password: {
                    required,
                    strongPassword(password1) {
                        return (
                            /[a-z]/.test(password1) && //checks for a-z
                            /[0-9]/.test(password1) && //checks for 0-9
                            /\W|_/.test(password1) && //checks for special char
                            password1.length >= 6
                        );
                    }
                },
                confirmPassword: {required, sameAsPassword: sameAs('password')}
            }
        },

        methods: {
            clearForm(user) {
                user.firstName = null;
                user.lastName = null;
                user.email = null;
                user.role = null;
                user.password = null;
                user.confirmPassword = null;
                this.roleDataList = [];
            },

            onSubmit() {
                this.$log.info("FORM SUBMIT METHOD CALLED!");
                // stop here if form is invalid
                this.$v.$touch();
                if (this.$v.$invalid) {
                    this.$log.info("FORM INVALID!");
                    return;
                }
                this.$log.info("FORM VALID!");
                // api call to create user.
                this.createUser(this.user);
            },

            viewPassword() {
                let passwordInput = document.getElementById('password');
                let pwdEyeIcon = document.getElementById('view-pwd');

                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    pwdEyeIcon.className = 'fa fa-eye-slash';
                } else {
                    passwordInput.type = 'password';
                    pwdEyeIcon.className = 'fa fa-eye';
                }
            },

            onLoadPage() {
                getItemDataList(role_resource).then(data => {
                    let roleList = extractApiData(data);
                    this.$log.info("Role list json: ", JSON.stringify(roleList));

                    // update local variables with data from API
                    this.fields = roleList['fields'];
                    for (let i = 0; i < roleList.items.length; i++) {
                        this.roleDataList.push({
                            'Code': roleList.items[i].Code,
                            'Name': roleList.items[i].Name,
                        });
                    }
                    this.$log.info("Extracted data as json fields: ", this.fields);
                    this.$log.info("Extracted roleDataList items: ", this.roleDataList)
                })
            },


            createUser: function (user) {
                let self = this;

                this.user.role = getSelectedItem(this.roleDataList, this.user.role);
                axios.post(user_resource, {
                    first_name: user.firstName,
                    last_name: user.lastName,
                    email: user.email,
                    role: user.role,
                    password: user.password
                })
                    .then((response) => {
                        // redirect after successful signUp
                        if (response.status === 201) {
                            showFlashMessage(self, 'success', 'User Created', 'Redirecting you to home page in ' + countDownTimer(self, this.countDown) + " seconds");
                            // todo: store jwt tokens to be used for transactions
                            // this.countDownTimer();
                        }
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 409) {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            } else if (error.response.status === 400) {
                                showFlashMessage(self, 'error', error.response.data['message'], 'Kindly refill the form');
                            } else if (error.response.status === 500) {
                                showFlashMessage(self, 'error', "Fatal Error", 'Admin has been contacted.');
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    })

            },
        },
        created() {
            this.onLoadPage();
        }

    }
</script>