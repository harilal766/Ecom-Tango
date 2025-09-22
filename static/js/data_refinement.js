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

/*
Types of report filtration needed
    injecting additional option select tags according to the report type

*/
const reportType = document.getElementById("reportType");
const dateRangeHtml = document.getElementById("dateRange");
const shipDateHtml = document.getElementById("shipDates")


/* To make sure only a particular form will be affected */
const reportForm = document.getElementById("reportForm");
const formTitle = document.getElementById("formTitle");
const submitButton = document.getElementById("submitButton");


let columnDiv = document.getElementById("columnCheckBoxes");

function injectReportFilters(){
    
}

function injectCheckBoxes(checkNames, parentDiv, commonName, preSelected,resetting = "off"){
    try{
        if (resetting !== "off"){
            parentDiv.innerHTML = ""
        }
        if (checkNames.length > 0){
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

async function injectReportColumns(){
    try{
        columnDiv.innerHTML = ""; /*resetting report column selector*/
        let profiles = await apiAccess(apiUrl = baseUrl + 'reports');
        let columns; let selected_columns; 
        profiles.forEach((profile) => {
            if (profile["main_section"] === reportType.value){
                columns = profile["columns"].split(",");
                selected_columns = profile["selected_columns"].split(",");
            }
        });
        injectCheckBoxes(
            checkNames = columns, parentDiv = columnDiv,commonName="report_column",
            preSelected = selected_columns,resetting = "on"
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

async function additionalSheets(){
    try{
        let extrasheets = document.getElementsByName("additional_sheet");
        extrasheets.forEach((sheet)=>{
            sheet.addEventListener("change",(event)=>{
            let pivotColumns = document.getElementById("pivotColumns");
            pivotColumns.innerHTML = "";
            if (sheet.checked == true){
                if (sheet.value === "pivot_table"){
                    let selectedReportColumns = findSelectedCheckBoxes(checkBoxes = reportColumns);
                    injectSelectTag(
                        parentDiv=pivotColumns,
                        title="Index",id="pivotIndex",selectName = "pivot_index",
                        options = selectedReportColumns
                    );

                    injectCheckBoxes(
                        checkNames = selectedReportColumns,
                        parentDiv = pivotColumns,
                        commonName = "pivot_column",resetting = "off"
                    );
                }
            }                
            });
        });
    }
    catch(error){
        console.error(error);
    }
}





reportType.addEventListener("change",async ()=>{
    injectReportColumns();
    additionalSheets();
});
document.addEventListener("DOMContentLoaded",async ()=>{
    injectReportColumns();
    additionalSheets();
});