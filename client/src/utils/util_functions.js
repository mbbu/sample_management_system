import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import SecureLS from "secure-ls";
import Vue from "vue";
import axios from "axios";

export function showFlashMessage(self, status, title, message) {
    self.flashMessage.show({
        status: status,
        title: title, message: message
    });
}

export function countDownTimer(self, countDown, route) {
    if (countDown > 0) {
        setTimeout(() => {
            countDown -= 1;
            countDownTimer(self, countDown, route);
        }, 1000)
    } else if (countDown === 0) {
        self.$log.info("**** Timer out ... ****");
        self.$log.info("ROUTE PASSED" + route)
        self.$router.push({path: route});
    }
    return countDown;
}

/*
* Form Util Functions */
export function clearForm(form) {
    form = {}
    return form
}

export function viewPassword() {
    let passwordInput = document.getElementById('password');
    let pwdEyeIcon = document.getElementById('view-pwd');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        pwdEyeIcon.className = 'fa fa-eye-slash';
    } else {
        passwordInput.type = 'password';
        pwdEyeIcon.className = 'fa fa-eye';
    }
}

// DropDownList Functions
// eslint-disable-next-line no-unused-vars
export function getItemDataList(resource) {
    return axios.get(resource)
        .then((res) => {
            console.log("Response: " + res.status);
            // return a promise to be evaluated ...
            return res.data.message
        })
        .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
        });
}

export function extractApiData(data) {
    let itemList = [];
    let fields = {text: '', value: ''};
    let resultObject = {items: itemList, fields: fields};

    for (var item = 0; item < data.length; item++) {
        itemList.push({
            'Code': data[item].code,
            'Name': data[item].name
        });
        fields.text = 'Name';
        fields.value = 'Code';
    }
    return resultObject;
}

export function extractQTData(data) {
    let itemList = [];
    let fields = {text: '', value: ''};
    let resultObject = {items: itemList, fields: fields};

    for (var item = 0; item < data.length; item++) {
        itemList.push({
            'Code': data[item].id,
            'Name': data[item].name
        });
        fields.text = 'Name';
        fields.value = 'Code';
    }
    return resultObject;
}

export function extractUserData(data) {
    let itemList = [];
    let fields = {text: '', value: ''};
    let resultObject = {items: itemList, fields: fields};

    for (var item = 0; item < data.length; item++) {
        itemList.push({
            'Code': data[item].email,
            'Name': data[item].first_name + " " + data[item].last_name
        });
        fields.text = 'Name';
        fields.value = 'Code';
    }
    return resultObject;
}

export function extractBoxData(data) {
    let itemList = [];
    let fields = {text: '', value: ''};
    let resultObject = {items: itemList, fields: fields};

    for (var item = 0; item < data.length; item++) {
        itemList.push({
            'Code': data[item].code,
            'Name': data[item].label,
            'Tray': data[item]['tray.number'],
            'Rack': data[item]['tray.rack.number'],
            'Chamber': data[item]['tray.rack.chamber.type'],
            'Freezer': data[item]['tray.rack.chamber.freezer.number'],
            'Lab': data[item]['tray.rack.chamber.freezer.lab.name'] + " room " + data[item]['tray.rack.chamber.freezer.lab.room'],
        });
        fields.text = 'Name';
        fields.value = 'Code';
    }
    return resultObject;
}

export function extractFreezerData(data) {
    let itemList = [];
    let fields = {text: '', value: ''};
    let resultObject = {items: itemList, fields: fields};

    for (var item = 0; item < data.length; item++) {
        itemList.push({
            'Code': data[item].code,
            'Name': "Freezer number(" + data[item].number + ") in room " + data[item].room
        });
        fields.text = 'Name';
        fields.value = 'Code';
    }
    return resultObject;
}

export function extractChamberData(data) {
    let itemList = [];
    let fields = {text: '', value: ''};
    let resultObject = {items: itemList, fields: fields};

    for (var item = 0; item < data.length; item++) {
        itemList.push({
            'Code': data[item].code,
            'Name': data[item].type
        });
        fields.text = 'Name';
        fields.value = 'Code';
    }
    return resultObject;
}

export function extractRackData(data) {
    let itemList = [];
    let fields = {text: '', value: ''};
    let resultObject = {items: itemList, fields: fields};

    for (var item = 0; item < data.length; item++) {
        itemList.push({
            'Code': data[item].code,
            'Name': "Rack number(" + data[item].number + ") in chamber " + data[item]['chamber.type']
        });
        fields.text = 'Name';
        fields.value = 'Code';
    }
    return resultObject;
}

