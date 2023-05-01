<script lang="ts">
   import Button from "./Button.svelte";
   import sendImg from "../assets/icons/send.png";
   import { onMount } from "svelte";
    import LogRegSwitchBtn from "./log-reg/LogReg_switch-btn.svelte";

   export let buttonDisabled: boolean = false;
   export let textarea: HTMLTextAreaElement;
   export let whenClk: () => void = () => {
      console.log(textarea.value);
   };

   const loggedin = localStorage.getItem("logged") === "true";
   
   let toEvaluate: string;
   
   onMount(() => {
      if (!loggedin) {
         buttonDisabled = true;
         const overlay = <HTMLDivElement>document.querySelector("#overlay");
         const inputSection = <HTMLDivElement>document.querySelector(".input-section");
         overlay.style.display = "flex";
         const inputSectionRect = inputSection.getBoundingClientRect();
         // overlay.style.top = `${inputSectionRect.top -2.5}px`;
         // overlay.style.left = `${inputSectionRect.left -2.5}px`;
         // overlay.style.width = `${inputSectionRect.width}px`;
         overlay.style.height = `${inputSectionRect.height}px`;
      }
      else {
         document.querySelector(".input-section").addEventListener("click", () => {
            textarea.focus;
         })
      }

   })

   function checkSize() {
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
   }
</script>

<div id="overlay" class="overlay">
  <div class="message">
    <p class="no-margin">For free evaluation please register</p>
    <div class="buttons no-margin">
      <a href="/users/login" class="button no-margin" id="login">Login</a>
      <a href="/users/register" class="button no-margin" id="register">Register</a>
    </div>
  </div>
</div>

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
      <Button text={sendImg} whenClicked={whenClk} disabled={buttonDisabled} isIcon={true}/>
   </div>
</section>

<style>
   .no-margin {
      margin: 0;
   }

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

   .overlay {
      position: fixed;
      bottom: 50px;
      left: 0;

      width: 100%;

      display: none;
      z-index: 1000;

      /* border-radius: 12px; */

      background-color: rgba(0, 0, 0, 0.3);
      backdrop-filter: blur(3px);

      flex-direction: column;
      align-items: center;
      justify-content: center;
   }

   .overlay > .message {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;

      padding: 20px;
   }

   .overlay > .message > .buttons {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-evenly;
      
      width: 100%;
   }

   .buttons > a {
      text-decoration: underline;
      color: var(--color-text);

      font-size: 1em;
      font-weight: 500;
      text-transform: uppercase;
      cursor: pointer;

      padding: 5px;
      margin-right: 5px;

      border-radius: 10px;
      border: none;
   }

   .buttons > a:hover {
      text-shadow: 0px 0px 1px #ffffffb0, 0px 0px 5px #cccccc56;
   }
</style>