<template>
    <div id="jumbotron">
        <div class="container">
            <top-nav :page_title="page_title"></top-nav>

            <form-wizard @submit.prevent="formSubmit" ref="formContainer"
                         subtitle="Kindly input the correct information" title="Sample Data Form">
                <!-- FLASH MESSAGES -->
                <FlashMessage :position="'right bottom'"></FlashMessage>

                <tab-content :before-change="handleSubmit"
                             title="Sample Details">
                    <!--THEME-->
                    <div class="form-group">
                        <b-form-group id="form-theme" label="Select a Theme:" label-for="form-theme-input">
                            <ejs-dropdownlist
                                    :dataSource='themeDataList'
                                    :fields="fields"
                                    :v-model="sample.theme"
                                    :value="selectDropDownItemForUpdate('theme-dropdownlist', sample.theme, themeDataList)"
                                    @change="setTheme"
                                    id="theme-dropdownlist"
                                    placeholder='Select a theme'
                            ></ejs-dropdownlist>
                        </b-form-group>
                    </div>

                    <!-- PROJECT -->
                    <div class="form-group">
                        <label for="project"> Project</label>
                        <input class="form-control" id="project" required type="text" v-model="sample.project"/>
                    </div>

                    <!--PROJECT OWNER-->
                    <div class="form-group">
                        <label for="projectOwner"> Project Owner</label>
                        <input class="form-control" id="projectOwner" required type="text"
                               v-model="sample.projectOwner"/>
                    </div>

                    <!--SAMPLE OWNER-->
                    <div class="form-group">
                        <b-form-group id="form-user" label="Select the Sample Owner:" label-for="form-user-input">
                            <ejs-dropdownlist
                                    :dataSource='userDataList'
                                    :fields="fields"
                                    :v-model="sample.user"
                                    :value="selectDropDownItemForUpdate('user-dropdownlist', sample.user, userDataList)"
                                    @change="setUser"
                                    id="user-dropdownlist"
                                    placeholder='Select the sample owner(i.e. One in-charge of handling the sample)'
                            ></ejs-dropdownlist>
                        </b-form-group>
                    </div>

                    <!--SAMPLE TYPE-->
                    <div class="form-group">
                        <label for="sampleType"> Sample Type</label>
                        <input class="form-control" id="sampleType" required type="text" v-model="sample.sampleType"/>
                    </div>

                    <!--SPECIES-->
                    <div class="form-group">
                        <label for="species"> Species</label>
                        <input class="form-control" id="species" required type="text" v-model="sample.species"/>
                    </div>

                    <!--DESC-->
                    <div class="form-group">
                        <label for="description"> Description</label>
                        <textarea class="form-control" id="description" name="description" type="text"
                                  v-model="sample.description"/>
                    </div>
                    <errors-display :errors="errors"></errors-display>
                </tab-content>

                <!-- TAB 2 -->
                <tab-content :before-change="handleSubmit" title="Sample Location in Institution">
                    <div class="form-group">
                        <label for="locationCollected">Location Collected</label>
                        <input class="form-control" id="locationCollected" required type="text"
                               v-model="sample.locationCollected"/>
                    </div>

                    <div class="form-group">
                        <b-form-group id="box" label="Select a Box for the sample:" label-for="form-box-input">
                            <ejs-dropdownlist
                                    :dataSource='boxDataList'
                                    :fields="fields"
                                    :v-model="sample.box"
                                    :value="selectDropDownItemForUpdate('box-dropdownlist', sample.box, boxDataList)"
                                    @change="fillFormFieldsDependentOnBox"
                                    id="box-dropdownlist"
                                    placeholder='Select a box and its location will be shown'
                            ></ejs-dropdownlist>
                        </b-form-group>
                    </div>

                    <!-- Start row -->
                    <div class="row">
                        <div class="col">
                            <div class="form-group">
                                <label for="tray">Tray Number</label>
                                <input class="form-control" disabled="disabled" id="tray" placeholder="Tray having box"
                                       required
                                       type="text"
                                       v-model="sample.tray"/>
                            </div>
                        </div>

                        <div class="col">
                            <div class="form-group">
                                <label for="rack">Rack Number</label>
                                <input class="form-control" disabled="disabled" id="rack"
                                       placeholder="Rack holding tray" required
                                       type="text" v-model="sample.rack"/>
                            </div>
                        </div>

                        <div class="col">
                            <div class="form-group">
                                <label for="chamber"> Chamber Type </label>
                                <input class="form-control" disabled="disabled" id="chamber"
                                       placeholder="Chamber where rack is" required
                                       type="text" v-model="sample.chamber"/>
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
                                       placeholder="Freezer where box is stored" required
                                       type="text" v-model="sample.freezer"/>
                            </div>
                        </div>

                        <div class="col">
                            <div class="form-group">
                                <label for="lab">Lab</label>
                                <input class="form-control" disabled="disabled" id="lab"
                                       placeholder="Lab where freezer is" required
                                       type="text" v-model="sample.lab"/>
                            </div>
                        </div>
                    </div>
                    <!-- End Row -->

                    <!-- Start row -->
                    <div class="row">
                        <div class="col">
                            <div class="form-group">
                                <label for="temperature">Temperature (Default in Celsius)</label>
                                <input class="form-control" id="temperature" required type="number"
                                       v-model="sample.temperature"/>
                            </div>

                        </div>

                        <div class="col">
                            <div class="form-group">
                                <label for="amount">Amount</label>
                                <input class="form-control" id="amount" required type="number" min="1"
                                       v-model="sample.amount"/>
                            </div>

                        </div>
                        <div class="col">
                            <div class="form-group">
                                <b-form-group id="form-QT" label="Select a Quantity Type:"
                                              label-for="form-user-input">
                                    <ejs-dropdownlist
                                            :dataSource='QTDataList'
                                            :fields="fields"
                                            :v-model="sample.quantity_type"
                                            :value="selectDropDownItemForUpdate('QT-dropdownlist', sample.quantity_type, QTDataList)"
                                            @change="setQuantityType"
                                            id="QT-dropdownlist"
                                            placeholder='Select a quantity type(e.g. ML, L, G ...)'
                                    ></ejs-dropdownlist>
                                </b-form-group>
                            </div>
                        </div>
                    </div>
                    <!-- End Row -->
                    <errors-display :errors="errors"></errors-display>
                </tab-content>


                <tab-content :before-change="handleSubmit" title="Finishing Up">
                    <div class="form-group">
                        <b-form-group id="form-securityLevel" label="Security Level Needed:"
                                      label-for="form-securityLevel-input">
                            <ejs-dropdownlist
                                    :dataSource='secLevelDataList'
                                    :fields="fields"
                                    :v-model="sample.securityLevel"
                                    :value="selectDropDownItemForUpdate('securityLevel-dropdownlist', sample.securityLevel, secLevelDataList)"
                                    @change="setSecurityLevel"
                                    id="securityLevel-dropdownlist"
                                    placeholder='Select Security Level Needed'
                            ></ejs-dropdownlist>
                        </b-form-group>
                    </div>

                    <div class="form-group">
                        <label for="code"> Code</label>
                        <input class="form-control" id="code" required
                               type="text"
                               v-model="sample.code"/>
                        <div class="invalid-feedback" v-if="submitted && error in errors">
                            <span> Code is required + {{ error }} </span>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="barcode"> Barcode</label>
                        <input class="form-control" id="barcode" required type="text" v-model="sample.barcode"/>
                    </div>

                    <div class="form-group">
                        <label for="analysis"> Analysis</label>
                        <input class="form-control" id="analysis" required type="text" v-model="sample.analysis"/>
                    </div>

                    <div class="row">
                        <div class="col">
                            <div class="form-group">
                                <label for="retention"> Retention</label>
                                <input class="form-control" id="retention" min="1" required type="number"
                                       v-model="sample.retention"/>
                            </div>
                        </div>

                        <div class="col">
                            <div class="form-group">
                                <label for="period">Select Retention Length:</label>
                                <select @change="setRetentionPeriod" class="custom-select" id="period" required>
                                    <option selected>Select period(Days, Weeks ...)</option>
                                    <option value="1">Days</option>
                                    <option value="2">Weeks</option>
                                    <option value="3">Months</option>
                                    <option value="4">Years</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <errors-display :errors="errors"></errors-display>
                </tab-content>

                <template scope="props" slot="footer">
                    <div class=wizard-footer-left>
                        <wizard-button :style="props.fillButtonStyle" @click.native="props.prevTab()"
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
import axios from 'axios';
import {
  countDownTimer,
  extractApiData,
  extractBoxData,
  extractQTData,
  extractUserData,
  getItemDataList,
  getSampleDetailsForEditing,
  getSelectedBoxSetTextFieldValue,
  getSelectedItemCode,
  isUpdate,
  respondTo401,
  secureStoreGetString,
  selectDropDownItemForUpdate,
  showFlashMessage
} from "@/utils/util_functions";
import {
  bio_hazard_level_resource,
  box_resource,
  quantity_type_resource,
  sample_resource,
  theme_resource,
  user_resource
} from "@/utils/api_paths";
import TopNav from "../../components/TopNav";
import ErrorsDisplay from "../../components/ErrorsDisplay";

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
                    convertedRetentionPeriod: "",
                    barcode: "",
                    analysis: "",
                    temperature: "",
                    amount: "",
                    quantity_type: "",
                    securityLevel: "",
                    code: "",

                    // extra fields
                    tray: "",
                    rack: "",
                    chamber: "",
                    freezer: "",
                    lab: "",

                },
                submitted: false,

                errors: [],
                tabNum: 0,
                tabOne: 0,
                tabTwo: 1,
                tabThree: 2,
                QTDataList: [],
                boxDataList: [],
                userDataList: [],
                themeDataList: [],
                secLevelDataList: [],
                fields: {text: '', value: ''},
                page_title: "Add Sample",
            };
        },

        methods: {
            // util functions
            selectDropDownItemForUpdate,
            onLoadPage() {
                this.$log.info("Is Update True? ", isUpdate())

                if (isUpdate()) {
                    // call function to fill form
                    this.fillSampleFormForUpdate()
                } else {
                    this.$log.info("Just create a new sample")
                    this.getDataListItemsForForm()
                }
            },

            getDataListItemsForForm() {
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
                })

                // GET SECURITY LEVEL LIST
                getItemDataList(bio_hazard_level_resource).then(data => {
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
                this.sample.tray = dropdownSelection.tray;
                this.sample.rack = dropdownSelection.rack;
                this.sample.chamber = dropdownSelection.chamber;
                this.sample.freezer = dropdownSelection.freezer;
                this.sample.lab = dropdownSelection.lab;
            },

            handleSubmit() {
                if (this.tabNum === 0) {
                    this.errors = []
                    return this.validateForm(this.tabOne)
                } else if (this.tabNum === 1) {
                    this.errors = []
                    return this.validateForm(this.tabTwo)
                } else if (this.tabNum === 2) {
                    this.errors = []
                    return this.validateForm(this.tabThree)
                }
            },

            validateForm(tabs) {
                let self = this;

                switch (tabs) {
                    case 0:
                        if (!this.sample.theme) {
                            this.errors.push("Theme is required");
                        }
                        if (!this.sample.project) {
                            this.errors.push("Project is required");
                        }
                        if (!this.sample.projectOwner) {
                            this.errors.push("Project Owner is required");
                        }
                        if (!this.sample.user) {
                            this.errors.push("Sample Owner is required");
                        }
                        if (!this.sample.sampleType) {
                            this.errors.push("Sample Type is required");
                        }
                        if (!this.sample.species) {
                            this.errors.push("Animal species is required");
                        }
                        if (!this.sample.description || this.sample.description.length < 25) {
                            this.errors.push("Description is required and should be at least 2 sentences.");
                        }
                        if (this.errors.length) {
                            showFlashMessage(self, "error", "Check Form for Errors", "Correct errors to proceed!")
                        }
                        if (!this.errors.length) {
                            this.tabNum++
                            return true;
                        }
                        break;

                    case 1:
                        if (!this.sample.locationCollected) {
                            this.errors.push("Location is required");
                        }
                        if (!this.sample.box) {
                            this.errors.push("Box is required");
                        }
                        if (!this.sample.temperature) {
                            this.errors.push("Temperature is required");
                        }
                        if (!this.sample.amount) {
                            this.errors.push("Amount is required");
                        }
                        if (!this.sample.quantity_type) {
                            this.errors.push("Quantity Type is required");
                        }
                        if (this.errors.length) {
                            showFlashMessage(self, "error", "Check Form for Errors", "Correct errors to proceed!")
                        }
                        if (!this.errors.length) {
                            this.tabNum++
                            return true;
                        }
                        break;

                    case 2:
                        if (!this.sample.securityLevel) {
                            this.errors.push("Security level is required");
                        }
                        if (!this.sample.code) {
                            this.errors.push("Code is required");
                        }
                        if (!this.sample.barcode) {
                            this.errors.push("Barcode Owner is required");
                        }
                        if (!this.sample.analysis) {
                            this.errors.push("Analysis is required");
                        }
                        if (!this.sample.retention) {
                            this.errors.push("Retention period is required");
                        }
                        if (this.errors.length) {
                            showFlashMessage(self, "error", "Check Form for Errors", "Correct errors to proceed!")
                        }
                        if (!this.errors.length) {
                            this.tabNum = 0
                            return true;
                        }
                        break;

                    default:
                        this.errors = [];
                        if (!this.errors.length) {
                            return true;
                        }
                        break;
                }
            },

            setTheme() {
                this.sample.theme = getSelectedItemCode("theme-dropdownlist", this.themeDataList)
            },
            setUser() {
                this.sample.user = getSelectedItemCode("user-dropdownlist", this.userDataList)
            },
            setSecurityLevel() {
                this.sample.securityLevel = getSelectedItemCode("securityLevel-dropdownlist", this.secLevelDataList)
            },
            setQuantityType() {
                this.sample.quantity_type = getSelectedItemCode("QT-dropdownlist", this.QTDataList)
            },

            setRetentionPeriod() {
                let periodSelect = document.getElementById("period")
                let periodValue = parseInt(periodSelect.options[periodSelect.selectedIndex].value);

                if (periodValue === 1) {
                    this.sample.convertedRetentionPeriod = this.sample.retention * 1
                } else if (periodValue === 2) {
                    // convert week to days
                    this.sample.convertedRetentionPeriod = this.sample.retention * 7
                } else if (periodValue === 3) {
                    // convert months to days
                    this.sample.convertedRetentionPeriod = this.sample.retention * 30
                } else if (periodValue === 4) {
                    //  convert years to days
                    this.sample.convertedRetentionPeriod = this.sample.retention * 365
                }
            },

            formSubmit() {
                if (isUpdate()) {
                    this.updateSample()
                } else {
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

                    axios.post(sample_resource, {
                      theme: this.sample.theme,
                      user: this.sample.user,
                      box: this.sample.box,
                      animal_species: this.sample.species,
                      sample_type: this.sample.sampleType,
                      sample_description: this.sample.description,
                      project: this.sample.project,
                      project_owner: this.sample.projectOwner,
                      retention_period: this.sample.convertedRetentionPeriod,
                      barcode: this.sample.barcode,
                      analysis: this.sample.analysis,
                      temperature: this.sample.temperature,
                      amount: this.sample.amount,
                      quantity_type: this.sample.quantity_type,
                      bio_hazard_level: this.sample.securityLevel,
                      location_collected: this.sample.locationCollected,
                      code: this.sample.code,
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
                                if (error.response.status === 409) {
                                    showFlashMessage(self, 'error', error.response.data['message'], '');
                                } else if (error.response.status === 400) {
                                    showFlashMessage(self, 'error', 'Kindly refill the form', error.response.data['message']);
                                } else if (error.response.status === 401) {
                                    respondTo401(self)
                                } else {
                                    showFlashMessage(self, 'error', error.response.data['message'], '');
                                }
                            }
                        });
                }
            },

            /* UPDATE FUNCTIONS */
            fillSampleFormForUpdate() {
                // 1st update the page title
                this.page_title = "Update Sample"

                // get data-lists for drop-downs
                this.getDataListItemsForForm()

                // set sample details
                let sampleForUpdate = getSampleDetailsForEditing()

                this.sample.project = sampleForUpdate['project'];
                this.sample.projectOwner = sampleForUpdate['project_owner'];
                this.sample.sampleType = sampleForUpdate['sample_type'];
                this.sample.species = sampleForUpdate['animal_species'];
                this.sample.description = sampleForUpdate['sample_description'];
                this.sample.locationCollected = sampleForUpdate['location_collected'];
                this.sample.retention = sampleForUpdate['retention_period'];
                this.sample.barcode = sampleForUpdate['barcode'];
                this.sample.analysis = sampleForUpdate['analysis'];
                this.sample.temperature = sampleForUpdate['temperature'];
                this.sample.amount = sampleForUpdate['amount'];
                this.sample.code = sampleForUpdate['code'];
                this.sample.tray = sampleForUpdate['box.tray.number'];
                this.sample.rack = sampleForUpdate['box.tray.rack.number'];
                this.sample.chamber = sampleForUpdate['box.tray.rack.chamber.type'];
                this.sample.freezer = sampleForUpdate['box.tray.rack.chamber.freezer.number'];
                this.sample.lab = sampleForUpdate['box.tray.rack.chamber.freezer.lab.name']
                    + " room " + sampleForUpdate['box.tray.rack.chamber.freezer.lab.room'];

                // drop-down data
                this.sample.theme = sampleForUpdate['theme.name'];
                this.sample.user = sampleForUpdate['user.first_name'] + " " + sampleForUpdate['user.last_name'];
                this.sample.box = sampleForUpdate['box.label'];
                this.sample.quantity_type = sampleForUpdate['quantity.id'];
                this.sample.securityLevel = sampleForUpdate['bioHazardLevel.code'];
                this.sample.convertedRetentionPeriod = this.sample.retention;

                document.getElementById('period').selectedIndex = 1;

                let x = document.getElementById("period").selectedIndex;
                let y = document.getElementById("period").options;

                document.getElementById('period').value = y[x].text;
            },

            updateSample() {
                let self = this;
                let loader = self.$loading.show({
                    isFullPage: true,
                    canCancel: false,
                    color: '#074880',
                    loader: 'dots',
                    width: 255,
                    height: 255,
                    backgroundColor: '#FAAB2C',
                    opacity: 0.7,
                    zIndex: 999,
                })

                axios.put(sample_resource, {
                  theme: this.sample.theme,
                  user: this.sample.user,
                  box: this.sample.box,
                  animal_species: this.sample.species,
                  sample_type: this.sample.sampleType,
                  sample_description: this.sample.description,
                  project: this.sample.project,
                  project_owner: this.sample.projectOwner,
                  retention_period: this.sample.convertedRetentionPeriod,
                  barcode: this.sample.barcode,
                  analysis: this.sample.analysis,
                  temperature: this.sample.temperature,
                  amount: this.sample.amount,
                  quantity_type: this.sample.quantity_type,
                  bio_hazard_level: this.sample.securityLevel,
                  location_collected: this.sample.locationCollected,
                  code: this.sample.code,
                }, {
                    headers:
                        {
                            code: this.sample.code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        setTimeout(() => {
                            // stopLoader(self)
                            loader.hide()
                            showFlashMessage(self, 'success', response.data['message'], '');
                            // todo: redirect to sample view page
                            countDownTimer(self, 2, '/sample')
                        }, 4000)
                    })
                    .catch((error) => {
                        // stopLoader(self)
                        loader.hide()
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 409) {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            } else if (error.response.status === 400) {
                                showFlashMessage(self, 'error', 'Kindly refill the form', error.response.data['message']);
                            } else if (error.response.status === 401) {
                                respondTo401(self)
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });

            },
        },
        created() {
            this.onLoadPage();
        },
        components: {TopNav, ErrorsDisplay}
    };


</script>
