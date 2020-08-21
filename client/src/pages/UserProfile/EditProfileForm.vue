<template>
    <div>
        <top-nav :page_title="page_title"></top-nav>
        <br>
        <mdb-card>
            <!-- FLASH MESSAGES -->
            <FlashMessage :position="'right bottom'"></FlashMessage>
            <div class="header pt-3 blue-gradient">
                <mdb-card-header :data-background-color="dataBackgroundColor">
                    <mdb-row class="d-flex justify-content-center">
                        <h4 class="white-text mb-3 pt-3 title">Complete your profile</h4>
                    </mdb-row>
                </mdb-card-header>
            </div>

            <mdb-card-body class="mx-4 mt-4">
                <form @submit.prevent="onSubmit">
                    <div>
                        <!--FIRST NAME-->
                        <b-form-group :class="{ 'form-group--error': $v.user.firstName.$error }">
                            <mdb-input icon="user" id="fName"
                                       label="First name" type="text" v-model.trim="$v.user.firstName.$model"/>
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
                            <mdb-input icon="user" id="lName"
                                       label="Last name" type="text" v-model.trim="$v.user.lastName.$model"/>
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
                                    :dataSource='roleDataList'
                                    :fields="fields"
                                    :v-model="user.role"
                                    :value="selectDropDownItemForUpdate('dropdownlist', user.role, roleDataList)"
                                    id='dropdownlist'
                                    placeholder='Select a role'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <!--EMAIL-->
                        <b-form-group :class="{ 'form-group--error': $v.user.email.$error }">
                            <mdb-input icon="envelope" id="email"
                                       label="Your email" type="email" v-model.trim="$v.user.email.$model"/>
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

                    <mdb-row class="d-flex align-items-center mb-4 mt-5">
                        <mdb-col class="d-flex align-items-start" md="5">
                            <a href="/user">
                                <button class="btn btn-outline-info btn-rounded" type="button">
                                    <i class="fas fa-arrow-left"></i>
                                    Back
                                </button>
                            </a>
                        </mdb-col>
                        <mdb-col class="d-flex justify-content-end" md="7">
                            <div class="text-center">
                                <button @click="onSubmit" class="btn btn-outline-info btn-rounded"
                                        type="button"> Update
                                    <i class="fas fa-pencil-alt"></i></button>
                            </div>

                            <!--  DEACTIVATE USER    -->
                            <div>
                                <div class="text-center">
                                    <button v-b-modal.modal-user-deactivate
                                            class="btn btn-outline-danger btn-rounded"
                                            type="button"> Deactivate Account
                                        <i class="fas fa-user-lock"></i>
                                    </button>
                                </div>

                                <b-modal
                                        @ok="deactivateAccount"
                                        cancel-variant="info"
                                        id="modal-user-deactivate"
                                        ok-title="Deactivate"
                                        ok-variant="danger"
                                        title="Deactivate Account?"
                                >
                                    <p>
                                        Are you sure you want to deactivate your account?
                                        <i class="far fa-sad-tear menu_icon"></i>
                                        You can always reactivate by <em>Signing Up</em> again!
                                    </p>
                                </b-modal>
                            </div>
                        </mdb-col>
                    </mdb-row>
                </form>
            </mdb-card-body>
        </mdb-card>
    </div>
</template>
<script>
import {mdbCard, mdbCardBody, mdbCardHeader, mdbCol, mdbInput, mdbRow} from "mdbvue";
import TopNav from "../../components/TopNav";
import {
  extractApiData,
  getItemDataList,
  getSelectedItem,
  getStoredUserDetails,
  getUserEmail,
  redirectAfterCountDown,
  respondTo401,
  secureStoreDeleteUserInfo,
  secureStoreGetString,
  selectDropDownItemForUpdate,
  showFlashMessage,
  startLoader,
  viewPassword
} from '@/utils/util_functions';
import {email, minLength, required} from "vuelidate/lib/validators";
import {role_resource, user_resource} from "@/utils/api_paths";
import axios from "axios";

