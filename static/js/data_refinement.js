class injectHtml{
    constructor (parentDiv,title,reset){
        this.parentDiv = parentDiv;
        this.title = title;
        this.reset = reset;
    }

    resetinnerHtml(){
        if (this.reset == "on"){
            this.parentDiv.innerHTML = "";
        }
    }

    async getPreSelectedData(endpoint = 'reports'){
        try{
            let reportProfiles = await apiAccess(apiUrl = baseUrl + endpoint);
            let columns; let preselectedColumns;
            reportProfiles.forEach((profile) => {
                if (profile["main_section"] === reportType.value){
                    columns = profile["columns"].split(",");
                    preselectedColumns = profile["selected_columns"].split(",");
                }
            });
            return preselectedColumns;
        } catch (error){
            console.error(error);
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

                        parentDiv.appendChild(checkDiv);
                    }
                });
            }
            
        } catch(error){
            console.error(error);
        }
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


const reportType = document.getElementById("reportType");
const dateRangeHtml = document.getElementById("dateRange");
const shipDateHtml = document.getElementById("shipDates")


const reportForm = document.getElementById("reportForm");
const formTitle = document.getElementById("formTitle");
const submitButton = document.getElementById("submitButton");


let columnDiv = document.getElementById("columnCheckBoxes");


async function injectReportColumns(){
    let injector = new injectHtml(
        parentDiv=columnDiv, title = "Select Report Columns", reset = "on"
    );
    try{
        let reportProfiles = await apiAccess(apiUrl = baseUrl + 'reports');
        let columns; let selected_columns; 
        reportProfiles.forEach((profile) => {
            if (profile["main_section"] === reportType.value){
                columns = profile["columns"].split(",");
                selected_columns = profile["selected_columns"].split(",");
            }
        });
        let preselected_fields = injector.getPreSelectedData(endpoint="reports");

        injector.injectCheckBoxes(
            checkNames = columns,commonName="report_column",
            preSelected = selected_columns
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
            console.log(checkBox.checked);
                selected.push(checkBox);
            }
        });
        return selected;
    }catch(error){
        console.error(error)
    }
}

function injectSelectTag(parentDiv,title,id,selectName,options){
    try{
        let selectDiv = document.createElement("div");


        let injectedTitle = document.createElement("h5");
        injectedTitle.innerText = title;

        let injectedSelectTag = document.createElement("select");
        injectedSelectTag.className = "form-select";
        injectSelectTag.id = id; injectedSelectTag.name = selectName;

        options.forEach(option => {
            let injectedOption = document.createElement("option");
            injectedOption.value = option.value;
            injectedOption.innerText = option.value;

            injectedSelectTag.appendChild(injectedOption);
        });

        selectDiv.appendChild(injectedTitle);
        selectDiv.appendChild(injectedSelectTag);

        parentDiv.appendChild(selectDiv);
    } catch(error){
        console.error(error);
    }
}

let reportColumns = document.getElementsByName("report_column");
let pivotDiv = document.getElementById("pivotColumns");

/*
async function additionalReportSheets(){
    let pivotColumns = document.getElementById("pivotColumns");
    let injector = new injectHtml(parentDiv = pivotColumns,title = "Pivot Index",reset = "on");
    try{
        let extrasheets = document.getElementsByName("additional_sheet");
        extrasheets.forEach((sheet)=>{
            sheet.addEventListener("change",(event)=>{
            
            pivotColumns.innerHTML = "";
            if (sheet.checked == true){
                if (sheet.value === "pivot_table"){
                    let selectedReportColumns = findSelectedCheckBoxes(checkBoxes = reportColumns);
                    injectSelectTag(
                        parentDiv=pivotColumns,
                        title="Index",id="pivotIndex",selectName = "pivot_index",
                        options = selectedReportColumns
                    );

                    injector.injectCheckBoxes(
                        checkNames = selectedReportColumns,commonName="pivot_column",
                        preSelected = 0
                    )
                }
            }                
            });
        });
    }
    catch(error){
        console.error(error);
    }
}

*/
reportType.addEventListener("change",async ()=>{
    injectReportColumns();
});

document.addEventListener("DOMContentLoaded",async ()=>{
    injectReportColumns();
});