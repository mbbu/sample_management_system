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
                  :title="`Update house_hold_data ${ house_hold_data.name }`" class="border border-info rounded"
                  font-scale="2.0" icon="pencil"
                  variant="info"
                  @mouseover="fillFormForUpdate(house_hold_data)"
              ></b-icon>
              &nbsp;
              <b-icon
                  v-b-tooltip.hover
                  :title="`Delete house_hold_data ${house_hold_data.name}!`"
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
        <b-modal
            id="modal-house_hold_data"
            cancel-variant="danger"
            ok-title="Save"
            title="Add HouseHoldData"
            @hidden="clearForm"
            @ok="createHouseHoldData"
            @submit="clearForm"
        >
          <form @submit.prevent="createHouseHoldData">
            <b-form-group id="form-theme-group" label="Theme:" label-for="form-theme-input">
              <ejs-dropdownlist
                  id='dropdownlist'
                  :dataSource='themeDataList'
                  :fields="fields"
                  :v-model="house_hold_data.theme"
                  placeholder='Select a theme'
              ></ejs-dropdownlist>
            </b-form-group>

            <b-form-group id="form-head-group" label="HouseHoldData Head:" label-for="form-head-input">
              <ejs-dropdownlist
                  id='dropdownlist-head'
                  :dataSource='headDataList'
                  :fields="fields"
                  :v-model="house_hold_data.head"
                  placeholder='Select the house_hold_data head'
              ></ejs-dropdownlist>
            </b-form-group>

            <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model="house_hold_data.code"
                  placeholder="Enter Code"
                  required
                  type="text"
              ></b-form-input>
            </b-form-group>

            <b-form-group id="form-name-group" label="Name:" label-for="form-name-input">
              <b-form-input
                  id="form-name-input"
                  v-model="house_hold_data.name"
                  placeholder="Enter HouseHoldData Name"
                  required
                  type="text">
              </b-form-input>
            </b-form-group>

            <b-form-group id="form-desc-group" label="Description:" label-for="form-desc-input">
              <b-form-textarea
                  id="form-desc-input"
                  v-model="house_hold_data.description"
                  placeholder="Enter Description"
                  required
                  type="text">
              </b-form-textarea>
            </b-form-group>

          </form>
        </b-modal>
      </div>

      <div v-else-if="isEditing">
        <b-modal
            id="modal-house_hold_data-edit"
            cancel-variant="danger"
            ok-title="Update"
            title="Edit HouseHoldData"
            @hidden="clearForm"
            @ok="updateHouseHoldData(old_code)"
            @shown="selectDropDownItemsForUpdate(house_hold_data.study_block)"
            @submit="showModal = false"
        >
          <form @submit.prevent="updateHouseHoldData">
            <b-form-group id="form-theme-group-edit" label="Theme:" label-for="form-theme-input">
              <ejs-dropdownlist
                  id='dropdownlist'
                  :dataSource='themeDataList'
                  :fields="fields"
                  :v-model="house_hold_data.theme"
                  placeholder='Select a theme'
              ></ejs-dropdownlist>
            </b-form-group>

            <b-form-group id="form-head-group-edit" label="HouseHoldData Head:" label-for="form-head-input">
              <ejs-dropdownlist
                  id='dropdownlist-head'
                  :dataSource='headDataList'
                  :fields="fields"
                  :v-model="house_hold_data.head"
                  placeholder='Select the house_hold_data head'
              ></ejs-dropdownlist>
            </b-form-group>

            <b-form-group id="form-code-group-edit" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model="house_hold_data.code"
                  placeholder="Enter Code"
                  required
                  type="text"
              ></b-form-input>
            </b-form-group>

            <b-form-group id="form-name-group-edit" label="Name:" label-for="form-name-input">
              <b-form-input
                  id="form-name-input"
                  v-model="house_hold_data.name"
                  placeholder="Enter HouseHoldData Name"
                  required
                  type="text">
              </b-form-input>
            </b-form-group>

            <b-form-group id="form-desc-group-edit" label="Description:" label-for="form-desc-input">
              <b-form-textarea
                  id="form-desc-input"
                  v-model="house_hold_data.description"
                  placeholder="Enter Description"
                  required
                  type="text">
              </b-form-textarea>
            </b-form-group>
          </form>
        </b-modal>
      </div>

      <b-button v-if="isAuth" v-b-modal.modal-house_hold_data class="float_btn" style="border-radius: 50%"
                variant="primary">
        <span>Add HouseHoldData</span> <i class="fas fa-plus-circle menu_icon"></i>
      </b-button>


      <div style="margin: auto;">
        <loading-progress
            :hide-background="hideBackground"
            :indeterminate="indeterminate"
            :progress="progressPath"
            :size="size"
            fillDuration="2"
            rotate
            rotationDuration="1"
        />
      </div>
    </div>
  </div>
