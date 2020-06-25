import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import SecureLS from "secure-ls";
import Vue from "vue";
import axios from "axios";
import {logout_resource} from "./api_paths";

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
* Combined responses for status codes */
export function respondTo401(self) {
    showFlashMessage(self, 'error', "Session Expired", "You need to log in to perform this operation")
    countDownTimer(self, 3, '/login')
}

/*
* Form Util Functions */
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


export function extractProjectData(data) {
    let itemList = [];
    let fields = {text: '', value: ''};
    let resultObject = {items: itemList, fields: fields};

    for (let item = 0; item < data.length; item++) {
        itemList.push({
            'Code': data[item].code,
            'Name': data[item].name + " headed by " + data[item]['lead.first_name'] + " " + data[item]['lead.last_name']
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
            console.log("NOT FOUND")
        }
    }
}

// todo: ideal fn
export function getSelectedItemCode(elementId, itemDataList) {
    let item = document.getElementById(elementId).value;

    for (var i = 0; i < itemDataList.length; i++) {
        if (item === itemDataList[i].Name) {
            return itemDataList[i].Code
        } else {
            console.log("NOT FOUND")
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
            console.log("NOT FOUND")
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
            console.log("NOT FOUND")
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
// todo: redesign secure store.

const ls = new SecureLS({isCompression: false});

Vue.use(Vuex);

const store = new Vuex.Store({
    state: {
        jwtString: "",
        user: {
            email: "",
            firstName: "",
            lastName: "",
            role: ""
        },
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
            value ? (state.jwtString = value) : (state.jwtString = ""),

        userInfo: (state, payload) => {
            return payload ?
                (
                    state.user = {
                        email: payload.email,
                        firstName: payload.firstName,
                        lastName: payload.lastName,
                        role: payload.role,
                    }
                )
                :
                (
                    state.user = {
                        email: "",
                        firstName: "",
                        lastName: "",
                        role: ""
                    }
                )
        },
    }
});

/*
* User Authentication and Identification functions */
export function secureStoreGetString() {
    let jwtString = store.state.jwtString;

    if (jwtString != null) {
        return 'Bearer ' + jwtString;
    } else {
        // ensures server returns 401 rather than 422
        return ""
    }
}

export function secureStoreSetString(jwtString, email, fName, lName, role) {
    store.commit("jwtToken", jwtString);
    store.commit('userInfo', {
        email: email,
        firstName: fName,
        lastName: lName,
        role: role
    });
}

export function secureStoreDeleteString() {
    store.commit("jwtToken", null);
    store.commit('userInfo', null);
}

export function getUserEmail() {
    return store.state.user.email
}

export function getStoredUserDetails() {
    let user = {
        'first_name': null,
        'last_name': null,
        'role': null,
    }

    user.first_name = store.state.user.firstName
    user.last_name = store.state.user.lastName
    user.role = store.state.user.role

    return user
}

export function strongPassword(password1) {
    return (
        /[a-z]/.test(password1) && //checks for a-z
        /[0-9]/.test(password1) && //checks for 0-9
        /\W|_/.test(password1) && //checks for special char
        password1.length >= 6
    );
}

// user status
export function isUserLoggedIn() {
    return store.state.jwtString !== "" || getUserEmail() !== "";
}

export function logOutUser(self) {
    let loader = startLoader(self)
    axios.get(logout_resource, {
        headers:
            {
                Authorization: secureStoreGetString()
            }
    })
        .then((response) => {
            // redirect after successful signUp
            if (response.status === 200) {
                setTimeout(() => {
                    secureStoreDeleteString()
                    loader.hide()
                    showFlashMessage(self, 'success', 'Logged Out', 'Redirecting you to home page ' +
                        countDownTimer(self, 3, '/home') + " seconds");
                }, 2500)
            }
        })
        .catch((error) => {
            console.log(error);
            loader.hide()
            if (error.response) {
                showFlashMessage(self, 'error', error.response.data['message'], '');
            }
        })
}

// accessor for sample code; used when requesting to view detailed sample page
let sampleCode = ""
let sample = []
let updateSample = false;

export function setSampleCode(code) {
    sampleCode = code
}

export function getSampleCode() {
    return sampleCode
}

export function setSampleDetailsForEditing(sampleRes) {
    sample = sampleRes
}

export function getSampleDetailsForEditing() {
    return sample;
}

export function setUpdateSample(updateVal) {
    updateSample = updateVal;
}

export function isUpdate() {
    return updateSample;
}


export function selectDropDownItemForUpdate(elementId, item, itemDataList) {
    // set dropdownItem to the selected item
    let element = document.getElementById(elementId);

    // look up the datalist for a similar name as the value the holder has;
    for (var i = 0; i < itemDataList.length; i++) {
        if (item === itemDataList[i].Name || item === itemDataList[i].Code) {
            // -> assign the code to the itemCode
            item = itemDataList[i].Code

            // -> Update the dropdown element value to have the itemName
            element.value = itemDataList[i].Name
            return item
        } else {
            console.log("NOT FOUND")
        }
    }
}

// DATE FUNCTIONS
export function isRetentionPeriodValid(dbDate) {
    return Date.parse(dbDate) >= Date.now();
}

export function overDueRetentionPeriod(dbDate) {
    let timeDiff = Math.abs(Date.parse(dbDate) - Date.now())
    let oneDay = 1000 * 60 * 60 * 24; //milliseconds

    let totalDays = timeDiff / oneDay; // take out milliseconds and convert to days
    let years = Math.floor(totalDays / 365)
    let months = Math.floor(totalDays % 365 / 30)
    let days = Math.floor(totalDays % 365 % 30)

    let yearsDisplay = years > 0 ? years + (years === 1 ? " year " : " years ") : "";
    let monthsDisplay = months > 0 ? months + (months === 1 ? " month " : " months ") : "";
    let daysDisplay = days > 0 ? days + (days === 1 ? " day" : " days") : "";
    return yearsDisplay + monthsDisplay + daysDisplay;
}

export function getThisYear() {
    return (new Date().getFullYear()).toString()
}

// loader function
export function startLoader(self) {
    return self.$loading.show({
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
}