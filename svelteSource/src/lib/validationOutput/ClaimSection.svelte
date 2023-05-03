<script lang="ts">
   import { onMount } from "svelte";

   import Sentence from "./Sentence.svelte";
   import PercentageBar from "./PercentageBar.svelte";
   import SentenceValidation from "./SentenceValidation.svelte";
   import Button from "../Button.svelte";

    import hideImg from "../../assets/icons/hide.png";
    import showImg from "../../assets/icons/show.png";

    let btnImg = hideImg;

   export let claims: Array<{
      claim: string,
      evidence: string,
      label: string,
      refutes: number,
      supports: number,
      nei: number,
      justify: string,
      url: Array<string>,
      is_error: boolean
   }>;
   export let id_offset: number = 0;

   let claimSection;
   let validationSection;
   let averageSection;

   function claimsBlock(where, claims, id_offset = 0) {
      let average = {
         supports: 0,
         refutes: 0,
         nei: 0
      };

      // create clickable claims, that are put to the top of its claim section
      claims.forEach(claim => {
         average.supports += claim.supports;
         average.refutes += claim.refutes;
         average.nei += claim.nei;        

         let sentence = new Sentence({
            target: where,
            props: {
               claim: claim,
               outputId: `${id_offset.toString()+"m"}`,
               whenClicked: () => {
                  validationSection.style.display = "block";
                  btnImg = hideImg;
               }
            }
         })
      });

      // calculates the average of all sentences (claims)
      average.supports /= claims.length;
      average.refutes /= claims.length;
      average.nei /= claims.length;

      new PercentageBar({
         target: averageSection,
         props: {
            supports: average.supports,
            refutes: average.refutes,
            nei: average.nei
         }
      })
      
      // shows details of the first claim 
      new SentenceValidation({
         target: validationSection,
         props: {
            claim: claims[0],
         }
      })
   }

   onMount(() => {
      claimsBlock(claimSection, claims, id_offset);
   })

   function clear_validation_section() {
        if (validationSection.style.display == "none") {
            validationSection.style.display = "block";
            btnImg = hideImg;
        } else {
            validationSection.style.display = "none";
            btnImg = showImg;
        }
   }
</script>

<section class="claim-section">
   <p>Claim: </p>
   <section class="claim" bind:this={claimSection}></section>
   <div class="average-wrapper">
      <section bind:this={averageSection} class="average-section"></section>
      <Button
         text={btnImg}
         whenClicked={clear_validation_section}
         disabled={false}
         isIcon={true}
      />
   </div>
   <section id={id_offset.toString()+"m"} class="sentence-validation-section" bind:this={validationSection}>
   </section>
</section>

<style>
   .claim-section {
      display: block;
      
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

   .average-wrapper {
      display: flex;
      flex-direction: row;
      align-items: flex-end;
      
      width: 100%;
   }

   .average-wrapper > .average-section {
      width: 100%;
      margin-right: 0.5rem;
   }
</style>