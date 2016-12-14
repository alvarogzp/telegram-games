function submit_score(score) {
    hash = window.location.hash
    auth_data = hash.substring(1, hash.indexOf("&"))
    request = new XMLHttpRequest()
    request.open("POST", "https://cgb.ohbah.com:4343/cgbapi/set_score")
    request.send(auth_data + "&" + score)
}
