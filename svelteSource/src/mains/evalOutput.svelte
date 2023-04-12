<script lang="ts">
   import Navbar from "../lib/Navbar.svelte";
   import Footer from "../lib/Footer.svelte";
   import Loading from "../lib/Loading.svelte";
   import ClaimBlock from "../lib/validationOutput/ClaimBlock.svelte";
   import Warning from "../lib/notifications/Warning.svelte";

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

      if (!(new URLSearchParams(window.location.search).get("text")) && (new URLSearchParams(window.location.search).get("evalued"))) {
         const fromBase64 = atob((new URLSearchParams(window.location.search)).get("evalued"));
         console.log(decodeURIComponent(fromBase64));
         console.log("From base64")
         return JSON.parse(decodeURIComponent(fromBase64));
      }

      switch (type) {
         case "Dummy":
            url = `/dummy?text=${(new URLSearchParams(window.location.search)).get("text")}`;
            break;
         case "Evaluation":
            url = `/evaluation?text=${(new URLSearchParams(window.location.search)).get("text")}`;
            break;
         case "NoServer":
            return [
               {
                  "claim": "The sky is blue",
                  "label": "Supports",
                  "supports": 85.0,
                  "refutes": 15.0,
                  "evidence": "The sky appears blue due to the scattering of light."
               },
               {
                  "claim": "Humans need water to survive",
                  "label": "Supports",
                  "supports": 100.0,
                  "refutes": 0.0,
                  "evidence": "Water is essential for many bodily functions, including regulating body temperature and transporting nutrients."
               },
               {
                  "claim": "All birds can fly",
                  "label": "Refutes",
                  "supports": 20.0,
                  "refutes": 80.0,
                  "evidence": "Some birds, such as ostriches and penguins, are flightless."
               },
               {
                  "claim": "The moon is made of cheese",
                  "label": "Refutes",
                  "supports": 0.0,
                  "refutes": 100.0,
                  "evidence": "This is a myth and has been debunked by scientific studies."
               },
               {
                  "claim": "Electric cars are better for the environment than gas cars",
                  "label": "Supports",
                  "supports": 95.0,
                  "refutes": 5.0,
                  "evidence": "Electric cars produce less greenhouse gas emissions and have lower operating costs than gas cars."
               },
               {
                  "claim": "The earth is flat",
                  "label": "Refutes",
                  "supports": 0.0,
                  "refutes": 100.0,
                  "evidence": "This claim has been debunked by scientific evidence and observations, including satellite imagery."
               },
               {
                  "claim": "Exercise is good for your health",
                  "label": "Supports",
                  "supports": 100.0,
                  "refutes": 0.0,
                  "evidence": "Regular exercise has been shown to improve physical and mental health."
               },
               {
                  "claim": "Cats are better pets than dogs",
                  "label": "Refutes",
                  "supports": 30.0,
                  "refutes": 70.0,
                  "evidence": "This is subjective and depends on individual preferences and lifestyle."
               },
               {
                  "claim": "The earth revolves around the sun",
                  "label": "Supports",
                  "supports": 100.0,
                  "refutes": 0.0,
                  "evidence": "This has been proven by scientific observations and experiments."
               },
               {
                  "claim": "Chocolate is bad for dogs",
                  "label": "Supports",
                  "supports": 90.0,
                  "refutes": 10.0,
                  "evidence": "Chocolate contains theobromine, which is toxic to dogs and can cause various health problems."
               },
               {
                  "claim": "Climate change is a hoax",
                  "label": "Refutes",
                  "supports": 5.0,
                  "refutes": 95.0,
                  "evidence": "This claim has been widely debunked by scientific studies and evidence."
               },
               {
                  "claim": "The Great Wall of China is visible from space",
                  "label": "Refutes",
                  "supports": 0.0,
                  "refutes": 100.0,
                  "evidence": "This is a common misconception, but scientific studies and observations have shown that the Great Wall of China is not visible from space without aid."
               }
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
      evalued = await getEvaluated("Evaluation");
      console.log(evalued);

      const urlParams = new URLSearchParams(window.location.search);
      urlParams.delete("text");
      const base64Objects = btoa(encodeURI(JSON.stringify(evalued)));
      urlParams.set('evalued', base64Objects);
      window.history.replaceState({}, '', `${window.location.pathname}?${urlParams}`);

      // console.log(btoa(JSON.stringify(evalued)))

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
