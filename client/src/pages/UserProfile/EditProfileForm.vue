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
              <mdb-input id="fName" v-model.trim="$v.user.firstName.$model"
                         icon="user" label="First name" type="text"/>
              <div v-if="$v.user.firstName.$dirty">
                <div v-if="!$v.user.firstName.required" class="error">Field is
                  required
                </div>
                <div v-if="!$v.user.firstName.minLength" class="error">Name must
                  have at least {{ $v.user.firstName.$params.minLength.min }}
                  letters.
                </div>
              </div>
            </b-form-group>

            <!--LAST NAME-->
            <b-form-group :class="{ 'form-group--error': $v.user.lastName.$error }">
              <mdb-input id="lName" v-model.trim="$v.user.lastName.$model"
                         icon="user" label="Last name" type="text"/>
              <div v-if="$v.user.lastName.$dirty">
                <div v-if="!$v.user.lastName.required" class="error">Field is
                  required
                </div>
                <div v-if="!$v.user.lastName.minLength" class="error">Name must have
                  at least {{ $v.user.lastName.$params.minLength.min }} letters.
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
                  :v-model="user.role"
                  :value="selectDropDownItemForUpdate('dropdownlist', user.role, roleDataList)"
                  placeholder='Select a role'
              ></ejs-dropdownlist>
            </b-form-group>

            <!--EMAIL-->
            <b-form-group :class="{ 'form-group--error': $v.user.email.$error }">
              <mdb-input id="email" v-model.trim="$v.user.email.$model"
                         icon="envelope" label="Your email" type="email"/>
              <div v-if="$v.user.email.$dirty">
                <div v-if="!$v.user.email.required" class="error">Field is
                  required
                </div>
                <div v-if="!$v.user.email.email" class="error">Email mismatch.
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
                <button class="btn btn-outline-info btn-rounded" type="button"
                        @click="onSubmit"> Update
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
                    id="modal-user-deactivate"
                    cancel-variant="info"
                    ok-title="Deactivate"
                    ok-variant="danger"
                    title="Deactivate Account?"
                    @ok="deactivateAccount"
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
  handleError,
  logOutUser,
  redirectAfterCountDown,
  secureStoreDeleteUserInfo,
  secureStoreGetAuthString,
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
        return;
      }
      this.updateUser(this.user);
    },
    onLoadPage() {
      getItemDataList(role_resource).then(data => {
        let roleList = extractApiData(data);

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
              Authorization: secureStoreGetAuthString()
            }
      })
          .then((response) => {
            // redirect after successful signUp
            if (response.status === 202) {
              setTimeout(() => {
                loader.hide()
                showFlashMessage(this, 'success', 'User Updated', 'Please log-in for changes to take effect ');
              }, 1500)
              logOutUser(this)
            }
          })
          .catch((error) => {
            handleError(this, error, loader)
          })

    },
    deactivateAccount() {
      let loader = startLoader(this)

      axios.delete(user_resource, {
        headers:
            {
              Authorization: secureStoreGetAuthString(),
              deactivate: true
            }
      }).then((response) => {
        // redirect after successful signUp
        if (response.status === 200) {
          setTimeout(() => {
            secureStoreDeleteUserInfo()
            loader.hide()
            showFlashMessage(this, 'success', 'Account Deactivated', 'Your account has been successfully deactivated.' +
                '\nSorry to see you go.');
            +redirectAfterCountDown(this, '/home')
          }, 2500)
        }
      }).catch((error) => {
        handleError(this, error, loader)
      })
    },
  },
  components: {mdbCard, mdbCardHeader, mdbCardBody, mdbRow, mdbCol, mdbInput, TopNav},
  created() {
    this.onLoadPage();
  }
};
</script>
