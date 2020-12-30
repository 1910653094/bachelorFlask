jQuery(document).ready(function() {
    const registerModal = $('#registerModal');

    $('.registerOverlay').click(function (e) {
        e.preventDefault()
        $('#username').val('')
        $('#password').val('')

        registerModal.modal("show")
    })

    $('#closeModal').click( () => {
        $('#modalerror').css("display", "none")
    })

    const eyeBtn = document.querySelectorAll('.eye-btn');//document.getElementById("eye-btn");
    const passwordField = document.querySelectorAll('.password');//document.getElementById("password");

    eyeBtn.forEach( (eye) => {
        eye.addEventListener("click", (e) => {
            passwordField.forEach( (password) => {
                if (password.type === "password") {
                    e.target.setAttribute("class", "fa fa-eye-slash eye-btn");
                    password.type = "text";
                } else {
                    e.target.setAttribute("class", "fa fa-eye eye-btn");
                    password.type = "password";
                }
            })
        })
    })

    const infoBtn = document.querySelectorAll('.info-btn');

    infoBtn.forEach( (info) => {
        info.addEventListener("click", () => {
            let info = $("#myModal")
            if (info.css("display") === "none") {
                info.css("display", "block")
            } else {
                info.css("display", "none")
            }
        })
    })

    $('#register-password').on('input', (e) => {
        const input = e.target.value;
        if (input && checkstrong(input)) {
            $('#register-password').css("border-bottom", "2px solid green");
        } else if (input === "") {
            $('#register-password').css("border-bottom", "2px solid white")
        } else {
            $('#register-password').css("border-bottom", "2px solid red");
        }
    })
})

const checkstrong = (password) => {
    return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/.test(password) ||
            /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(password)
}

window.onclick = (e) => {
    const modal = document.getElementById("myModal");
    if (e.target === modal) {
        modal.style.display = "none"
    }
}

const trysubmit = (form, register) => {
    if (!register) {
        if ($('#username').val() !== '' && $('#password').val() !== '') {
            form.submit()
        } else {
            alert("Please fill out your username \n and password")
        }
    } else {
        const password = $('#register-password').val();
        console.log(password)
        if ($('#register-username').val() !== '' && password !== '') {
            if (register && !checkstrong(password)) {
                alert("Please check your passwords strength")
            } else {
                form.submit()
            }
        } else {
            alert("Please fill out your username \n and password")
        }
    }
}