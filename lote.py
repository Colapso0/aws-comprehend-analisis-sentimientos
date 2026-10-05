import boto3, json

s3 = boto3.client("s3", region_name="us-east-1")
comprehend = boto3.client("comprehend", region_name="us-east-1")

BUCKET = "g3-ae-datos"  # Cambia esto si tu bucket se llama distinto

s3.download_file(BUCKET, "raw/muestra.jsonl", "muestra.jsonl")

resultados = []
with open("muestra.jsonl", "r", encoding="utf-8") as f:
    lineas = [json.loads(linea) for linea in f]

textos = [item["text"] for item in lineas]
for i in range(0, len(textos), 25):
    lote = textos[i:i+25]
    res = comprehend.batch_detect_sentiment(TextList=lote, LanguageCode="es")
    
    for idx, r in enumerate(res["ResultList"]):
        item_orig = lineas[i + idx]
        resultados.append({
            "texto": item_orig["text"],
            "estrellas": item_orig["label"] + 1,
            "sentimiento_detectado": r["Sentiment"]
        })

with open("muestra_resultados.jsonl", "w", encoding="utf-8") as f:
    for item in resultados:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

s3.upload_file("muestra_resultados.jsonl", BUCKET, "results/muestra_resultados.jsonl")
print("Proceso por lotes completado con éxito.")
