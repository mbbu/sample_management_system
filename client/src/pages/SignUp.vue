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
                                                        :v-model="$v.user.role"
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
    // import axios from 'axios';
    import {mdbBtn, mdbCard, mdbCardBody, mdbCol, mdbInput, mdbRow} from "mdbvue";
    import TopNav from "../components/TopNav";
    import {email, minLength, required, sameAs} from "vuelidate/lib/validators"
    import {role_resource} from "../utils/api_paths";
    import {extractApiData, getItemDataList} from "../utils/util_functions"

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
                }
            };
        },

        validations: {
            user: {
                firstName: {required, minLength: minLength(3)},
                lastName: {required, minLength: minLength(3)},
                role: {required},
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
            onSubmit() {
                this.$log.info("FORM SUBMIT METHOD CALLED!");
                // stop here if form is invalid
                this.$v.$touch();
                if (this.$v.$invalid) {
                    this.$log.info("FORM INVALID!");
                    return;
                }
                this.$log.info("FORM VALID!");
                alert("SUCCESS!! :-)\n\n" + JSON.stringify(this.user));
                // api call to create user.
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
                    this.$log.info("Returned Data: " + data);
                    let roleList = extractApiData(data);
                    this.$log.info("Extracted Data: " + roleList);
                    this.$log.info("Role list json: ", JSON.stringify(roleList));
                })

                // let roleList = getItemDataList(role_resource);
                // this.roleDataList = roleList['items'];
                // this.fields = roleList['fields'];


                // this.$log.info("Role list: ", roleList);
                // this.$log.info("Role list items: ", roleList.items);
                // this.$log.info("Role list items: ", roleList['items']);
                // this.$log.info("Role list fields: ", roleList['fields']);
                // this.$log.info("Role list fields text: " + roleList['fields'].text);
                // this.$log.info("Role list fields value: " + roleList['fields'].value);
                //
                //
                // for (let i=0; i < roleList.items.length; i ++){
                //     this.$log.info("FOR LOOP");
                //     this.$log.info(i)
                // }


                // this.$log.info("Role list: ", roleList.toString());
                // this.$log.info("Role list type: ", typeof(roleList));
                // this.$log.info("Role list json: ", JSON.stringify(roleList));
                // this.$log.info("Role Data List: " , this.roleDataList);
                // this.$log.info("Fields: " + this.fields);
                // return getItemDataList(role_resource, this.roleDataList, this.fields);
            }


            // getRoleDataList() {
            //     axios.get(role_resource)
            //         .then((res) => {
            //             this.$log.info("Response: " + res.status + " " + res.data['message']);
            //             for (var lab_item = 0; lab_item < res.data.message.length; lab_item++) {
            //                 this.roleDataList.push({
            //                     'Code': res.data.message[lab_item].code,
            //                     'Name': res.data.message[lab_item].name
            //                 });
            //                 this.fields = {text: 'Name', value: 'Code'};
            //             }
            //         })
            //         .catch((error) => {
            //             // eslint-disable-next-line
            //             this.$log.error(error);
            //         });
            // },
        },
        created() {
            this.onLoadPage();
        }

    }
</script>