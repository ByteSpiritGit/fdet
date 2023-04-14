<script lang="ts">
   export let theComponent: HTMLElement;
   export let notificationNumber: number = 1;

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
</script>

<section class="warning-section" bind:this={theComponent} />

<style>
   .warning-section {
      position: absolute;
      bottom: 85px;
      right: 0;

      overflow: hidden;
   }
</style>
