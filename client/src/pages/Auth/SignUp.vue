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
                                   icon="user" label="First name"
                                   type="text"/>
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
                                   icon="user" label="Last name"
                                   type="text"/>
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
                            placeholder='Select a role'
                        ></ejs-dropdownlist>
                      </b-form-group>

                      <!--EMAIL-->
                      <b-form-group :class="{ 'form-group--error': $v.user.email.$error }">
                        <mdb-input id="email" v-model.trim="$v.user.email.$model"
                                   icon="envelope" label="Your email"
                                   type="email"/>
                        <div v-if="$v.user.email.$dirty">
                          <div v-if="!$v.user.email.required" class="error">Field is
                            required
                          </div>
                          <div v-if="!$v.user.email.email" class="error">Email mismatch.
                            Example johndoe123@icipe.org
                          </div>
                        </div>
                      </b-form-group>

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
                            Passwords must be
                            identical!
                          </div>
                        </div>
                      </b-form-group>
                    </div>

                    <mdb-row class="d-flex align-items-center mb-4 mt-5">
                      <mdb-col class="d-flex align-items-start" md="5">
                        <div class="text-center">
                          <mdb-btn class="z-depth-1a" rounded type="submit">Register</mdb-btn>
                        </div>
                      </mdb-col>
                      <mdb-col class="d-flex justify-content-end" md="7">
                        <p class="font-small grey-text mt-3">Have an account already? <a
                            class="dark-grey-text ml-1 font-weight-bold"
                            href="/login">
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
import TopNav from "../../components/TopNav";
import {email, minLength, required, sameAs} from "vuelidate/lib/validators"
import {role_resource, user_resource} from "@/utils/api_paths";
import {
  extractApiData,
  getItemDataList,
  getSelectedItem,
  handleError,
  isUserLoggedIn,
  redirectAfterCountDown,
  showFlashMessage,
  startLoader,
  viewPassword
} from "@/utils/util_functions"

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
    viewPassword,
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
      // stop here if form is invalid
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      this.createUser(this.user);
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
    },


    createUser: function (user) {
      let loader = startLoader(this)

      this.user.role = getSelectedItem(this.roleDataList, this.user.role);
      axios.post(user_resource, {
        first_name: user.firstName,
        last_name: user.lastName,
        email: user.email,
        role: user.role,
        password: user.password
      })
          .then((response) => {
            setTimeout(() => {
              loader.hide()
              // redirect after successful signUp
              if (response.status === 201) {
                showFlashMessage(this, 'success', response.data.message, '');
                redirectAfterCountDown(this, '/home')
              }
            }, 3500)
          })
          .catch((error) => {
            handleError(this, error, loader)
          })

    },
  },
  created() {
    if (isUserLoggedIn()) redirectAfterCountDown(this, '/user');
    else this.onLoadPage();
  }

}
</script>