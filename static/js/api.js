async function apiAccess(apiUrl){
    try{
        const response = await fetch(apiUrl);
        if (!response.ok){
            throw new Error(`Response : ${response.status}`);
        }
        const result = await response.json();
        console.log(result);
        return result;
    }
    catch(error){
        console.error(error.message);
    }
}

const baseUrl = '/api/router/';