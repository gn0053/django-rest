const loginForm = document.getElementById("login-form");
const content_container = document.getElementById("content");

function getFetchOption(method, body){
    return {
        method: method === null ? "GET": method,
        headers:{
            "Content-type":"application/json",
            "Authorization":`Bearer ${localStorage.getItem("access")}`
        },
        body: body ? body : null
    };
}

function validateJWTToken(){
    const endpoint = `${baseEndpoint}/v1/token/verify/`;
    const options = {
        method: "POST",
        headers:{
            "Content-type":"application/json",
        },
        body: JSON.stringify({token: localStorage.getItem("access")})
    };
    fetch(endpoint, options)
    .then(response=>response.json)
    .then(x=>{
        console.log(x)
    });
}

function writeContent(data){
    if (content_container){
        content_container.innerHTML = "<pre>" + JSON.stringify(data, null, 4) + "<pre>";
    }
}

function istokenNotValid(jsonData){
    if (jsonData.code && jsonData.code === "token_not_valid"){
        // or refresh token query
        alert("Please login again.");
        return false;
    }
    return true;
}

function getProductList(){
    const endpoint = `${baseEndpoint}/v1/products/`;
    const options = getFetchOption();
    fetch(endpoint, options)
        .then(response=>{
            return response.json();

        })
        .then(data=>{
            const isValid = istokenNotValid(data);
            if (isValid){
                writeContent(data);
            }
        });
}

function handeAuthData(authData){
    localStorage.setItem("access", authData.access);
    localStorage.setItem("refresh", authData.refresh);
    getProductList();
}

function errorResponse(x){
    console.log(x);
}
function testResponse(x){
    console.log(x);
}

function serverResponse(response){
    return response.json()
}

function handleLogin(event){
    event.preventDefault();
    
    let loginFormData = new FormData(loginForm);
    let loginObjectData = Object.fromEntries(loginFormData);
    const loginEndpoint = `${baseEndpoint}/v1/token/`;

    const options = getFetchOption("POST", JSON.stringify(loginObjectData));
    // const options = {
    //     method: "POST",
    //     headers:{
    //         "Content-type":"application/json"
    //     },
    //     body: JSON.stringify(loginObjectData)
    // };
    fetch(loginEndpoint, options).then(serverResponse).then(handeAuthData).catch(errorResponse);
}

const baseEndpoint = "http://localhost:8000/api";


if (loginForm){
    loginForm.addEventListener("submit", handleLogin);
}
getProductList();
