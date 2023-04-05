<script lang="ts">
   // import Counter from './lib/Counter.svelte'
   // import Navbar from './lib/MainNavbar.svelte'

   let output = false;
   let evalued = [];

   function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
         const cookies = document.cookie.split(";");
         for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
               cookieValue = decodeURIComponent(
                  cookie.substring(name.length + 1)
               );
               break;
            }
         }
      }
      return cookieValue;
   }
   const csrftoken = getCookie("csrftoken");

   async function getEvaluated() {
      let data = (<HTMLInputElement>document.getElementById("eval-input"))
         .value;
      let url = `/evaluation?text=${data}`;

      console.log("Evaluating...");

      const request = new Request(`${url}`, {
         method: "POST",
         headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
            mode: "same-origin",
         },
      });

      const response = await fetch(request);
      const jsoned = await response.json();
      return jsoned.validated;
   }

   async function evaluate(e) {
      const btn = e.currentTarget;
      btn.disabled = true;

      evalued = await getEvaluated();
      console.log(evalued);

      btn.disabled = false;

      output = true;
   }
</script>

<!-- * HTML -->
<main>
   <section class="everything">
      <h1 id="title">fDet beta0.1_noUI</h1>

      <section class="input-section">
         <textarea id="eval-input" placeholder="Enter text to evaluate by AI" />
         <input
            type="submit"
            id="eval-button"
            value="Evaluate"
            on:click={evaluate}
         />
      </section>

      <section class="output-section">
         <h2 id="output-title">Output test</h2>
         <p id="output-text">
            <!-- {@html output} -->
            {#if output}
               {#each evalued as ev}
                  <b>Claim:</b>
                  {ev.claim} (ID: {ev.id})<br />
                  <b>Label:</b>
                  {ev.label}<br />
                  <b>Supports:</b>
                  {(ev.supports * 100).toFixed(2)}%<br />
                  <b>Refutes:</b>
                  {(ev.refutes * 100).toFixed(2)}%<br />
                  <b>Evidence:</b> <br />{ev.evidence}<br />
               {/each}
            {/if}
         </p>
      </section>

      <!-- <section class="feedback-section">
      <h2 id="feedback-title">Feedback</h2>
      <input name="feedbackButton" type="checkbox" id="feedback-button">
    </section> -->
   </section>
</main>

<!-- * css -->
<style>
   @import "./main.css";

   .everything {
      display: flex;
      flex-direction: column;
      align-items: center;

      width: fit-content;
      height: fit-content;

      min-height: 500px;
      min-width: 500px;

      max-width: 650px;

      margin: 2% auto;
      padding: 30px;

      background-color: #1f1f20;

      border-radius: 15px;
   }

   .input-section {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;

      width: 100%;
      height: fit-content;

      margin: 0 auto;
   }

   .input-section > #eval-input {
      margin: 0 0 10px 0;
      padding: 5px;

      width: 400px;
      max-width: 525px;
      max-height: 250px;

      min-width: 400px;
      min-height: 50px;

      border-radius: 5px;
      border-width: 1px;
      border-color: #bd2c2c8c;

      background-color: rgba(0, 0, 0, 0.295);

      font-size: 18px;
      outline: none;

      color: #e1f1fe;
      font-family: "roboto", sans-serif;
   }

   .input-section #eval-input::placeholder {
      color: #8c9eac;
   }

   .input-section > #eval-button {
      margin: 0 0 10px 0;
      padding: 5px;

      width: 100px;

      border-radius: 5px;
      border: none;
      font-size: 20px;

      transition: 200ms;

      /* background-image: linear-gradient(to right top, #2f40d8, #3444d9, #3848db, #3d4cdc, #4150dd, #4150dd, #4150dd, #4150dd, #3d4cdc, #3848db, #3444d9, #2f40d8); */
      background-color: #2c36bd8c;
      color: #e1f1fe;

      box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.5);
   }

   .input-section > #eval-button:hover#eval-button:enabled {
      color: rgb(255, 255, 255);
      width: 104px;
      letter-spacing: 1px;
   }

   .input-section > #eval-button:active#eval-button:enabled {
      color: rgb(255, 255, 255);
      width: 98px;
      font-size: 19px;
      letter-spacing: 0px;
   }

   .input-section > #eval-button:disabled {
      background-color: #bd2c2c8c;
      background-image: none;
      color: #be4940;
   }

   #title {
      margin: 0 auto 20px auto;
      font-size: 30px;
   }

   .output-section,
   .feedback-section {
      margin: 0;
      padding: 0;

      width: 100%;
   }

   #output-text {
      margin: 10px 0;
   }

   #feedback-button {
      margin: 0;
      padding: 0;
   }

   h2 {
      margin: 0;
      padding: 0;
   }
</style>
