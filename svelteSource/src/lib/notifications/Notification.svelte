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

<div class="whole" bind:this={whole}>
   <div class="line" style="background-color: {color};">
      <img src="{icon}" alt="icon" class="icon"/>
      
      <div class="description">
         <h3>{name}</h3>
         <p>{description}</p>
      </div>
   </div>
</div>

<style>
   .whole {
      user-select: none;

      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-between;

      width: 300px;
      height: fit-content;

      border-radius: 4px 0 0 4px;

      background-color: var(--color-secondary);

      overflow: hidden;

      animation: show 0.4s ease-in-out;

      margin: 10px 0;
   }

   .whole > .line {
      width: 7px;
      height: fit-content;
      
      position: relative;
      display: flex;
      align-items: center;

   }

   .icon {
      height: 25px;
      margin-left: 20px;
      margin-right: 15px;
   }

   .description {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: space-evenly;

      height: 100%;
      width: 100%;

      white-space: nowrap;

      line-height: 1.3em;
   }

   .description h3 {
      margin: 2px;
      padding: 0;

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
         transform: translateX(300px);
      }
      100% {
         transform: translateX(0);
      }
   }
</style>
