function storeForms(selection){
    const commonCredentials = ["Name of the store"]
    const formDict = {
        "Amazon" : commonCredentials.concat(["Client Id", "Client Secret", "Refresh Token"]),
        "Shopify" : commonCredentials.concat(["Storename", "Access Token"])
    }
    try{
        console.log(formDict.key);
        
        let formDiv = document.getElementById('store-form');
        let credDiv = document.getElementById('credentials');
        let submissionDiv = document.getElementById("submission");

        credDiv.innerHTML = ""; submissionDiv.innerHTML = "";

        /* add the input tags to the credential div*/
        let selectedCreds = formDict[selection];
        console.log(selectedCreds);
        selectedCreds.forEach(cred => {
            let input = document.createElement('input');
            input.type = "text";
            input.placeholder = `Enter ${cred}`;
            input.name = cred; input.className = "form-control";
            credDiv.appendChild(input);
            credDiv.appendChild(document.createElement("br"));
        });

        
        let submitButton = document.createElement("button");
        submitButton.innerHTML = `Add store`;
        submitButton.className = "btn btn-primary";
        submissionDiv.appendChild(submitButton);
        /* add the credential div and submit button to the form div */
    }
    catch(e) {
        console.log(e);
    }
}


const platformSelector = document.querySelector('select');

platformSelector.addEventListener('change',(event)=>{
    storeForms(selection = event.target.value);
});

const selectedReportType = document.getElementById("reportType");
const dateRangeHtml = document.getElementById("dateRange");

/* To make sure only a particular form will be affected */
const reportForm = document.getElementById("reportForm");
const formTitle = document.getElementById("formTitle");
const submitButton = document.getElementById("submitButton");

function arrangeDateRange(){
    if (selectedReportType.value !== "Settlement Report"){
        reportForm.insertBefore(dateRangeHtml,submitButton);
    }
    else if (selectedReportType.value === "Settlement Report"){
        reportForm.removeChild(dateRangeHtml);
    }
}
