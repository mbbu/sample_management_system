// flash messages

import axios from "axios";

export function showFlashMessage(status, title, message) {
    this.flashMessage.show({
        status: status,
        title: title, message: message
    });
}

// DropDownList Functions
export function getItemDataList(resource, itemDataList) {
    axios.get(resource)
        .then((res) => {
            this.$log.info("Response: " + res.status + " " + res.data['message']);
            for (var lab_item = 0; lab_item < res.data.message.length; lab_item++) {
                itemDataList.push({
                    'Code': res.data.message[lab_item].code,
                    'Name': res.data.message[lab_item].name
                });
                this.fields = {text: 'Name', value: 'Code'};
            }
        })
        .catch((error) => {
            // eslint-disable-next-line
            this.$log.error(error);
        });
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