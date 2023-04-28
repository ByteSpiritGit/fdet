<script lang="ts">
   import Button from "./Button.svelte";
   import sendImg from "../assets/icons/send.png";
    import { onMount } from "svelte";

   export let buttonDisabled: boolean = false;
   export let textarea: HTMLTextAreaElement;
   export let whenClk: () => void = () => {
      console.log(textarea.value);
   };
   
   let toEvaluate: string;
   
   onMount(() => {
      document.querySelector(".input-section").addEventListener("click", () => {
         textarea.focus;
      })
   })

   function checkSize() {
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
   }
</script>

<section class="input-section">
   <div class="input-wrapper">
      <textarea
         bind:this={textarea}
         on:input={checkSize}
         on:paste={checkSize}
         class="input"
         placeholder="Paste your statement here"
         bind:value={toEvaluate}
      />
      <Button
         text={sendImg}
         whenClicked={whenClk}
         disabled={buttonDisabled}
         isIcon={true}
      />
   </div>
</section>

<style>
   .input-section {
      position: fixed;

      bottom: 50px;
      left: 0;

      width: 100%;
      height: fit-content;

      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;

      height: fit-content;
      background-color: var(--color-secondary);

      margin-top: 75px;

      padding: 20px;

      border-top: 3px solid var(--color-primary-alpha);

      cursor: pointer;
   }

   .input-wrapper {
      display: flex;
      flex-direction: row;
      align-items: flex-end;
      justify-content: space-evenly;

      width: 100%;
      height: fit-content;
      max-width: 700px;
      max-height: 200px;

      border-radius: 10px;

      padding: 0.5em;

      background-color: var(--color-primary);
   }

   .input-section > .input-wrapper > .input {
      background-color: var(--color-primary);
      color: var(--color-text);

      max-width: 700px;
      width: 100%;

      max-height: 180px;

      border: none;
      border-radius: 10px;
      font-size: 1.2em;
      font-weight: 500;
      text-transform: uppercase;
      cursor: text;

      /* margin-bottom: 20px; */
      padding: 5px;
      margin-right: 5px;

      resize: none;
      text-transform: none;
   }

   .input:focus {
      /* outline: var(--color-tertiary) solid 2px; */
      outline: none;
   }
</style>