</template>

<script>
import {
  extractApiData,
  getItemDataList,
  getSelectedItem,
  getSelectedItemCode, handleError,
  isResearcher,
  pageStartLoader,
  respondTo401,
  secureStoreGetAuthString,
  showFlashMessage
} from "@/utils/util_functions";
import {house_hold_data_resource, study_block_resource} from "@/utils/api_paths";
import axios from "axios";
import TopNav from "@/components/TopNav";

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
      this.$log.info('data to update is ', data)
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
      this.old_code = data.code;
      this.isEditing = true;
      this.showModal = true;
    },

    onLoadPage() {
      getItemDataList(study_block_resource).then(data => {
        let study_blockList = extractApiData(data);
        this.$log.info("Study block list json: ", JSON.stringify(study_blockList));

        // update local variables with data from API
        this.fields = study_blockList['fields'];
        for (let i = 0; i < study_blockList.items.length; i++) {
          this.studyBlockDataList.push({
            'Code': study_blockList.items[i].Code,
            'Name': study_blockList.items[i].Name,
          });
        }
      })
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
            setTimeout(() => { this.haltProgressPath(); this.response = res.data;}
            , this.time) }).catch((error) => {
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
              loader.hide(); this.getHouseHoldData();
              showFlashMessage(this, 'success', response.data['message'], '');
            }, this.time)
          }).catch((error) => {
            this.$log.error(error); loader.hide();
            if (error.response) { handleError(this, error) }
          });
      this.clearForm();
    },

    updateHouseHoldData: function (code) {
      let self = this;
      this.house_hold_data.theme = getSelectedItem(this.themeDataList, this.house_hold_data.theme);
      this.house_hold_data.head = getSelectedItemCode('dropdownlist-head', this.headDataList);
      let loader = pageStartLoader(this)

      axios.put(house_hold_data_resource, {
        code: this.house_hold_data.code,
        name: this.house_hold_data.name,
        head: this.house_hold_data.head,
        theme: this.house_hold_data.theme,
        description: this.house_hold_data.description,
      }, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      })
          .then((response) => {
            setTimeout(() => {
              loader.hide()
              this.getHouseHoldData();
              showFlashMessage(self, 'success', response.data['message'], '');
              this.clearForm();
            }, this.time)
          })
          .catch((error) => {
            this.clearForm();
            loader.hide();
            this.$log.error(error);
            if (error.response) {
              if (error.response.status === 304) {
                showFlashMessage(self, 'info', 'Record not modified!', '');
              } else if (error.response.status === 401) {
                respondTo401(self);
              } else if (error.response.status === 403) {
                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
              } else {
                showFlashMessage(self, 'error', error.response.data['message'], '');
              }
            }
          });
    },

    deleteHouseHoldData: function (code) {
      let self = this;
      let loader = pageStartLoader(this)
      axios.delete(house_hold_data_resource, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      })
          .then((response) => {
            setTimeout(() => {
              loader.hide()
              this.getHouseHoldData();
              showFlashMessage(self, 'success', response.data['message'], '');
            }, this.time)
          })
          .catch((error) => {
            this.$log.error(error);
            loader.hide();
            if (error.response) {
              if (error.response.status === 401) {
                respondTo401(self);
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
    this.getHouseHoldData();
  },
  components: {TopNav}
}
</script>