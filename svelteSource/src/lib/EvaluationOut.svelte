<script lang="ts">
    export let evaluedStatement;
</script>

<section class="evaluation">
    <b>Claim:</b> {evaluedStatement.claim} (ID: {evaluedStatement.id})<br/>
    <b>Label:</b> {evaluedStatement.label}<br/>
    <b>Supports:</b> {(evaluedStatement.supports * 100).toFixed(2)}%<br/>
    <b>Refutes:</b> {(evaluedStatement.refutes * 100).toFixed(2) }%<br/>
    <b>Evidence:</b> <br/>{evaluedStatement.evidence}<br/>
</section>

