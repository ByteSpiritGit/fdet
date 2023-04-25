<script lang="ts">
   import Login from "../mains/Login.svelte";

   function showProfile() {
      
   }
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
            <!-- <img src="/assets/logo.png" alt="logo" width="50px" height="50px"> -->
            **logo**
         </a>
      </section>
      <section class="profile-section">
         <a href="/#/login" on:click={showProfile}>**profile**</a>
      </section>
   </section>
</nav>


<style>
   .navbar {
      position: absolute;
      top: 0;

      width: 100%;

      font-size: 1.2em;
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
      .sides-section {
         position: fixed;
         top: 2.6em;
      }
      .sides-section > section:first-child {
         border-radius: 0 0 10px 0;
      }

      .sides-section > section:last-child {
         border-radius: 0 0 0 10px;
      }
      
      .menu-section {
         border-radius: 0 0 0 0;

         width: 100%;
      }
   }
</style>

<!-- 
<style>
   @import "../main.css";

   .navbar {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-between;

      font-size: 1.2em;
      font-weight: 500;
      text-transform: uppercase;

      height: 55px;
   }

   .navbar > section {
      background-color: var(--color-secondary);
      height: 100%;

      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: baseline;

      overflow: hidden;
   }

   .navbar > section > a {
      color: var(--color-text);
      text-decoration: none;

      width: 100%;
      height: 100%;

      display: flex;
      align-items: center;
      justify-content: center;

      transition: 0.1s;
   }

   .menu-section {
      border-radius: 0 0 10px 10px;
      width: fit-content;
      min-width: 440px;
   }

   .menu-section > a {
      padding: 0 20px;
      white-space: nowrap;
   }

   .navbar > .profile-section {
      border-radius: 0 0 0 10px;
      width: 180px;
   }

   .logo-section {
      border-radius: 0 0 10px 0;
      width: 180px;
   }

   .navbar > .menu-section > a:hover {
      background-color: var(--color-tertiary);
   }
</style> -->