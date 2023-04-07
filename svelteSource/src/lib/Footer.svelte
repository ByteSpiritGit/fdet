<script lang="ts">
   import github from "../assets/socials/github.png";
   import instagram from "../assets/socials/instagram.png";
   import twitter from "../assets/socials/twitter.png";
   import youtube from "../assets/socials/youtube.png";

   let svgElements = [];

   let links = [
      {
         "name": "Instagram",
         "link": "https://www.instagram.com/fdet_official/",
         "icon": instagram
      },
      {
         "name": "Youtube",
         "link": "https://www.youtube.com/@fdet",
         "icon": youtube
      },
      {
         "name": "Twitter",
         "link": "https://twitter.com/fDet_Official",
         "icon": twitter
      },
      {
         "name": "Github",
         "link": "https://github.com/fdet/fDet",
         "icon": github
      }
   ]

   function maskSvg(svgElems) {
      svgElems.forEach(element => {
         element.style.webkitMask = `url(${element.dataset.png})`;
         element.style.mask = `url(${element.dataset.png})`;
         element.style.webkitMaskSize = "100%";
         element.style.maskSize = "100%";
         element.style.webkitMaskPosition = "center";
         element.style.maskPosition = "center";
         element.style.webkitMaskRepeat = "no-repeat";
         element.style.maskRepeat = "no-repeat";
      });
   }

   $: if (svgElements) {
      maskSvg(svgElements);
   }
</script>

<section class="footer-section">
   <section class="link-section">
      {#each links as link}
            <a href="{link.link}" class="mask" bind:this={svgElements[links.indexOf(link)]} data-png="{link.icon}">
               <img src="{link.icon}" alt="{link.name}">
            </a>
      {/each}
   </section>
</section>

<style>
   @import "../main.css";

   .footer-section {
      background-color: var(--color-secondary);

      position: fixed;
      bottom: 0;
      
      width: 100%;

      margin: 0;
      padding: 0;
   }

   .link-section {
      height: 50px;

      width: 200px;

      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-evenly;
   }

   .mask {
      display: inline-block;
      width: 30px;
      height: 30px;
      margin: 5px;

      background-color: var(--color-text);
   }

   .mask img {
      display: none;
   }

   .mask:hover {
      background-color: var(--color-tertiary);
   }
</style>