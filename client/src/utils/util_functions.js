// flash messages

import axios from "axios";

export function showFlashMessage(self, status, title, message) {
    self.flashMessage.show({
        status: status,
        title: title, message: message
    });
}

export function countDownTimer(self, countDown) {
    if (countDown > 0) {
        console.log("CountDown: ", countDown);
        setTimeout(() => {
            self.$log.info("**** Timer in setTimeout function ... **** --> ", countDown);
            countDown -= 1;
            countDownTimer(self, countDown);
            self.$log.info("**** Timer almost out of setTimeout function ... **** --> ", countDown);
        }, 1000)
    } else if (countDown === 0) {
        self.$log.info("**** Timer out ... ****");
        self.$router.push({path: '/home'});
    }
    return countDown;
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

export function selectItemForUpdate(elementId, item) {
    // set dropdownItem to the selected item
    var element = document.getElementById(elementId);
    element.value = item;
}