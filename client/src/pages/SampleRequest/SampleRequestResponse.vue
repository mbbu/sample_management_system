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
                                        <!-- STATUS -->
                                        <b-form-group class="form_input_margin">
                                            <i class="fas fa-question"></i> Status: <br/>
                                            <ejs-dropdownlist
                                                    :dataSource='statusDataList'
                                                    :fields="fields"
                                                    :v-model="sampleResponse.status"
                                                    id='dropdownlist'
                                                    placeholder='Select a response'
                                            ></ejs-dropdownlist>
                                        </b-form-group>


                                        <!-- APPROVED AMOUNT -->
                                        <b-form-group>
                                            <mdb-input class="form_input_margin" icon="fas fa-balance-scale-right"
                                                       id="amount" label="Amount Approved"
                                                       min=0 type="number"
                                                       v-model.trim="$v.sampleResponse.amount.$model"/>

                                            <div v-if="$v.sampleResponse.amount.$dirty">
                                                <div class="error" v-if="!$v.sampleResponse.amount.required">Amount is
                                                    required
                                                </div>
                                            </div>
                                        </b-form-group>

                                        <!--Notes-->
                                        <div class="form-group">
                                            <label for="description">Notes: (Quick response to the requester)</label>
                                            <textarea class="form-control" id="description" name="description"
                                                      type="text"
                                                      v-model="sampleResponse.notes"/>
                                        </div>

                                        <mdb-row class="d-flex align-items-center mb-4 mt-5">
                                            <mdb-col class="d-flex align-items-start" md="12">
                                                <div class="text-center">
                                                    <mdb-btn class="z-depth-1a" rounded type="submit">Respond</mdb-btn>
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
    import axios from "axios";
    import TopNav from "../../components/TopNav";
    import {required} from "vuelidate/lib/validators"
    import {sample_response_resource} from "../../utils/api_paths";
    import {APPROVED_STATUS, DECLINED_STATUS} from "../../utils/constants";
    import {mdbBtn, mdbCard, mdbCardBody, mdbCol, mdbInput, mdbRow} from "mdbvue";
    import {
        countDownTimer,
        getSelectedItemCode,
        respondTo401,
        secureStoreGetString,
        showFlashMessage,
        startLoader
    } from "../../utils/util_functions";

    export default {
        name: "SampleRequestResponse",
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
                page_title: "Sample Request Response",
                statusDataList: [
                    {'Code': APPROVED_STATUS, 'Name': 'Approved'},
                    {'Code': DECLINED_STATUS, 'Name': 'Declined'},
                ],
                fields: {
                    text: 'Name',
                    value: 'Code'
                },
                sampleResponse: {
                    status: null,
                    amount: null,
                    notes: null
                }
            }
        },

        validations: {
            sampleResponse: {
                amount: {required}
            }
        },

        methods: {
            onSubmit() {
                this.$v.$touch();
                if (this.$v.$invalid) {
                    this.$log.info("FORM INVALID!");
                    return;
                }
                this.responsePath = sample_response_resource.concat(this.$router.currentRoute.params.pathMatch)
                this.makeResponse(this.responsePath)
            },

            makeResponse: function (path) {
                let self = this;
                let loader = startLoader(this)
                this.sampleResponse.status = getSelectedItemCode('dropdownlist', this.statusDataList);

                axios.put(path, {
                    status: this.sampleResponse.status,
                    approved_amount: this.sampleResponse.amount,
                    notes: this.sampleResponse.notes
                }, {
                    headers: {
                        Authorization: secureStoreGetString()
                    }
                })
                    .then((response) => {
                        setTimeout(() => {
                            loader.hide()
                            if (response.status === 200) {
                                showFlashMessage(self, 'success', response.data['message'], '')
                                countDownTimer(self, 5, '/user')
                            }
                        }, 1000)
                    })
                    .catch((error) => {
                        loader.hide()
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 409) {
                                showFlashMessage(self, 'error', 'Error', error.response.data['message'])
                            } else if (error.response.status === 401) {
                                respondTo401(self);
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', 'Error', error.response.data['message'])
                            }
                        }
                    })
            }
        },
        created() {
        }
    }
</script>
