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
      <div class="row" @mouseover="slotsCreated">
        <div class="col">
          <table id="slots" class="grid" style="--cols:0;">
            <tr :key="i" v-for="(x,i) in this.loc.slots">
              <td>
                <div v-if="x.available === true">
                  <div  ref="cells" class="cell-available" @click="runCellAvailable(x, i)">
                  </div>
                </div>
                <div v-else>
                  <div class="cell-occupied"></div>
                </div>
              </td>
            </tr>
          </table>
        </div>

          <!--LEGEND-->
          <div class="col">
            <ul class="legend">
              <li><em>Key: </em></li>
              <li><span class="available"></span> Slot Available</li>
              <li><span class="occupied"></span> Slot Occupied</li>
              <li><span class="selected"></span> Slot Selected</li>
            </ul>
        </div>
      </div>
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
        rack: '', tray: '', box: '', slots: [],
      },

      // disabled fields
      freezerEnabled: false,
      boxEnabled: false,
      slotEnabled: false,

      // data lists
      labData: [],
      freezerData: [],
      boxData: [],
      selectedSlots: [],

      // slots data
      rows: null,
      cols: null,

      // slotDeselection
      cellPos: [],
      cellData: [],
      availableSlots: [],

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

      slotsCreated(){ return this.$refs.cells },

      resetBeforeChange(){
          this.$log.info('resetBeforeChange called')
          this.rows = '';
          this.cols = '';
          this.loc.box = '';
          this.loc.tray = '';
          this.loc.rack = '';
          this.loc.slots = [];
          this.loc.chamber = '';
          document.getElementById('slots').style.setProperty("--cols", "0");

          // remove selections
          const len = this.selectedSlots.length
          for (let x=0; x < len; x++){
             // capture the code of the element
            if (this.selectedSlots.includes(this.cellData[x].code)){
              this.$log.info('Cell has been found!: ', this.cellData[x], 'at position ', this.cellPos[x])
              this.revertCellSelection(this.cellData[x], this.cellPos[x])
            }
          }

          this.selectedSlots = [] // reset list now!
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

          // get slots that are available
          this.availableSlots = []
          for (let x=0; x < this.loc.slots.length; x++){
            if (this.loc.slots[x].available === true ){
              this.availableSlots.push(this.loc.slots[x])
            }
          }

          let pad = document.getElementById('slots').style.getPropertyValue("--cols");
          document.getElementById('slots').style.setProperty("--cols", parseInt(pad) + this.cols);
      },

      runCellAvailable(cellData, pos){
          // check for the position of this slot in the available slots and assign pos to it
          for (let x=0; x < this.availableSlots.length; x++) {
            if (this.availableSlots[x].code === cellData.code ) {
              pos = x;
              this.cellPos.push(pos); this.cellData.push(cellData); // update relevant lists
            }
          }

          // capture the code of the element
          if (this.selectedSlots.includes(cellData.code)){
            this.revertCellSelection(cellData, pos)
          } else{
            // add to list
            this.selectedSlots.push(cellData.code)

            // update the cell formatting
            this.$refs.cells[pos].style.backgroundColor = 'blue'
            this.$refs.cells[pos].style.border = "1px solid rgba(81, 203, 238, 1)";
            this.$refs.cells[pos].style.boxShadow = "0 0 5px rgba(81, 203, 238, 1)";
          }
      },

    revertCellSelection(cellData, pos){
      // revert the selection; remove from array
      for( let i = 0; i < this.selectedSlots.length; i++)
      {if ( this.selectedSlots[i] === cellData.code) { this.selectedSlots.splice(i, 1); i--; }}

      // revert the cell formatting
      this.$refs.cells[pos].style.backgroundColor = 'green'
      this.$refs.cells[pos].style.border = "none";
      this.$refs.cells[pos].style.boxShadow = "none";
    },
  },
}
</script>
