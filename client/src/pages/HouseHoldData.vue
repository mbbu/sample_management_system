<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-12">
        <top-nav :page_title="page_title"></top-nav>

        <!-- FLASH MESSAGES -->
        <FlashMessage :position="'right bottom'"></FlashMessage>
        <br> <br>
        <table class=" table table-hover">
          <thead>
          <tr>
            <th class="table-header-style" scope="col"> Id</th>
            <th class="table-header-style" scope="col"> Study Block</th>
            <th class="table-header-style" scope="col"> Farmer Name</th>
            <th class="table-header-style" scope="col"> Cattle ID</th>
            <th class="table-header-style" scope="col"> Cattle Name</th>
            <th class="table-header-style" scope="col"> Color</th>
            <th class="table-header-style" scope="col"> Sex</th>
            <th class="table-header-style" scope="col"> Collar</th>
            <th class="table-header-style" scope="col"> PCV</th>
            <th class="table-header-style" scope="col"> Dx</th>
            <th class="table-header-style" scope="col"> Rx</th>
            <th class="table-header-style" scope="col"> Notes</th>
            <th v-if="isAuth" class="table-header-style" scope="col"> Actions</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(house_hold_data, index) in response.message" :key="house_hold_data.id">
            <td> {{ index + 1 }}</td>
            <td> {{ house_hold_data['study_block.name'] }}</td>
            <td> {{ house_hold_data.farmer }}</td>
            <td> {{ house_hold_data.cattle_id }}</td>
            <td> {{ house_hold_data.cattle_name }}</td>
            <td> {{ house_hold_data.cattle_color }}</td>
            <td> {{ house_hold_data.cattle_sex }}</td>
            <td> {{ house_hold_data.collar }}</td>
            <td> {{ house_hold_data.pcv }}</td>
            <td> {{ house_hold_data.diagnosis }}</td>
            <td> {{ house_hold_data.treatment }}</td>
            <td> {{ house_hold_data.notes }}</td>

            <td v-if="isAuth">
              <b-icon
                  v-b-modal.modal-house_hold_data-edit
                  v-b-tooltip.hover
                  :title="`Update house_hold_data ${ house_hold_data.farmer }`" class="border border-info rounded"
                  font-scale="2.0" icon="pencil"
                  variant="info"
                  @mouseover="fillFormForUpdate(house_hold_data)"
              ></b-icon>
              &nbsp;
              <b-icon
                  v-b-tooltip.hover
                  :title="`Delete house_hold_data ${house_hold_data.farmer}!`"
                  class="border rounded bg-danger p-1" font-scale="1.85"
                  icon="trash" variant="light"
                  @click="deleteHouseHoldData(house_hold_data.code)"
              ></b-icon>
            </td>
          </tr>
          </tbody>
        </table>
      </div>

      <div v-if="!isEditing">
        <b-modal id="modal-house_hold_data"
                 :title="`Add ${page_title}`" cancel-variant="danger" ok-title="Save"
                 @hidden="clearForm" @ok="createHouseHoldData" @submit="clearForm"
        >
          <form @submit.prevent="createHouseHoldData">
            <vue-tiny-tabs id="mytabs" :anchor="false" :closable="false" :hideTitle="true" class="tinytabs tabs">
              <div id="farmer-info" class="section tab">
                <h4 class="title"><small><b>Farmer Info</b></small></h4>

                <!--STUDY-BLOCK-->
                <b-form-group id="form-study_block-group" label="Study Block:" label-for="form-study_block-input">
                  <ejs-dropdownlist
                      id='dropdownlist'
                      :dataSource='studyBlockDataList'
                      :fields="fields"
                      :v-model="house_hold_data.study_block"
                      placeholder='Select a study block'
                  ></ejs-dropdownlist>
                </b-form-group>

                <!--FARMER-->
                <b-form-group id="form-farmer-group" label="Farmer Name:" label-for="form-farmer-input">
                  <b-form-input id="form-farmer-input" v-model="house_hold_data.farmer"
                                placeholder="Enter Farmer Name" required type="text"></b-form-input>
                </b-form-group>
              </div>

              <div id="cattle-info" class="section tab">
                <h4 class="title"><small><b>Cattle Info</b></small></h4>
                <!--CATTLE_ID-->
                <b-form-group id="form-cattle_id-group" label="Cattle ID:" label-for="form-cattle_id-input">
                  <b-form-input id="form-cattle_id-input" v-model="house_hold_data.cattle_id"
                                placeholder="Enter Cattle ID" required type="text"></b-form-input>
                </b-form-group>

                <!--CATTLE NAME-->
                <b-form-group id="form-cattle_name-group" label="Cattle Name:" label-for="form-cattle_name-input">
                  <b-form-input id="form-cattle_name-input" v-model="house_hold_data.cattle_name"
                                placeholder="Enter Cattle Name" required type="text"></b-form-input>
                </b-form-group>

                <!--CATTLE COLOR-->
                <b-form-group id="form-cattle-color-group" label="Cattle Color:" label-for="form-cattle-color-input">
                  <b-form-input id="form-cattle-color-input" v-model="house_hold_data.cattle_color"
                                placeholder="Enter Cattle Color" required type="text"></b-form-input>
                </b-form-group>


                 <!--CATTLE COLOR-->
                <b-form-group id="form-cattle-collar-group" label="Collar:" label-for="form-cattle-collar-input">
                  <b-form-input id="form-cattle-collar-input" v-model="house_hold_data.collar"
                                placeholder="Enter Collar" required type="text"></b-form-input>
                </b-form-group>

                <!--CATTLE Sex-->
                <div id="cattle-sex">
                  <p>Cattle Sex:</p>
                  <input id="male" v-model="house_hold_data.cattle_sex" type="radio" value="Male">
                  <label for="male">Male</label>
                  <br>
                  <input id="female" v-model="house_hold_data.cattle_sex" type="radio" value="Female">
                  <label for="female">Female</label>
                  <br>
                </div>
              </div>

              <div id="health-info" class="section tab">
                <h4 class="title"><small><b>Health Info</b></small></h4>

                <!--CATTLE PCV-->
                <b-form-group id="form-pcv-group" label="PCV(Packed Cell Volume):" label-for="form-pcv-input">
                  <b-form-input id="form-pcv-input" v-model="house_hold_data.pcv"
                                placeholder="Enter PCV" required type="text"></b-form-input>
                </b-form-group>

                <!--CATTLE Diagnosis-->
                <b-form-group id="form-diagnosis-group" label="Diagnosis:" label-for="form-diagnosis-input">
                  <b-form-input id="form-diagnosis-input" v-model="house_hold_data.diagnosis"
                                placeholder="Enter Diagnosis" required type="text"></b-form-input>
                </b-form-group>

                <!--CATTLE Treatment-->
                <b-form-group id="form-treatment-group" label="Treatment:" label-for="form-treatment-input">
                  <b-form-input id="form-treatment-input" v-model="house_hold_data.treatment"
                                placeholder="Enter Treatment" required type="text"></b-form-input>
                </b-form-group>

                <!--CATTLE CC/ML-->
                <b-form-group id="form-cc/ml-group" label="Dosage:" label-for="form-cc/ml-input">
                  <b-form-input id="form-cc/ml-input" v-model="house_hold_data.cc"
                                placeholder="Enter cc/ml" required type="number"></b-form-input>
                </b-form-group>

                <!--CATTLE Notes-->
                <b-form-group id="form-notes-group" label="Notes:" label-for="form-notes-input">
                  <b-form-textarea id="form-notes-input" v-model="house_hold_data.notes"
                                   placeholder="Enter Notes" required type="text"></b-form-textarea>
                </b-form-group>
              </div>
            </vue-tiny-tabs>
          </form>
        </b-modal>
      </div>

      <div v-else-if="isEditing">
        <b-modal id="modal-house_hold_data-edit" :title="`Edit ${page_title}`"
                 cancel-variant="danger" ok-title="Update"
                 @hidden="clearForm" @ok="updateHouseHoldData(old_code)"
                 @shown="selectDropDownItemsForUpdate(house_hold_data.study_block)"
                 @submit="showModal = false"
        >
          <form @submit.prevent="updateHouseHoldData">
            <vue-tiny-tabs id="mytabs" :anchor="false" :closable="false" :hideTitle="true" class="tinytabs tabs">
              <div id="farmer-info-edit" class="section tab">
                <h4 class="title"><small><b>Farmer Info</b></small></h4>

                <!--STUDY-BLOCK-->
                <b-form-group id="form-study_block-group-edit" label="Study Block:" label-for="form-study_block-input">
                  <ejs-dropdownlist
                      id='dropdownlist'
                      :dataSource='studyBlockDataList'
                      :fields="fields"
                      :v-model="house_hold_data.study_block"
                      placeholder='Select a study block'
                  ></ejs-dropdownlist>
                </b-form-group>

                <!--FARMER-->
                <b-form-group id="form-farmer-group-edit" label="Farmer Name:" label-for="form-farmer-input">
                  <b-form-input id="form-farmer-input" v-model="house_hold_data.farmer"
                                placeholder="Enter Farmer Name" required type="text"></b-form-input>
                </b-form-group>
              </div>

              <div id="cattle-info-edit" class="section tab">
                <h4 class="title"><small><b>Cattle Info</b></small></h4>
                <!--CATTLE_ID-->
                <b-form-group id="form-cattle_id-group-edit" label="Cattle ID:" label-for="form-cattle_id-input">
                  <b-form-input id="form-cattle_id-input" v-model="house_hold_data.cattle_id"
                                placeholder="Enter Cattle ID" required type="text"></b-form-input>
                </b-form-group>

                <!--CATTLE NAME-->
                <b-form-group id="form-cattle_name-group-edit" label="Cattle Name:" label-for="form-cattle_name-input">
                  <b-form-input id="form-cattle_name-input" v-model="house_hold_data.cattle_name"
                                placeholder="Enter Cattle Name" required type="text"></b-form-input>
                </b-form-group>

                <!--CATTLE COLOR-->
                <b-form-group id="form-cattle-color-group-edit" label="Cattle Color:"
                              label-for="form-cattle-color-input">
                  <b-form-input id="form-cattle-color-input" v-model="house_hold_data.cattle_color"
                                placeholder="Enter Cattle Name" required type="text"></b-form-input>
                </b-form-group>

                <!--CATTLE COLOR-->
                <b-form-group id="form-cattle-collar-group-edit" label="Collar:" label-for="form-cattle-collar-input">
                  <b-form-input id="form-cattle-collar-input" v-model="house_hold_data.collar"
                                placeholder="Enter Collar" required type="text"></b-form-input>
                </b-form-group>

                <!--CATTLE Sex-->
                <div id="cattle-sex-edit">
                  <p>Cattle Sex:</p>
                  <input id="male-edit" v-model="house_hold_data.cattle_sex" type="radio" value="Male">
                  <label for="male-edit">Male</label>
                  <br>
                  <input id="female-edit" v-model="house_hold_data.cattle_sex" type="radio" value="Female">
                  <label for="female-edit">Female</label>
                  <br>
                </div>
              </div>

              <div id="health-info-edit" class="section tab">
                <h4 class="title"><small><b>Health Info</b></small></h4>

                <!--CATTLE PCV-->
                <b-form-group id="form-pcv-group-edit" label="PCV(Packed Cell Volume):" label-for="form-pcv-input">
                  <b-form-input id="form-pcv-input" v-model="house_hold_data.pcv"
                                placeholder="Enter PCV" required type="text"></b-form-input>
                </b-form-group>

                <!--CATTLE Diagnosis-->
                <b-form-group id="form-diagnosis-group-edit" label="Diagnosis:" label-for="form-diagnosis-input">
                  <b-form-input id="form-diagnosis-input" v-model="house_hold_data.diagnosis"
                                placeholder="Enter Diagnosis" required type="text"></b-form-input>
                </b-form-group>

                <!--CATTLE Treatment-->
                <b-form-group id="form-treatment-group-edit" label="Treatment:" label-for="form-treatment-input">
                  <b-form-input id="form-treatment-input" v-model="house_hold_data.treatment"
                                placeholder="Enter Treatment" required type="text"></b-form-input>
                </b-form-group>

                <!--CATTLE CC/ML-->
                <b-form-group id="form-cc/ml-group-edit" label="Dosage:" label-for="form-cc/ml-input">
                  <b-form-input id="form-cc/ml-input" v-model="house_hold_data.cc"
                                placeholder="Enter cc/ml" required type="number"></b-form-input>
                </b-form-group>

                <!--CATTLE Notes-->
                <b-form-group id="form-notes-group-edit" label="Notes:" label-for="form-notes-input">
                  <b-form-textarea id="form-notes-input" v-model="house_hold_data.notes"
                                   placeholder="Enter Notes" required type="text"></b-form-textarea>
                </b-form-group>
              </div>
            </vue-tiny-tabs>
          </form>
        </b-modal>
      </div>

      <b-button v-if="isAuth" v-b-modal.modal-house_hold_data class="float_btn" style="border-radius: 50%"
                variant="primary">
        <span>Add House Data</span> <i class="fas fa-plus-circle menu_icon"></i>
      </b-button>


      <div style="margin: auto;">
        <loading-progress
            :hide-background="hideBackground" :indeterminate="indeterminate" :progress="progressPath" :size="size"
            fillDuration="2" rotate rotationDuration="1"/>
      </div>
    </div>
  </div>
