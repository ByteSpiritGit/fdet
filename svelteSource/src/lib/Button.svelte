<script lang="ts">
    import { onMount } from "svelte";

   export let text: string;
   export let whenClicked: () => void = () => {
      console.log("buttonClicked");
   };
   export let disabled: boolean = false;
   export let isIcon: boolean = false;

   let btn: HTMLButtonElement;

   onMount(() => {
      if (isIcon && btn) {
         Object.assign(btn.style, {
            padding: "0",
            width: "2em",
            height: "2em",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
         });
      }
   });
</script>

<div class="button">
   <button on:click={whenClicked} disabled={disabled} bind:this={btn}>
      {#if isIcon}
         <img src={text} alt="icon" />
      {:else}
         {text}
      {/if}
   </button>
</div>

<style>
   .button {
      display: flex;
      align-items: center;
      justify-content: center;

      user-select: none;
   }

   .button > button {
      background-color: var(--color-tertiary);
      color: var(--color-text);
      border: none;
      border-radius: 10px;

      padding: 8px 20px;
      font-size: 1.2em;
      font-weight: 500;
      text-transform: uppercase;
      cursor: pointer;
      transition: 0.1s;
   }

   .button > button:disabled {
      background-color: var(--color-disabled);
      cursor: not-allowed;
      color: var(--color-tertiary-hover);
   }
   .button > button:disabled:hover {
      background-color: var(--color-disabled);
      color: var(--color-tertiary-hover);
   }
   .button > button:hover {
      background-color: var(--color-tertiary-hover);
   }

   img {
      width: 1.2em;
      height: 1.2em;

      margin: 0;
   }
</style>