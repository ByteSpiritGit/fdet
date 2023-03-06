const input = document.querySelector('#eval-input');
const output = document.querySelector('#output-text');
const button = document.querySelector('#eval-button');

button.addEventListener("click", c => {
    const text = input.value;
    button.disabled = true;
    output.innerHTML = "Loading...";
    
    let processResult = async () => {
        let result = await fetchResult(text);
        result = result["validated"][0];
        printResults(result, output);
        button.disabled = false;
    }
    processResult();
})

