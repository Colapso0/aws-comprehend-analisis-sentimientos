import json, os

def mapear(e):
    if e in [1, 2]: return "NEGATIVE"
    if e == 3: return "NEUTRAL"
    return "POSITIVE"

fpath = "muestra_resultados.jsonl" if os.path.exists("muestra_resultados.jsonl") else ("results/muestra_resultados.jsonl" if os.path.exists("results/muestra_resultados.jsonl") else None)

if not fpath:
    print("Error: No se encuentra 'muestra_resultados.jsonl'. Ejecuta primero 'python3 lote.py'.")
else:
    correctos, total = 0, 0
    errores = []
    matriz = {}
    with open(fpath, "r", encoding="utf-8") as f:
        for linea in f:
            if not linea.strip(): continue
            d = json.loads(linea)
            real = mapear(d.get("estrellas", 0))
            pred = d.get("sentimiento_detectado", d.get("sentimiento", "UNKNOWN"))
            txt = d.get("texto", "")
            total += 1
            par = (real, pred)
            matriz[par] = matriz.get(par, 0) + 1
            if real == pred:
                correctos += 1
            else:
                errores.append({"texto": txt, "real": real, "estrellas": d.get("estrellas", 0), "pred": pred})

    print("="*40)
    print(f"PORCENTAJE DE ACIERTO: {(correctos/total)*100:.2f}% ({correctos}/{total})" if total else "Archivo vacio")
    print("="*40)
    print("\nMATRIZ DE CONFUSION (Real vs Predicho):")
    for (r, p), cant in matriz.items():
        print(f"Real: {r:<8} | Predicho: {p:<8} -> {cant} casos")
    print("\nPRIMEROS 5 ERRORES PARA ANALISIS:")
    for i, err in enumerate(errores[:5], 1):
        print(f"\nError {i}:")
        print(f"  Texto: \"{err['texto']}\"")
        print(f"  Estrellas: {err['estrellas']} (Esperado: {err['real']}) | Comprehend predijo: {err['pred']}")
