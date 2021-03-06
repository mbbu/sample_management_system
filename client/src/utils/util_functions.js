import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import SecureLS from "secure-ls";
import Vue from "vue";
import axios from "axios";
import {logout_resource, sample_resource} from "./api_paths";
import EventBus from "../components/EventBus";

self.flashMessage = undefined;


export const SYS_ADMIN = "-1"
export const THEME_ADMIN = "1"
export const RESEARCHER = "2"
export const LAB_ADMIN = "3"

export function showFlashMessage(self, status, title, message) {
    self.flashMessage.show({
        icon: "../assets/logo.png",
        status: status,
        title: title, message: message
    });
}

export function redirectAfterCountDown(self, route, countDown = 5) {
    if (countDown > 0) {
        setTimeout(() => {
            countDown -= 1;
            redirectAfterCountDown(self, route, countDown);
        }, 1000)
        return countDown
    } else if (countDown === 0) {

        // eslint-disable-next-line no-unused-vars
        self.$router.push({path: route}).then(r => { return r});
    }
    return countDown;
}

/*
* Combined responses for status codes */
export function respondTo401(self) {
    showFlashMessage(self, 'error', "Session Expired", "You need to log in to perform this operation")
    secureStoreDeleteUserInfo()
    redirectAfterCountDown(self, '/login')
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
export function getItemDataList(resource, params=null) {
    return axios.get(resource, {
                    params : params
        })
        .then((res) => {
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

    for (let item = 0; item < data.length; item++) {
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

    for (let item = 0; item < data.length; item++) {
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

    for (let item = 0; item < data.length; item++) {
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

    for (let item = 0; item < data.length; item++) {
        itemList.push({
            'Code': data[item].code,
            'Name': data[item].label,
            'Tray': data[item]['tray.number'],
            'Rack': data[item]['tray.rack.number'],
            'Chamber': data[item]['tray.rack.chamber.type'],
            'Slots': data[item].slots
            // 'Freezer': data[item]['tray.rack.chamber.freezer.number'],
            // 'Lab': data[item]['tray.rack.chamber.freezer.lab.name'] + " room " + data[item]['tray.rack.chamber.freezer.lab.room'],
        });
        fields.text = 'Name';
        fields.value = 'Code';
    }
    return resultObject;
}

export function extractLabData(data) {
    let labList = [];
    let fields = {text: '', value: ''};
    let resultObject = {items: labList, fields: fields};

    for (let item = 0; item < data.length; item++) {
        labList.push({
            'Code': data[item].code,
            'Name': data[item].building,
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

    for (let item = 0; item < data.length; item++) {
        itemList.push({
            'Code': data[item].code,
            'Name': "Freezer number(" + data[item].number + ") in " + data[item]['lab.building'] + " room "
                + data[item]['lab.room']
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

    for (let item = 0; item < data.length; item++) {
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

    for (let item = 0; item < data.length; item++) {
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

    for (let item = 0; item < data.length; item++) {
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

    for (let item = 0; item < data.length; item++) {
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

    for (let i = 0; i < itemDataList.length; i++) {
        if (item === itemDataList[i].Name) {
            itemVar = itemDataList[i].Code;
            return itemVar
        }
    }
}

// todo: ideal fn
export function getSelectedItemCode(elementId, itemDataList) {
    let item = document.getElementById(elementId).value;

    for (let i = 0; i < itemDataList.length; i++) {
        if (item === itemDataList[i].Name) {
            return itemDataList[i].Code
        }
    }
}

export function getSelectedItemSetTextFieldValue(itemDataList, itemVar) {
    let element = document.getElementById("dropdownlist");
    let item

    if (element !== null) {
        item = element.value
    }

    for (let i = 0; i < itemDataList.length; i++) {
        if (item === itemDataList[i].Name) {
            itemVar = itemDataList[i].Code;
            let textValue = itemDataList[i].authorName;
            let textCode = itemDataList[i].authorCode
            return {'sampleCode': itemVar, 'authorText': textValue, 'authorCode': textCode}
        }
    }
}

export function getSelectedBoxSetTextFieldValue(elementId, itemDataList) {
    let item = document.getElementById(elementId).value;

    for (let i = 0; i < itemDataList.length; i++) {
        if (item === itemDataList[i].Name) {
            let boxCode = itemDataList[i].Code;
            let trayNum = itemDataList[i].Tray;
            let rackNum = itemDataList[i].Rack;
            let chamberType = itemDataList[i].Chamber;
            let slots = itemDataList[i].Slots;
            return {
                'boxCode': boxCode,
                'tray': trayNum,
                'rack': rackNum,
                'chamber': chamberType,
                'slots': slots,
            }
        }
    }
}

export function selectItemForUpdate(item) {
    // set dropdownItem to the selected item
    let element = document.getElementById("dropdownlist");
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
export function secureStoreGetAuthString() {
    let jwtString = store.state.jwtString;

    if (jwtString != null) {
        return 'Bearer ' + jwtString;
    } else {
        // ensures server returns 401 rather than 422
        return ""
    }
}

export function secureStoreSetUserInfo(jwtString, email, fName, lName, role) {
    store.commit("jwtToken", jwtString);
    store.commit('userInfo', {
        email: email,
        firstName: fName,
        lastName: lName,
        role: role
    });
}

export function secureStoreDeleteUserInfo() {
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

    console.log("User details", user)
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
    return store.state.jwtString !== "";
}

export function getLoggedInUser() {
    let loggedIn = isUserLoggedIn()
    if (loggedIn === true) {
        return getStoredUserDetails()
    }
}

export function logOutUser(self) {
    let loader = startLoader(self)
    axios.get(logout_resource, {
        headers:
            {
                Authorization: secureStoreGetAuthString()
            }
    })
        .then((response) => {
            // redirect after successful signUp
            if (response.status === 200) {
                setTimeout(() => {
                    secureStoreDeleteUserInfo()
                    loader.hide()
                    showFlashMessage(self, 'success', 'Logged Out', 'Redirecting you to home page ' +
                        redirectAfterCountDown(self, '/home') + " seconds");
                }, 2500)
            }
        })
        .catch((error) => {
            loader.hide()
            if (error.response) {
                showFlashMessage(self, 'error', error.response.data['message'], '');
            }
        })
}


// SYSTEM ADMIN FUNCTIONS
export function isAdmin() {
    let userStatus = getLoggedInUser()
    return !!(userStatus && userStatus.role === SYS_ADMIN);
}

// THEME ADMIN FUNCTIONS
export function isThemeAdmin() {
    let userStatus = getLoggedInUser()
    return !!(userStatus && (userStatus.role === SYS_ADMIN || userStatus.role === THEME_ADMIN));
}

export function isResearcher() {
    let userStatus = getLoggedInUser()
    return !!(userStatus && (userStatus.role === SYS_ADMIN || userStatus.role === RESEARCHER));
}

export function isLabAdmin() {
    let userStatus = getLoggedInUser()
    return !!(userStatus && (userStatus.role === SYS_ADMIN || userStatus.role === LAB_ADMIN));
}

// PUBLICATION OWNER FUNCTIONS
export function isPublicationOwner(email) {
    let userEmail = getUserEmail()

    return !!(userEmail && userEmail === email);
}

// SAMPLE OWNER FUNCTIONS
export function isSampleOwner(email) {
    let userEmail = getUserEmail()

    return !!(userEmail && (userEmail === email || isThemeAdmin()));
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

// todo: functions could be modularised
export function viewSample(self, code) {
    // 1st call the setter function to set the code
    setSampleCode(code)
    // redirect to sample view page
    redirectAfterCountDown(self, '/view-sample')
}

let fields = null;
let sampleDataList = []
let payload = {}

export function setSampleDataList() {
    getItemDataList(sample_resource).then(data => {
        let sampleList = extractApiDataForPub(data);

        // update local variables with data from API
        fields = sampleList['fields'];
        for (let i = 0; i < sampleList.items.length; i++) {
            sampleDataList.push({
                'Code': sampleList.items[i].sampleCode,
                'Name': sampleList.items[i].sampleName,
                'authorCode': sampleList.items[i].authorCode,
                'authorName': sampleList.items[i].authorName
            });
        }
        payload.fields = fields
        payload.sampleData = sampleDataList
        EventBus.$emit('sample-data-list', payload)
    })
}

// end of sample util functions

export function selectDropDownItemForUpdate(elementId, item, itemDataList) {
    // set dropdownItem to the selected item
    let element = document.getElementById(elementId);

    // look up the datalist for a similar name as the value the holder has;
    for (let i = 0; i < itemDataList.length; i++) {
        if (item === itemDataList[i].Name || item === itemDataList[i].Code) {
            // -> assign the code to the itemCode
            item = itemDataList[i].Code

            // -> Update the dropdown element value to have the itemName
            element.value = itemDataList[i].Name
            return item
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

// loader function for get
export function pageStartLoader(self) {
    return self.$loading.show({
        isFullPage: false,
        canCancel: false,
        color: '#074880',
        loader: 'spinner',
        width: 128,
        height: 128,
        backgroundColor: '#FAAB2C',
        opacity: 0.7,
        zIndex: 999,
    })
}


// PAGINATION FUNCTIONS
let page_info = {};
let page_array = [];

export function paginate(data) {
    let start, end;

    start = page_info.pageSize * (page_info.pageNumber - 1)
    end = start + page_info.pageSize

    page_array.splice(0, page_array.length);

    if (end > data.length) end = data.length;
    for (let i = start; i < end; i++) {
        page_array.push(data[i])
    }

    return {'arr': page_array, 'pg_len': data.length}
}

EventBus.$on('page-info', (payload) => {
    page_info = payload.pgInfo
    paginate(payload.pgData)
})


// generic function to handle errors on web-server response
export function handleError(self, error, loader){
    self.$log.error(error);
    loader.hide();

    if (error.response){
        if (error.response.status === 304) {
            showFlashMessage(self, 'info', 'Record not modified!', '');
        } else if (error.response.status === 400) {
            showFlashMessage(self, 'error', error.response.data['message'], 'Kindly refill the form');
        } else if (error.response.status === 401) {
            respondTo401(self);
        } else if (error.response.status === 403) {
            showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
        } else if (error.response.status === 404) {
            showFlashMessage(self, 'error', 'Not found', "");
        } else if (error.response.status === 408) {
            redirectAfterCountDown(self, '/forgot')
            return error.response.data.message
        } else if (error.response.status === 409) {
            showFlashMessage(self, 'error', error.response.data['message'], '');
        } else if (error.response.status === 422) {
            showFlashMessage(self, 'error', error.response.data['message'], 'Unable to process request');
        } else if (error.response.status === 500) {
            showFlashMessage(self, 'error', "Fatal Error", 'Admin has been contacted.');
        } else {
            showFlashMessage(self, 'error', error.response.data['message'], '');
        }
    }
}
