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
                                        <h3 class="white-text mb-3 pt-3"><i class="fa fa-lock"></i> Log In:</h3>
                                    </mdb-row>
                                </div>

                                <mdb-card-body class="mx-4 mt-4">
                                    <form>
                                        <div class="grey-text">
                                            <mdb-input label="Your email" icon="envelope" type="email"/>
                                            <div class="md-form row">
                                                <mdb-input id="password-field" label="Your password"
                                                           icon="lock" class="form_input_margin"
                                                           type="password"/>
                                                <span id="view-pwd" class="fa fa-fw fa-eye" aria-hidden="true"
                                                      v-b-tooltip.hover :title="'see raw password'"
                                                      @click="viewPassword()"/>
                                            </div>
                                        </div>
                                    </form>

                                    <br>
                                    <p class="font-small grey-text d-flex justify-content-end">Forgot <a href="#"
                                                                                                         class="dark-grey-text ml-1 font-weight-bold">
                                        Password?</a></p>
                                    <mdb-row class="d-flex align-items-center mb-4 mt-5">
                                        <mdb-col md="5" class="d-flex align-items-start">
                                            <div class="text-center">
                                                <mdb-btn rounded type="button" class="z-depth-1a">Login</mdb-btn>
                                            </div>
                                        </mdb-col>
                                        <mdb-col md="7" class="d-flex justify-content-end">
                                            <p class="font-small grey-text mt-3">Don't have an account? <a
                                                    href="/register"
                                                    class="dark-grey-text ml-1 font-weight-bold">
                                                Sign up</a></p>
                                        </mdb-col>
                                    </mdb-row>
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
          form: {
              email: '',
              checked: []
          },
          show: true
      }
    },
    methods: {
        viewPassword() {
            let passwordInput = document.getElementById('password-field');
            let pwdEyeIcon = document.getElementById('view-pwd');

            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                pwdEyeIcon.className = 'fa fa-eye-slash';
            } else {
                passwordInput.type = 'password';
                pwdEyeIcon.className = 'fa fa-eye';
            }
        },
        onSubmit(evt) {
            evt.preventDefault();
            alert(JSON.stringify(this.form))
        },
        onReset(evt) {
            evt.preventDefault();
            // Reset our form values
            this.form.email = '';
            this.form.checked = [];
            // Trick to reset/clear native browser form validation state
        this.show = false;
        this.$nextTick(() => {
          this.show = true
        })
      }
    }
  }
</script>
