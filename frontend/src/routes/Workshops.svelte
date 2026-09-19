<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '../lib/api';
  import type { Workshop } from '../lib/types';

  let rows: Workshop[] = [];
  let error = '';
  let form = { name: '', site: '', notes: '' };
  let editingId: number | null = null;

  async function load() {
    error = '';
    try {
      rows = await api<Workshop[]>('/workshops');
    } catch (e) {
      error = e instanceof Error ? e.message : '加载失败';
    }
  }

  onMount(load);

  function reset() {
    form = { name: '', site: '', notes: '' };
    editingId = null;
  }

  function edit(row: Workshop) {
    editingId = row.id;
    form = {
      name: row.name || '',
      site: row.site || '',
      notes: row.notes || '',
    };
  }

  async function save() {
    error = '';
    try {
      if (editingId) {
        await api(`/workshops/${editingId}`, {
          method: 'PUT',
          body: JSON.stringify(form),
        });
      } else {
        await api('/workshops', {
          method: 'POST',
          body: JSON.stringify(form),
        });
      }
      reset();
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : '保存失败';
    }
  }

  async function remove(id: number) {
    if (!confirm('确认删除该车间？关联研磨机将一并删除。')) return;
    try {
      await api(`/workshops/${id}`, { method: 'DELETE' });
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : '删除失败';
    }
  }
</script>

<header class="page-head">
  <h1>车间</h1>
  <p>油墨研磨车间基础信息（非仓库库存）</p>
</header>

{#if error}
  <div class="err">{error}</div>
{/if}

<section class="panel">
  <h2>{editingId ? '编辑车间' : '新增车间'}</h2>
  <div class="fields">
    <div class="field"><label>名称<input bind:value={form.name} /></label></div>
    <div class="field"><label>厂区/位置<input bind:value={form.site} /></label></div>
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
        <th>名称</th>
        <th>位置</th>
        <th>备注</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      {#each rows as row}
        <tr>
          <td>{row.id}</td>
          <td>{row.name}</td>
          <td>{row.site || '—'}</td>
          <td>{row.notes || '—'}</td>
          <td class="ops">
            <button class="link-btn" on:click={() => edit(row)}>编辑</button>
            <button class="link-btn danger" on:click={() => remove(row.id)}>删除</button>
          </td>
        </tr>
      {:else}
        <tr><td colspan="5">暂无数据</td></tr>
      {/each}
    </tbody>
  </table>
</section>
