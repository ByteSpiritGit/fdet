<script lang="ts">
   import { onDestroy } from "svelte";

   import warningIcon from "../../assets/icons/warning-sign-color.png";
   import errorIcon from "../../assets/icons/error-color.png";
   import notFoundIcon from "../../assets/icons/404-color.png";

   export let name: string;
   export let iconType: string = null;
   export let description: string;
   export let duration: number;

   let icon: string;
   let whole;

   let color: string;

   switch (iconType) {
      case "Warning":
         icon = warningIcon;
         color = "#fc5557";
         break;
      case "Error":
         icon = errorIcon;
         color = "#fc5557";
         break;
      default:
         icon = notFoundIcon;
         color = "#f1982e";
         break;
   }
   
   setTimeout(() => {
      whole.remove();
   }, duration);

   onDestroy(() => {
      console.log("Notification deleted.");
   });
</script>

<div class="whole" bind:this={whole} style="border-left: 0.4em solid {color};">
   <!-- <div class="line" style="background-color: {color};"></div> -->
   <img src="{icon}" alt="icon" class="icon"/>
   <div class="text">
      
      <div class="description">
         <h3>{name}</h3>
         <p>{@html description}</p>
      </div>
   </div>
</div>

<style>
   .whole {
      user-select: text;

      display: inline-flex; /* Changed display property */
      flex-direction: row;
      align-items: flex-start;
      justify-content: space-between;

      width: fit-content;

      border-radius: 4px 0 0 4px;

      background-color: var(--color-secondary);

      animation: show 0.4s ease-in-out;

      margin: 10px 0;
      padding: 0.4em;
      padding-left: 0;
   }

   .text {
      display: flex;
   }

   .icon {
      /* height: 25px; */
      height: 2em;
      margin-top: 0.3em;
      margin-left: 0.6em;
      margin-right: 0.5em;
   }

   .description {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: space-evenly;

      height: 100%;
      width: 100%;

      line-height: 1.3em;
   }

   .description h3 {
      margin: 0;
      margin-right: 0.8rem;
      padding: 0;

      white-space: nowrap;

      font-size: 1.2rem;
      font-weight: 600;
   }

   .description p {
      margin: 2px;
      padding: 0;

      font-size: 1rem;
      font-weight: 400;

      width: 100%;
   }

   @keyframes show {
      0% {
         transform: translateX(100%);
      }
      100% {
         transform: translateX(0);
      }
   }
</style>
