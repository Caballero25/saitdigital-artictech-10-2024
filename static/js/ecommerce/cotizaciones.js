function cotizar_email(producto) {
    var mailto = "saittdocuments@gmail.com"
    var gmailUrl = `mailto:${mailto}?subject=Cotización%20-%20ArtItTech&body=Me%20interesa%20cotizar%20el%20producto%20${producto}.`
    window.open(gmailUrl)
}


function cotizar_whatsaap(producto) {
    var phoneNumber = "593962636961"
    var whatsAppUrl = `https://wa.me/${phoneNumber}?text=Me%20interesa%20recibir%20una%20cotización%20del%20producto%20*${producto}*`;
    //location.href = whatsAppUrl
    window.open(whatsAppUrl)
    //window.location.href = whatsAppUrl
}