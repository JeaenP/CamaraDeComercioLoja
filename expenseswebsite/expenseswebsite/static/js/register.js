
const usernameField= document.querySelector("#usernameField")
const feedbackArea= document.querySelector(".invalid_feedback")
const emailField= document.querySelector("#emailField")
const emailFeedbackArea = document.querySelector(".emailFeedbackArea")
const passwordField = document.querySelector("#passwordField")
const usernameSuccesOutput = document.querySelector(".usernameSuccesOutput")
const emailSuccesOutput = document.querySelector(".emailSuccesOutput")
const showPasswordToggle = document.querySelector(".showPasswordToggle")
const submitBtn = document.querySelector(".submit-btn")



const hadleToggleInput= (e) => {
    if(showPasswordToggle.textContent === "Mostrar") {
        showPasswordToggle.textContent = "Ocultar";
        passwordField.setAttribute("type","text")
    } else {
        showPasswordToggle.textContent = "Mostrar"
        passwordField.setAttribute("type","password")
    }
}
showPasswordToggle.addEventListener("click", hadleToggleInput);

emailField.addEventListener("keyup", (e) => {
    const emailVal=e.target.value;
    emailSuccesOutput.style.display = "block";
    emailSuccesOutput.textContent = `Probando con ${emailVal}`;

    emailField.classList.remove("is-invalid");
    emailFeedbackArea.style.display = "none";
    if(emailVal.length>0) {
        fetch("/authentication/validate-email", {
            body: JSON.stringify({email: emailVal}) ,
            method: "POST" 
        })
        .then((res) => res.json())
        .then((data) => {
            emailSuccesOutput.style.display = "none";
            if(data.email_error){
                
                submitBtn.disabled = true;
                emailField.classList.add("is-invalid");
                emailFeedbackArea.style.display = "block";
                emailFeedbackArea.innerHTML=`<p>${data.email_error}<p>`
            } else { 
                submitBtn.removeAttribute("disabled")
            }
           
        });
    }

})


usernameField.addEventListener("keyup", (e) => {
    
 
    const usernameVal=e.target.value;
    usernameSuccesOutput.style.display = "block";
    usernameSuccesOutput.textContent = `Probando con ${usernameVal}`;

    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display = "none";
    if(usernameVal.length>0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({username: usernameVal}) ,
            method: "POST" 
        })
        .then((res) => res.json())
        .then((data) => {
            usernameSuccesOutput.style.display = "none";
            if(data.username_error){
                usernameField.classList.add("is-invalid");
                feedbackArea.style.display = "block";
                feedbackArea.innerHTML=`<p>${data.username_error}<p>`
                submitBtn.disabled = true;
            } else { 
                submitBtn.removeAttribute("disabled")
            }
           
        });
    }


   
    
})