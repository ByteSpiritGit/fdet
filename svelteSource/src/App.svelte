<script lang="ts">
   import Navbar from "./lib/Navbar.svelte";
   import Button from "./lib/Button.svelte";
   import Footer from "./lib/Footer.svelte";
   import WhatWeDo from "./lib/WhatWeDo.svelte";
   import Warning from "./lib/Warning.svelte";

   let toEvaluate;
   
   let textarea;

   let warnings;
   let buttonDisabled: boolean = false;

   function whenclk() {
      toEvaluate = textarea.value;
      if (toEvaluate) {
         window.location.href = "/evalOutput?text=" + toEvaluate;
         return;
      };

      if (warnings.children.length >= 1) {
         setTimeout(() => {
            warnings.children[0].remove()
         }, 500);
      }

      new Warning({
         target: warnings,
         props: {
            name: "Text missing",
            description: "There is nothing to evaluate",
            iconType: "Warning",
            duration: 5000
         }
      });
      return;
   }

   function checkSize() {
      textarea.style.height = 'auto';
      textarea.style.height = textarea.scrollHeight + 'px';
   }
</script>

<main>
   <Navbar />   

   <section class="content-section">
      <section class="title-section">
         <h1>Fake statement detector powered by AI</h1>
      </section>
   
      <WhatWeDo />
   
      <section class="input-section">
         <textarea bind:this={textarea} on:input={checkSize} on:paste={checkSize} class="input" placeholder="Paste your statement here" bind:value={toEvaluate}></textarea>
         <Button text="Evaluate" whenClicked={whenclk} disabled={buttonDisabled} />
      </section>
   </section>

   <Footer />
   <section class="warning-section" bind:this={warnings}></section>
</main>

<style>
   @import "./main.css";

   /* title section */
   .title-section {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;

      height: 100px;
      background-color: var(--color-secondary);

      margin-top: 100px;
   }

   .input-section {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;

      height: fit-content;
      background-color: var(--color-secondary);

      margin-top: 75px;

      padding: 20px;
   }

   .input-section > .input {
      background-color: var(--color-primary);
      color: var(--color-text);

      max-width: 700px;
      width: 50%;
      height: fit-content;
      max-height: 200px;

      border: none;
      border-radius: 10px;
      font-size: 1.2em;
      font-weight: 500;
      text-transform: uppercase;
      cursor: text;

      margin-bottom: 20px;
      padding: 5px;

      resize: none;
      text-transform: none;
   }

   .input-section > .input:focus {
      outline: none;
   }

   .input-section > .input::-webkit-scrollbar {
      width: 7px;
   }

   .input-section > .input::-webkit-scrollbar-thumb {
      background-color: var(--color-tertiary);
      border-radius: 10px;
   }

   .input-section > .input::-webkit-scrollbar-track {
      background-color: var(--color-primary);
      border-radius: 10px;
      border-width: 1px;
      border-style: solid;
      border-color: var(--color-primary);
   }

   .input-section > .input::-webkit-scrollbar-thumb:hover {
      background-color: var(--color-text);
   }

   .warning-section {
      position: absolute;
      bottom: 85px;
      right: 0;

      overflow: hidden;
   }
</style>
