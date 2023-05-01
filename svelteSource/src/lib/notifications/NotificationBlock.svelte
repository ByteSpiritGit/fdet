<script lang="ts">
   import { onMount, onDestroy } from "svelte";

   export let theComponent: HTMLElement;
   export let notificationNumber: number = 1;
   const notifNumberDefault = notificationNumber;
   let isSmallScreen = false;

   function handleMutation(mutationsList, observer) {
      // console.log("Mutation observed:", theComponent.children.length);

      if (theComponent.children.length > notificationNumber) {
         // theComponent.children[0].remove();
         setTimeout(() => {
            if (theComponent.children.length > notificationNumber) {
               theComponent.children[0].remove();
            }
         }, 500);
      }
   }

   $: {
      if (theComponent) {
         const observer = new MutationObserver(handleMutation);
         observer.observe(theComponent, { childList: true });
      }
   }

   // if the screen size is smaller then 680px then the notification block will be at the bottom of the screen and notificationNumber 1

   function updateNotificationBlock() {
    if (window.innerWidth < 680) {
      theComponent.style.bottom = "3rem";
      notificationNumber = 1;
      isSmallScreen = true;
    } else {
      theComponent.style.bottom = "10rem";
      notificationNumber = notifNumberDefault;
      isSmallScreen = false;
    }
  }

  onMount(() => {
    updateNotificationBlock();
    window.addEventListener("resize", updateNotificationBlock);
  });

  onDestroy(() => {
    window.removeEventListener("resize", updateNotificationBlock);
  });

</script>

<section class="warning-section" bind:this={theComponent} />

<style>
   .warning-section {
      position: absolute;
      bottom: 10rem;
      right: 0;

      overflow: hidden;

      display: flex;
      flex-direction: column;
      align-items: flex-end;
   }
</style>
