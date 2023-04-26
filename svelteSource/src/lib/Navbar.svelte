<script lang="ts">
   import Login from "../mains/Login.svelte";

   function showProfile() {
      
   }

   let logedin: boolean = true;
</script>

<nav class="navbar">
   <section class="menu-section">
      <a href="/">Home</a>
      <a href="/evaluation?text=The sky is blue">About us</a>
      <a href="/">Learn</a>
      <a href="https://github.com/fdet/fDet">Github</a>
      <a href="/">History</a>
   </section>
   <section class="sides-section">
      <section class="logo-section">
         <a href="/#/evaluations">
            
            **logo**
         </a>
      </section>
      <section class="profile-section">
         <a href="/#/login" on:click={showProfile}>
            **profile**
         </a>
      </section>
   </section>
</nav>


<style>
   .navbar {
      position: fixed;
      top: 0;
      z-index: 200;

      width: 100%;
      height: 3em;

      font-size: 1.2em;

      background-color: var(--color-primary);
   }
   
   .sides-section {
      position: fixed;
      z-index: 250;
      top: 0;

      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-between;

      width: 100%;
   }

   .sides-section > section {
      width: 150px;
      background-color: var(--color-secondary);

   }

   .sides-section > section:first-child {
      border-radius: 0 0 10px 0;
      box-shadow: 0 0 10px 1px var(--color-primary);
   }

   .sides-section > section:last-child {
      border-radius: 0 0 0 10px;
      box-shadow: 0 0 10px 1px var(--color-primary);
   }

   .sides-section > section > a {
      color: var(--color-text);
      text-decoration: none;

      width: 100%;
      height: 100%;

      display: flex;
      align-items: center;
      justify-content: center;

      transition: 0.1s;

      white-space: nowrap;

      padding: 0 0.5em;
      height: 2.6em;
   }

   .menu-section {
      position: fixed;
      z-index: 500;

      width: 100%;

      border-radius: 0 0 10px 10px;
      width: fit-content;

      margin: 0 auto;
      left: 0;
      right: 0;


      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-evenly;

      overflow: hidden;

      background-color: var(--color-secondary);

      box-shadow: 0 0 10px 1px var(--color-primary);
   }

   .menu-section > a {
      color: var(--color-text);
      text-decoration: none;

      width: 100%;
      height: 100%;

      display: flex;
      align-items: center;
      justify-content: center;

      transition: 0.1s;

      white-space: nowrap;

      padding: 0 0.5em;
      height: 2.6em;
   }

   .menu-section > a:hover {
      background-color: var(--color-tertiary);
   }

   @media (max-width: 680px) {
      .navbar {
         height: 5.7em;
      }

      .sides-section {
         position: fixed;
         top: 2.6em;
      }

      .sides-section > section {
         width: 50%;
         height: 2.6em;
         
         border-width: 2px 0 0 0;
         border-color: var(--color-primary);
         border-style: solid;
      }

      .sides-section > section:first-child {
         /* border-radius: 0 0 10px 0; */
         border-radius: 0 0 0 0;
         box-shadow: none;

         border-width: 2px 2px 0 0;
      }

      .sides-section > section:last-child {
         /* border-radius: 0 0 0 10px; */
         border-radius: 0 0 0 0;
         box-shadow: none;
      }
      
      .menu-section {
         border-radius: 0 0 0 0;

         width: 100%;
      }
   }
</style>