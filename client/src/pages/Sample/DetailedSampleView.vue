<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title"></top-nav>

                <FlashMessage :position="'center bottom'"></FlashMessage>
                <br> <br>
                <em>About Sample</em>
                <br> <br>
                <table class="table table-hover">
                    <thead class="blue-gradient white-text">
                    <tr>
                        <th scope="col"><em><b>THEME</b></em></th>
                        <th scope="col"><em><b>PROJECT</b></em></th>
                        <th scope="col"><em><b>PROJECT HEAD</b></em></th>
                        <th scope="col"><em><b>SAMPLE HANDLER</b></em></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td v-if="sample.theme"> {{ sample.theme}}</td>
                        <td v-else-if="!sample.theme">N/A</td>
                        <td v-if="sample.project"> {{ sample.project}}</td>
                        <td v-else-if="!sample.project">N/A</td>
                        <td v-if="sample.projectOwner"> {{ sample.projectOwner}}</td>
                        <td v-else-if="!sample.projectOwner">N/A</td>
                        <td v-if="sample.user"> {{ sample.user}} &nbsp; <i :title="sample.userEmail"
                                                                           class="far fa-envelope fa-lg"></i></td>
                        <td v-else-if="!sample.user">N/A</td>

                    </tr>
                    </tbody>
                </table>

                <hr>
                <hr>
                <em>Sample Details</em>
                <br> <br>
                <table class="table table-hover">
                    <thead class="blue-gradient white-text">
                    <tr>
                        <th id="blank">&nbsp;</th>
                        <th headers="blank" id="co1" scope="col"><em><b>SAMPLE TYPE</b></em></th>
                        <th headers="blank" id="co3" scope="col"><em><b>SPECIES</b></em></th>
                        <th headers="blank" id="co4" scope="col"><em><b>LOCATION COLLECTED</b></em></th>
                        <th headers="blank" id="co5" scope="col"><em><b>ANALYSIS</b></em></th>
                    </tr>
                    </thead>
                    <tr>
                        <th headers="blank" id="c1"></th>
                        <td headers="co1 c1" v-if="sample.sampleType">{{ sample.sampleType}}</td>
                        <td v-else-if="!sample.sampleType">N/A</td>
                        <td headers="co3 c1" v-if="sample.species">{{ sample.species}}</td>
                        <td v-else-if="!sample.species">N/A</td>
                        <td headers="co4 c1" v-if="sample.locationCollected">{{ sample.locationCollected}}</td>
                        <td v-else-if="!sample.locationCollected">N/A</td>
                        <td headers="co5 c1" v-if="sample.analysis">{{ sample.analysis}}</td>
                        <td v-else-if="!sample.analysis">N/A</td>
                    </tr>
                    <thead class="blue-gradient white-text">
                    <tr>
                        <th>&nbsp;</th>
                        <th headers="blank" id="co6" scope="col"><em><b>PUBLICATIONS</b></em></th>
                        <th headers="blank" id="co7" scope="col"><em><b>SURVEYS</b></em></th>
                        <th headers="blank" id="co8" scope="col"><em><b>DESCRIPTION</b></em></th>
                        <th headers="blank" id="co8." scope="col"><em><b></b></em></th>
                    </tr>
                    </thead>
                    <tr>
                        <th headers="blank" id="c2"></th>
                        <td headers="co6 c2" v-if="sample.publication">{{ sample.publication}}</td>
                        <td v-else-if="!sample.publication">N/A</td>
                        <td headers="co7 c2" v-if="sample.survey">{{ sample.survey}}</td>
                        <td v-else-if="!sample.survey">N/A</td>
                        <td headers="co8 c2" v-if="sample.description">{{ sample.description}}</td>
                        <td v-else-if="!sample.description">N/A</td>
                        <td headers="co8. c2"></td>
                    </tr>
                </table>

                <hr>
                <hr>
                <em>Sample Location at I.C.I.P.E</em>
                <br> <br>
                <table class="table table-hover">
                    <thead class="blue-gradient white-text">
                    <tr>
                        <th id="loc_blank">&nbsp;</th>
                        <th headers="loc_blank" id="loc_co1" scope="col"><em><b>LAB NAME</b></em></th>
                        <th headers="loc_blank" id="loc_co2" scope="col"><em><b>ROOM NUM</b></em></th>
                        <th headers="loc_blank" id="loc_co3" scope="col"><em><b>FREEZER NUM</b></em></th>
                        <th headers="loc_blank" id="loc_co4" scope="col"><em><b>CHAMBER TYPE</b></em></th>
                    </tr>
                    </thead>
                    <tr>
                        <th headers="loc_blank" id="loc_c1"></th>
                        <td headers="loc_co1 loc_c1" v-if="sample.lab">{{ sample.lab }}</td>
                        <td v-else-if="!sample.lab">N/A</td>
                        <td headers="loc_co2 loc_c1" v-if="sample.room">{{ sample.room }}</td>
                        <td v-else-if="!sample.room">N/A</td>
                        <td headers="loc_co3 loc_c1" v-if="sample.freezer">{{ sample.freezer }}</td>
                        <td v-else-if="!sample.freezer">N/A</td>
                        <td headers="loc_co4 loc_c1" v-if="sample.chamber">{{ sample.chamber }}</td>
                        <td v-else-if="!sample.chamber">N/A</td>
                    </tr>
                    <thead class="blue-gradient white-text">
                    <tr>
                        <th>&nbsp;</th>
                        <th headers="loc_blank" id="loc_co5" scope="col"><em><b>RACK NUM</b></em></th>
                        <th headers="loc_blank" id="loc_co6" scope="col"><em><b>TRAY NUM</b></em></th>
                        <th headers="loc_blank" id="loc_co7" scope="col"><em><b>BOX LABEL</b></em></th>
                        <th headers="loc_blank" id="loc_co8" scope="col"><em><b>RETENTION PERIOD (Sample will be stored
                            until)</b></em></th>
                    </tr>
                    </thead>
                    <tr>
                        <th headers="loc_blank" id="loc_c2"></th>
                        <td headers="loc_co5 loc_c2" v-if="sample.rack">{{ sample.rack }}</td>
                        <td v-else-if="!sample.rack">N/A</td>
                        <td headers="loc_co6 loc_c2" v-if="sample.tray">{{ sample.tray }}</td>
                        <td v-else-if="!sample.tray">N/A</td>
                        <td headers="loc_co7 loc_c2" v-if="sample.box">{{ sample.box }}</td>
                        <td v-else-if="!sample.box">N/A</td>
                        <td headers="loc_co8 loc_c2" v-if="sample.retention">
                            {{sample.retention }}
                        </td>
                        <td v-else-if="!sample.retention">N/A</td>
                    </tr>
                </table>

                <em>Other Important Details</em>
                <br> <br>
                <table class="table table-hover">
                    <thead class="blue-gradient white-text">
                    <tr>
                        <th scope="col"><em><b>AMOUNT</b></em></th>
                        <th scope="col"><em><b>STORAGE TEMP (Degree Celsius)</b></em><i
                                class="fas fa-temperature-low"></i></th>
                        <th scope="col"><em><b>SECURITY LEVEL</b></em></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td v-if="sample.amount">{{ sample.amount }} {{ sample.quantity_type }} available on
                            {{ sample.date }}
                        </td>
                        <td v-else-if="!sample.amount">N/A</td>
                        <td v-if="sample.temperature">{{ sample.temperature}}</td>
                        <td v-else-if="!sample.temperature">N/A</td>
                        <td v-if="sample.securityLevel">{{ sample.securityLevel}}</td>
                        <td v-else-if="!sample.securityLevel">N/A</td>
                    </tr>
                    </tbody>
                </table>
                <mdb-row class="d-flex align-items-center mb-4 mt-5">
                    <mdb-col class="d-flex align-items-start" md="5">
                        <a href="/sample">
                            <button class="btn btn-outline-info btn-rounded" type="button">
                                <i class="fas fa-arrow-left"></i>
                                Back
                            </button>
                        </a>
                    </mdb-col>
                    <mdb-col class="d-flex justify-content-end" md="7">
                        <div class="text-center">
                            <a href="https://redcap.icipe.org/surveys/?s=W7A7TFJ89J">
                                <button class="btn btn-outline-info btn-rounded" type="button"> Request Sample
                                    <i aria-hidden="true" class="fa fa-inbox menu_icon"> </i>
                                </button>
                            </a>
                        </div>
                        <div class="text-center">
                            <button @click="requestUpdateSample" class="btn btn-outline-info btn-rounded"
                                    type="button"> Update Sample
                                <i class="fas fa-pencil-alt"></i></button>
                        </div>
                        <div class="text-center">
                            <button @click="deleteSample(sample.code)" class="btn btn-outline-danger btn-rounded"
                                    type="button"> Delete Sample
                                <i class="far fa-trash-alt"></i></button>
                        </div>
                    </mdb-col>
                </mdb-row>
            </div>
        </div>
    </div>
