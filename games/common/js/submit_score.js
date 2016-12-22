function submit_score(score) {
    auth_data = get_auth_data()
    submit_data = auth_data + "&" + score
    call_api("set_score", submit_data)
}

function get_auth_data() {
    hash = window.location.hash
    auth_data = hash.substring(1)
    additionalDataStart = auth_data.indexOf("&")
    if (additionalDataStart > 0) {
        auth_data = auth_data.substring(0, additionalDataStart)
    }
    return auth_data
}

function call_api(name, data) {
    request = new XMLHttpRequest()
    request.open("POST", "https://cgb.ohbah.com:4343/cgbapi/" + name)
    request.send(data)
}
