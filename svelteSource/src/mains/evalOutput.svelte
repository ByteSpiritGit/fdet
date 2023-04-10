
<script lang="ts">
   import Navbar from "../lib/Navbar.svelte";
   import Footer from "../lib/Footer.svelte";
   import Loading from "../lib/Loading.svelte";
   import ClaimBlock from "../lib/validationOutput/ClaimBlock.svelte";
   import Warning from "../lib/Warning.svelte";

   let loading: boolean;
   let evalued: Array<{
      claim: string,
      evidence: string,
      label: string,
      refutes: number,
      supports: number
   }>;

   function getCsrfToken() {
      var xhr = new XMLHttpRequest();
   
      // Set up a callback function to handle the response
      xhr.onreadystatechange = function () {
         if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
               // Save the response text as a cookie
               document.cookie = "csrftoken=" + encodeURIComponent(JSON.parse(xhr.responseText).csrf_token) + "; path=/";
            } else {
               console.log("Request failed");
            }
         }
      };
   
      // Open a new request with the GET method and a URL
      xhr.open("GET", "http://127.0.0.1:8000/csrf_view");
   
      // Send the request
      xhr.send();
   }
   // getCsrfToken();
   
   function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
         const cookies = document.cookie.split(';');
         for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
            }
         }
      }
      return cookieValue;
   }

   async function getEvaluated(type="") {
      let url: string;

      switch (type) {
         case "Dummy":
            url = `/dummy?text=${(new URLSearchParams(window.location.search)).get("text")}`;
            break;
         case "Evaluation":
            url = `/evaluation?text=${(new URLSearchParams(window.location.search)).get("text")}`;
            break;
         case "NoServer":
            return [
               {"claim": "The world is flat", "label": "Refutes", "supports": 0.0, "refutes": 1.0, "evidence": "The world is round"}, 
               {"claim": "The world is round", "label": "Supports", "supports": 1.0, "refutes": 0.0, "evidence": "The world is round"}
            ];
         default:
            url = `/evaluation?text=${(new URLSearchParams(window.location.search)).get("text")}`;
            break;
      }
      
      const csrftoken = getCookie('csrftoken');

      const request = new Request(
         url, 
         {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin'
         }
      );

      try {
         const response = (await (await fetch(request)).json()).validated;
         return response;
      }
      catch (error) {
         console.log(error);

         return null;
      }
   }

   async function evaluate() {
      evalued = await getEvaluated("NoServer");

      console.log(evalued);
   }
   evaluate();
</script>

<section>
   <Navbar />

   {#if evalued}
      <ClaimBlock claims={evalued} />
   {:else if !evalued}
      <div class="loading">
         <Loading />
         <p>Calculating the universe</p>
      </div>
   {/if}

   <Footer />
</section>

<style>
   .loading {
      position: fixed;
      top: 48%;
      left: 50%;
      transform: translate(-50%, -50%);

      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
   }

   .loading > p {
      font-size: 1.2em;
      font-weight: 500;
      color: var(--color-text);

      margin-top: 0px;
      animation: loading 2s ease-in infinite;
   }

   @keyframes loading {
      0% {
         opacity: 0.6;
      }
      50% {
         opacity: 1;
      }
      100% {
         opacity: 0.6;
      }
   }
</style>