<template>
  <div id="app">
    <div id='container'>
      
      <!-- START ROW 1 -->
      <div class="row">
        <!-- LAB -->
        <div class="col">
          <div class="form-group">
            <b-form-group id="lab" label="Lab:" label-for="form-lab-input">
                <ejs-dropdownlist
                        id="lab-dropdownlist"
                        :dataSource='labData' :fields="labFields" :v-model="loc.lab"
                        placeholder='Select a lab' @change='getFreezersOfSelectedLab'
                ></ejs-dropdownlist>
            </b-form-group>
          </div>
      </div>

      <!-- FREEZER -->
      <div class="col">
        <div class="form-group">
          <b-form-group id="freezer" label="Freezer:" label-for="form-freezer-input">
            <ejs-dropdownlist
                      id='freezer-dropdownlist' ref='freezer'
                      :dataSource='freezerData' :fields='freezerFields'
                      :enabled='freezerEnabled' :change='getBoxesInSelectedFreezer'
                      :v-model="loc.freezer" placeholder='Select a freezer'
            ></ejs-dropdownlist>
          </b-form-group>
        </div>
      </div>

      <!-- BOX -->
      <div class="col form-group">
<!--      USEFUL 4 UPDATE
  :value="selectDropDownItemForUpdate('box-dropdownlist', sample.box, boxDataList)"
-->
        <b-form-group id="box" label="Box:" label-for="form-box-input">
          <ejs-dropdownlist
              id='box-dropdownlist' ref='box'
              :dataSource='boxData' :enabled='boxEnabled' :fields='boxFields'
              :v-model="loc.box" placeholder='Select a box' @change="fillFormFieldsDependentOnBox"
          ></ejs-dropdownlist>
        </b-form-group>
      </div>
    </div>
    <!-- END ROW 1 -->


    <!--DRAWING BOX SLOTS-->
      <table id="slots" class="grid" style="--cols:0;">
        <tr :key="x" v-for="x in this.loc.slots.length">
          <td>
            <input type="hidden">
            <div class="cell"></div>
          </td>
        </tr>
      </table>
    <!-- END SLOTS -->

    <!-- START ROW 2 -->
    <div class="row">
      <!-- CHAMBER-->
      <div class="col">
          <div class="form-group">
              <label for="chamber"> Chamber: </label>
              <input class="form-control" disabled="disabled" id="chamber"
                     placeholder="Chamber" required
                     type="text" v-model="loc.chamber"/>
          </div>
      </div>

      <!-- RACK -->
      <div class="col">
          <div class="form-group">
              <label for="rack">Rack: </label>
              <input class="form-control" disabled="disabled" id="rack"
                     placeholder="Rack Number" required
                     type="text" v-model="loc.rack"/>
          </div>
      </div>

      <!-- TRAY -->
      <div class="col">
          <div class="form-group">
              <label for="tray">Tray: </label>
              <input class="form-control" disabled="disabled" id="tray" placeholder="Tray Number"
                     required type="text" v-model="loc.tray"/>
          </div>
      </div>
    </div>
    <!-- END ROW 2 -->

      </div>
    </div>
</template>
<script>
import {
  extractApiData, extractBoxData, extractFreezerData,
  getItemDataList, getSelectedBoxSetTextFieldValue, getSelectedItemCode
} from "@/utils/util_functions";
import {box_resource, freezer_resource, lab_resource} from "@/utils/api_paths";
import EventBus from "@/components/EventBus";

export default {
  data () {
    return {
      loc: {
        lab: '', freezer: '', chamber: '',
        rack: '', tray: '', box: '', slots: '',
      },

      // disabled fields
      freezerEnabled: false,
      boxEnabled: false,

      // data lists
      labData: [],
      freezerData: [],
      boxData: [],
      slotData: [],

      // slots data
      rows: null,
      cols: null,

      // fields
      labFields: { value: '', text: '' },
      freezerFields: { value: '', text: '' },
      boxFields: { value: '', text: '' },
      slotFields: { value: '', text: '' },
    }
  },

  mounted() {
    EventBus.$on('locationFinder', () => {
      this.getLabList()
    })
  },

  methods: {
      // GET LAB LIST
      getLabList() {
        getItemDataList(lab_resource).then(data => {
          let labList = extractApiData(data);

          // update local variables with data from API
          this.labFields = labList['fields'];
          for (let i = 0; i < labList.items.length; i++) {
            this.labData.push({
              'Code': labList.items[i].Code,
              'Name': labList.items[i].Name,
            });
          }
        })
      },

      getFreezersOfSelectedLab() {
          // set the lab selected
          this.loc.lab = getSelectedItemCode("lab-dropdownlist", this.labData)

          // enable freezer fields
          this.freezerEnabled = true

          // reset list on getting new list
          this.freezerData = []
          this.loc.freezer = ''
          this.boxData = []
          this.loc.box = ''
          this.boxEnabled = false

          getItemDataList(freezer_resource, {
              'q': this.loc.lab
          }).then(data => {
            let freezerList = extractFreezerData(data);

            // update local variables with data from API
            this.freezerFields = freezerList['fields'];
            for (let i = 0; i < freezerList.items.length; i++) {
              this.freezerData.push({
                'Code': freezerList.items[i].Code,
                'Name': freezerList.items[i].Name,
              });
            }
          })
      },

      getBoxesInSelectedFreezer() {
          // set the lab selected
          this.loc.freezer = getSelectedItemCode("freezer-dropdownlist", this.freezerData)

          // enable box fields
          this.boxEnabled = true

          // reset list on getting new list
          this.boxData = []
          this.loc.box = ''

          getItemDataList(box_resource, {
              'q' : this.loc.freezer
          }).then(data => {
            let boxList = extractBoxData(data);

            // update local variables with data from API
            this.boxFields = boxList['fields'];
            for (let i = 0; i < boxList.items.length; i++) {
              this.boxData.push({
                'Code': boxList.items[i].Code,
                'Name': boxList.items[i].Name,
                'Tray': boxList.items[i].Tray,
                'Rack': boxList.items[i].Rack,
                'Chamber': boxList.items[i].Chamber,
                'Slots': boxList.items[i].Slots
              });
            }
          })
      },

      resetBeforeChange(){
          this.rows = '';
          this.cols = '';
          this.loc.box = '';
          this.loc.tray = '';
          this.loc.rack = '';
          this.loc.slots = '';
          this.loc.chamber = '';
          document.getElementById('slots').style.setProperty("--cols", "0");
      },
    
      fillFormFieldsDependentOnBox() {
          this.resetBeforeChange();

          let dropdownSelection = getSelectedBoxSetTextFieldValue("box-dropdownlist", this.boxData);
          this.loc.box = dropdownSelection.boxCode;

          // SET FIELDS TEXT
          this.loc.tray = dropdownSelection.tray;
          this.loc.rack = dropdownSelection.rack;
          this.loc.chamber = dropdownSelection.chamber;
          this.loc.slots = dropdownSelection.slots

          // draw the slots of the selected box.
          // det the dimension of slots i.e rows and cols
          let last_slot = this.loc.slots[this.loc.slots.length - 1]
          this.rows = last_slot.position.row
          this.cols = last_slot.position.col

          let pad = document.getElementById('slots').style.getPropertyValue("--cols");
          document.getElementById('slots').style.setProperty("--cols", parseInt(pad) + this.cols);
      },
  }
}
</script>
