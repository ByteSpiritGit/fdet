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

<section>
   <div class="mask" bind:this={img}>
      <img src="{whatWeDoPng}" alt="What we do">
   </div>
</section>

<style>
   .mask {
      background-color: var(--color-text);
      width: 45em;
      /* min-width: 700px; */
      margin: 0px auto;

      margin-top: 70px;
   }

   .mask img {
      /* display: none; */
      opacity: 0;
      
      width: 100%;
      height: 100%;
   }
</style>