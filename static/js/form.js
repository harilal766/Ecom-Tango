function storeForms(selection){
    const formDict = {
        "Amazon" : ("Client Id", "Client Secret", "Refresh Token"),
        "Shopify" : ("Storename", "Access Token")
    }
    try{
        console.log(formDict.key);
        let credDiv = document.createElement('div');
        let formDiv = document.getElementById('store-form');

        /* add the input tags to the credential div*/

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