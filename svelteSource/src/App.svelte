<script lang="ts">
  // import Counter from './lib/Counter.svelte'
  // import Navbar from './lib/MainNavbar.svelte'
  function evaluate() {
    // const text = input.value;
    // button.disabled = true;
    // output.innerHTML = "Loading...";
    
    // let processResult = async () => {
    //     // let result = await fetchResult(text);
    //     // result = result["validated"][0];
    //     // printResults(result, output);
    //     // button.disabled = false;
    // }
    // processResult();
  
    console.log("Evaluating");
    
  }

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
</script>

<!-- * HTML -->
<!-- <main>
  <header>
    <logo />
    <Navbar />
    <profile />
  </header>

  <section>
    
  </section>
</main>

 * CSS 
<style>
  
</style>
-->

<main> 
  <!-- {% csrf_token %} -->
  <section id="everything">
    <h1 id="title">fDet Test site</h1>
    <section id="input-section">
        <textarea id="eval-input" name="text" placeholder="Enter text to evaluate by AI"></textarea>
        <input name="evalButton" type="submit" id="eval-button" value="Evaluate" on:click={evaluate}>
    <section id="output-section">
        <h2 id="output-title">Output test</h2>
        <p id="output-text"></p> <!-- Do tohohle dávej output-->
        <input name="feedbackButton" type="checkbox" id="feedback-button">
</main>