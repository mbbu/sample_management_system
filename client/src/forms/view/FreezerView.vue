<template>
  <div id="app">
    <div id="container">
      <b-modal id="modal-freezer-view" title="Freezer View" cancel-variant="danger" @ok="save">
        <div class="row">
          <!--CHAMBER-->
          <div class="col form-group">
            <b-form-group id="chamber" label="Chamber:" label-for="form-chamber-input">
              <ejs-dropdownlist
                  id='chamber-dropdownlist' ref='chamber'
                  :dataSource='chamberData' :enabled='chamberEnabled' :fields='chamberFields'
                  :v-model="chamberCode" placeholder='Select a chamber' @change="getChamberRacks"
              ></ejs-dropdownlist>
            </b-form-group>
          </div>

          <!--RACK-->
          <div class="col form-group">
            <b-form-group id="rack" label="Rack:" label-for="form-rack-input">
              <ejs-dropdownlist
                  id='rack-dropdownlist' ref='rack'
                  :dataSource='rackData' :enabled='rackEnabled' :fields='rackFields'
                  placeholder='Select a rack' @change="getTraysInRack"
              ></ejs-dropdownlist>
            </b-form-group>
          </div>
        </div>

        <div class="row">
          <!--TRAY-->
          <div class="col form-group">
            <b-form-group id="tray" label="Tray:" label-for="form-tray-input">
              <ejs-dropdownlist
                  id='tray-dropdownlist' ref='tray'
                  :dataSource='trayData' :enabled='trayEnabled' :fields='trayFields'
                  placeholder='Select a tray' @change="getBoxesInTray"
              ></ejs-dropdownlist>
            </b-form-group>
          </div>

          <!--BOX-->
          <div class="col form-group">
            <b-form-group id="box" label="Box:" label-for="form-box-input">
              <ejs-dropdownlist
                  id='box-dropdownlist' ref='box'
                  :dataSource='boxData' :enabled='boxEnabled' :fields='boxFields'
                  placeholder='Select a box' @change="getSlotsOfBox"
              ></ejs-dropdownlist>
            </b-form-group>
          </div>
      </div>
        <div class="justify-content-center">
          <div v-if="boxCode" class="col justify-content-center">
            <rectangle></rectangle>
          </div>
        </div>
      </b-modal>
    </div>
  </div>
</template>

<script>
import Rectangle from "@/components/Rectangle";
import {extractBoxData, extractChamberData, extractRackData, extractTrayData,
        getItemDataList, getSelectedItemCode} from "@/utils/util_functions";
import {
  box_resource,
  chamber_resource,
  freezer_resource,
  rack_resource,
  tray_resource
} from "@/utils/api_paths";
import EventBus from "@/components/EventBus";

export default {
  name: "FreezerView",

  components: {Rectangle},

  data() {
    return{
      freezerCode: '', chamberCode: '', rackCode: '', trayCode: '', boxCode: '',
      chamberData: [], chamberFields: {text: '', value: ''}, chamberEnabled: true,
      rackData: [], rackFields: {text: '', value: ''}, rackEnabled: false,
      trayData: [], trayFields: {text: '', value: ''}, trayEnabled: false,
      boxData: [], boxFields: {text: '', value: ''}, boxEnabled: false
    }
  },

  mounted() {
    EventBus.$on('freezerSet', freezer=>{
      this.freezerCode = freezer
      this.onLoadPage()
    })
  },

  methods: {
    onLoadPage(){
      // get freezer chamber
      getItemDataList(freezer_resource, {q: this.freezerCode}).then(data => {
        this.resetFields()
        let chamberList = extractChamberData(data);

        // update local variables with data from API
        this.chamberFields = chamberList['fields'];
        for (let i = 0; i < chamberList.items.length; i++) {
          this.chamberData.push({
            'Code': chamberList.items[i].Code,
            'Name': chamberList.items[i].Name,
          });
        }
      })
    },

    resetFields(){
      this.freezerCode= ''; this.chamberCode= ''; this.rackCode= ''; this.trayCode = ''; this.boxCode = '';
      this.chamberData= []; this.chamberFields= {text:'', value:''}; this.chamberEnabled= true;
      this.rackData= []; this.rackFields= {text:'', value:''}; this.rackEnabled= false;
      this.trayData= []; this.trayFields= {text:'', value:''}; this.trayEnabled= false;
      this.boxData= []; this.boxFields= {text:'', value:''}; this.boxEnabled= false
    },
    
    getChamberRacks(){
      // reset some fields
      this.rackData= []; this.trayData= []; this.boxData= [];
      this.chamberCode = getSelectedItemCode('chamber-dropdownlist', this.chamberData)

      // get racks of the selected chamber
      getItemDataList(chamber_resource, {q: this.chamberCode}).then(data => {
        this.rackData = []
        let rackList = extractRackData(data);

        // update local variables with data from API
        this.rackFields = rackList['fields'];
        for (let i = 0; i < rackList.items.length; i++) {
          this.rackData.push({
            'Code': rackList.items[i].Code,
            'Name': rackList.items[i].Name,
          });
        }
        this.rackEnabled = true
      })
    },

    getTraysInRack(){
      this.rackCode = getSelectedItemCode('rack-dropdownlist', this.rackData)

      // get trays of the selected rack
      getItemDataList(rack_resource, {q: this.rackCode}).then(data => {
        this.trayData = []
        let trayList = extractTrayData(data);

        // update local variables with data from API
        this.trayFields = trayList['fields'];
        for (let i = 0; i < trayList.items.length; i++) {
          this.trayData.push({
            'Code': trayList.items[i].Code,
            'Name': trayList.items[i].Name,
          });
        }
        this.trayEnabled = true
      })
    },

    getBoxesInTray(){
      this.trayCode = getSelectedItemCode('tray-dropdownlist', this.trayData)

      // get trays of the selected rack
      getItemDataList(tray_resource, {q: this.trayCode}).then(data => {
        this.boxData = []
        let boxList = extractBoxData(data);

        // update local variables with data from API
        this.boxFields = boxList['fields'];
        for (let i = 0; i < boxList.items.length; i++) {
          this.boxData.push({
            'Code': boxList.items[i].Code,
            'Name': boxList.items[i].Name,
          });
        }
        this.boxEnabled = true
      })
    },

    getSlotsOfBox(){
      this.boxCode = getSelectedItemCode('box-dropdownlist', this.boxData)

      // get trays of the selected rack
      getItemDataList(box_resource, {q: this.boxCode}).then(data => {
        EventBus.$emit('slots-fetched', data)
      })
    },

    save(){EventBus.$emit('update-slots')},
  },
}
</script>
