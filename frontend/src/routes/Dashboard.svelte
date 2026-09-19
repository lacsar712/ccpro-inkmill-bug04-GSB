<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '../lib/api';
  import type { DashboardStats } from '../lib/types';

  let data: DashboardStats | null = null;
  let error = '';
  let loading = true;

  onMount(async () => {
    try {
      data = await api<DashboardStats>('/dashboard');
    } catch (e) {
      error = e instanceof Error ? e.message : '加载失败';
    } finally {
      loading = false;
    }
  });
</script>

<header class="page-head">
  <h1>仪表盘</h1>
  <p>车间规模、在研机台与近 24h / 7 日台账概览</p>
</header>

{#if loading}
  <div class="muted">加载中…</div>
{:else if error}
  <div class="err">{error}</div>
{:else if data}
  <div class="grid">
    <article>
      <div class="k">车间数</div>
      <div class="v">{data.workshopTotal}</div>
    </article>
    <article>
      <div class="k">研磨中机台</div>
      <div class="v accent">{data.grindingMillCount}</div>
    </article>
    <article>
      <div class="k">近 24h 粘度取样</div>
      <div class="v">{data.samplesLast24h}</div>
    </article>
    <article>
      <div class="k">近 7 日研磨遍次</div>
      <div class="v">{data.passesLast7d}</div>
    </article>
  </div>
{/if}

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 1rem;
  }

  article {
    padding: 1.2rem 1.1rem;
    background: rgba(18, 18, 18, 0.85);
    border: 1px solid var(--line);
    border-top: 3px solid var(--ink-700);
  }

  article:nth-child(2) {
    border-top-color: var(--vermillion-700);
  }

  article:nth-child(3) {
    border-top-color: var(--paper);
  }

  .k {
    color: var(--steel);
    font-size: 0.85rem;
  }

  .v {
    margin-top: 0.55rem;
    font-family: var(--font-display);
    font-size: 2.4rem;
    letter-spacing: 0.04em;
  }

  .accent {
    color: var(--vermillion-400);
  }

  @media (max-width: 900px) {
    .grid {
      grid-template-columns: 1fr 1fr;
    }
  }
</style>
