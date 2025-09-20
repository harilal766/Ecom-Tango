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

function injectCheckBoxes(checkNames, parentDiv, commonName){
    try{
        /* 
        inject a div for each checkbox, 
        the checkbox and its label should be inside it
        */
        if (checkNames.length > 0){
            let columnCount = 0;
            checkNames.forEach((checkName)=>{
                columnCount ++;
                let checkDiv = document.createElement("div");
                checkDiv.className = "check";

                let columnLabel = document.createElement("label");
                columnLabel.className = "form-check-label"; 
                columnLabel.innerText = `${columnCount}. ${checkName.value}`;

                let columnInput = document.createElement("input");
                columnInput.className = "form-check-input";
                columnInput.type = "checkbox";
                columnInput.name = commonName; 
                columnInput.value = checkName.value;

                checkDiv.appendChild(columnLabel);
                checkDiv.appendChild(columnInput);

                parentDiv.appendChild(checkDiv);
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
        if (columns.length > 0){
            let columnCount = 0;
            columns.forEach((column) =>{
                columnCount ++;

                let checkDiv = document.createElement("div");
                checkDiv.className = "check";

                let columnLabel = document.createElement("label");
                columnLabel.className = "form-check-label"; 
                columnLabel.innerText = `${columnCount}. ${column}`;

                let columnInput = document.createElement("input");
                columnInput.className = "form-check-input";
                columnInput.type = "checkbox";
                columnInput.name = "report_column"; columnInput.value = column;

                if (selected_columns.includes(column)){
                    columnInput.checked = true;
                }

                checkDiv.appendChild(columnLabel);
                checkDiv.appendChild(columnInput);

                columnDiv.appendChild(checkDiv);
            });
    }
    }catch(error){
        console.error(error);
    }
}

async function additionalSheets(){
    try{
        let pivot = document.getElementById("pivot_table");
        console.log
    }
    catch(error){
        console.error(error);
    }
}



let reportColumns = document.getElementsByName("report_column");
let selectedReportColumns;

let extrasheets = document.getElementsByName("additional_sheet");
let pivotDiv = document.getElementById("pivotColumns");
extrasheets.forEach((sheet)=>{
    sheet.addEventListener("click",()=>{
        console.log(reportColumns);
        injectCheckBoxes(
            checkNames=reportColumns, parentDiv=pivotDiv,commonName="pivot_columns"
        );
    });
});

reportType.addEventListener("change",async ()=>{
    injectReportColumns();
});
document.addEventListener("DOMContentLoaded",async ()=>{
    injectReportColumns();
});