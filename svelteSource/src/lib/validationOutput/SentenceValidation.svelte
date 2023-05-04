<script lang="ts">
    import PercentageBar from "./PercentageBar.svelte";

    export let claim: {
        claim: string;
        evidence: string;
        label: string;
        refutes: number;
        supports: number;
        nei: number;
        justify: string;
        url: Array<string>;
        is_error: boolean;
    };

    let highlight: string;

    if (!claim.is_error) {
        const splitedEv = claim.evidence.split("=").slice(-1).toString().split(" ");
        const firstPiece = splitedEv.slice(0, splitedEv.length/4).join(" ");
        const secondPiece = splitedEv.slice(-splitedEv.length/4).join(" ");
    
        highlight = `${firstPiece.replace(/^\s/, "")}, ${secondPiece}`;
    }
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
        {#each claim.url as url}
            {#if claim.is_error}
                <a class="evidence-url" href={`${url}#${claim.evidence}`}>
                    {url.split("/").slice(-1)}...
                </a>
            {:else}
                <a class="evidence-url" href={`${url}#:~:text=${highlight}`}>
                    {url.split("/").slice(-1)}...
                </a>
            {/if}
        {/each}
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

    .evidence-url {
        background-color: var(--color-tertiary-alpha);
        border-radius: 0.35em;
        color: var(--color-text);
        padding: 0.1em;
        text-decoration: none;

        transition: 0.4s;

        margin-right: 0.5em;
    }

    .evidence-url:hover {
        background-color: var(--color-tertiary);
        text-decoration: dotted underline;
    }
</style>
