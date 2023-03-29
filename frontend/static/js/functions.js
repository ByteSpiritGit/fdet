function getCookie(name) {
    if (!document.cookie) {return null;}
    
    const token = document.cookie.split(';')
        .map(c => c.trim())
    
    if (token.length === 0) {return null;}
    return decodeURIComponent(token[0].split('=')[1]);
}

async function fetchResult(text) {
    const csrfToken = getCookie('CSRF-TOKEN');

    const request = new Request(
        `/evaluation?text=${text}`, 
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

// {
//     "Response"= 1,
//     "EvaluationID" = data["id"]
// }

