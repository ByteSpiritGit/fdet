<section>
   <nav class="navbar">
      <section class="logo-section">
         <a href="/#/evaluations">Logo</a>
      </section>
      <section class="menu-section">
         <a href="/">Home</a>
         <a href="/evaluation?text=The sky is blue">About us</a>
         <a href="/#/login">Learn</a>
         <a href="/#/register">History</a>
      </section>
      <section class="profile-section">
         <a href="/#/login">Login</a>
         <a href="/#/register">Register</a>
      </section>
   </nav>

   <section class="title-section">
      <h1>Fake statement detector powered by AI</h1>
   </section>
</section>

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
      justify-content: space-evenly;

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
   }

   .menu-section {
      border-radius: 0 0 10px 10px;
      flex-basis: calc(100% / 4);
      min-width: 390px;
   }

   .navbar > .profile-section {
      border-radius: 0 0 0 10px;
      width: 230px;

      display: flex;
      flex-direction: column;
      align-items: start;
   }

   .navbar > .profile-section > a {
      height: 50%;
      width: fit-content;      
   }

   .logo-section {
      border-radius: 0 0 10px 0;
      width: 150px;
   }

   .navbar > .menu-section > a:hover {
      background-color: var(--color-tertiary);
   }

   /* title section */
   .title-section {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;


   }
</style>