</template>

<script>
import {
  extractApiData,
  getItemDataList,
  getSelectedItemCode,
  handleError,
  isResearcher,
  pageStartLoader,
  secureStoreGetAuthString,
  showFlashMessage
} from "@/utils/util_functions";
import {house_hold_data_resource, study_block_resource} from "@/utils/api_paths";
import axios from "axios";
import TopNav from "@/components/TopNav";
import VueTinyTabs from 'vue-tiny-tabs'

export default {
  name: "HouseHoldData",
  data() {
    return {
      page_title: "HouseHoldData",
      response: [],
      house_hold_data: {
        farmer: '', cattle_id: '', cattle_name: '', cattle_color: '', cc: '', notes: '',
        cattle_sex: '', collar: '', pcv: '', diagnosis: '', treatment: '', study_block: ''
      },

      // variable to check user status and role
      isAuth: null,

      time: 2000, // loader-time

      // progressPath
      indeterminate: true, hideBackground: true, progressPath: 5, size: 180,

      studyBlockDataList: [],
      fields: {text: '', value: ''},

      // values for data modification
      old_code: null, showModal: true, isEditing: false,
    };
  },
  methods: {
    // Util Functions
    clearForm() {
      this.house_hold_data.farmer = '';
      this.house_hold_data.cattle_id = '';
      this.house_hold_data.cattle_name = '';
      this.house_hold_data.cattle_color = '';
      this.house_hold_data.cattle_sex = '';
      this.house_hold_data.collar = '';
      this.house_hold_data.pcv = '';
      this.house_hold_data.diagnosis = '';
      this.house_hold_data.treatment = '';
      this.house_hold_data.cc = '';
      this.house_hold_data.notes = '';
      this.house_hold_data.study_block = '';
      this.isEditing = false;
      this.studyBlockDataList = [];
      this.onLoadPage();
    },

    fillFormForUpdate(data) {
      this.$log.info('data for form is ', data)
      this.house_hold_data.farmer = data.farmer;
      this.house_hold_data.cattle_id = data.cattle_id;
      this.house_hold_data.cattle_name = data.cattle_name;
      this.house_hold_data.cattle_color = data.cattle_color;
      this.house_hold_data.cattle_sex = data.cattle_sex;
      this.house_hold_data.collar = data.collar;
      this.house_hold_data.pcv = data.pcv;
      this.house_hold_data.diagnosis = data.diagnosis;
      this.house_hold_data.treatment = data.treatment;
      this.house_hold_data.cc = data.cc;
      this.house_hold_data.notes = data.notes;
      this.house_hold_data.study_block = data['study_block.name'];
      this.old_code = data.code;
      this.isEditing = true;
      this.showModal = true;
    },

    onLoadPage() {
      getItemDataList(study_block_resource).then(data => {
        let study_blockList = extractApiData(data);

        // update local variables with data from API
        this.fields = study_blockList['fields'];
        for (let i = 0; i < study_blockList.items.length; i++) {
          this.studyBlockDataList.push({
            'Code': study_blockList.items[i].Code,
            'Name': study_blockList.items[i].Name,
          });
        }
      })
      this.getHouseHoldData();
    },

    selectDropDownItemsForUpdate(study_block) {
      console.log("Study block:" + study_block)
      let elementTheme = document.getElementById("dropdownlist");
      elementTheme.value = study_block;
    },
    // stop&hide progressPath
    haltProgressPath(cont = false, path = 0, size = 0) {
      this.indeterminate = cont;
      this.progressPath = path;
      this.size = size
    },

    // Functions to interact with api
    getHouseHoldData() {
      this.isAuth = isResearcher();
      axios.get(house_hold_data_resource)
          .then((res) => {
            setTimeout(() => {
                  this.haltProgressPath();
                  this.response = res.data;
                }
                , this.time)
          }).catch((error) => {
        // eslint-disable-next-line
        this.$log.error(error);
      });
    },

    createHouseHoldData: function () {
      this.house_hold_data.study_block = getSelectedItemCode('dropdownlist', this.studyBlockDataList);
      let loader = pageStartLoader(this)

      axios.post(house_hold_data_resource, {
        farmer: this.house_hold_data.farmer, cattle_id: this.house_hold_data.cattle_id,
        cattle_name: this.house_hold_data.cattle_name, cattle_color: this.house_hold_data.cattle_color,
        cattle_sex: this.house_hold_data.cattle_sex, collar: this.house_hold_data.collar,
        pcv: this.house_hold_data.pcv, diagnosis: this.house_hold_data.diagnosis,
        treatment: this.house_hold_data.treatment, cc: this.house_hold_data.cc,
        notes: this.house_hold_data.notes, study_block: this.house_hold_data.study_block,
      }, {
        headers:
            {
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          loader.hide();
          this.getHouseHoldData();
          showFlashMessage(this, 'success', response.data['message'], '');
        }, this.time)
      }).catch((error) => {
        this.$log.error(error);
        loader.hide();
        if (error.response) {
          handleError(this, error)
        }
      });
      this.clearForm();
    },

    updateHouseHoldData: function (code) {
      this.house_hold_data.study_block = getSelectedItemCode('dropdownlist', this.studyBlockDataList);
      let loader = pageStartLoader(this)

      axios.put(house_hold_data_resource, {
        farmer: this.house_hold_data.farmer, cattle_id: this.house_hold_data.cattle_id,
        cattle_name: this.house_hold_data.cattle_name, cattle_color: this.house_hold_data.cattle_color,
        cattle_sex: this.house_hold_data.cattle_sex, collar: this.house_hold_data.collar,
        pcv: this.house_hold_data.pcv, diagnosis: this.house_hold_data.diagnosis,
        treatment: this.house_hold_data.treatment, cc: this.house_hold_data.cc,
        notes: this.house_hold_data.notes, study_block: this.house_hold_data.study_block,
      }, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          loader.hide();
          this.getHouseHoldData();
          showFlashMessage(this, 'success', response.data['message'], '');
        }, this.time)
      }).catch((error) => {
        loader.hide();
        this.$log.error(error);
        if (error.response) { handleError(this, error) }
      });
      this.clearForm();
    },

    deleteHouseHoldData: function (code) {
      let loader = pageStartLoader(this)
      axios.delete(house_hold_data_resource, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          loader.hide()
          showFlashMessage(this, 'success', response.data['message'], '');
          this.getHouseHoldData();
        }, this.time)
      }).catch((error) => {
        this.$log.error(error);
        loader.hide();
        if (error.response) { handleError(this, error) }
      });
    },
  },
  created() { this.onLoadPage(); },
  components: {TopNav, VueTinyTabs}
}
</script>