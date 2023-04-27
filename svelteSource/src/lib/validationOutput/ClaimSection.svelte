<script lang="ts">
   import { onMount } from "svelte";

   import Sentence from "./Sentence.svelte";
   import PercentageBar from "./PercentageBar.svelte";
    import SentenceValidation from "./SentenceValidation.svelte";

   export let claims: Array<{
      claim: string,
      evidence: string,
      label: string,
      refutes: number,
      supports: number,
      nei: number,
      justify: string,
   }>;
   export let id_offset: number = 0;

   let claimSection;
   let validationSection;
   let highestAverage;

   function claimsBlock(where, claims, id_offset = 0) {
      let average = {
         supports: 0,
         refutes: 0,
         nei: 0
      };

      claims.forEach(claim => {
         average.supports += claim.supports;
         average.refutes += claim.refutes;
         average.nei += claim.nei;        

         let sentence = new Sentence({
            target: where,
            props: {
               text: claim.claim,
               id: `${claims.indexOf(claim)}-${id_offset}`
            }
         })
      });

      average.supports /= claims.length;
      average.refutes /= claims.length;
      average.nei /= claims.length;

      new PercentageBar({
         target: validationSection,
         props: {
            supports: average.supports,
            refutes: average.refutes,
            nei: average.nei
         }
      })

      // highestAverage = average.supports > average.refutes && average.supports > average.nei 
      // ? "supports" 
      // : average.refutes > average.nei 
      //    ? "refutes" 
      //    : "nei";
   }

   onMount(() => {
      claimsBlock(claimSection, claims, id_offset);
   })
</script>

<section class="claim-section">
   <p>Claim: </p>
   <section bind:this={claimSection}></section>
   <section class="sentence-validation-section" bind:this={validationSection}>
      <!-- <SentenceValidation claim={claims[0]} id="" /> -->
   </section>
</section>

<style>
   .claim-section {
      display: block;
      top: 60px;
      z-index: 200;
      background-color: var(--color-secondary);

      border-radius: 10px;

      margin: 0;
      margin-bottom: 10px;
      padding: 10px; 

      width: 100%;

      border: 1px solid var(--color-primary);

      transition: 0.1s;
   }

   .claim-section:hover {
      border: 1px solid var(--color-tertiary);
   }

   .claim-section > p {
      margin: 0;
      padding: 0;
   }
</style>