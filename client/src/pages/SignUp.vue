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
                                    <form>
                                        <div class="grey-text">
                                            <mdb-input label="First name" icon="user" type="text"/>
                                            <mdb-input label="Last name" icon="user" type="text"/>
                                            <mdb-input label="Your email" icon="envelope" type="email"/>
                                            <mdb-input label="Your password" icon="lock" type="password"/>
                                            <mdb-input label="Confirm your password" icon="exclamation-triangle"
                                                       type="password"/>
                                        </div>
                                    </form>

                                    <mdb-row class="d-flex align-items-center mb-4 mt-5">
                                        <mdb-col md="5" class="d-flex align-items-start">
                                            <div class="text-center">
                                                <mdb-btn rounded type="button" class="z-depth-1a">Register</mdb-btn>
                                            </div>
                                        </mdb-col>
                                        <mdb-col md="7" class="d-flex justify-content-end">
                                            <p class="font-small grey-text mt-3">Have an account already? <a
                                                    href="/login"
                                                    class="dark-grey-text ml-1 font-weight-bold">
                                                Log In</a></p>
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
            }
        }

    }
</script>