class injectHtml{
    constructor (parentDiv,title,reset){
        this.parentDiv = parentDiv;
        this.title = title;
        this.reset = reset;
    }

    resetinnerHtml(){
        if (this.reset == true){
            this.parentDiv.innerHTML = "";
        }
    }


    injectTitle(){
        let titleDiv = document.createElement("div");

        let injectedTitle = document.createElement("h5");
        injectedTitle.innerText = this.title;

        titleDiv.appendChild(injectedTitle);
        this.parentDiv.appendChild(titleDiv);
    }

    injectCheckBoxes(checkNames,commonName, preSelected){
        this.resetinnerHtml();
        try{
            if (checkNames.length > 0){
                this.injectTitle();

                let checksDiv = document.createElement("div");
                checksDiv.className = "checkboxes"

                let columnCount = 0;
                checkNames.forEach((checkName)=>{
                    let checkValue;
                    if (typeof(checkName) === "string"){
                        checkValue = checkName;
                    }
                    else{
                        checkValue = checkName.value;
                    }
                    if (checkValue){
                        columnCount ++;
                        let checkDiv = document.createElement("div");
                        checkDiv.className = "check";

                        let columnLabel = document.createElement("label");
                        columnLabel.className = "form-check-label"; 
                        columnLabel.innerText = `${columnCount}. ${checkValue}`;

                        let columnInput = document.createElement("input");
                        columnInput.className = "form-check-input";
                        columnInput.type = "checkbox";
                        columnInput.name = commonName; 
                        columnInput.value = checkValue;

                        if (preSelected && preSelected.includes(checkValue)){
                            columnInput.checked = true;
                        }

                        checkDiv.appendChild(columnLabel);
                        checkDiv.appendChild(columnInput);

                        checksDiv.appendChild(checkDiv);
                        this.parentDiv.appendChild(checksDiv);
                    }
                });
            }
            
        } catch(error){
            console.error(error);
        }
    }

    injectSelectTag(id,selectName,options){
        this.resetinnerHtml();
        try{
            let selectDiv = document.createElement("div");
            selectDiv.id = id;

            /* Title for index*/
            let injectedTitle = document.createElement("h5");
            injectedTitle.innerText = title;
            selectDiv.appendChild(injectedTitle);

            let injectedSelect = document.createElement("select");
            injectedSelect.name = selectName;
            injectedSelect.className = "form-select";
            options.forEach(opt =>{
                let injectedOptionTag = document.createElement("option");
                injectedOptionTag.name = opt; injectedOptionTag.value = opt;
                injectedOptionTag.innerText = opt;
                injectedSelect.appendChild(injectedOptionTag);
            });
            selectDiv.appendChild(injectedSelect);

            this.parentDiv.appendChild(selectDiv);
        } catch(error){
            console.error(error);
        }
    }
}

async function getSelectedReportColumns(endpoint,filtering_field,filtering_value){
    let preselected;
    try{
        let reportProfiles = await apiAccess(apiUrl = baseUrl + endpoint);
        for (const profile of reportProfiles){
            if (profile[filtering_field] == filtering_value){
                preselected = profile;
                break;
            }
        }
        return preselected;
    } catch (error){
        console.error(error);
    }
}

const baseUrl = '/api/router/';
async function apiAccess(apiUrl){
    try{
        const response = await fetch(apiUrl);
        if (!response.ok){
            throw new Error(`Response : ${response.status}`);
        }
        const result = await response.json();
        return result;
    }
    catch(error){
        console.error(error.message);
    }
}

async function injectReportColumns(){
    let columnDiv = document.getElementById("reportColumns");
    let injector = new injectHtml(
        parentDiv=columnDiv, title = "Select Report Columns", reset = true
    );
    try{
        const reportType = document.getElementById("reportType");
        let reportProfile = await getSelectedReportColumns(
            endpoint="reports",
            filtering_field="main_section",filtering_value=reportType.value
        );
        injector.injectCheckBoxes(
            checkNames = reportProfile["columns"].split(","),
            commonName="report_column",
            preSelected = reportProfile["selected_columns"]
        );
        
    }catch(error){
        console.error(error);
    }
}

function findSelectedCheckBoxes(checkBoxes){
    let selected = [];
    try{
        Array.from(checkBoxes).forEach(checkBox =>{
            if (checkBox.checked == true){
                selected.push(checkBox);
            }
        });
        return selected;
    }catch(error){
        console.error(error)
    }
}

async function configureAdditionalReportSheet(){
    let checkboxes = document.getElementsByName("additional_sheet");
    let sheetConfigDiv = document.getElementById("sheetConfig");
    let reportColumns = document.getElementsByName("report_column");

    let reportType = document.getElementById("reportType");
    let preselection = await getSelectedReportColumns(
        endpoint="reports",
        filtering_field = "main_section", filtering_value = reportType.value
    );
    try{
        checkboxes.forEach(box => {
            box.addEventListener("change",() => {
                let sheetDiv = document.createElement("div");
                sheetDiv.id = box.id;

                let injector = new injectHtml(
                    parentDiv = sheetDiv,title = "select Column",
                    reset = true
                );
                if (box.checked){
                    title = "Index"
                    if (box.value == "pivot_table"){
                        injector.injectSelectTag(
                            id=box.id, selectName = "pivot_index",
                            options = preselection["pivot_columns"].split(",")
                        );
                        
                        let injectedSelect = document.getElementById(box.id);
                        console.log(injectedSelect);

                        injector.reset = false;
                        injector.title = "select Pivot Columns"

                        preselectedColumns = preselection["pivot_columns"].split(",");
                        injector.injectCheckBoxes(
                            checkNames = preselection["selected_columns"].split(","),
                            commonName = box.id,
                            preSelected = preselectedColumns
                        );
                        console.log(preselectedColumns[1]);
                    }
                    sheetConfigDiv.appendChild(sheetDiv);
                }else {
                    sheetConfigDiv.innerHTML = "";
                }
            });
        });
    } catch(error){
        console.error(error);
    }
}


configureAdditionalReportSheet()
/* Events configuration */


document.addEventListener("DOMContentLoaded",async ()=>{
    injectReportColumns();

    let checkboxes = document.getElementsByName("additional_sheet");
    checkboxes.forEach(box => {
        box.checked = false;
    });
});

reportType.addEventListener("change",async ()=>{
    injectReportColumns();
});