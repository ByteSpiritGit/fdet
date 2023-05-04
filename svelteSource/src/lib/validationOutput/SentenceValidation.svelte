<script lang="ts">
    import { onMount } from "svelte";
    
    import EvidenceUrl from "./EvidenceURL.svelte";
    import PercentageBar from "./PercentageBar.svelte";

    export let claim: {
        claim: string;
        evidence: Array<string>;
        label: string;
        refutes: number;
        supports: number;
        nei: number;
        justify: string;
        url: Array<string>;
    };

    let urlEvidences;

    onMount(() => {
        claim.evidence.forEach((evidence, index) => {
            new EvidenceUrl({
                target: urlEvidences,
                props: {
                    url: claim.url[index],
                    evidence: evidence
                }
            });
        });
    });
</script>

<section class="output-validation-section border-top">
    <h3>{claim.claim}</h3>
    <p class="label">Label: {claim.label}</p>

    <PercentageBar
        supports={claim.supports}
        refutes={claim.refutes}
        nei={claim.nei}
    />
    <div class="evidence">
        <p>Justification:</p>
        <p>{claim.justify}</p>
    </div>

    <div class="evidence border-top smaller-text">
        <p>Evidence:</p>
        <div bind:this={urlEvidences}></div>
    </div>
</section>

<style>
    h3 {
        margin: 0;
        padding: 0;
    }

    p {
        margin: 0;
        padding: 0;
    }

    .border-top {
        border-top: 2px var(--color-tertiary-alpha) solid;
        margin-top: 0.5em;
    }

    .smaller-text {
        font-size: 0.9rem;
    }
</style>
