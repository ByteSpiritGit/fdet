<script lang="ts">
   import whatWeDoPng from "../assets/whatWeDo.png";

   let img;

   $: if (img) {
      img.style.webkitMask = `url(${whatWeDoPng})`;
      img.style.mask = `url(${whatWeDoPng})`;
      img.style.webkitMaskSize = "100%";
      img.style.maskSize = "100%";
      img.style.webkitMaskPosition = "center";
      img.style.maskPosition = "center";
      img.style.webkitMaskRepeat = "no-repeat";
      img.style.maskRepeat = "no-repeat";
   }
</script>


<section class="whatWeDo">
   <section class="block">
      <h3>You state a fact</h3>
      <p>"The human body is made up of about 60% water"</p>
   </section>
   <div class="hyphen"></div>
   <section class="block">
      <h3>We find the evidence</h3>
      <p>"The human body contains from 55% to 78% of water"</p>
   </section>
   <div class="hyphen"></div>
   <section class="block">
      <h3>And return results</h3>
      <p>"Supports: 83.74% <br /> Refutes: 16.26%"</p>
   </section>
</section>   

<style>
   .whatWeDo {
      position: relative;

      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-between;

      max-width: 45em;

      height: 100%;

      margin: 0 auto;
      margin-top: 70px;
   }

   .hyphen {
      width: 2em;
      height: 0.25em;

      border-radius: 2em;

      background-color: var(--color-text);

      margin: 0 1em;
   }

   h3 {
      margin: 0;
      /* margin-bottom: 0.2em; */
   }

   p {
      margin: 0;
      margin-top: 0.2em;

      /* text-align: center; */
      color: var(--color-text-darker);
   }

   .block {
      width: 200px;
   }

   
   @media (max-width: 768px) {
      .whatWeDo {
         flex-direction: column;

         margin: 30px;

         /* margin-top: 125px; */
      }

      .hyphen {
         width: 0.25em;
         height: 1em;

         margin: 0.5em 0;
      }

      p {
         text-align: center;
      }

      .block {
         display: flex;
         flex-direction: column;
         align-items: center;
         justify-content: center;
      }
   }

   @media (max-height: 770px) and (max-width: 768px) {
      .whatWeDo {
         margin-top: 125px;
      }
   }

   @media (max-height: 640px) and (min-width: 768px) {
      .whatWeDo {
         margin-top: 125px;
      }
   }
</style>

<!-- <section>
   <div class="mask" bind:this={img}>
      <img src={whatWeDoPng} alt="What we do" />
   </div>
</section> -->

<!-- <style>
   .mask {
      background-color: var(--color-text);
      max-width: 45em;
      width: 90%;
      margin: 0px auto;

      margin-top: 70px;
   }

   .mask img {
      /* display: none; */
      opacity: 0;

      width: 100%;
      height: 100%;
   }
</style> -->
