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
        this.injectTitle();
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

            this.parentDiv.appendChild(selectDiv);
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

async function configureReportFiltration(){
    let columnDiv = document.getElementById("reportColumns");
    let injector = new injectHtml(
        parentDiv=columnDiv, title = "Select Report Columns", reset = true
    );
    try{
        let reportProfiles = await apiAccess(apiUrl = baseUrl + 'reports');
        const reportType = document.getElementById("reportType");
        let columns; let selected_columns; 
        reportProfiles.forEach((profile) => {
            if (profile["main_section"] === reportType.value){
                columns = profile["columns"].split(",");
                selected_columns = profile["selected_columns"].split(",");
            }
        });

        let preselectedReportColumns = injector.getPreSelectedData(endpoint="reports");

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
                selected.push(checkBox);
            }
        });
        return selected;
    }catch(error){
        console.error(error)
    }
}

async function configureAdditionalReportSheets(){
    let sheetConfigDiv = document.getElementById("sheetConfig");
    let reportColumns = document.getElementsByName("report_column");
    let checkboxes = document.getElementsByName("additional_sheet");

    let injector =  new injectHtml(
        parentDiv = sheetConfigDiv, title = "Select Pivot Columns", reset = true
    );

    try{
        checkboxes.forEach(checkbox =>{
            checkbox.addEventListener("change", ()=>{
                if (checkbox.checked == true){
                    if (checkbox.value === "pivot_table"){
                        injector.injectCheckBoxes(
                            checkNames = findSelectedCheckBoxes(checkboxes = reportColumns),
                            commonName = "pivot_columns", preSelected = ""
                        );
                    }
                } else {
                    injector.resetinnerHtml();
                }
            },true);
        });
    } catch(error){
        console.error(error);
    }

}


/* Events configuration */
document.addEventListener("DOMContentLoaded",async ()=>{
    configureReportFiltration();
    configureAdditionalReportSheets();
});

reportType.addEventListener("change",async ()=>{
    configureReportFiltration();
});

