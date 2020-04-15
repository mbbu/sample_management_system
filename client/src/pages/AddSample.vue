<template>
    <div id="jumbotron">
        <div class="container">
            <form-wizard @submit.prevent="handleSubmit" subtitle="Kindly input the correct information"
                         title="Sample Data Form">
                <tab-content @click.native="handleSubmit" title="Sample Details">

                    <div class="form-group">
                        <b-form-group id="form-theme" label="Select a Theme:" label-for="form-theme-input">
                            <ejs-dropdownlist
                                    :dataSource='themeDataList'
                                    :fields="fields"
                                    :v-model="sample.theme"
                                    id="theme-dropdownlist"
                                    placeholder='Select a theme'
                            ></ejs-dropdownlist>
                        </b-form-group>
                        <div class="invaid-feedback" v-if="submitted && $v.sample.theme.$error">
                            <span v-if="!$v.sample.theme.required"> Theme is required </span>
                            <span v-if="!$v.sample.theme.theme"> Select one </span>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="project"> Project</label>
                        <input :class="{ 'is-invalid': submitted && $sample.project.$error}" class="form-control"
                               id="project" type="text"
                               v-model="sample.project"/>
                    </div>

                    <div class="form-group">
                        <label for="projectOwner"> Project Owner</label>
                        <input :class="{ 'is-invalid': submitted && $sample.projectOwner.$error}" class="form-control"
                               id="projectOwner" type="text"
                               v-model="sample.projectOwner"/>
                        <div class="invalid-feedback" v-if="submitted && !$v.sample.projectOwner.required"> Project
                            owner is required
                        </div>
                    </div>

                    <div class="form-group">
                        <b-form-group id="form-user" label="Select the Sample Owner:" label-for="form-user-input">
                            <ejs-dropdownlist
                                    :dataSource='userDataList'
                                    :fields="fields"
                                    :v-model="sample.user"
                                    id="user-dropdownlist"
                                    placeholder='Select the sample owner(i.e. One in-charge of handling the sample)'
                            ></ejs-dropdownlist>
                        </b-form-group>
                        <div class="invaid-feedback" v-if="submitted && $v.sample.user.$error">
                            <span v-if="!$v.sample.user.required"> Sample owner is required </span>
                            <span v-if="!$v.sample.user.user"> Select one </span>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="sampleType"> Sample Type</label>
                        <input :class="{ 'is-invalid': submitted && $sample.sampleType.$error}" class="form-control"
                               id="sampleType" type="text"
                               v-model="sample.sampleType"/>
                        <div class="invalid-feedback" v-if="submitted && !$v.sample.sampleType.required"> Sample Type is
                            required
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="species"> Species</label>
                        <input :class="{ 'is-invalid': submitted && $sample.species.$error}" class="form-control"
                               id="species" type="text"
                               v-model="sample.species"/>
                        <div class="invalid-feedback" v-if="submitted && !$v.sample.species.required"> Species is
                            required
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="description"> Description</label>
                        <textarea :class="{ 'is-invalid': submitted && $sample.description.$error}" class="form-control"
                                  id="description" name="description"
                                  type="text" v-model="sample.description"/>
                        <div class="invalid-feedback" v-if="submitted && $v.sample.description.$error">
                            <span v-if="!$v.sample.description.required"> Description is required </span>
                            <span v-if="!$v.sample.description.minLength"> Description must be at least 25 words </span>
                        </div>
                    </div>

                </tab-content>

                <tab-content @click.native="handleSubmit" title="Sample Location in Institution">

                    <div class="form-group">
                        <label for="locationCollected">Location Collected</label>
                        <input :class="{ 'is-invalid': submitted && $sample.locationCollected.$error}"
                               class="form-control" id="locationCollected"
                               type="text"
                               v-model="sample.locationCollected"/>
                        <div class="invalid-feedback" v-if="submitted && !$v.sample.locationCollected">
                            <span v-if="!$v.sample.locationCollected.required"> Location Collected is required </span>
                            <span v-if="!$v.sample.locationCollected.minLength"> Location Collected must be at least 25 words </span>
                        </div>
                    </div>

                    <div class="form-group">
                        <b-form-group ::class="{ 'is-invalid': submitted && $sample.box.$error}"
                                      id="box" label="Select a Box for the sample:"
                                      label-for="form-box-input">
                            <ejs-dropdownlist
                                    :dataSource='boxDataList'
                                    :fields="fields"
                                    :v-model="sample.box"
                                    @change="fillFormFieldsDependentOnBox"
                                    id="box-dropdownlist"
                                    placeholder='Select a box and its location will be shown'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <div class="invalid-feedback" v-if="submitted && !$v.sample.box">
                            <span v-if="!$v.sample.box.required"> Box Collected is required </span>
                            <span v-if="!$v.sample.box.minValue"> Box Should be more than zero </span>
                        </div>
                    </div>


                    <!-- Start row -->
                    <div class="row">

                        <div class="col">
                            <div class="form-group">
                                <label for="tray">Tray Number</label>
                                <input class="form-control" disabled="disabled" id="tray" placeholder="Tray having box"
                                       type="text"/>
                            </div>
                        </div>

                        <div class="col">
                            <div class="form-group">
                                <label for="rack">Rack Number</label>
                                <input class="form-control" disabled="disabled" id="rack"
                                       placeholder="Rack holding tray"
                                       type="text"/>
                            </div>
                        </div>

                        <div class="col">
                            <div class="form-group">
                                <label for="chamber"> Chamber Type </label>
                                <input class="form-control" disabled="disabled" id="chamber"
                                       placeholder="Chamber where rack is" type="text"/>
                            </div>

                        </div>
                    </div>
                    <!-- End row -->


                    <!-- Start Row -->
                    <div class="row">
                        <div class="col">
                            <div class="form-group">
                                <label for="freezer">Freezer Number</label>
                                <input class="form-control" disabled="disabled" id="freezer"
                                       placeholder="Freezer where box is stored" type="text"/>
                            </div>
                        </div>

                        <div class="col">
                            <div class="form-group">
                                <label for="lab">Lab</label>
                                <input class="form-control" disabled="disabled" id="lab"
                                       placeholder="Lab where freezer is"
                                       type="text"/>
                            </div>
                        </div>
                    </div>

                    <!-- Start Row -->


                    <!-- Start row -->
                    <div class="row">
                        <div class="col">
                            <div class="form-group">
                                <label for="temperature">Temperature (Default in Celsius)</label>
                                <input :class="{ 'is-invalid': submitted && $sample.temperature.$error}"
                                       class="form-control" id="temperature" type="number"
                                       v-model="sample.temperature"/>
                                <div class="invalid-feedback" v-if="submitted && !$v.sample.temperature"> Temperature
                                    Collected is required
                                </div>
                            </div>

                        </div>

                        <div class="col">
                            <div class="form-group">
                                <label for="amount">Amount</label>
                                <input :class="{ 'is-invalid': submitted && $sample.amount.$error}" class="form-control"
                                       id="amount" type="number"
                                       v-model="sample.amount"/>
                                <div class="invalid-feedback" v-if="submitted && !$v.sample.amount">
                                    <span v-if="!$v.sample.amount.required"> Amount is required </span>
                                    <span v-if="!$v.sample.amount.minValue"> Amount Should be more than zero </span>
                                </div>
                            </div>

                        </div>
                        <div class="col">
                            <div class="form-group">
                                <b-form-group :class="{ 'is-invalid' : submitted && $v.sample.quantity_type.$error }"
                                              id="form-QT"
                                              label="Select a Quantity Type:"
                                              label-for="form-user-input">
                                    <ejs-dropdownlist
                                            :dataSource='QTDataList'
                                            :fields="fields"
                                            :v-model="sample.quantity_type"
                                            id="QT-dropdownlist"
                                            placeholder='Select a quantity type(e.g. ML, L, G ...)'
                                    ></ejs-dropdownlist>
                                </b-form-group>
                                <div class="invalid-feedback" v-if="submitted && $v.sample.quantity_type.$error">
                                    <span v-if="!$v.sample.quantity_type.required"> Quantity Type is required </span>
                                    <span v-if="!$v.sample.quantity_type.quantity_type"> Select one </span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- End Row -->

                </tab-content>


                <tab-content @click.native="handleSubmit" title="Finishing Up">

                    <div class="form-group">
                        <b-form-group id="form-securityLevel" label="Security Level Needed:"
                                      label-for="form-securityLevel-input">
                            <ejs-dropdownlist
                                    :dataSource='secLevelDataList'
                                    :fields="fields"
                                    :v-model="sample.securityLevel"
                                    id="securityLevel-dropdownlist"
                                    placeholder='Select Security Level Needed'
                            ></ejs-dropdownlist>
                        </b-form-group>
                        <div class="invaid-feedback" v-if="submitted && $v.sample.securityLevel.$error">
                            <span v-if="!$v.sample.securityLevel.required"> Security Level is required </span>
                            <span v-if="!$v.sample.securityLevel.securityLevel"> Select one </span>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="code"> Code</label>
                        <input :class="{ 'is-invalid': submitted && $sample.code.$error}" class="form-control" id="code"
                               type="text"
                               v-model="sample.code"/>
                        <div class="invalid-feedback" v-if="submitted && !$v.sample.code"> Code is required</div>
                    </div>

                    <div class="form-group">
                        <label for="barcode"> Barcode</label>
                        <input :class="{ 'is-invalid': submitted && $sample.barcode.$error}" class="form-control"
                               id="barcode" type="text"
                               v-model="sample.barcode"/>
                        <div class="invalid-feedback" v-if="submitted && !$v.sample.barcode"> Barcode is required</div>
                    </div>

                    <div class="form-group">
                        <label for="analysis"> Analysis</label>
                        <input :class="{ 'is-invalid': submitted && $sample.analysis.$error}" class="form-control"
                               id="analysis" type="text"
                               v-model="sample.analysis"/>
                        <div class="invalid-feedback" v-if="submitted && !v.sample.analysis"> Analysis is required</div>
                    </div>

                    <div class="form-group">
                        <label for="retention"> Retention</label>
                        <input :class="{ 'is-invalid': submitted && $sample.retention.$error}" class="form-control"
                               id="retention" type="number"
                               v-model="sample.retention"/>
                        <div class="invalid-feedback" v-if="submitted && !$v.sample.retention">
                            <span v-if="!$v.sample.retention.required"> Retention is required </span>
                            <span v-if="!$v.sample.retention.minValue"> Retention Should be more than zero </span>
                        </div>
                    </div>

                </tab-content>

                <template scope="props" slot="footer">
                    <div class=wizard-footer-left>
                        <wizard-button :style="props.fillButtonStyle"
                                       v-if="props.activeTabIndex > 0 && !props.isLastStep">Previous
                        </wizard-button>
                    </div>

                    <div class="wizard-footer-right">
                        <wizard-button :style="props.fillButtonStyle" @click.native="props.nextTab()"
                                       class="wizard-footer-right" v-if="!props.isLastStep">Next
                        </wizard-button>

                        <wizard-button :style="props.fillButtonStyle" @click.native="formSubmit"
                                       class="wizard-footer-right finish-button"
                                       v-else>{{props.isLastStep ? 'Done' : 'Next'}}
                        </wizard-button>
                    </div>
                </template>
            </form-wizard>
        </div>
    </div>
