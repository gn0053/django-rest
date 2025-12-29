const loginForm = document.getElementById("login-form");
const searchForm = document.getElementById("search-form");
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

function refreshToken(callback=null){
    const endpoint = `${baseEndpoint}/v1/token/refresh/`;
    const options = {
        method: "POST",
        headers:{
            "Content-type":"application/json"
        },
        body:JSON.stringify({"refresh":localStorage.getItem("refresh")})
    };
    fetch(endpoint, options)
    .then(response=>{
        return response.json();

    })
    .then(data=>{
        if (localStorage.getItem("refresh") !== null) {
            if (data.code && data.code === "token_not_valid"){
                localStorage.clear();
                alert("Please login again");
            }
            else{
                localStorage.setItem("access", data.access)
                if (callback){
                    callback();
                }
            }
            
        }
    });
}
function istokenNotValid(jsonData){
    if (jsonData.code && jsonData.code === "token_not_valid"){
        // alert("Please login again.");
        return false
    }
    return true;
}

function writeContent(data){
    if (content_container){
        let content = [];
        for (const i of data.results){
            content.push(`<li>${i.title}</li>`);
        }
        if (content.length > 0){
            content_container.innerHTML = `<ul>${content.join("")}</ul>`;
        }
        else{
            content_container.innerHTML = "No rresults found";
        }
        // content_container.innerHTML = "<pre>" + JSON.stringify(data, null, 4) + "<pre>";
    }
}

function getProductList(){
    const endpoint = `${baseEndpoint}/v1/products/`;
    const options = getFetchOption();
    fetch(endpoint, options)
        .then(response=>{
            return response.json();

        })
        .then(data=>{
            const isValid = istokenNotValid(data)
            if (isValid){
                writeContent(data);
            }
            else
            {
                refreshToken(getProductList);
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


// SEARCH
function searchContent(data){
    if(content_container){
        content_container.innerHTML = "";
        if (data){
            let content = [];
            for (const i of data.results){
                if (i.hits){
                    for (const j of i.hits){
                        content.push(`<li>${j.title}</li>`);
                    }
                }
            }
            if (content.length > 0){
                content_container.innerHTML = `<ul>${content.join("")}</ul>`;
            }
            else{
                content_container.innerHTML = "No rresults found";
            }
        }
            
    }
}
function handleSearch(event=null){
    if (event){
        event.preventDefault();
    }
   
    
    let formData = new FormData(searchForm);
    let data = Object.fromEntries(formData);
    let searchParams = new URLSearchParams(data)
    const endpoint = `${baseEndpoint}/v1/search/?${searchParams}`;
    const headers = {
        "Content-type":"application/json"
    };
    const authToken = localStorage.getItem("access");
    if(authToken){
        headers["Authorization"] = `Bearer ${authToken}`;
    }
    const options = {
        method: "GET",
        headers:headers
    };
    fetch(endpoint, options)
    .then(serverResponse)
    .then(data=>{
        const isValid = istokenNotValid(data);
        if (isValid){
            searchContent(data);
        }
        else{
            refreshToken(handleSearch);
        }
    })
    .catch(errorResponse);
}
if (searchForm){
    searchForm.addEventListener("submit", handleSearch);
}
getProductList();
