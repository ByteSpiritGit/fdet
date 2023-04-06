<script lang="ts">
   import whatWeDoPng from "../assets/whatWeDo.png";
</script>

<section>
   <div class="mask">
      <img src="{whatWeDoPng}" alt="What we do">
   </div>
</section>

<style>
   .mask {
      background-color: var(--color-text);
      width: 50%;
      margin: 0px auto;

      margin-top: 70px;

      -webkit-mask-image: url("../assets/whatWeDo.png");
      mask-image: url("../assets/whatWeDo.png");
      -webkit-mask-size: 100%;
      mask-size: 100%;
      -webkit-mask-position: center;
      mask-position: center;
      -webkit-mask-repeat: no-repeat;
      mask-repeat: no-repeat;
   }

   .mask img {
      /* display: none; */
      opacity: 0;
      /* height: 100%; */
      width: 100%;
   }
</style>