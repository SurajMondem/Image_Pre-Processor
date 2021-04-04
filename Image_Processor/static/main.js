const alertBox = document.getElementById('alert-box')
const imgBox = document.getElementById('img-box')
const form = document.getElementById('p-form')

const btnBox1 = document.getElementById('btn-box1')
const btnBox2 = document.getElementById('btn-box2')

const btns = [...btnBox1.children, ...btnBox2.children]


const name = document.getElementById('id_name')
const description = document.getElementById('id_description')
const image = document.getElementById('id_image')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

console.log(csrf)

const url = ""
const mediaURL = window.location.href + 'media/'
console.log(mediaURL)

const handleAlerts = (type, text) => {
    alertBox.innerHTML = `<div class ="alert alert-${type}" role="alert">
                            ${text}
                        </div>`
}

image.addEventListener('change', ()=> {
    const img_data = image.files[0]
    const url = URL.createObjectURL(img_data)
    console.log(url)
    imgBox.innerHTML = `<img src="${url}" width="50%">`
    btnBox1.classList.remove('not-visible')
    btnBox2.classList.remove('not-visible')

})

let id = null
let filter = null

btns.forEach(btn => btn.addEventListener('click', ()=> {
    filter = btn.getAttribute('data-filter')
    console.log(filter)
}))


form.addEventListener('submit', e=>{
    e.preventDefault()

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('name', name.value)
    fd.append('description', description.value)
    fd.append('image', image.files[0])
    fd.append('action', filter)
    fd.append('id', id)

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function (response) {
            const data = JSON.parse(response.data)
            console.log(data)
            id = data[0].pk
            imgBox.innerHTML = `<img src="${mediaURL + data[0].fields.image}" width="50%">`
            const successText = `Successfully saved ${data[0].fields.name}`
            handleAlerts('success', `${successText}`)
            setTimeout(() => {
                alertBox.innerHTML = ""
            }, 3000);
        },
        error: function (error) {
            console.log(error)
            handleAlerts('danger', 'Oops.. something went wrong')
        },
        cache: false,
        contentType: false,
        processData: false,
    })

})

console.log(form)