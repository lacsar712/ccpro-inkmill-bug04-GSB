<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '../lib/api';
  import type { GrindPass, Mill } from '../lib/types';

  let rows: GrindPass[] = [];
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
    startedAt: nowLocal(),
    passNo: '1',
    durationMin: '30',
    mediaType: '0.8mm 锆珠',
    operatorName: '',
  };

  async function load() {
    error = '';
    try {
      [rows, mills] = await Promise.all([
        api<GrindPass[]>('/grind-passes'),
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
      startedAt: nowLocal(),
      passNo: '1',
      durationMin: '30',
      mediaType: '0.8mm 锆珠',
      operatorName: '',
    };
    editingId = null;
  }

  function toLocalInput(iso: string): string {
    const d = new Date(iso.replace(' ', 'T'));
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
    return d.toISOString().slice(0, 16);
  }

  function edit(row: GrindPass) {
    editingId = row.id;
    form = {
      millId: String(row.millId),
      startedAt: toLocalInput(row.startedAt),
      passNo: String(row.passNo),
      durationMin: String(row.durationMin),
      mediaType: row.mediaType,
      operatorName: row.operatorName,
    };
  }

  async function save() {
    error = '';
    const payload = {
      millId: Number(form.millId),
      startedAt: form.startedAt,
      passNo: Number(form.passNo),
      durationMin: Number(form.durationMin),
      mediaType: form.mediaType,
      operatorName: form.operatorName,
    };
    try {
      if (editingId) {
        await api(`/grind-passes/${editingId}`, {
          method: 'PUT',
          body: JSON.stringify(payload),
        });
      } else {
        await api('/grind-passes', { method: 'POST', body: JSON.stringify(payload) });
      }
      reset();
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : '保存失败';
    }
  }

  async function remove(id: number) {
    if (!confirm('确认删除该研磨遍次？')) return;
    try {
      await api(`/grind-passes/${id}`, { method: 'DELETE' });
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : '删除失败';
    }
  }
</script>

<header class="page-head">
  <h1>研磨遍次</h1>
  <p>遍次 ≥ 1，时长(分钟) &gt; 0，记录介质与操作员</p>
</header>

{#if error}
  <div class="err">{error}</div>
{/if}

<section class="panel">
  <h2>{editingId ? '编辑遍次' : '新增遍次'}</h2>
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
    <div class="field"><label>开始时间<input type="datetime-local" bind:value={form.startedAt} /></label></div>
    <div class="field"><label>遍次<input type="number" min="1" step="1" bind:value={form.passNo} /></label></div>
    <div class="field"><label>时长(分钟)<input type="number" min="0.01" step="0.01" bind:value={form.durationMin} /></label></div>
    <div class="field"><label>研磨介质<input bind:value={form.mediaType} /></label></div>
    <div class="field"><label>操作员<input bind:value={form.operatorName} /></label></div>
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
        <th>开始</th>
        <th>遍次</th>
        <th>分钟</th>
        <th>介质</th>
        <th>操作员</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      {#each rows as row}
        <tr>
          <td>{row.id}</td>
          <td>{millLabel(row.millId)}</td>
          <td>{row.startedAt}</td>
          <td>{row.passNo}</td>
          <td>{row.durationMin}</td>
          <td>{row.mediaType}</td>
          <td>{row.operatorName}</td>
          <td class="ops">
            <button class="link-btn" on:click={() => edit(row)}>编辑</button>
            <button class="link-btn danger" on:click={() => remove(row.id)}>删除</button>
          </td>
        </tr>
      {:else}
        <tr><td colspan="8">暂无数据</td></tr>
      {/each}
    </tbody>
  </table>
</section>
