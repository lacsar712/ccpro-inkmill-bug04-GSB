<script lang="ts">
  import { token, user, clearSession } from './lib/auth';
  import Login from './routes/Login.svelte';
  import Dashboard from './routes/Dashboard.svelte';
  import Workshops from './routes/Workshops.svelte';
  import Mills from './routes/Mills.svelte';
  import ViscositySamples from './routes/ViscositySamples.svelte';
  import GrindPasses from './routes/GrindPasses.svelte';

  type PageId = 'dashboard' | 'workshops' | 'mills' | 'samples' | 'passes';

  let page: PageId = 'dashboard';

  const nav: { id: PageId; label: string }[] = [
    { id: 'dashboard', label: '仪表盘' },
    { id: 'workshops', label: '车间' },
    { id: 'mills', label: '研磨机' },
    { id: 'samples', label: '粘度取样' },
    { id: 'passes', label: '研磨遍次' },
  ];

  function logout() {
    clearSession();
    page = 'dashboard';
  }
</script>

{#if !$token}
  <Login />
{:else}
  <div class="shell">
    <aside class="side">
      <div class="brand">
        <div class="mark">IM</div>
        <div>
          <div class="name">InkMill</div>
          <div class="tag">油墨研磨 · 粘度台账</div>
        </div>
      </div>
      <nav>
        {#each nav as item}
          <button class:active={page === item.id} on:click={() => (page = item.id)}>
            {item.label}
          </button>
        {/each}
      </nav>
      <div class="side-foot">
        <div class="who">{$user?.displayName || $user?.username}</div>
        <div class="role">{$user?.role}</div>
        <button class="ghost" on:click={logout}>退出</button>
      </div>
    </aside>
    <main class="main">
      {#if page === 'dashboard'}
        <Dashboard />
      {:else if page === 'workshops'}
        <Workshops />
      {:else if page === 'mills'}
        <Mills />
      {:else if page === 'samples'}
        <ViscositySamples />
      {:else}
        <GrindPasses />
      {/if}
    </main>
  </div>
{/if}

<style>
  .shell {
    display: grid;
    grid-template-columns: 240px 1fr;
    min-height: 100vh;
  }

  .side {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 1.5rem 1.1rem;
    border-right: 1px solid var(--line);
    background: linear-gradient(180deg, rgba(10, 10, 10, 0.98), rgba(18, 18, 18, 0.92));
  }

  .brand {
    display: flex;
    gap: 0.75rem;
    align-items: center;
    padding: 0.25rem 0.4rem 1rem;
    border-bottom: 1px solid var(--line);
  }

  .mark {
    width: 42px;
    height: 42px;
    display: grid;
    place-items: center;
    font-family: var(--font-display);
    font-weight: 600;
    letter-spacing: 0.04em;
    color: var(--paper);
    background: linear-gradient(135deg, var(--vermillion-900), var(--vermillion-700));
    clip-path: polygon(8% 0, 100% 0, 92% 100%, 0 100%);
  }

  .name {
    font-family: var(--font-display);
    font-size: 1.35rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .tag {
    font-size: 0.75rem;
    color: var(--vermillion-400);
    margin-top: 0.15rem;
  }

  nav {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    flex: 1;
  }

  nav button {
    text-align: left;
    border: 1px solid transparent;
    background: transparent;
    color: var(--steel);
    padding: 0.7rem 0.85rem;
    cursor: pointer;
    border-radius: 2px;
    transition: 0.15s ease;
  }

  nav button:hover {
    background: rgba(192, 57, 43, 0.15);
    color: white;
  }

  nav button.active {
    background: linear-gradient(90deg, rgba(139, 37, 0, 0.35), rgba(192, 57, 43, 0.12));
    border-color: rgba(231, 76, 60, 0.45);
    color: white;
  }

  .side-foot {
    padding-top: 1rem;
    border-top: 1px solid var(--line);
    font-size: 0.85rem;
  }

  .who {
    font-weight: 500;
  }

  .role {
    color: var(--vermillion-400);
    margin: 0.2rem 0 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-size: 0.72rem;
  }

  .ghost {
    width: 100%;
    border: 1px solid var(--line);
    background: transparent;
    color: var(--steel);
    padding: 0.55rem;
    cursor: pointer;
  }

  .ghost:hover {
    border-color: var(--vermillion-700);
    color: white;
  }

  .main {
    padding: 1.75rem 2rem 2.5rem;
    overflow: auto;
  }

  @media (max-width: 860px) {
    .shell {
      grid-template-columns: 1fr;
    }
    .side {
      border-right: none;
      border-bottom: 1px solid var(--line);
    }
    nav {
      flex-direction: row;
      flex-wrap: wrap;
    }
  }
</style>
