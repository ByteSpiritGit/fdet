<script lang="ts">
   import { onMount } from "svelte";

   import ClaimSection from "./ClaimSection.svelte";

   export let claims: Array<{
      claim: string,
      evidence: string,
      label: string,
      supports: number,
      refutes: number,
      nei: number,
      justify: string,
   }>;

   let chat;

   onMount(() => {
      new ClaimSection({
         target: document.querySelector(".chat"),
         props: {
            claims: claims,
            id_offset: 0
         }
      })
      // new ClaimSection({
      //    target: document.querySelector(".chat"),
      //    props: {
      //       claims: claims,
      //       id_offset: 1
      //    }
      // })
      // new ClaimSection({
      //    target: document.querySelector(".chat"),
      //    props: {
      //       claims: claims,
      //       id_offset: 2
      //    }
      // })
      // new ClaimSection({
      //    target: document.querySelector(".chat"),
      //    props: {
      //       claims: claims,
      //       id_offset: 3
      //    }
      // })
   chat.scrollTop = chat.scrollHeight - chat.clientHeight;
   });
</script>

<output class="chat" bind:this={chat}>

</output>

<style>
   .chat {
      position: absolute;
      top: 3.5rem;
      bottom: 10rem;
   
      width: 100%;
      max-width: 800px;

      overflow-y: auto;
      overflow-x: hidden;

      padding: 0.5rem;
      padding-bottom: 0;
   }

   @media (max-width: 680px) {
      .chat {
         top: 7rem;
      }
   }
</style>