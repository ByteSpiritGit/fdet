<script>
   import Footer from "../lib/Footer.svelte";
   import Navbar from "../lib/Navbar.svelte";
   import RegisterSection from "../lib/log-reg/RegisterSection.svelte";

   let registered = false;
</script>

<main>
   <Navbar />

   {#if !registered}
      <RegisterSection />
   {:else}
      <LoginSection />
   {/if}

   <Footer />
</main>
