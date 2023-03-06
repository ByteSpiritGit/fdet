function getCookie(name) {
    if (!document.cookie) {return null;}
    
    const token = document.cookie.split(';')
        .map(c => c.trim())
    
    if (token.length === 0) {return null;}
    return decodeURIComponent(token[0].split('=')[1]);
}

// async function fetchResult(text, output, button) {
//     const csrfToken = getCookie('CSRF-TOKEN');

//     const xhttp = new XMLHttpRequest();
//     xhttp.open("POST", `/test_view?text=${text}`, true);
//     xhttp.setRequestHeader("Content-Type", "application/json");
//     xhttp.setRequestHeader("X-CSRFToken", csrfToken);
//     xhttp.send();

//     xhttp.onreadystatechange = function() {
//         if (this.readyState == 4 && this.status == 200) {
//             const data = JSON.parse(xhttp.responseText)["validated"][0];
//             printResults(data, output);
//             button.disabled = false;
//         }
//     }
// }

async function fetchResult(text) {
    const csrfToken = getCookie('CSRF-TOKEN');

    const request = new Request(
        `/test_view?text=${text}`, 
        {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            mode: 'same-origin'
        }
    });

    const response = await fetch(request);
    const data = await response.json();
    return data;
}

function printResults(data, output) {
    output.innerHTML = `<b>Claim:</b> ${data.claim}<br/>`;
    output.innerHTML += `<b>Label:</b> ${data.label}<br/>`;
    output.innerHTML += `<b>Supports:</b> ${(data.supports * 100).toFixed(2)
}%<br/>`;
    output.innerHTML += `<b>Refutes:</b> ${(data.refutes * 100).toFixed(2) }%<br/>`;
    output.innerHTML += `<b>Evidence:</b> <br/>${data.evidence}<br/>`;
}