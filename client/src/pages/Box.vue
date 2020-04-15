<template>

    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title"></top-nav>

                <FlashMessage :position="'center bottom'"></FlashMessage>
                <br> <br>

                <table class=" table table-hover">
                    <thead>
                    <tr>
                        <th scope="col"> Id</th>
                        <th scope="col"> Label</th>
                        <th scope="col"> Tray</th>
                        <th scope="col"> Rack</th>
                        <th scope="col"> Chamber</th>
                        <th scope="col"> Freezer</th>
                        <th scope="col"> Lab Name</th>
                        <th scope="col"> Lab Room</th>
                        <th scope="col"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="box.id" v-for="(box, index) in response.message">
                        <td> {{index + 1}}</td>
                        <td> {{box.label}}</td>
                        <td> {{box['tray.number']}}</td>
                        <td> {{box['tray.rack.number']}}</td>
                        <td> {{box['tray.rack.chamber.type']}}</td>
                        <td> {{box['tray.rack.chamber.freezer.number']}}</td>
                        <td> {{box['tray.rack.chamber.freezer.lab.name']}}</td>
                        <td> {{box['tray.rack.chamber.freezer.lab.room']}}</td>

                        <td>
                            <b-icon
                                    :title="`Update box ${ box.label }`"
                                    @mouseover="fillFormForUpdate(box['tray.number'], box.label, box.code)"
                                    class="border border-info rounded" font-scale="2.0"
                                    icon="pencil" v-b-modal.modal-freezer-edit
                                    v-b-tooltip.hover
                                    variant="info"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    :title="`Delete box ${box.label}!`" @click="deleteBox(box.code)"
                                    class="border rounded bg-danger p-1" font-scale="1.85"
                                    icon="trash" v-b-tooltip.hover
                                    variant="light"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>

            <div v-if="!isEditing">
                <b-modal
                        :title="`Add ${page_title}`"
                        @hidden="clearForm"
                        @ok="createBox"
                        @submit="clearForm"
                        cancel-variant="danger"
                        id="modal-freezer"
                        ok-title="Save"
                >
                    <form @submit.prevent="createBox">
                        <b-form-group id="form-tray-group" label="Tray Number:" label-for="form-tray-input">
                            <ejs-dropdownlist
                                    :dataSource='trayDataList'
                                    :fields="fields"
                                    :v-model="box.tray"
                                    id='dropdownlist'
                                    placeholder='Select a tray'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-label-group" label="Box Label:" label-for="form-label-input">
                            <b-form-input
                                    id="form-label-input"
                                    placeholder="Enter box label"
                                    required="true"
                                    type="text"
                                    v-model="box.label"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required="true"
                                    type="text"
                                    v-model="box.code">
                            </b-form-input>
                        </b-form-group>

                    </form>
                </b-modal>
            </div>

            <div v-else-if="isEditing">
                <b-modal
                        :title="`Edit ${page_title}`"
                        @hidden="clearForm"
                        @ok="updateBox(old_code)"
                        @shown="selectItemForUpdate(box.tray)"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-freezer-edit"
                        ok-title="Update"
                >
                    <form>
                        <b-form-group id="form-tray-group-edit" label="Tray Number:" label-for="form-tray-input">
                            <ejs-dropdownlist
                                    :dataSource='trayDataList'
                                    :fields="fields"
                                    :v-model="box.tray"
                                    id='dropdownlist'
                                    placeholder='Select a tray'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-label-group-edit" label="Box Label:" label-for="form-label-input">
                            <b-form-input
                                    id="form-label-input"
                                    placeholder="Enter box label"
                                    required="true"
                                    type="text"
                                    v-model="box.label"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required="true"
                                    type="text"
                                    v-model="box.code">
                            </b-form-input>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>

            <b-button class="float_btn"
                      v-b-modal.modal-freezer variant="primary"
            >Add Box
            </b-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import TopNav from "../components/TopNav";
    import {
        extractTrayData,
        getItemDataList,
        getSelectedItem,
        secureStoreGetString,
        selectItemForUpdate,
        showFlashMessage
    } from "../utils/util_functions";
    import {box_resource, tray_resource} from "../utils/api_paths";

    export default {
        name: 'Box',
        data() {
            return {
                response: [],
                page_title: 'Boxes',

                box: {
                    tray: null,
                    label: null,
                    code: null
                },

                trayDataList: [],
                fields: {text: '', value: ''},

                // values for data modification
                old_code: null,
                showModal: true,
                isEditing: false,

            };
        },

        methods: {
            // component util functions
            selectItemForUpdate,
            clearForm() {
                this.box.tray = null;
                this.box.code = null;
                this.box.label = null;
                this.isEditing = false;
                this.trayDataList = [];
                this.onLoadPage();
            },

            fillFormForUpdate(tray, label, code) {
                this.box.tray = tray;
                this.box.code = code;
                this.box.label = label;
                this.old_code = code;
                this.isEditing = true;
                this.showModal = true;
            },

            onLoadPage() {
                getItemDataList(tray_resource).then(data => {
                    let trayList = extractTrayData(data);
                    this.$log.info("Tray list json: ", JSON.stringify(trayList));

                    // update local variables with data from API
                    this.fields = trayList['fields'];
                    for (let i = 0; i < trayList.items.length; i++) {
                        this.trayDataList.push({
                            'Code': trayList.items[i].Code,
                            'Name': trayList.items[i].Name,
                        });
                    }
                    this.$log.info("FIELDS: ", this.fields);
                    this.$log.info("Data: ", this.fields);
                })
            },

            // functions to interact with API
            getBox() {
                this.clearForm();
                axios.get('http://localhost:5000/box')
                    .then((res) => {
                        this.response = res.data;
                        console.log(this.response)
                    })
                    .catch((error) => {
                        console.error(error);
                    });
            },

            createBox: function () {
                let self = this;
                this.box.tray = getSelectedItem(this.trayDataList, this.tray);

                axios.post(box_resource, {
                    tray: this.box.tray,
                    label: this.box.label,
                    code: this.box.code,
                }, {
                    headers:
                        {
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getBox();
                        showFlashMessage(self, 'success', response.data['message'], '');
                        this.clearForm();
                    })
                    .catch((error) => {
                        this.clearForm();
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 409) {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            } else if (error.response.status === 400) {
                                showFlashMessage(self, 'error', error.response.data['message'], 'Kindly refill the form');
                            } else if (error.response.status === 401) {
                                showFlashMessage(self, 'error', "Session Expired", 'You need to log in to perform this operation');
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });
            },

            updateBox: function (code) {
                let self = this;
                this.box.tray = getSelectedItem(this.trayDataList, this.box.tray);

                axios.put(box_resource, {
                    tray: this.box.tray,
                    label: this.box.label,
                    code: this.box.code,
                }, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getBox();
                        showFlashMessage(self, 'success', response.data['message'], '');
                        this.clearForm();
                    })
                    .catch((error) => {
                        this.clearForm();
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 304) {
                                showFlashMessage(self, 'info', 'Record not modified!', '');
                            } else if (error.response.status === 401) {
                                showFlashMessage(self, 'error', "Session Expired", 'You need to log in to perform this operation');
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });
            },

            deleteBox: function (code) {
                let self = this;
                axios.delete(box_resource, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getBox();
                        showFlashMessage(self, 'success', response.data['message'], '');
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 401) {
                                showFlashMessage(self, 'error', "Session Expired", 'You need to log in to perform this operation');
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });
            },
        },
        created() {
            this.getBox();
        },
        components: {TopNav}
    };
</script>


