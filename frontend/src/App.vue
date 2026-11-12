<script setup>
import { ref, onMounted } from 'vue'

const estado = ref(null)
const error = ref('')
const cargando = ref(false)

async function verificar() {
  cargando.value = true
  error.value = ''
  try {
    const res = await fetch('/api/health')
    if (!res.ok) throw new Error(`La API respondió ${res.status}`)
    estado.value = await res.json()
  } catch (e) {
    estado.value = null
    error.value = 'No se pudo conectar con la API. ¿Está corriendo el contenedor "api"?'
  } finally {
    cargando.value = false
  }
}

onMounted(verificar)
</script>

<template>
  <header class="barra">
    <strong>Instech</strong>
    <span>Inventario de activos TI</span>
  </header>

  <main class="contenido">
    <h1>Estado del sistema</h1>
    <p class="sub">Comprobación de las 3 capas: interfaz (Vue) → API (FastAPI) → base de datos (PostgreSQL).</p>

    <section class="tarjetas">
      <article class="tarjeta">
        <h2>Interfaz</h2>
        <p class="ok">● Funcionando</p>
      </article>
      <article class="tarjeta">
        <h2>API</h2>
        <p :class="estado ? 'ok' : 'mal'">● {{ estado ? 'Funcionando' : (cargando ? 'Verificando…' : 'Sin respuesta') }}</p>
      </article>
      <article class="tarjeta">
        <h2>Base de datos</h2>
        <p :class="estado?.base_de_datos === 'conectada' ? 'ok' : 'mal'">
          ● {{ estado ? (estado.base_de_datos === 'conectada' ? 'Conectada' : 'Sin conexión') : '—' }}
        </p>
      </article>
    </section>

    <p v-if="error" class="mal">{{ error }}</p>
    <p v-if="estado" class="detalle">{{ estado.postgres }}<br />Hora Bogotá: {{ estado.hora_bogota }}</p>

    <button @click="verificar" :disabled="cargando">Volver a verificar</button>
  </main>
</template>

<style scoped>
.barra {
  display: flex; gap: 12px; align-items: baseline;
  padding: 14px 24px; background: var(--primary); color: #fff;
}
.contenido { max-width: 880px; margin: 0 auto; padding: 32px 16px; }
h1 { margin: 0 0 4px; }
.sub { color: var(--muted); margin: 0 0 24px; }
.tarjetas { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px; }
.tarjeta { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 16px 20px; }
.tarjeta h2 { font-size: 1rem; margin: 0 0 8px; color: var(--muted); }
.tarjeta p { margin: 0; font-weight: 600; }
.ok { color: var(--ok); }
.mal { color: var(--error); }
.detalle { font-size: .85rem; color: var(--muted); }
button {
  background: var(--primary); color: #fff; border: 0; border-radius: 8px;
  padding: 10px 18px; font-size: 1rem; cursor: pointer;
}
button:disabled { opacity: .6; cursor: wait; }
</style>
