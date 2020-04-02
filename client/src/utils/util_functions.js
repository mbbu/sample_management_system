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
            console.log("Response: " + res.status + " " + res.data['message']);
            // extractApiData(res.data.message);
            return res.data.message
            // for (var item = 0; item < res.data.message.length; item++) {
            //     itemList.push({
            //         'Code': res.data.message[item].code,
            //         'Name': res.data.message[item].name
            //     });
            //     // fields = {text: 'Name', value: 'Code'};
            //     fields.text='Name';
            //     fields.value='Code';
            // }
            // console.log("Item list: " , itemList);
            // console.log("Item fields: " , fields);
            // console.log("resultObject before: " , resultObject);
            // console.log("resultObject before fields: " , resultObject.fields);
            // console.log("resultObject before items: " , resultObject.items);

            // resultObject['items'] = itemList;
            // // resultObject['fields'] = fields;
            // console.log("resultObject after: " , resultObject);
            // console.log("resultObject after fields: " , resultObject.fields);
            // console.log("resultObject after items: " , resultObject.items);
            // return resultObject;

        })
        .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
        });
    // console.log("resultObject before: " , resultObject);
    // console.log(resultObject.items);
    // console.log(resultObject.fields);
    // return resultObject;
}

export function extractApiData(data) {
    console.log("extract api data function: ", data);
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
    console.log("resultObject: ", resultObject);
    console.log("resultObject items: ", resultObject.items);
    console.log("resultObject fields: ", resultObject.fields);
    return resultObject;
}

// eslint-disable-next-line no-unused-vars
export function getSelectedItem(elementId, itemDataList, itemVar) {
    let item = document.getElementById(elementId).value;

    for (var i = 0; i < itemDataList.length; i++) {
        this.$log.info("ITEM: " + item + " itemDataList Item: " + itemDataList[i].Name);
        if (item === itemDataList[i].Name) {
            itemVar = itemDataList[i].Code;
        } else {
            this.$log.info("** ITEM NOT FOUND ***")
        }
    }
}

export function selectItemForUpdate(elementId, item) {
    // set dropdownItem to the selected item
    var element = document.getElementById(elementId);
    element.value = item;
}