</template>

<script>
    import Vue from 'vue';
    import VueFormWizard, {TabContent} from 'vue-form-wizard';
    import 'vue-form-wizard/dist/vue-form-wizard.min.css';
    import {minLength, minValue, required} from "vuelidate/lib/validators";
    import axios from 'axios';
    import {
        extractApiData,
        extractBoxData,
        extractQTData,
        extractUserData,
        getItemDataList,
        getSelectedBoxSetTextFieldValue,
        getSelectedItemCode,
        secureStoreGetString
    } from "../utils/util_functions";
    import {
        box_resource,
        quantity_type_resource,
        sample_resource,
        security_level_resource,
        theme_resource,
        user_resource
    } from "../utils/api_paths";

    Vue.use(VueFormWizard)
    Vue.use(TabContent)

    export default {
        name: "jumbotron",

        data() {
            return {
                response: [],
                sample: {
                    theme: "",
                    user: "",
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

                },
                submitted: false,

                QTDataList: [],
                boxDataList: [],
                userDataList: [],
                themeDataList: [],
                secLevelDataList: [],
                fields: {text: '', value: ''},
            };
        },

        validations: {
            sample: {
                theme: {required},
                projectOwner: {required},
                user: {required},
                project: {required},
                sampleType: {required},
                species: {required},
                description: {required, minLength: minLength(25)},
                box: {required, minValue: minValue(0)},
                locationCollected: {required},
                retention: {required},
                barcode: {required},
                analysis: {required},
                temperature: {required},
                amount: {required, minValue: minValue(0)},
                quantity_type: {required},
                securityLevel: {required},
                code: {required},
            },
        },

        methods: {
            onLoadPage() {

                // GET THEME LIST
                getItemDataList(theme_resource).then(data => {
                    let themeList = extractApiData(data);

                    // update local variables with data from API
                    this.fields = themeList['fields'];
                    for (let i = 0; i < themeList.items.length; i++) {
                        this.themeDataList.push({
                            'Code': themeList.items[i].Code,
                            'Name': themeList.items[i].Name,
                        });
                    }
                })

                // GET USER LIST
                getItemDataList(user_resource).then(data => {
                    let userList = extractUserData(data);

                    // update local variables with data from API
                    this.fields = userList['fields'];
                    for (let i = 0; i < userList.items.length; i++) {
                        this.userDataList.push({
                            'Code': userList.items[i].Code,
                            'Name': userList.items[i].Name,
                        });
                    }
                })

                // GET QUANTITY TYPE LIST
                getItemDataList(quantity_type_resource).then(data => {
                    let QTList = extractQTData(data);

                    // update local variables with data from API
                    this.fields = QTList['fields'];
                    for (let i = 0; i < QTList.items.length; i++) {
                        this.QTDataList.push({
                            'Code': QTList.items[i].Code,
                            'Name': QTList.items[i].Name,
                        });
                    }
                })

                // GET BOX LIST
                getItemDataList(box_resource).then(data => {
                    let boxList = extractBoxData(data);

                    // update local variables with data from API
                    this.fields = boxList['fields'];
                    for (let i = 0; i < boxList.items.length; i++) {
                        this.boxDataList.push({
                            'Code': boxList.items[i].Code,
                            'Name': boxList.items[i].Name,
                            'Tray': boxList.items[i].Tray,
                            'Rack': boxList.items[i].Rack,
                            'Chamber': boxList.items[i].Chamber,
                            'Freezer': boxList.items[i].Freezer,
                            'Lab': boxList.items[i].Lab
                        });
                    }
                    this.$log.info("Box list has: ", this.boxDataList)
                })

                // GET SECURITY LEVEL LIST
                getItemDataList(security_level_resource).then(data => {
                    let secLevelList = extractApiData(data);

                    // update local variables with data from API
                    this.fields = secLevelList['fields'];
                    for (let i = 0; i < secLevelList.items.length; i++) {
                        this.secLevelDataList.push({
                            'Code': secLevelList.items[i].Code,
                            'Name': secLevelList.items[i].Name,
                        });
                    }
                })
            },

            fillFormFieldsDependentOnBox() {
                let dropdownSelection = getSelectedBoxSetTextFieldValue("box-dropdownlist", this.boxDataList);
                this.sample.box = dropdownSelection.boxCode;

                // SET FIELDS TEXT
                document.getElementById("tray").value = dropdownSelection.tray;
                document.getElementById("rack").value = dropdownSelection.rack;
                document.getElementById("chamber").value = dropdownSelection.chamber;
                document.getElementById("freezer").value = dropdownSelection.freezer;
                document.getElementById("lab").value = dropdownSelection.lab;
            },

            handleSubmit() {
                this.$log.info("HANDLE SUBMIT CALLED");
                this.submitted = true;

                this.$v.$touch();
                if (this.$v.$invalid) {
                    this.$log.info("HANDLE SUBMIT FAILED");
                    return;
                }

                this.$log.info("HANDLE SUBMIT PASSED");
                // this.sample.theme = getSelectedItemCode("theme-dropdownlist", this.themeDataList)
                // this.sample.user = getSelectedItemCode("user-dropdownlist", this.userDataList)
                // this.sample.securityLevel = getSelectedItemCode("secLevel-dropdownlist", this.secLevelDataList)
                // this.sample.quantity_type = getSelectedItemCode("QT-dropdownlist", this.QTDataList)

                alert("Sucsess! :-)\n\n" + JSON.stringify(this.sample));

            },

            formSubmit(e) {
                e.preventDefault();
                let currentObj = this;
                this.sample.theme = getSelectedItemCode("theme-dropdownlist", this.themeDataList)
                this.sample.user = getSelectedItemCode("user-dropdownlist", this.userDataList)
                this.sample.securityLevel = getSelectedItemCode("securityLevel-dropdownlist", this.secLevelDataList)
                this.sample.quantity_type = getSelectedItemCode("QT-dropdownlist", this.QTDataList)

                this.$log.info("DATA FROM DROPDOWN SELECTION: \n1. Theme " + this.sample.theme)
                this.$log.info("DATA FROM DROPDOWN SELECTION: \n1. User " + this.sample.user)
                this.$log.info("DATA FROM DROPDOWN SELECTION: \n1. secLevel " + this.sample.securityLevel)
                this.$log.info("DATA FROM DROPDOWN SELECTION: \n1. quantityType " + this.sample.quantity_type)

                axios.post(sample_resource, {
                    theme: this.sample.theme,
                    user: this.sample.user,
                    box: this.sample.box,
                    animal_species: this.sample.species,
                    sample_type: this.sample.sampleType,
                    sample_description: this.sample.description,
                    project: this.sample.project,
                    project_owner: this.sample.projectOwner,
                    retention_period: this.sample.retention,
                    barcode: this.sample.barcode,
                    analysis: this.sample.analysis,
                    temperature: this.sample.temperature,
                    amount: this.sample.amount,
                    quantity_type: this.sample.quantity_type,
                    security_level: this.sample.securityLevel,
                    code: this.sample.code,
                }, {
                    headers:
                        {
                            Authorization: secureStoreGetString()
                        }
                })
                    .then(function (response) {
                        currentObj.output = response.data;
                    })
                    .catch(function (error) {
                        currentObj.output = error;
                    });
            },
        },
        created() {
            this.onLoadPage();
        }
    };


</script>
