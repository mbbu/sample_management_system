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
                        <th scope="col"> Lab Located</th>
                        <th scope="col"> Room</th>
                        <th scope="col"> Freezer Number</th>
                        <th scope="col"> Code</th>
                        <th scope="col"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="freezer.id" v-for="(freezer, index) in response.message">
                        <td> {{ index + 1 }}</td>
                        <td> {{ freezer['lab.name'] }}</td>
                        <td> {{ freezer.room }}</td>
                        <td> {{ freezer.number }}</td>
                        <td> {{ freezer.code }}</td>

                        <td>
                            <b-icon
                                    icon="pencil" font-scale="2.0"
                                    class="border border-info rounded" variant="info"
                                    v-b-tooltip.hover :title="`Update freezer ${ freezer.number }`"
                                    v-b-modal.modal-freezer-edit
                                    @mouseover="fillFormForUpdate(freezer.number, freezer.code, freezer.room, freezer.lab)"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    icon="trash" font-scale="1.85"
                                    class="border rounded bg-danger p-1" variant="light"
                                    v-b-tooltip.hover :title="`Delete freezer ${freezer.number}!`"
                                    @click="deleteFreezer(freezer.code)"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>

            <div v-if="!isEditing">
                <b-modal
                        title="Add Freezer"
                        id="modal-freezer"
                        ok-title="Save"
                        cancel-variant="danger"
                        @ok="createFreezer"
                        @submit="showModal = false"
                        @hidden="clearForm"
                >
                    <form @submit.prevent="createFreezer">
                        <b-form-group id="form-lab-group" label="Lab:" label-for="form-lab-input">
                            <ejs-dropdownlist
                                    id='dropdownlist'
                                    :dataSource='labDataList'
                                    :fields="fields"
                                    placeholder='Select a lab'
                                    :v-model="laboratory"
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-room-group" label="Room:" label-for="form-room-input">
                            <b-form-input
                                    id="form-room-input"
                                    placeholder="Enter Room Number"
                                    required="true"
                                    type="text"
                                    v-model="room"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-num-group" label="Num:" label-for="form-num-input">
                            <b-form-input
                                    id="form-num-input"
                                    placeholder="Enter Freezer Number"
                                    required="true"
                                    type="text"
                                    v-model="number">
                            </b-form-input>
                        </b-form-group>

                        <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required="true"
                                    type="text"
                                    v-model="code">
                            </b-form-input>
                        </b-form-group>

                    </form>
                </b-modal>
            </div>

            <div v-else-if="isEditing">
                <b-modal
                        title="Edit Freezer"
                        @ok="updateFreezer(old_code)"
                        @submit="showModal = false"
                        id="modal-freezer-edit"
                        ok-title="Update"
                        cancel-variant="danger"
                        @hidden="clearForm"
                >
                    <form>

                        <b-form-group id="form-lab-group-edit" label="Lab:" label-for="form-lab-input">
                            <b-form-input
                                    id="form-lab-input"
                                    placeholder="Enter Lab"
                                    required="true"
                                    type="text"
                                    v-model="laboratory"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-room-group-edit" label="Room:" label-for="form-room-input">
                            <b-form-input
                                    id="form-room-input"
                                    placeholder="Enter Room Number"
                                    required="true"
                                    type="text"
                                    v-model="room"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-num-group-edit" label="Num:" label-for="form-num-input">
                            <b-form-input
                                    id="form-num-input"
                                    placeholder="Enter Freezer Number"
                                    required="true"
                                    type="text"
                                    v-model="number">
                            </b-form-input>
                        </b-form-group>

                        <b-form-group id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required="true"
                                    type="text"
                                    v-model="code">
                            </b-form-input>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
            <b-button class="float_btn"
                      v-b-modal.modal-freezer variant="primary"
            >Add Freezer
            </b-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import {freezer_resource, lab_resource} from '../../src/utils/api_paths'
    import TopNav from "@/components/TopNav";

    export default {
        name: 'Freezer',
        data() {
            return {
                page_title: "Freezer",
                response: [],
                laboratory: null,
                number: null,
                code: null,
                room: null,
                labData: [],
                labDataList: [],
                fields: {text: '', value: ''},

                // values for data modification
                old_code: null,
                showModal: true,
                isEditing: false,
            };
        },
        methods: {
            clearForm() {
                this.laboratory = null;
                this.number = null;
                this.code = null;
                this.room = null;
                this.isEditing = false;
                this.labData = [];
                this.labDataList = [];
                this.getLabDataList();
            },

            fillFormForUpdate(number, code, room, laboratory) {
                this.laboratory = laboratory;
                this.number = number;
                this.code = code;
                this.room = room;
                this.old_code = code;
                this.isEditing = true;
                this.showModal = true;
            },

            getLabDataList() {
                axios.get(lab_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " " + res.data['message']);
                        this.labData = res.data;
                        for (var lab_item = 0; lab_item < this.labData.message.length; lab_item++) {
                            this.labDataList.push({
                                'Code': this.labData.message[lab_item].code,
                                'Name': this.labData.message[lab_item].name
                            });

                            this.fields = {text: 'Name', value: 'Code'};
                        }
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        this.$log.error(error);
                    });
            },

            getSelectedLabItem() {
                var item = document.getElementById("dropdownlist").value;
                this.$log.info("*****> SELECTED ITEM VALUE: " + item);

                for (var i = 0; i < this.labDataList.length; i++) {
                    this.$log.info("ITEM: " + item + " labDataList Item: " + this.labDataList[i].Name);

                    if (item === this.labDataList[i].Name) {
                        this.laboratory = this.labDataList[i].Code;
                        this.$log.info("Item Value: " + item + " LabDataList Item Value: " + this.labDataList[i].Name +
                            " Lab Code is: " + this.laboratory)
                    } else {
                        this.$log.info("** ITEM NOT FOUND ***")
                    }
                }
            },

            getFreezer() {
                axios.get(freezer_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " " + res.data['message']);
                        this.response = res.data;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        this.$log.error(error);
                    });
                this.getLabDataList();
            },

            createFreezer: function () {
                this.getSelectedLabItem();

                axios.post(freezer_resource, {
                    laboratory: this.laboratory,
                    number: this.number,
                    code: this.code,
                    room: this.room,
                })
                    .then((response) => {
                        this.getFreezer();
                        this.flashMessage.show({
                            status: 'success',
                            title: "", message: response.data['message']
                        });
                        this.clearForm();
                    })
                    .catch((error) => {
                        this.clearForm();
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 409) {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Error",
                                    message: error.response.data['message']
                                });
                            } else if (error.response.status === 400) {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Form Error",
                                    message: "Kindly refill the form"
                                });
                            } else if (error.response.status === 401) {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Session Expired",
                                    message: "You need to log in to perform this operation"
                                });
                            } else {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Error",
                                    message: "Freezer already exists"
                                });
                            }
                        }
                    });
            },

            updateFreezer: function (code) {
                axios.put(freezer_resource, {
                        laboratory: this.laboratory,
                        number: this.number,
                        code: this.code,
                        room: this.room,
                    }, {headers: {code: code}}
                )
                    .then((response) => {
                        this.getFreezer();
                        this.flashMessage.show({
                            status: 'success',
                            title: response.data['message'], message: ""
                        });
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 304) {
                                this.flashMessage.show({
                                    status: 'info',
                                    title: "Info",
                                    message: "Record not modified"
                                });
                            } else if (error.response.status === 401) {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Session Expired",
                                    message: "You need to log in to perform this operation"
                                });
                            } else {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Error",
                                    message: error.response.data['message']
                                });
                            }
                        }
                    });
                this.clearForm();
            },

            deleteFreezer: function (code) {
                axios.delete(freezer_resource, {
                    headers: {
                        code: code
                    }
                })
                    .then((response) => {
                        this.getFreezer();
                        this.flashMessage.show({
                            status: 'success',
                            title: response.data['message'], message: ""
                        });
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 401) {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Session Expired",
                                    message: "You need to log in to perform this operation"
                                });
                            } else {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: error, message: ""
                                });
                            }
                        }
                    });
            },
        },
        created() {
            this.getFreezer();
        },
        components: {TopNav}
    };
</script>