export function extractTrayData(data) {
    let itemList = [];
    let fields = {text: '', value: ''};
    let resultObject = {items: itemList, fields: fields};

    for (var item = 0; item < data.length; item++) {
        itemList.push({
            'Code': data[item].code,
            'Name': "Tray number(" + data[item].number + ") in rack number " + data[item]['rack.number']
        });
        fields.text = 'Name';
        fields.value = 'Code';
    }
    return resultObject;
}

export function extractApiDataForPub(data) {
    let itemList = [];
    let fields = {text: '', value: ''};
    let resultObject = {items: itemList, fields: fields};

    for (var item = 0; item < data.length; item++) {
        itemList.push({
            'sampleCode': data[item].code,
            'sampleName': "Sample under theme: " + data[item]['theme.name'] + " by " + data[item]['user.first_name'],
            'authorCode': data[item]['user.email'],
            'authorName': data[item]['user.first_name'] + " " + data[item]['user.last_name']
        });
        fields.text = 'Name';
        fields.value = 'Code';
    }
    return resultObject;
}

// eslint-disable-next-line no-unused-vars
export function getSelectedItem(itemDataList, itemVar) {
    let item = document.getElementById("dropdownlist").value;

    for (var i = 0; i < itemDataList.length; i++) {
        if (item === itemDataList[i].Name) {
            itemVar = itemDataList[i].Code;
            return itemVar
        } else {
            console.log("** ITEM NOT FOUND ***")
        }
    }
}

export function getSelectedItemCode(elementId, itemDataList) {
    let item = document.getElementById(elementId).value;

    for (var i = 0; i < itemDataList.length; i++) {
        if (item === itemDataList[i].Name) {
            return itemDataList[i].Code
        } else {
            console.log("** ITEM NOT FOUND ***")
        }
    }
}

export function getSelectedItemSetTextFieldValue(itemDataList, itemVar) {
    let item = document.getElementById("dropdownlist").value;
    console.log("Item passed", itemDataList)

    for (var i = 0; i < itemDataList.length; i++) {
        if (item === itemDataList[i].Name) {
            itemVar = itemDataList[i].Code;
            let textValue = itemDataList[i].authorName;
            let textCode = itemDataList[i].authorCode
            return {'sampleCode': itemVar, 'authorText': textValue, 'authorCode': textCode}
        } else {
            console.log("** ITEM NOT FOUND ***")
        }
    }
}

export function getSelectedBoxSetTextFieldValue(elementId, itemDataList) {
    let item = document.getElementById(elementId).value;

    for (var i = 0; i < itemDataList.length; i++) {
        if (item === itemDataList[i].Name) {
            let boxCode = itemDataList[i].Code;
            let trayNum = itemDataList[i].Tray;
            let rackNum = itemDataList[i].Rack;
            let chamberType = itemDataList[i].Chamber;
            let freezerNum = itemDataList[i].Freezer;
            let lab = itemDataList[i].Lab;
            return {
                'boxCode': boxCode,
                'tray': trayNum,
                'rack': rackNum,
                'chamber': chamberType,
                'freezer': freezerNum,
                'lab': lab
            }
        } else {
            console.log("** ITEM NOT FOUND ***")
        }
    }
}

export function selectItemForUpdate(item) {
    // set dropdownItem to the selected item
    var element = document.getElementById("dropdownlist");
    element.value = item;
}

/*
* Set secure storage for jwt tokens */

const ls = new SecureLS({isCompression: false});

Vue.use(Vuex);

const store = new Vuex.Store({
    state: {
        string: ""
    },
    plugins: [
        createPersistedState({
            storage: {
                getItem: key => ls.get(key),
                setItem: (key, value) => ls.set(key, value),
                removeItem: key => ls.remove(key)
            }
        })
    ],
    mutations: {
        jwtToken: (state, value) =>
            value ? (state.string = value) : (state.string = "")
    }
});

export function secureStoreGetString() {
    let jwtString = store.state.string;

    let tokenPrefix = 'Bearer ';
    return tokenPrefix + jwtString;
}

export function secureStoreSetString(string) {
    store.commit("jwtToken", string);
}

export function secureStoreDeleteString() {
    store.commit("jwtToken");
}
