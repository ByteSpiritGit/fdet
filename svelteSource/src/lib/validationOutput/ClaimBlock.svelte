<script lang="ts">
   import Sentence from "./Sentence.svelte";
   
   let claimSection;

   export let claims: Array<{
      claim: string,
      evidence: string,
      label: string,
      refutes: number,
      supports: number
   }>;

   $: if (claimSection) {
      claims.forEach(claim => {
         new Sentence({
            target: claimSection,
            props: {
               text: claim.claim
            }
         })
      });
   }
</script>

<output>
   <section class="claim-section" bind:this={claimSection}></section>
   <section class="validation-section"></section>
</output>

<style>
   .claim-section {
      display: flex;
      width: 50%;
      height: 100%;
   }
</style>