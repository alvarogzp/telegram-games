function submit_score(score) {
    auth_data = get_auth_data()
    submit_data = auth_data + "&" + score
    call_api("set_score", submit_data)
}

function get_auth_data() {
    hash = window.location.hash
    return hash.substring(1, hash.indexOf("&"))
}

function call_api(name, data) {
    request = new XMLHttpRequest()
    request.open("POST", "https://cgb.ohbah.com:4343/cgbapi/" + name)
    request.send(data)
}
