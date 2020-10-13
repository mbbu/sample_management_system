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
                        placeholder='Select a lab' :change='getFreezersOfSelectedLab'
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


    <!-- SLOT -->
    <div class="form-group">
      <ejs-dropdownlist id='slot' ref='slot' :dataSource='slotData' :fields='slotFields' placeholder='Select a slot'></ejs-dropdownlist>
    </div>

      </div>
    </div>
</template>
<script>
import {extractApiData, getItemDataList, getSelectedBoxSetTextFieldValue} from "@/utils/util_functions";
import {box_resource, freezer_resource, lab_resource} from "@/utils/api_paths";
import EventBus from "@/components/EventBus";

export default {
  data () {
    return {
      loc: {
        lab: '', freezer: '', chamber: '',
        rack: '', tray: '', box: '', slot: '',
      },

      // disabled fields
      freezerEnabled: false,
      boxEnabled: false,

      // data lists
      labData: [],
      freezerData: [],
      boxData: [],
      slotData: [],

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
          // enable freezer fields
          this.freezerEnabled = true

          getItemDataList(freezer_resource, {

          }).then(data => {
            let freezerList = extractApiData(data);
  
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
          // enable box fields
          this.boxEnabled = true

          getItemDataList(box_resource, {

          }).then(data => {
            let boxList = extractApiData(data);

            // update local variables with data from API
            this.boxFields = boxList['fields'];
            for (let i = 0; i < boxList.items.length; i++) {
              this.boxData.push({
                'Code': boxList.items[i].Code,
                'Name': boxList.items[i].Name,
              });
            }
          })
      },

      fillFormFieldsDependentOnBox() {
          let dropdownSelection = getSelectedBoxSetTextFieldValue("box-dropdownlist", this.boxDataList);
          this.loc.box = dropdownSelection.boxCode;

          // SET FIELDS TEXT
          this.loc.tray = dropdownSelection.tray;
          this.loc.rack = dropdownSelection.rack;
          this.loc.chamber = dropdownSelection.chamber;
      },
    }
}
</script>