<script lang="ts">
   import Navbar from "./lib/Navbar.svelte";
   import Button from "./lib/Button.svelte";
    import { text } from "svelte/internal";

   let toEvaluate
   let textarea;

   function whenclk() {
      console.log("clicked");
   }

   function checkSize() {
      textarea.style.height = 'auto';
      textarea.style.height = textarea.scrollHeight + 'px';
   }
</script>

<!-- * HTML -->
<main>
   <Navbar />   

   <section class="title-section">
      <h1>Fake statement detector powered by AI</h1>
   </section>

   <section class="input-section">
      <textarea bind:this={textarea} on:input={checkSize} on:paste={checkSize} class="input" placeholder="Paste your statement here" bind:value={toEvaluate}></textarea>

      <Button text="Evaluate" whenClicked={whenclk} disabled={false}/>
   </section>
</main>

<!-- * css -->
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

      margin-top: 100px;

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

   /* .input-section > .input::-webkit-scrollbar {
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
   } */
</style>