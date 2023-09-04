<script lang="ts">
   import Navbar from "./lib/Navbar.svelte";
   import Footer from "./lib/Footer.svelte";
   import WhatWeDo from "./lib/WhatWeDo.svelte";
   import Notification from "./lib/notifications/Notification.svelte";
   import NotificationBlock from "./lib/notifications/NotificationBlock.svelte";

   import InputSection from "./lib/InputSection.svelte";

   let toEvaluate;
   
   let textarea;

   let notifs;

   function whenclk() {
      toEvaluate = textarea.value;
      
      let urlText = "";
      toEvaluate.split("\n").forEach(claim => {
         urlText += claim + " ";
      });

      if (toEvaluate) {
         window.location.href = "/evalOutput?text=" + encodeURIComponent(urlText);
         return;
      }

      const notification = new Notification({
         target: notifs,
         props: {
            name: 'Text missing',
            description: 'There is nothing to evaluate',
            iconType: 'Warning',
            duration: 5000
         }
      });
   }
</script>

<main>
   <Navbar />   

   <section class="content-section">
      <section class="title-section">
         <h1>Fake statement detector powered by AI</h1>
      </section>
   
      <WhatWeDo />

      <InputSection bind:textarea={textarea} whenClk={whenclk} />
   </section>

   <Footer />

   <NotificationBlock bind:theComponent={notifs} notificationNumber={1}  />
</main>

<style>
   .title-section {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;

      height: 100px;
      background-color: var(--color-secondary);

      margin-top: 125px;
   }

   ::-webkit-scrollbar {
      width: 7px;
   }

   ::-webkit-scrollbar-thumb {
      background-color: var(--color-tertiary);
      border-radius: 10px;
   }

   ::-webkit-scrollbar-track {
      background-color: var(--color-primary);
      border-radius: 10px;
      border-width: 1px;
      border-style: solid;
      border-color: var(--color-primary);
   }

   ::-webkit-scrollbar-thumb:hover {
      background-color: var(--color-tertiary-hover);
   }

   @media (max-width: 680px) {
      .title-section {
         display: none;
      }
   }

   @media (max-height: 560px) {
      .title-section {
         display: none;
      }
   }
</style>
