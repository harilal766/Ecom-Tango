function storeForms(selection){
    const formDict = {
        "Amazon" : ["Client Id", "Client Secret", "Refresh Token"],
        "Shopify" : ["Storename", "Access Token"]
    }
    try{
        console.log(formDict.key);
        
        let formDiv = document.getElementById('store-form');
        let credDiv = document.getElementById('credentials');

        credDiv.innerHTML = "";

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

        let submissionDiv = document.getElementById("submission");
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