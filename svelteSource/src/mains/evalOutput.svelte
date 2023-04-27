<script lang="ts">
   import Navbar from "../lib/Navbar.svelte";
   import Footer from "../lib/Footer.svelte";
   import Loading from "../lib/Loading.svelte";
   import ClaimBlock from "../lib/validationOutput/ClaimBlock.svelte";
   import Warning from "../lib/notifications/Warning.svelte";
   import Button from "../lib/Button.svelte";
   import NotificationBlock from "../lib/notifications/NotificationBlock.svelte";

   import sendImg from "../assets/icons/send.png";

   import { onMount } from "svelte";

   let evalued: Array<{
      claim: string;
      evidence: string;
      label: string;
      refutes: number;
      supports: number;
      nei: number;
      justify: string;
   }>;

   function getCsrfToken() {
      var xhr = new XMLHttpRequest();
      // Set up a callback function to handle the response
      xhr.onreadystatechange = function () {
         if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
               try {
                  document.cookie =
                     "csrftoken=" +
                     encodeURIComponent(
                        JSON.parse(xhr.responseText).csrf_token
                     ) +
                     "; path=/";
               } catch (error) {
                  console.log(error);
               }
            } else {
               console.log("Request failed");
            }
         }
      };

      xhr.open("GET", "/csrf_view");
      xhr.send();
   }

   function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
         const cookies = document.cookie.split(";");
         for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
               cookieValue = decodeURIComponent(
                  cookie.substring(name.length + 1)
               );
               break;
            }
         }
      }
      return cookieValue;
   }

   async function getEvaluated(text: string, type = "") {
      let url: string;

      if (window.sessionStorage.getItem("evalued") && !text) {
         console.log("from sessionStorage");
         return JSON.parse(window.sessionStorage.getItem("evalued"));
      }

      switch (type) {
         case "Dummy":
            url = `/dummy?text=${text}`;
            break;
         case "Evaluation":
            url = `/rag_evaluation?text=${text}`;
            break;
         case "NoServer":
            // return [
            //    {
            //       "claim": "The sky is blue",
            //       "label": "Supports",
            //       "supports": 85.0,
            //       "refutes": 15.0,
            //       "evidence": "The sky appears blue due to the scattering of light."
            //    },
            //    {
            //       "claim": "Humans need water to survive",
            //       "label": "Supports",
            //       "supports": 2.0,
            //       "refutes": 98.0,
            //       "evidence": "Water is essential for many bodily functions, including regulating body temperature and transporting nutrients."
            //    },
            //    {
            //       "claim": "All birds can fly",
            //       "label": "Refutes",
            //       "supports": 20.0,
            //       "refutes": 80.0,
            //       "evidence": "Some birds, such as ostriches and penguins, are flightless."
            //    },
            //    {
            //       "claim": "The moon is made of cheese",
            //       "label": "Refutes",
            //       "supports": 0.0,
            //       "refutes": 100.0,
            //       "evidence": "This is a myth and has been debunked by scientific studies."
            //    },
            //    {
            //       "claim": "Electric cars are better for the environment than gas cars",
            //       "label": "Supports",
            //       "supports": 95.0,
            //       "refutes": 5.0,
            //       "evidence": "Electric cars produce less greenhouse gas emissions and have lower operating costs than gas cars."
            //    },
            //    {
            //       "claim": "The earth is flat",
            //       "label": "Refutes",
            //       "supports": 0.0,
            //       "refutes": 100.0,
            //       "evidence": "This claim has been debunked by scientific evidence and observations, including satellite imagery."
            //    },
            //    {
            //       "claim": "Exercise is good for your health",
            //       "label": "Supports",
            //       "supports": 100.0,
            //       "refutes": 0.0,
            //       "evidence": "Regular exercise has been shown to improve physical and mental health."
            //    },
            //    {
            //       "claim": "Cats are better pets than dogs",
            //       "label": "Refutes",
            //       "supports": 30.0,
            //       "refutes": 70.0,
            //       "evidence": "This is subjective and depends on individual preferences and lifestyle."
            //    },
            //    {
            //       "claim": "The earth revolves around the sun",
            //       "label": "Supports",
            //       "supports": 100.0,
            //       "refutes": 0.0,
            //       "evidence": "This has been proven by scientific observations and experiments."
            //    },
            //    {
            //       "claim": "Chocolate is bad for dogs",
            //       "label": "Supports",
            //       "supports": 90.0,
            //       "refutes": 10.0,
            //       "evidence": "Chocolate contains theobromine, which is toxic to dogs and can cause various health problems."
            //    },
            //    {
            //       "claim": "Climate change is a hoax",
            //       "label": "Refutes",
            //       "supports": 5.0,
            //       "refutes": 95.0,
            //       "evidence": "This claim has been widely debunked by scientific studies and evidence."
            //    },
            //    {
            //       "claim": "The Great Wall of China is visible from space",
            //       "label": "Refutes",
            //       "supports": 0.0,
            //       "refutes": 100.0,
            //       "evidence": "This is a common misconception, but scientific studies and observations have shown that the Great Wall of China is not visible from space without aid."
            //    }
            // ];

            return [
               {
                  claim: "Vaccines do not cause autism",
                  evidence:
                     "Numerous studies have shown that there is no link between vaccines and autism. The original study that suggested a link has been discredited and retracted by the journal that published it.",
                  label: "Supports",
                  refutes: 0.1,
                  supports: 0.9,
                  nei: 0,
                  justify:
                     "The overwhelming majority of scientific evidence shows that there is no link between vaccines and autism. This includes large-scale studies involving millions of children, as well as reviews by independent expert panels. The original study that suggested a link has been widely discredited and retracted by the journal that published it.",
               },
               {
                  claim: "Vaccines are not effective",
                  evidence:
                     "Vaccines have been proven to be highly effective at preventing infectious diseases. For example, the measles vaccine has been estimated to prevent 13.3 million deaths worldwide between 2000 and 2018.",
                  label: "Refutes",
                  refutes: 0.8,
                  supports: 0.1,
                  nei: 0.1,
                  justify:
                     "Numerous studies have shown that vaccines are highly effective at preventing infectious diseases. For example, the measles vaccine has been estimated to prevent 13.3 million deaths worldwide between 2000 and 2018. Vaccines have also been instrumental in eradicating diseases like smallpox and nearly eradicating others like polio.",
               },
               {
                  claim: "Vaccines are dangerous and can cause serious side effects",
                  evidence:
                     "Vaccines are rigorously tested and monitored for safety. Serious side effects are rare and typically outweighed by the benefits of vaccination in preventing serious illness and death.",
                  label: "Refutes",
                  refutes: 0.7,
                  supports: 0.15,
                  nei: 0.15,
                  justify:
                     "Vaccines are one of the most rigorously tested and monitored medical interventions. The vast majority of people who receive vaccines experience only mild side effects, such as soreness at the injection site or a low-grade fever. Serious side effects are rare and typically outweighed by the benefits of vaccination in preventing serious illness and death.",
               },
               {
                  claim: "Vaccines are not necessary because diseases are no longer a threat",
                  evidence:
                     "Vaccine-preventable diseases are still a threat in many parts of the world, and outbreaks can occur when vaccination rates drop. For example, there have been recent outbreaks of measles in several countries including the United States and Europe.",
                  label: "Refutes",
                  refutes: 0.7,
                  supports: 0.2,
                  nei: 0.1,
                  justify:
                     "Vaccine-preventable diseases are still a threat in many parts of the world, and outbreaks can occur when vaccination rates drop. For example, there have been recent outbreaks of measles in several countries including the United States and Europe. Vaccines have been instrumental in reducing the incidence of many serious infectious diseases and have saved countless lives.",
               },
               {
                  claim: "Vaccines can cause the disease they are intended to prevent",
                  evidence:
                     "Vaccines do not contain live viruses or bacteria for the diseases they are intended to prevent, so they cannot cause the disease. Some vaccines do contain weakened or inactivated forms of the virus or bacteria, but these are not capable of causing the disease.",
                  label: "Supports",
                  refutes: 0.05,
                  supports: 0.95,
                  nei: 0,
                  justify:
                     "This claim is a common misconception about vaccines. In reality, vaccines do not contain live viruses or bacteria for the diseases they are intended to prevent, so they cannot cause the disease. Some vaccines do contain weakened or inactivated forms of the virus or bacteria, but these are not capable of causing the disease. The side effects of vaccines are usually mild and temporary, such as soreness or redness at the injection site or a low-grade fever.",
               },
               {
                  claim: "Vaccines are only for children",
                  evidence:
                     "While childhood vaccination is important, vaccines are also recommended and available for adults. Some vaccines, such as the flu vaccine, are recommended for all adults, while others are recommended for specific groups based on age, occupation, travel plans, or other factors.",
                  label: "Supports",
                  refutes: 0.2,
                  supports: 0.7,
                  nei: 1,
                  justify:
                     "While childhood vaccination is important, vaccines are also recommended and available for adults. Some vaccines, such as the flu vaccine, are recommended for all adults, while others are recommended for specific groups based on age, occupation, travel plans, or other factors. Vaccination is an important part of protecting public health and preventing the spread of infectious diseases.",
               },
               {
                  claim: "Natural immunity is better than vaccine-induced immunity",
                  evidence:
                     "While natural immunity can provide protection against some diseases, it is not always as effective or long-lasting as vaccine-induced immunity. Additionally, getting vaccinated can prevent serious complications or death from vaccine-preventable diseases.",
                  label: "Refutes",
                  refutes: 0.6,
                  supports: 0.1,
                  nei: 0.3,
                  justify:
                     "While natural immunity can provide protection against some diseases, it is not always as effective or long-lasting as vaccine-induced immunity. Additionally, getting vaccinated can prevent serious complications or death from vaccine-preventable diseases. It is important to follow the recommended vaccination schedule to ensure adequate protection against infectious diseases.",
               },
               {
                  claim: "Vaccines contain dangerous chemicals",
                  evidence:
                     "Vaccines do contain some chemicals, but these are used to enhance the effectiveness and safety of the vaccine. The chemicals in vaccines are carefully evaluated for safety and are used in very small amounts.",
                  label: "Supports",
                  refutes: 0.15,
                  supports: 0.7,
                  nei: 0.25,
                  justify:
                     "Vaccines do contain some chemicals, but these are used to enhance the effectiveness and safety of the vaccine. The chemicals in vaccines are carefully evaluated for safety and are used in very small amounts. In fact, many of the chemicals found in vaccines are also present in everyday foods and consumer products.",
               },
               {
                  claim: "Vaccines are a plot by pharmaceutical companies to make money",
                  evidence:
                     "Vaccines are developed and recommended by independent organizations, such as the Centers for Disease Control and Prevention and the World Health Organization. While pharmaceutical companies do produce vaccines, they are subject to strict regulation and are required to provide evidence of safety and effectiveness before they can be approved for use.",
                  label: "Refutes",
                  refutes: 0.8,
                  supports: 0.1,
                  nei: 0.1,
                  justify:
                     "Vaccines are developed and recommended by independent organizations, such as the Centers for Disease Control and Prevention and the World Health Organization. While pharmaceutical companies do produce vaccines, they are subject to strict regulation and are required to provide evidence of safety and effectiveness before they can be approved for use. Vaccination is an important part of protecting public health and preventing the spread of infectious diseases.",
               },
            ];
         default:
            url = `/evaluation?text=${text}`;
            break;
      }

      const csrftoken = getCookie("csrftoken");

      const request = new Request(url, {
         method: "POST",
         headers: { "X-CSRFToken": csrftoken },
         mode: "same-origin",
      });

      try {
         const response = (await (await fetch(request)).json()).validated;
         return response;
      } catch (error) {
         console.log(error);

         return null;
      }
   }

   async function evaluate(text: string) {
      if (text) {
         evalued = await getEvaluated(text, "Evaluation");
         window.sessionStorage.setItem("evalued", JSON.stringify(evalued));
      } else {
         evalued = await getEvaluated(text, "NoServer");
      }

      const urlParams = new URLSearchParams(window.location.search);
      urlParams.delete("text");
      window.history.replaceState(
         {},
         "",
         `${window.location.pathname}?${urlParams}`
      );
   }

   onMount(() => {
      let text: string;
      if (new URLSearchParams(window.location.search).get("text")) {
         text = new URLSearchParams(window.location.search).get("text");
      }

      getCsrfToken();
      evaluate(text);
   });

   let toEvaluate;

   let textarea;

   let warnings;
   let buttonDisabled: boolean = false;

   function whenclk() {

   }

   function checkSize() {
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
   }
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

   <section class="input-section">
      <div class="input-wrapper">
         <textarea
            bind:this={textarea}
            on:input={checkSize}
            on:paste={checkSize}
            class="input"
            placeholder="Paste your statement here"
            bind:value={toEvaluate}
         />
         <Button
            text={sendImg}
            whenClicked={whenclk}
            disabled={buttonDisabled}
            isIcon={true}
         />
      </div>
   </section>

   <Footer />
   <NotificationBlock bind:theComponent={warnings} notificationNumber={1} />
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

   .input-section {
      position: fixed;

      bottom: 50px;
      left: 0;

      width: 100%;
      height: fit-content;

      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;

      height: fit-content;
      background-color: var(--color-secondary);

      margin-top: 75px;

      padding: 20px;

      border-top: 3px solid var(--color-primary-alpha);
   }

   .input-wrapper {
      display: flex;
      flex-direction: row;
      align-items: flex-end;
      justify-content: space-evenly;

      width: 100%;
      height: fit-content;
      max-width: 700px;
      max-height: 200px;

      border-radius: 10px;

      padding: 0.5em;

      background-color: var(--color-primary);
   }

   .input-section > .input-wrapper > .input {
      background-color: var(--color-primary);
      color: var(--color-text);

      max-width: 700px;
      width: 100%;

      max-height: 180px;

      border: none;
      border-radius: 10px;
      font-size: 1.2em;
      font-weight: 500;
      text-transform: uppercase;
      cursor: text;

      /* margin-bottom: 20px; */
      padding: 5px;
      margin-right: 5px;

      resize: none;
      text-transform: none;
   }

   .input:focus {
      /* outline: var(--color-tertiary) solid 2px; */
      outline: none;
   }
</style>
