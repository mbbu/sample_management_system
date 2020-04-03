// flash messages

import axios from "axios";

export function showFlashMessage(status, title, message) {
    this.flashMessage.show({
        status: status,
        title: title, message: message
    });
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
    console.log("data received: " + data + "\nresultObject: ", resultObject);
    return resultObject;
}

// eslint-disable-next-line no-unused-vars
export function getSelectedItem(itemDataList, itemVar) {
    let item = document.getElementById("dropdownlist").value;

    for (var i = 0; i < itemDataList.length; i++) {
        console.log("ITEM: " + item + " itemDataList Item: " + itemDataList[i].Name);
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