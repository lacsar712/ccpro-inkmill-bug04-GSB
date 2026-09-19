<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '../lib/api';
  import type { Mill, ViscositySample } from '../lib/types';

  let rows: ViscositySample[] = [];
  let mills: Mill[] = [];
  let error = '';
  let editingId: number | null = null;

  function nowLocal(): string {
    const d = new Date();
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
    return d.toISOString().slice(0, 16);
  }

  let form = {
    millId: '',
    sampledAt: nowLocal(),
    viscosityPaS: '10',
    tempC: '',
    notes: '',
  };

  async function load() {
    error = '';
    try {
      [rows, mills] = await Promise.all([
        api<ViscositySample[]>('/viscosity-samples'),
        api<Mill[]>('/mills'),
      ]);
      if (!form.millId && mills[0]) form.millId = String(mills[0].id);
    } catch (e) {
      error = e instanceof Error ? e.message : '加载失败';
    }
  }

  onMount(load);

  function millLabel(id: number): string {
    const m = mills.find((x) => x.id === id);
    return m ? `${m.millCode} (#${m.id})` : `#${id}`;
  }

  function reset() {
    form = {
      millId: mills[0] ? String(mills[0].id) : '',
      sampledAt: nowLocal(),
      viscosityPaS: '10',
      tempC: '',
      notes: '',
    };
    editingId = null;
  }

  function toLocalInput(iso: string): string {
    const d = new Date(iso.replace(' ', 'T'));
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
    return d.toISOString().slice(0, 16);
  }

  function edit(row: ViscositySample) {
    editingId = row.id;
    form = {
      millId: String(row.millId),
      sampledAt: toLocalInput(row.sampledAt),
      viscosityPaS: String(row.viscosityPaS),
      tempC: row.tempC != null ? String(row.tempC) : '',
      notes: row.notes || '',
    };
  }

  async function save() {
    error = '';
    const payload = {
      millId: Number(form.millId),
      sampledAt: form.sampledAt,
      viscosityPaS: Number(form.viscosityPaS),
      tempC: form.tempC === '' ? null : Number(form.tempC),
      notes: form.notes,
    };
    try {
      if (editingId) {
        await api(`/viscosity-samples/${editingId}`, {
          method: 'PUT',
          body: JSON.stringify(payload),
        });
      } else {
        await api('/viscosity-samples', { method: 'POST', body: JSON.stringify(payload) });
      }
      reset();
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : '保存失败';
    }
  }

  async function remove(id: number) {
    if (!confirm('确认删除该粘度取样记录？')) return;
    try {
      await api(`/viscosity-samples/${id}`, { method: 'DELETE' });
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : '删除失败';
    }
  }
</script>

<header class="page-head">
  <h1>粘度取样</h1>
  <p>记录 Pa·s 粘度（必须 &gt; 0），配合温度与备注</p>
</header>

{#if error}
  <div class="err">{error}</div>
{/if}

<section class="panel">
  <h2>{editingId ? '编辑取样' : '新增取样'}</h2>
  <div class="fields">
    <div class="field">
      <label>研磨机
        <select bind:value={form.millId}>
          {#each mills as m}
            <option value={String(m.id)}>{m.millCode}</option>
          {/each}
        </select>
      </label>
    </div>
    <div class="field"><label>取样时间<input type="datetime-local" bind:value={form.sampledAt} /></label></div>
    <div class="field"><label>粘度 Pa·s<input type="number" step="0.0001" min="0.0001" bind:value={form.viscosityPaS} /></label></div>
    <div class="field"><label>温度 ℃<input type="number" step="0.1" bind:value={form.tempC} /></label></div>
    <div class="field full"><label>备注<textarea rows="2" bind:value={form.notes} /></label></div>
  </div>
  <div class="actions">
    <button class="btn-primary" on:click={save}>{editingId ? '保存' : '创建'}</button>
    {#if editingId}
      <button class="btn-ghost" on:click={reset}>取消</button>
    {/if}
  </div>
</section>

<section class="panel">
  <table class="data-table">
    <thead>
      <tr>
        <th>ID</th>
        <th>研磨机</th>
        <th>取样时间</th>
        <th>Pa·s</th>
        <th>℃</th>
        <th>备注</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      {#each rows as row}
        <tr>
          <td>{row.id}</td>
          <td>{millLabel(row.millId)}</td>
          <td>{row.sampledAt}</td>
          <td>{row.viscosityPaS}</td>
          <td>{row.tempC ?? '—'}</td>
          <td>{row.notes || '—'}</td>
          <td class="ops">
            <button class="link-btn" on:click={() => edit(row)}>编辑</button>
            <button class="link-btn danger" on:click={() => remove(row.id)}>删除</button>
          </td>
        </tr>
      {:else}
        <tr><td colspan="7">暂无数据</td></tr>
      {/each}
    </tbody>
  </table>
</section>