export default {
  name: "edit-profile-form",
  props: {
    dataBackgroundColor: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      page_title: "Edit Profile",
                roleDataList: [],
                fields: {text: '', value: ''},
                user: {
                    firstName: '',
                    lastName: '',
                    role: '',
                    email: ''
                },
            };
        },
        validations: {
            user: {
                firstName: {required, minLength: minLength(3)},
                lastName: {required, minLength: minLength(3)},
                email: {required, email},
            }
        },
        methods: {
            viewPassword, selectDropDownItemForUpdate,
            onSubmit() {
                this.$v.$touch();
                if (this.$v.$invalid) {
                    this.$log.info("FORM INVALID!");
                    return;
                }
                this.updateUser(this.user);
            },
            onLoadPage() {
                getItemDataList(role_resource).then(data => {
                    let roleList = extractApiData(data);
                    // this.$log.info("Role list json: ", JSON.stringify(roleList));

                    // update local variables with data from API
                    this.fields = roleList['fields'];
                    for (let i = 0; i < roleList.items.length; i++) {
                        this.roleDataList.push({
                            'Code': roleList.items[i].Code,
                            'Name': roleList.items[i].Name,
                        });
                    }
                })

                this.fillUserFormForUpdate()
            },

            // set user details in form
            fillUserFormForUpdate: function () {
                let userForUpdate = getStoredUserDetails()
                this.user.firstName = userForUpdate['first_name']
                this.user.lastName = userForUpdate['last_name']
                this.user.role = userForUpdate['role']
                this.user.email = getUserEmail()
            },


            updateUser: function (user) {
                let self = this;
                let loader = startLoader(this)

                this.user.role = getSelectedItem(this.roleDataList, this.user.role);
                axios.put(user_resource, {
                    first_name: user.firstName,
                    last_name: user.lastName,
                    email: user.email,
                    role: user.role
                }, {
                    headers:
                        {
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        // redirect after successful signUp
                        if (response.status === 202) {
                            setTimeout(() => {
                              loader.hide()
                              showFlashMessage(self, 'success', 'User Updated', 'Redirecting you to your dashboard ' +
                                  redirectAfterCountDown(self, '/user') + " seconds");
                            }, 2500)
                        }
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        loader.hide()
                        if (error.response) {
                            if (error.response.status === 409) {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            } else if (error.response.status === 304) {
                                showFlashMessage(self, 'error', 'Record not modified', "You didn't make any changes");
                            } else if (error.response.status === 400) {
                                showFlashMessage(self, 'error', error.response.data['message'], 'Kindly refill the form');
                            } else if (error.response.status === 401) {
                                respondTo401(self)
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else if (error.response.status === 500) {
                                showFlashMessage(self, 'error', "Fatal Error", 'Admin has been contacted.');
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    })

            },
            deactivateAccount() {
                let self = this;
                let loader = startLoader(this)

                axios.delete(user_resource, {
                    headers:
                        {
                            Authorization: secureStoreGetString(),
                            deactivate: true
                        }
                })
                    .then((response) => {
                        // redirect after successful signUp
                        if (response.status === 200) {
                            setTimeout(() => {
                              secureStoreDeleteUserInfo()
                              loader.hide()
                              showFlashMessage(self, 'success', 'Account Deactivated', 'Your account has been successfully deactivated.' +
                                  '\nSorry to see you go.');
                              +redirectAfterCountDown(self, '/home')
                            }, 2500)
                        }
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        loader.hide()
                        if (error.response) {
                            if (error.response.status === 409) {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            } else if (error.response.status === 404) {
                                showFlashMessage(self, 'error', 'User not found', "");
                            } else if (error.response.status === 400) {
                                showFlashMessage(self, 'error', error.response.data['message'], 'Kindly refill the form');
                            } else if (error.response.status === 401) {
                                respondTo401(self)
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else if (error.response.status === 500) {
                                showFlashMessage(self, 'error', "Fatal Error", 'Admin has been contacted.');
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    })
            },
        },
        components: {mdbCard, mdbCardHeader, mdbCardBody, mdbRow, mdbCol, mdbInput, TopNav},
        created() {
            this.onLoadPage();
        }
    };
</script>
<style></style>