</template>

<script>
    import TopNav from "../../components/TopNav";
    import {mdbCol, mdbRow} from "mdbvue";
    import {sample_resource} from "../../utils/api_paths";
    import axios from 'axios';
    import {
        countDownTimer,
        getSampleCode,
        secureStoreGetString,
        setSampleDetailsForEditing,
        setUpdateSample,
        showFlashMessage
    } from "../../utils/util_functions";

    export default {
        name: "DetailedSampleView",
        data() {
            return {
                page_title: "Sample MetaData",
                response: [],
                sample: {
                    theme: "",
                    user: "",
                    userEmail: "",
                    project: "",
                    projectOwner: "",
                    sampleType: "",
                    species: "",
                    description: "",
                    box: "",
                    locationCollected: "",
                    retention: "",
                    barcode: "",
                    analysis: "",
                    temperature: "",
                    amount: "",
                    quantity_type: "",
                    securityLevel: "",
                    code: "",

                    // extra fields
                    publication: "",
                    survey: "",
                    lab: "",
                    room: "",
                    freezer: "",
                    chamber: "",
                    rack: "",
                    tray: "",
                    date: "",
                },
            }
        },
        methods: {
            setSampleData(res) {
                this.sample.theme = res['theme.name'];
                this.sample.user = res['user.first_name'] + " " + res['user.last_name'];
                this.sample.userEmail = res['user.email'];
                this.sample.project = res['project'];
                this.sample.projectOwner = res['project_owner'];
                this.sample.sampleType = res['sample_type'];
                this.sample.species = res['animal_species'];
                this.sample.description = res['sample_description'];
                this.sample.box = res['box.label'];
                this.sample.locationCollected = res['location_collected'];
                this.sample.retention = res['retention_date'];
                this.sample.barcode = res['barcode'];
                this.sample.analysis = res['analysis'];
                this.sample.temperature = res['temperature'];
                this.sample.amount = res['amount'];
                this.sample.quantity_type = res['quantity.id'];
                this.sample.securityLevel = res['secLevel.name'];
                this.sample.code = res['code'];
                this.sample.date = this.dateNow();
                this.sample.lab = res['box.tray.rack.chamber.freezer.lab.name']
                this.sample.room = res['box.tray.rack.chamber.freezer.lab.room']
                this.sample.freezer = res['box.tray.rack.chamber.freezer.number']
                this.sample.chamber = res['box.tray.rack.chamber.type']
                this.sample.rack = res['box.tray.rack.number']
                this.sample.tray = res['box.tray.number']
            },

            dateNow() {
                let now = Date();

                // Converting the number of millisecond in date string
                return now.toString();
            },

            showLoader() {
                return this.$loading.show({
                    isFullPage: true,
                    canCancel: false,
                    color: '#074880',
                    loader: 'bars',
                    width: 255,
                    height: 255,
                    backgroundColor: '#FAAB2C',
                    opacity: 0.7,
                    zIndex: 999,
                });
            },

            getSampleByCode(code) {
                let self = this;

                // show loader while request is being made
                let loader = this.showLoader()

                axios.get(sample_resource, {
                    headers:
                        {
                            code: code,
                        }
                })
                    .then((res) => {
                        setTimeout(() => {
                            loader.hide()
                            this.response = res.data.message;
                            this.setSampleData(this.response)
                            this.$log.info("Response: " + res.status + " " + res.data +
                                " this.response has", this.response);
                        }, 2500)
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        loader.hide()
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 401) {
                                showFlashMessage(self, 'error', "Session Expired", 'You need to log in to perform this operation');
                            } else if (error.response.status === 404) {
                                showFlashMessage(self, 'error', 'Connection Error', 'Request was timed out');
                                countDownTimer(self, 3, '/sample')
                            }
                        }
                    });
            },

            requestUpdateSample() {
                let self = this;
                let loader = this.showLoader()

                setTimeout(() => {
                    loader.hide()
                    setSampleDetailsForEditing(this.response)
                    setUpdateSample(true)
                    countDownTimer(self, 1, '/addsample')
                }, 1000)
            },

            deleteSample: function (code) {
                let self = this;

                let loader = this.showLoader()
                axios.delete(sample_resource, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        setTimeout(() => {
                            loader.hide()
                            showFlashMessage(self, 'success', response.data['message'], '');
                            countDownTimer(self, 1, '/sample')
                        }, 1500)
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 401) {
                                showFlashMessage(self, 'error', "Session Expired", 'You need to log in to perform this operation');
                                countDownTimer(self, 3, '/login')
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });
            },
        },
        components: {TopNav, mdbCol, mdbRow},
        created() {
            let code = getSampleCode()
            this.getSampleByCode(code)
        }
    }
</script>

<style scoped>

</style>