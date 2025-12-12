async function uploadPDF() {
    let fileInput = document.getElementById("pdfInput").files[0];
    let formData = new FormData();
    formData.append("file", fileInput);

    let res = await fetch("http://127.0.0.1:8000/upload_pdf", {
        method: "POST",
        body: formData
    });

    let data = await res.json();
    alert(data.message);
}

async function sendMessage() {
    let q = document.getElementById("userInput").value;

    let res = await fetch("http://127.0.0.1:8000/chat?q=" + q);
    let data = await res.json();

    document.getElementById("response").innerText = data.answer;
}
