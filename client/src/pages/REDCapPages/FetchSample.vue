<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title"></top-nav>

                <section class="form-gradient" style="margin-top: 2%">
                    <mdb-row>
                        <mdb-col md="12">
                            <mdb-card>
                                <FlashMessage :position="'center bottom'"></FlashMessage>
                                <div class="header pt-3 blue-gradient">
                                    <mdb-row class="d-flex justify-content-center">
                                        <h3 class="white-text mb-3 pt-3"><i class="fas fa-fill"></i> Fetch Samples:</h3>
                                    </mdb-row>
                                </div>

                                <errors-display :errors="errors"></errors-display>

                                <mdb-card-body class="mx-4 mt-4">
                                    <form @submit.prevent="onSubmit">
                                        <div class="black-text">

                                            <mdb-row>
                                                <mdb-col md="12">
                                                    <mdb-input icon="fas fa-project-diagram" id="project"
                                                               v-model="request.project"
                                                               label="Enter Project Id" type="text"/>
                                                </mdb-col>
                                            </mdb-row>

                                            <br>

                                            <mdb-row>
                                                <!-- DATE PICKER -->
                                                <mdb-col md="10">
                                                    <label title="Specify dates to download samples of">
                                                        Date Range (From-To):
                                                    </label>
                                                    <functional-calendar
                                                            :change-month-function='true' :change-year-function='true'
                                                            :is-dark="true" :is-date-picker='true'
                                                            :is-date-range='true' :is-layout-expandable="true"
                                                            :is-modal='true' :is-typeable="true"
                                                            v-model="request.date_range"
                                                    ></functional-calendar>
                                                </mdb-col>
                                            </mdb-row>
                                        </div>

                                        <br>
                                        <mdb-row class="d-flex align-items-center mb-4 mt-5">
                                            <mdb-col class="d-flex justify-content-end" md="12">
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
    import {mdbBtn, mdbCard, mdbCardBody, mdbCol, mdbInput, mdbRow} from "mdbvue";
    import TopNav from "../../components/TopNav";
    import {
        countDownTimer,
        respondTo401,
        secureStoreGetString,
        showFlashMessage, startLoader
    } from "../../utils/util_functions";
    import {redcap_sample_resource} from "../../utils/api_paths";
    import {FunctionalCalendar} from 'vue-functional-calendar';
    import ErrorsDisplay from "../../components/ErrorsDisplay";
    import axios from "axios";

    export default {
        name: "FetchSample",

        components: {
            mdbBtn,
            mdbCard,
            mdbCol,
            mdbRow,
            mdbInput,
            TopNav,
            mdbCardBody,
            ErrorsDisplay,
            FunctionalCalendar
        },

        data() {
            return {
                page_title: "REDCap Sample",
                showModal: false,
                request: {
                    project: null,
                    date_range: null,
                    to: null,
                    from: null,
                },
                errors: [],
            }
        },

        methods: {
            clearForm() {
                this.request.project = null;
                this.request.date_range = null;
            },

            onSubmit() {
                this.errors = []
                // ensure fields are not empty
                if (!this.request.project) {
                    this.errors.push("Project is required!")
                } else if (!this.request.date_range) {
                    this.errors.push(" Enter date range is required")
                } else {
                    // determine date range
                    this.dateSetter()
                    this.fetchSamples()
                }
            },

            dateSetter() {
                if (this.request.date_range) {
                    this.request.from = this.request.date_range.dateRange.start.date;
                    this.request.to = this.request.date_range.dateRange.end.date;
                } else if (!this.request.date_range) {
                    this.request.from = null;
                    this.request.to = null;
                }
            },

            fetchSamples() {
                let self = this;
                let loader = startLoader(this);

                axios.post(redcap_sample_resource, {
                    project: this.request.project,
                    from: this.request.from,
                    to: this.request.to
                }, {
                    headers:
                        {
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        setTimeout(() => {
                            loader.hide()
                            showFlashMessage(self, 'success', response.data['message'], '');
                            // todo: redirect to sample view page
                            countDownTimer(self, 2, '/sample')
                        }, 4000)
                    })
                    .catch((error) => {
                        loader.hide()
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 400) {
                                showFlashMessage(self, 'error', 'Kindly refill the form', error.response.data['message']);
                            } else if (error.response.status === 401) {
                                respondTo401(self);
                            } else if (error.response.status === 404) {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });

            }
        },
    }
</script>

<style scoped>

</style>