const loginForm = document.getElementById("login-form");

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
    const options = {
        method: "POST",
        headers:{
            "Content-type":"application/json"
        },
        body: JSON.stringify(loginObjectData)
    };
    fetch(loginEndpoint, options).then(serverResponse).then(testResponse).catch(errorResponse);
}

const baseEndpoint = "http://localhost:8000/api";


if (loginForm){
    loginForm.addEventListener("submit", handleLogin);
}
