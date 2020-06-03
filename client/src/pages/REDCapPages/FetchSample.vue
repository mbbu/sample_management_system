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
                                                    <!-- LIST POPULATED FROM PROJECT RESOURCE -->
                                                    <b-form-group class="form_input_margin">
                                                        <i class="fas fa-project-diagram"></i> Project: <br/>
                                                        <ejs-dropdownlist
                                                                :dataSource='projectDataList'
                                                                :fields="fields"
                                                                :v-model="request.project"
                                                                id='dropdownlist'
                                                                placeholder='Select a project'
                                                        ></ejs-dropdownlist>
                                                    </b-form-group>
                                                </mdb-col>
                                            </mdb-row>

                                            <br>

                                            <h4><label>Download Mode</label></h4>
                                            <mdb-row>
                                                <!-- DATE PICKER -->
                                                <mdb-col md="5">
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

                                                <mdb-col md="5" style="border-left: 5px solid grey; height: auto">
                                                    <label title="Download all samples for this project">
                                                        Download all samples:
                                                    </label>
                                                    <!-- ALL -->
                                                    <Checkbox :size="32" id="downloadCheck" v-model="request.all">
                                                        Download all?
                                                    </Checkbox>
                                                </mdb-col>
                                            </mdb-row>
                                        </div>

                                        <br>
                                        <mdb-row class="d-flex align-items-center mb-4 mt-5">
                                            <mdb-col class="d-flex align-items-start grey-text" md="5">
                                                <p v-b-modal.modal-ask-project>
                                                    <i class="fas fa-sad-cry"></i> Can't see project? <em>Ask
                                                    here</em>
                                                </p>
                                            </mdb-col>
                                            <mdb-col class="d-flex justify-content-end" md="7">
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

                <div>
                    <b-modal
                            @hidden="clearForm"
                            @ok="askProject"
                            @submit="showModal = false"
                            cancel-variant="danger"
                            id="modal-ask-project"
                            ok-title="Request"
                            title="Ask about project"
                    >
                        <form @submit.prevent="askProject">

                            <b-form-group id="form-title-group" label="Title:" label-for="form-title-input">
                                <b-form-input
                                        id="form-title-input"
                                        placeholder="Enter Title"
                                        required="true"
                                        type="text"
                                        v-model="projectRequest.title"
                                ></b-form-input>
                            </b-form-group>

                            <b-form-group id="form-head-group" label="Head(PI):" label-for="form-head-input">
                                <b-form-input
                                        id="form-head-input"
                                        placeholder="Enter Head"
                                        required="true"
                                        type="text"
                                        v-model="projectRequest.head"></b-form-input>
                            </b-form-group>
                        </form>
                    </b-modal>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
    import {mdbBtn, mdbCard, mdbCardBody, mdbCol, mdbRow} from "mdbvue";
    import TopNav from "../../components/TopNav";
    import {
        countDownTimer,
        extractProjectData,
        getItemDataList,
        getSelectedItemCode,
        respondTo401,
        secureStoreGetString,
        showFlashMessage
    } from "../../utils/util_functions";
    import {project_resource, redcap_sample_resource} from "../../utils/api_paths";
    import {FunctionalCalendar} from 'vue-functional-calendar';
    import ErrorsDisplay from "../../components/ErrorsDisplay";
    import axios from "axios";
    import Checkbox from 'vue-material-checkbox'

    export default {
        name: "FetchSample",

        components: {
            mdbBtn,
            mdbCard,
            mdbCol,
            mdbRow,
            TopNav,
            Checkbox,
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
                    all: false
                },
                projectDataList: [],
                fields: {text: '', value: ''},
                projectRequest: {
                    title: null,
                    head: null
                },
                errors: [],
            }
        },

        methods: {
            clearForm() {
                this.request.project = null;
                this.request.date_range = null;
                this.projectRequest.head = null;
                this.projectRequest.title = null;
            },

            onLoadPage() {
                getItemDataList(project_resource).then(data => {
                    let projectList = extractProjectData(data);
                    this.fields = projectList['fields'];
                    for (let i = 0; i < projectList.items.length; i++) {
                        this.projectDataList.push({
                            'Code': projectList.items[i].Code,
                            'Name': projectList.items[i].Name,
                        });
                    }
                })
            },

            onSubmit() {
                this.errors = []
                this.request.project = getSelectedItemCode('dropdownlist', this.projectDataList)
                // ensure fields are not empty
                if (!this.request.project) {
                    this.errors.push("Project is required!")
                } else if (!this.request.date_range && this.request.all === false) {
                    this.errors.push(" Enter dates or check the check box!")
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

            askProject() {

            },


            fetchSamples() {
                let self = this;
                let loader = this.$loading.show({
                    isFullPage: true,
                    canCancel: false,
                    color: '#074880',
                    loader: 'dots',
                    width: 255,
                    height: 255,
                    backgroundColor: '#FAAB2C',
                    opacity: 0.7,
                    zIndex: 999,
                });

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
                            } else if (error.response.status === 401 || error.response.status === 422) {
                                respondTo401(self);
                            } else if (error.response.status === 404) {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });

            }
        },

        created() {
            this.onLoadPage()
        }
    }
</script>

<style scoped>

</style>